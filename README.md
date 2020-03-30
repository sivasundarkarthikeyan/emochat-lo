# EmoChat

Emochat is a Flask based web application for chatting. This app incorporates IBM Watson module to detect the chat sentiment polarity.

Click [EmoChat Web App](http://fierce-cliffs-30257.herokuapp.com/) to experience the app.

## Folder Content and Description
* emochat.py - Server Side Script
* ToneAnalyzer.py - A class file used by emochat.py for sentiment detection
* requirements.txt - Text file with dependencies
* templates - folder containing page template
* static - folder containing image elements
* Procfile - To deploy in cloud, especially heroku

## Installation and Testing

Requires prior installation of python 3.6 or above followed by installations of packages in **requirements.txt**.
```python
python emochat.py
```
Open localhost:5000 in the browser to test locally

## Deployment on heroku

[Deployment on heroku](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) will give an overview of app deployment in heroku.

User **http** instead of **https** to access the app on heroku.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.