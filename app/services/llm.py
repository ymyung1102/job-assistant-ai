# llm.py
import logging
import requests
import re
import unicodedata

from app.models.llm_prompts import Prompt
from app.services.parser import ResumeParser

logger = logging.getLogger('llm')

def preprocess_resume(text: str) -> str:
    """
    Normalizes and replaces common special characters in resume text.

    Args:
        text (str): Raw extracted text from the resume.

    Returns:
        str: Preprocessed text with unified symbols and punctuation.
    """
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

    return text

def ask_llm(prompt: str) -> str:
    """
    Sends a prompt to the LLM server and returns the generated response.

    Args:
        prompt (str): The input prompt string.

    Returns:
        str: The LLM-generated output.
    """
    response = requests.post("http://host.docker.internal:11434/api/generate", json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "options": {'temperature': 0.2}
    })
    return response.json()["response"]


def format_resume_html(resume: str):
    """
    Parses and formats the given resume text into structured data.

    Args:
        resume (str): Preprocessed resume text.

    Returns:
        dict: Structured resume content (e.g., sections and parsed info).
    """
    try:
        logger.debug("Parsing resume")
        return ResumeParser(resume).parse()
    except Exception as e:
        logger.exception(e)
        return {}


def analyze_resume_vs_job(resume: str, job: str) -> str:
    """
    Analyzes how well a resume matches a job description using LLM.

    Args:
        resume (str): Resume text.
        job (str): Job description text.

    Returns:
        str: LLM's analysis comparing the resume and job.
    """
    prompt = Prompt(resume, job)
    raw_output = ask_llm(prompt.get_analyze_prompt())
    return raw_output


# TODO: Feature to highlight skills visually
# def highlight_skills(job_text, present_skills, missing_skills):
#     def highlight(term, color):
#         return rf'<span style="background-color:{color}">{term}</span>'
#
#     for skill in sorted(set(present_skills), key=len, reverse=True):
#         job_text = re.sub(rf"\b({re.escape(skill)})\b", highlight(r"\1", "lightgreen"), job_text,
#                           flags=re.IGNORECASE)
#
#     for skill in sorted(set(missing_skills), key=len, reverse=True):
#         job_text = re.sub(rf"\b({re.escape(skill)})\b", highlight(r"\1", "#ffcccc"), job_text,
#                           flags=re.IGNORECASE)
#
#     return job_text
