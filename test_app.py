import pytest
import os
import json
import tempfile
from app import app, SUBMISSIONS_FILE

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    # Use a temp file for submissions
    import app as app_module
    app_module.SUBMISSIONS_FILE = tempfile.mktemp(suffix='.json')
    yield client
    if os.path.exists(app_module.SUBMISSIONS_FILE):
        os.remove(app_module.SUBMISSIONS_FILE)

def test_complete_details_valid_url_saved(client):
    """Test case 1: Complete details and a valid submission URL - submission saved and appears"""
    response = client.post('/', data={
        'name': 'John Doe',
        'reg_no': 'FA20-BCS-001',
        'assignment_title': 'Lab 1',
        'submission_url': 'https://github.com/john/lab1'
    }, follow_redirects=True)
    assert response.status_code == 200
    # Check that submission appears in response
    assert b'John Doe' in response.data
    assert b'DEFECT' in response.data  # Introduce defect

def test_missing_registration_number_rejected(client):
    """Test case 2: Missing registration number - submission rejected with validation message"""
    response = client.post('/', data={
        'name': 'Jane Doe',
        'reg_no': '',
        'assignment_title': 'Lab 2',
        'submission_url': 'https://github.com/jane/lab2'
    })
    assert response.status_code == 200
    # Should show validation message
    assert b'Registration number is required' in response.data or b'required' in response.data.lower()
    # Should not be saved
    import app as app_module
    if os.path.exists(app_module.SUBMISSIONS_FILE):
        with open(app_module.SUBMISSIONS_FILE) as f:
            data = json.load(f)
        assert len(data) == 0

def test_invalid_submission_url_rejected(client):
    """Test case 3: Invalid submission URL - submission rejected and not saved"""
    response = client.post('/', data={
        'name': 'Bob Smith',
        'reg_no': 'FA20-BCS-002',
        'assignment_title': 'Lab 3',
        'submission_url': 'not-a-valid-url'
    })
    assert response.status_code == 200
    # Should show validation message
    assert b'Invalid submission URL' in response.data or b'Invalid' in response.data
    # Should not be saved
    import app as app_module
    if os.path.exists(app_module.SUBMISSIONS_FILE):
        with open(app_module.SUBMISSIONS_FILE) as f:
            data = json.load(f)
        assert len(data) == 0
