from os.path import join
from ibm_watson import ToneAnalyzerV3
from ibm_watson.tone_analyzer_v3 import ToneInput
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class ToneAnalyzer():
	#Method to initialize IBM API connection
	def __init__(self):
		self.tone_analyzer = ''
		authenticator = IAMAuthenticator('DUma1tFHRoi2LePb3uHHbWgPOtHF1YrSPJrtLv0-1NHu')
		self.tone_analyzer = ToneAnalyzerV3(version='2017-09-21', authenticator=authenticator)
		self.tone_analyzer.set_service_url('https://api.au-syd.tone-analyzer.watson.cloud.ibm.com/instances/943a9480-4385-4d56-bfde-9e236aa2efd2')

	def analyze_tone(self, msg):
		tone_input = ToneInput(msg)
		tone = self.tone_analyzer.tone(tone_input=tone_input, content_type="text/plain", sentences=True).get_result()
		estimated_polarity = self.polarity_finder(tone)
		

		return estimated_polarity
			
	def polarity_finder(self, tone):
		
		polarised_tones = {'positive':['joy', 'confident'], 'neutral': ['analytical']}
		global_tones = len(tone['document_tone']['tones'])
		polarity_result = ':|'
		
		if global_tones is 0: 
			return polarity_result
		else:
			if 'sentences_tone' in tone.keys() and len(tone['sentences_tone']) > 0:
				score = self.sentence_score(tone, polarised_tones)
			else:
				score = self.total_score(tone, polarised_tones)
		
		polarity = self.final_polarity(score)
		
		if polarity is 'negative':
			polarity_result = ':('
		elif polarity is 'positive':
			polarity_result = ':)'
		else:
			return polarity_result

		
		return polarity_result

	def total_score(self, tone, polarised_tones):
		global_score = {}
		global_score['positive'] = []
		global_score['negative'] = []
		global_score['neutral'] = []

		for current_tone in tone['document_tone']['tones']:
			positive_factor, neutral_factor, negative_factor = self.weighted_score(current_tone['tone_id'], polarised_tones)
			global_score['positive'].append(positive_factor * current_tone['score'])
			global_score['neutral'].append(neutral_factor * current_tone['score'])
			global_score['negative'].append(negative_factor * current_tone['score'])

		for polarity in global_score:
			global_score[polarity] = self.mean(global_score[polarity])
		
		global_score= self.normalize(global_score)
		
		
		return global_score

	def sentence_score(self, tone, polarised_tones):
		local_score = {}
		local_score['positive'] = []
		local_score['negative'] = []
		local_score['neutral'] = []

		for sentence in tone['sentences_tone']:
			for current_tone in sentence['tones']:
				positive_factor, neutral_factor, negative_factor = self.weighted_score(current_tone['tone_id'], polarised_tones)
				local_score['positive'].append(positive_factor * current_tone['score'])
				local_score['neutral'].append(neutral_factor * current_tone['score'])
				local_score['negative'].append(negative_factor * current_tone['score'])
					
		for polarity in local_score:
			local_score[polarity] = self.mean(local_score[polarity])
		
		local_score = self.normalize(local_score)


		return local_score

	def weighted_score(self, current_tone ,polarised_tones):
		
		positive_factor = 0.0
		neutral_factor = 0.0
		negative_factor = 0.0

		if current_tone in polarised_tones['positive']:
			positive_factor = 0.7 if current_tone == 'confident' else 1.0
			neutral_factor = 0.2 if current_tone == 'confident' else 0.0
			negative_factor = 0.1 if current_tone == 'confident' else 0.0
		elif current_tone in polarised_tones['neutral']:
			positive_factor = 0.1
			neutral_factor = 0.8
			negative_factor = 0.1
		else:
			positive_factor = 0.2 if current_tone == 'tentative' else 0.0
			neutral_factor = 0.3 if current_tone == 'tentative' else 0.0
			negative_factor = 0.5 if current_tone == 'tentative' else 1.0
		

		return (positive_factor, neutral_factor, negative_factor)

	#Computes mean of given list
	def mean(self, score_list):
		
		return sum(score_list)/len(score_list)

	#Method normalizes Polarity Scores between 0 and 1
	def normalize(self, score_dict):
		
		normalized_dict = {}
		total = sum(score_dict.values())
		normalized_dict = {x:score_dict[x]/total for x in score_dict}
		

		return normalized_dict

	#Method returns Estimated Polarity with MLE
	def final_polarity(self, score_dict):
		
		v=list(score_dict.values())
		k=list(score_dict.keys())
		

		return k[v.index(max(v))]
