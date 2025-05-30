# handler.py
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from app.services.llm import analyze_resume_vs_job, format_resume_html
from app.services.input_parser import extract_text

logger = logging.getLogger('handler')
app = Flask(__name__,
            template_folder='../resources/templates',
            static_folder='../resources/static')
CORS(app)

@app.route('/')
def home():
    """
    GET /
    Renders the main HTML page

    Returns:
        HTML: The rendered index.html page.
    """
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """
    GET /health
    Health check endpoint to verify the API is running.

    Returns:
        JSON: {"status": "OK"}
    """
    return jsonify({'status': 'OK'})


@app.route('/upload', methods=['POST'])
def upload_resume():
    """
    POST /upload
    Accepts a resume file, extracts its content, and formats it for display.

    Request:
        Form-data: 'resume' (file)

    Returns:
        JSON: Parsed resume content in structured format.
    """
    response = ''
    try:
        file = request.files['resume']
        file_bytes = file.read()
        text = extract_text(file_bytes)
        response = format_resume_html(text)
    except Exception as exc:
        logger.exception(exc)
    return jsonify(response)


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    POST /analyze
    Compares the resume content with a job description and returns an analysis.

    Request JSON:
        {
            "resume": "<resume text>",
            "job_description": "<job description text>"
        }

    Returns:
        JSON: Analysis result including match score, matched skills, etc.
        On error: JSON with error message and 500 status code.
    """
    try:
        data = request.get_json()
        resume = data['resume']
        job = data['job_description']
        raw_output = analyze_resume_vs_job(resume, job)
        return jsonify({'result': raw_output})
    except Exception as e:
        logger.exception(e)
        return jsonify({'error': 'Internal Server Error!!!'}), 500