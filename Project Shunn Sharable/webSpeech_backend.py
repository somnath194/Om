from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import webbrowser
import threading
import logging
import atexit
from time import sleep
import sys

sys.path.append("D:\\programs\\Project Shunn\\Features")
import general_functions as gf
import commands as cd
import pygetwindow as gw


# Silence Flask request logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
  <title>Auto Speech to Text</title>
</head>
<body>
  <h2>Listening...</h2>
  <div id="output"></div>
  <script>
    const output = document.getElementById('output');
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.continuous = true;
    recognition.lang = 'en-US';
    recognition.interimResults = false;

    recognition.onresult = (event) => {
      const lastResultIndex = event.results.length - 1;
      const transcript = event.results[lastResultIndex][0].transcript;
      output.innerHTML += `<div>${transcript}</div>`;

      fetch('/transcript', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript })
      });
    };

    recognition.start();  // Starts listening as soon as the page loads
  </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/transcript', methods=['POST'])
def receive_transcript():
    data = request.json
    transcript = data.get('transcript', '')
    print(transcript)
    File = open("D:\\programs\\Project Shunn\\Features\\SpeechRecogonisition.txt","w")
    File.write(str(transcript.strip().lower()))
    File.close()
    return transcript

def open_browser():
    webbrowser.open('http://localhost:5000/')
        

def close_chrome():
    gf.close_application('close chrome')

atexit.register(close_chrome)

def run_flask():
    threading.Timer(1, open_browser).start()
    app.run(port=5000)

run_flask()
