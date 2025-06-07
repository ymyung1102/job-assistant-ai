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

- **Backend Framework**: [`Flask`](https://flask.palletsprojects.com/) – lightweight Python web framework
- **LLM Integration**: [`Ollama`](https://ollama.com/) – local large language model runner
- **PDF Parsing**: [`fitz` (PyMuPDF)](https://pymupdf.readthedocs.io/) – extract text from resumes
- **Geolocation**: [`geopy`](https://geopy.readthedocs.io/) and [`us`](https://pypi.org/project/us/) – determine region-specific info
- **CORS Handling**: [`flask-cors`](https://flask-cors.readthedocs.io/) – enable CORS for frontend-backend communication
- **HTTP Requests**: [`requests`](https://docs.python-requests.org/) – interact with external APIs
- **Web Server Gateway**: [`Werkzeug`](https://werkzeug.palletsprojects.com/) – WSGI toolkit used by Flask

---
## 📊 Architecture & Diagrams
### High-Level Architecture
![High-Level Architecture](https://github.com/user-attachments/assets/6e5637e5-6be5-476b-a72c-bc3e17e48262)
*High-level architecture showing frontend/backend and LLM interaction.*

### Logic Flow
![Overall Flowchart](https://github.com/user-attachments/assets/73e62e0b-7eee-43b7-a40a-804fdd07861c)
*Data flow of resume processing and analysis logic.*

---

## 🔍 Preview
_Example: Parsing resume and matching to job description with LLM-generated suggestions._

<p align="center" >
  <img src="https://github.com/user-attachments/assets/c9a72a47-5b36-431f-a661-eb3cca66fd1f" alt="Screenshot 1" width="43%" style="vertical-align: top;" />
  &nbsp;
  <img src="https://github.com/user-attachments/assets/a3d52029-c1be-4874-bdb8-f2f30872e021" alt="Screenshot 2" width="52%" style="vertical-align: top;" />
</p>


## 🧪 Run Application Locally (Python)

### ✅ Prerequisites
- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/installation/)
- (Optional but recommended) [virtualenv](https://virtualenv.pypa.io/)
- [Ollama](https://ollama.com/)

### 📦 Steps

```bash
# Clone the repository
git clone https://github.com/ymyung1102/job-assistant-ai.git
cd job-assistant-ai

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Start Ollama in local
ollama serve

# Start the application
python -m app.main
```

- Open UI at http://127.0.0.1:5000/

## 🧪 Run Application Locally (Docker)

### ✅ Prerequisites
- [Docker](https://docs.docker.com/get-started/get-docker/)
- [Ollama](https://ollama.com/)

### 📦 Steps
```bash
# Clone the repository
git clone https://github.com/ymyung1102/job-assistant-ai.git
cd job-assistant-ai

# Build the Docker image
docker build -t resume-parser .

# Run the Docker container (-t is optional)
docker run -t -p 5000:5000 resume-parser
```
- Open UI at http://127.0.0.1:5000/

## 📁 Project Structure

```bash
job-assistant-ai/
├── app/                  # Core application logic (routes, services, sections)
│ ├── main.py             # Entry point for the Flask app
│ ├── models/             # Data models and LLM prompt templates
│ ├── resources/          # API route definitions
│ │ ├── static/           # Frontend JS/CSS
│ │ └── templates/        # HTML templates
│ ├── sections/           # Resume sections logic (skills, work experience, etc.)
│ ├── services/           # Business logic and data processing services
│ └── utils/              # Utility functions and constants
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🛠️ Features & Improvements
- [x] Basic resume parsing
- [ ] Add more resume sections to parse.
- [ ] Add fail back resume parsing using LLM
- [ ] Enhance skills section extraction with NLP
- [ ] Export parsed content as a machine-friendly resume or JSON.
- [ ] Add "Clear All" button for each section in the UI.
- [ ] Add validation highlighting (e.g., red border if a required field is empty).
- [x] Add Docker build support.
- [ ] Add configuration file for user to define host and port
- [ ] Improve accuracy of location identifier.
- [ ] Improve error handling and logging
- [ ] Add unit and integration tests
