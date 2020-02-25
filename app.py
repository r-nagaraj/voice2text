#!/usr/bin/env python
"""
Simple Flask application to demonstrate the Google Speech API usage.

Install the requirements first:
`pip install SpeechRecognition flask`

Then just run this file, go to http://127.0.0.1:5000/
and upload an audio (or may be even video) file there, using the html form.
(I've tested it with a .wav file only - relying on Google here).
"""

import os
import random, threading, webbrowser
from flask import Flask, request, redirect, flash, render_template
from werkzeug.utils import secure_filename

from textblob import TextBlob as blob

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')



import speech_recognition as sr

app = Flask(__name__)
UPLOAD_FOLDER = "./"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "generatedkey"

# You have 50 free calls per day, after that you have to register somewhere
# around here probably https://cloud.google.com/speech-to-text/
#GOOGLE_SPEECH_API_KEY = None


@app.route("/", methods=["GET", "POST"])
def index():
    extra_line = ''
    if request.method == "POST":
        # Check if the post request has the file part.
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If user does not select file, browser also
        # submit an empty part without filename.
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        if file:
            # Speech Recognition stuff.
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(
                audio_data, show_all=False)
                #audio_data, key=GOOGLE_SPEECH_API_KEY, language="ru-RU")
                tb = blob(str(text))
                tb_text = tb.sentiment
                if tb_text[0]>0:
                    a='Positive'
                elif tb_text[0]<0:
                    a= 'Negative'
                else:
                    a= 'Neutral'
                 
                              
                #text = str(text) + '' + str(tb_text) + '' + a
                #extra_line = f'Your text: "{text}"'
                
                extra_line = str(text)  + ":   "+ str(tb_text) + ":   " + a
                
                

            # Saving the file.
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            extra_line += f"<br>File saved to {filepath}"

    return f"""
    <!doctype html>
    <title>Upload new File</title>
    {extra_line}
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <p/>
      <input type=submit value=Upload>
      <h3>Contact</h3>
      <p>Nagaraj <em>for</em> <em>further</em><em>details.<em/></p>
    </form>
    """


if __name__ == "__main__":
    app.run()
    
    #app.run(debug=True, threaded=True)
