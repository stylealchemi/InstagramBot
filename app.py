from flask import Flask, render_template, request, jsonify
import threading
import os
from automation import start_automation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    threading.Thread(target=start_automation, args=(data,)).start()
    return jsonify({"status": "Automation started"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)

