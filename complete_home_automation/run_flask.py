from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import webbrowser
import threading
import logging
import sys
from flags import exit_event

sys.path.append("D:\\programs\\Project Shunn\\Features")
import general_functions as gf
import commands as cd


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
  recognition.interimResults = true;
  recognition.lang = 'en-US';

  let currentLine = '';
  let allLines = [];

  recognition.onresult = (event) => {
    let interimTranscript = '';
    let finalTranscript = '';

    for (let i = event.resultIndex; i < event.results.length; ++i) {
      const transcript = event.results[i][0].transcript.trim();
      if (event.results[i].isFinal) {
        finalTranscript += transcript + ' ';
      } else {
        interimTranscript += transcript + ' ';
      }
    }

    // Send interim only if not empty
    if (interimTranscript.trim()) {
      fetch('/transcript', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript: interimTranscript.trim(), type: 'interim' })
      });
      currentLine = interimTranscript.trim();
    }

    // If final, push to array and reset currentLine
    if (finalTranscript.trim()) {
      fetch('/transcript', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript: finalTranscript.trim(), type: 'final' })
      });
      allLines.push(finalTranscript.trim());
      currentLine = '';
    }

    // Update display
    const html = allLines.map(line => `<div>${line}</div>`).join('');
    const liveLine = currentLine ? `<div><i>${currentLine}</i></div>` : '';
    output.innerHTML = html + liveLine;
  };

  recognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error);
    recognition.stop();
    setTimeout(() => recognition.start(), 1000);
  };

  recognition.onend = () => {
    setTimeout(() => recognition.start(), 1000);
  };

  recognition.start();
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
    transcript_type = data.get('type', 'final')

    if transcript_type == 'interim':
        # Overwrite line for live feedback
        print(f"\r{transcript}", end='', flush=True)
    else:
        print(f"")
        with open("D:\\programs\\Project Shunn\\Features\\SpeechRecogonisition.txt", "w") as file:
            file.write(transcript.strip().lower())
            if transcript.strip().lower() in cd.goodbye_commands:
                exit_event.set()
    return jsonify({"status": "ok"})


def open_browser():
    webbrowser.open('http://localhost:5000/')
        

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func: func(); return 'Shutting down...'
    return 'Shutdown not available', 500


def run():
    threading.Timer(1, open_browser).start()
    app.run(port=5000)
