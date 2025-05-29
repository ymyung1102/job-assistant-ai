# 🧠 Job Assistant AI

**Job Assistant AI** is a privacy-focused web application designed to help job seekers tailor their resumes to job descriptions using LLMs. Built with FastAPI, it offers intelligent parsing, resume-job matching insights, and real-time suggestions—all without storing any user data.

---

## 🚀 Features

- 🔍 **LLM-Powered Job Description Analysis**  
  Understand what recruiters are looking for and how your resume matches up.

- 📄 **Modular In-Memory Resume Parsing**  
  Upload your PDF resume—parsed and analyzed in memory with no data stored.

- 💡 **Tailored Suggestions**  
  Get insights on skills and content to emphasize or improve based on job requirements.

- 🔐 **Privacy First**  
  No external storage or logging of user data. Everything runs in-memory and is ephemeral.

---

## ⚙️ Tech Stack

- **Backend Framework**: [Flask](https://flask.palletsprojects.com/) – lightweight Python web framework
- **LLM Integration**: [Ollama](https://ollama.com/) – local large language model runner
- **PDF Parsing**: [`fitz` (PyMuPDF)](https://pymupdf.readthedocs.io/) – extract text from resumes
- **Geolocation**: [`geopy`](https://geopy.readthedocs.io/) and [`us`](https://pypi.org/project/us/) – determine region-specific info
- **CORS Handling**: [`flask-cors`](https://flask-cors.readthedocs.io/) – enable CORS for frontend-backend communication
- **HTTP Requests**: [`requests`](https://docs.python-requests.org/) – interact with external APIs
- **Web Server Gateway**: [`Werkzeug`](https://werkzeug.palletsprojects.com/) – WSGI toolkit used by Flask

---

## 📁 Project Structure

```bash
job-assistant-ai/
├── app/                  # Core application logic (routes, services, sections)
│ ├── main.py             # Entry point for the Flask app
│ ├── models/             # Data models and LLM prompt templates
│ ├── routes/             # API route definitions
│ ├── sections/           # Resume sections logic (skills, work experience, etc.)
│ ├── services/           # Business logic and data processing services
│ └── utils/              # Utility functions and constants
│
├── static/               # Frontend JS/CSS
├── templates/            # HTML templates
├── Dockerfile
├── requirements.txt
└── README.md
