# Assignment Submission Portal - CSC418 DevOps Midterm

## Overview
A simple assignment submission portal with automated testing, CI/CD pipeline, and local test report receiver.

## Features
- Student submission form (Name, Registration Number, Assignment Title, Submission URL)
- Form validation (required fields and URL validation)
- Display of all submissions
- Automated tests on every push
- Test reports sent to local receiver and saved as JSON
- GitHub Actions CI pipeline

## Setup Instructions

### Prerequisites
- Python 3.11+
- Git
- A tunneling service (ngrok, cloudflared) or run GitHub Actions locally with act

### Running the Application Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask app:
```bash
python app.py
```
The app will be available at `http://localhost:5000`

### Running Tests

Run all tests:
```bash
python -m pytest test_app.py -v
```

Run with JSON report:
```bash
python -m pytest test_app.py -v --json-report --json-report-file=pytest-report.json
```

### Running the Local Report Receiver

1. Start the receiver:
```bash
python receiver.py
```
The receiver runs on `http://127.0.0.1:5001`

2. For GitHub-hosted runners to reach your local machine, use a tunnel:
```bash
ngrok http 5001
# or
cloudflared tunnel --url http://localhost:5001
```

3. Add the tunnel URL as a GitHub secret named `RECEIVER_URL` in your repository settings.

## CI/CD Pipeline

The pipeline (`.github/workflows/ci.yml`) runs on every push:
1. Checks out code
2. Sets up Python
3. Installs dependencies
4. Runs tests with JSON reporting
5. Processes results into required format and sends to receiver (if configured)
6. Uploads test report as artifact

## Test Cases
1. **Complete details and valid URL** - Submission saved and appears in list
2. **Missing registration number** - Rejected with validation message, not saved
3. **Invalid submission URL** - Rejected, not saved

## Test Report Format
The `test-report.json` contains:
- Repository name, branch, commit SHA, pipeline run ID, execution timestamp
- Each test's name, result, and failure message (if failed)
- Total, passed, failed counts and overall status

## Demonstration
For the midterm demo, you'll need to show:
1. Push with passing tests → receiver gets report
2. Introduce defect → push with failing tests → receiver gets report with failures
3. Fix defect → push with passing tests → receiver gets report

Make sure both receiver and tunnel (if using GitHub-hosted runner) are running during demonstration.
