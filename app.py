

import os
import random, threading, webbrowser
from flask import Flask, request, redirect, flash, render_template, abort, url_for
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

@app.route("/")
def fileFrontPage():
    return render_template('index.html')

@app.route("/handleUpload", methods=["GET", "POST"])
def handleFileUpload():
    extra_line = ''
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files["file"]
        
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        
        if file:
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(file)
            with audio_file as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(
                    audio_data, show_all=False)
                tb = blob(str(text))
                tb_text = tb.sentiment
                if tb_text[0]>0:
                    a='Positive'
                    
                elif tb_text[0]<0:
                    a= 'Negative'
                    
                else:
                    a= 'Neutral'
                    
                extra_line = str(text)  + ":   "+ str(tb_text) + ":   " + a
           
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        extra_line += f"<br>File saved to {filepath}"
                
    #return redirect(url_for('fileFrontPage'))
    return render_template('index.html', prediction_text='Voice to Text: {} \n'.format(extra_line))

if __name__ == '__main__':
    app.run()   