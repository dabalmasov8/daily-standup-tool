from flask import Flask, jsonify, request # type: ignore
import datetime

app = Flask(__name__)

# Default standup data
standup_data = {
    'participants': ['Alex Johnson', 'Jamie Smith', 'Taylor Brown', 'Jordan Lee', 'Casey Miller', 'Morgan Davis', 'Riley Wilson', 'Quinn Taylor', 'Avery Clark', 'Cameron Martinez'],
    'questions': ['What will I do today?', 'Do I have blockers?', 'Do I have capacity today to help others?'],
    'statuses': [''] * 10,  # Statuses for each participant
    'current_index': 0,
    'blockers': [],
    'standup_start_time': None
}

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(standup_data)

@app.route('/update_questions', methods=['POST'])
def update_questions():
    data = request.json
    standup_data['questions'] = data['questions']
    return '', 204

@app.route('/import_names', methods=['POST'])
def import_names():
    data = request.json
    standup_data['participants'] = data['names']
    standup_data['statuses'] = [''] * len(data['names'])  # Reset statuses
    return '', 204

@app.route('/start_standup', methods=['POST'])
def start_standup():
    standup_data['standup_start_time'] = datetime.datetime.now()
    standup_data['current_index'] = 0
    standup_data['statuses'] = [''] * len(standup_data['participants'])  # Reset statuses
    standup_data['blockers'] = []
    return '', 204

@app.route('/mark_completed', methods=['POST'])
def mark_completed():
    current_index = standup_data['current_index']
    if current_index < len(standup_data['participants']):
        standup_data['statuses'][current_index] = 'completed'
        standup_data['current_index'] += 1
        if standup_data['current_index'] >= len(standup_data['participants']):
            return jsonify({'end': True})
    return jsonify({'end': False})

@app.route('/mark_has_blockers', methods=['POST'])
def mark_has_blockers():
    current_index = standup_data['current_index']
    if current_index < len(standup_data['participants']):
        participant = standup_data['participants'][current_index]
        if participant not in standup_data['blockers']:
            standup_data['blockers'].append(participant)
        standup_data['statuses'][current_index] = 'blocker'
    return '', 204

@app.route('/mark_absent', methods=['POST'])
def mark_absent():
    current_index = standup_data['current_index']
    if current_index < len(standup_data['participants']):
        standup_data['statuses'][current_index] = 'absent'
        standup_data['current_index'] += 1
        if standup_data['current_index'] >= len(standup_data['participants']):
            return jsonify({'end': True})
    return jsonify({'end': False})

@app.route('/copy_blockers', methods=['GET'])
def copy_blockers():
    return jsonify({'blockers': standup_data['blockers']})

@app.route('/get_duration', methods=['GET'])
def get_duration():
    if standup_data['standup_start_time']:
        end_time = datetime.datetime.now()
        duration = end_time - standup_data['standup_start_time']
        minutes, seconds = divmod(int(duration.total_seconds()), 60)
        return jsonify({'duration': f'{minutes:02}:{seconds:02}'})
    return jsonify({'duration': '00:00'})

if __name__ == '__main__':
    app.run(debug=True)
