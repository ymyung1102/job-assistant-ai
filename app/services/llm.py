import traceback
import requests
import re
import unicodedata

from app.models.llm_prompts import Prompt
from app.services.parser import ResumeParser


def preprocess_resume(text):
    text = unicodedata.normalize('NFKD', text)

    replacements = {
        '•': '<<bullet>>',
        '●': '<<bullet>>',
        '▪': '<<bullet>>',
        '–': '-',
        '—': '-',
        '―': '-',
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
        '´': "'",
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)

    print(text)
    return text

def ask_llm(prompt: str) -> str:
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "options": {'temperature': 0.2}
    })
    return response.json()["response"]


def format_resume_html(resume: str):
    # resume = preprocess_resume(resume)
    try:
        print(resume)
        return ResumeParser(resume).parse()
    except Exception as e:
        print(e)
        print(traceback.print_stack())


def analyze_resume_vs_job(resume: str, job: str):
    prompt = Prompt(resume, job)
    raw_output = ask_llm(prompt.get_highlight_prompt())
    return raw_output


def highlight_skills(job_text, present_skills, missing_skills):
    def highlight(term, color):
        return rf'<span style="background-color:{color}">{term}</span>'

    for skill in sorted(set(present_skills), key=len, reverse=True):
        job_text = re.sub(rf"\b({re.escape(skill)})\b", highlight(r"\1", "lightgreen"), job_text,
                          flags=re.IGNORECASE)

    for skill in sorted(set(missing_skills), key=len, reverse=True):
        job_text = re.sub(rf"\b({re.escape(skill)})\b", highlight(r"\1", "#ffcccc"), job_text,
                          flags=re.IGNORECASE)

    return job_text
