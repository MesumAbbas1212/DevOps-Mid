from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

REPORT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test-report.json')

@app.route('/report', methods=['POST'])
def receive_report():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Add timestamp if not present
    if 'execution_timestamp' not in data:
        data['execution_timestamp'] = datetime.utcnow().isoformat() + 'Z'
    
    # Save report
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f'Report saved to {REPORT_FILE}')
    return jsonify({'status': 'success', 'message': 'Report saved'}), 200

@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'Receiver running', 'report_file': REPORT_FILE})

if __name__ == '__main__':
    print(f'Receiver starting. Reports will be saved to: {REPORT_FILE}')
    app.run(host='127.0.0.1', port=5001, debug=True)
