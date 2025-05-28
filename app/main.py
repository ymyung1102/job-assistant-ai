from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from services.llm import analyze_resume_vs_job, format_resume_html
from services.input_parser import extract_text

app = Flask(__name__, template_folder='../templates', static_folder='../static')

CORS(app)

# TODO:
# 0. Add loading icon to Upload not in analyzeMatch
# 1. Add certifications
# 2. Modify description textarea to be dynamic height
# 3. Fix upload issue as it does not parse correctly
# 4. Export the content as a new machine friendly resume or as JSON
# 5. Add Clear all button for each section
# 6. Add validation highlighting (e.g., red border if a required field is empty).
# 7. Add logging
# 8. Add Docker build
@app.route('/')
def home():
    # Renders the HTML page from templates folder
    return render_template('index.html')

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"})


@app.route("/upload", methods=["POST"])
def upload_resume():
    # parses resume
    response = ""
    try:
        file = request.files["resume"]
        file_bytes = file.read()
        text = extract_text(file_bytes)
        response = format_resume_html(text)
    except Exception as exc:
        print(exc)
    return jsonify(response)


@app.route("/analyze", methods=["POST"])
def analyze():
    # analyze job description vs resume
    try:
        data = request.get_json()
        resume = data["resume"]
        job = data["job_description"]
        raw_output = analyze_resume_vs_job(resume, job)
        return jsonify({"result": raw_output})
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Server Error!!!"}), 500

if __name__ == "__main__":
    app.run(debug=True)
