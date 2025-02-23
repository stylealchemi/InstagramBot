from flask import Flask, render_template, request, jsonify
import threading
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
    app.run(host="0.0.0.0", port=port)
