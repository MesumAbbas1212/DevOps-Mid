from flask import Flask, request, render_template, redirect, url_for
from urllib.parse import urlparse
import json
import os

app = Flask(__name__)

SUBMISSIONS_FILE = os.path.join(os.path.dirname(__file__), 'submissions.json')

def load_submissions():
    if os.path.exists(SUBMISSIONS_FILE):
        try:
            with open(SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_submissions(submissions):
    with open(SUBMISSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(submissions, f, indent=2, ensure_ascii=False)

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return all([parsed.scheme in ['http', 'https'], parsed.netloc])
    except Exception:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    submissions = load_submissions()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        reg_no = request.form.get('reg_no', '').strip()
        assignment_title = request.form.get('assignment_title', '').strip()
        submission_url = request.form.get('submission_url', '').strip()
        
        errors = []
        if not name:
            errors.append('Name is required')
        if not reg_no:
            errors.append('Registration number is required')
        if not assignment_title:
            errors.append('Assignment title is required')
        if not submission_url:
            errors.append('Submission URL is required')
        elif not is_valid_url(submission_url):
            errors.append('Invalid submission URL')
        
        if errors:
            return render_template('index.html', submissions=submissions, errors=errors, 
                                   form_data=request.form)
        
        submissions.append({
            'name': name,
            'reg_no': reg_no,
            'assignment_title': assignment_title,
            'submission_url': submission_url
        })
        save_submissions(submissions)
        return redirect(url_for('index'))
    
    return render_template('index.html', submissions=submissions, errors=[])

if __name__ == '__main__':
    app.run(debug=True)
