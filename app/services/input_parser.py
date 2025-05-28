from difflib import get_close_matches
import us as states
from geopy.geocoders import Nominatim
import fitz
import re

def extract_text(pdf_bytes: bytes) -> str:
    text = ""
    if pdf_bytes[:4] == b'%PDF':
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text("text")
    return text.strip()

def extract_block(content: str, block_type: str):
    match = re.search(rf'```{block_type}\n([\s\S]*?)```', content)
    return match.group(1).strip() if match else ''




SECTION_HEADERS = {
    "summary": ["summary", "about me", "objective"],
    "skills": ["skills", "skills & abilities", "technical skills", "skills & other"],
    "work_experience": ["work experience", "professional experience", "experience", "job experience"],
    "education": ["education", "academic background"],
    "certifications": ["training", "certification", "certifications"],
    "projects": ["project", "personal project"]
}
SAME_LINE_DATE_PATTERN = re.compile(r"^(.*?)((?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*)")



def detect_section(line):
    """Detects which section a line belongs to based on fuzzy matching."""
    line_lower = line.strip().lower()
    for section, keywords in SECTION_HEADERS.items():
        matches = get_close_matches(line_lower, keywords, n=1, cutoff=0.8)
        if matches:
            return section
    return None


def is_bullet(line):
    """Detects bullet points in a resume."""
    return line.strip().startswith(('-', '•', '●', '▪'))


def is_date(line):
    """Detects dates in a resume (e.g., 'Jan 2020 - Present')."""
    res = bool(re.search(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\.?\s?\d{4}.*\d{4}|current\b',
                   line, re.IGNORECASE))
    if not res:
        res = bool(re.search( r'(January|February|March|April|May|June|July|August|September|October|November|December)?\s?\d{4}|current',
                    line, re.IGNORECASE))
    return res

def extract_location(text):
    try:
        geolocator = Nominatim(user_agent="location_extractor")

        state_names = [state.name for state in states.STATES]
        state_abbreviations = [state.abbr for state in states.STATES]

        state_pattern = r'\b(' + '|'.join(state_names + state_abbreviations) + r')\b'
        state_match = re.search(state_pattern, text)
        state = state_match.group(1) if state_match else None

        city = None
        if state:
            text_without_state = text.replace(state, '')
            location = geolocator.geocode(text_without_state, country_codes='US')
            city = location.raw['address']['city'] if location and 'city' in location.raw['address'] else None
        elif geolocator.geocode(text, country_codes='US'):
            location = geolocator.geocode(text, country_codes='US')
            state = location.raw['address']['state'] if location and 'state' in location.raw['address'] else None
            city = location.raw['address']['city'] if location and 'city' in location.raw['address'] else None
        if city is None:
            return state
        return city, state
    except Exception as exc:
        print("Address not found")
    return None

def parse_ats_resume(text):
    """Parses the ATS-friendly resume into a structured format."""
    sections = {
        "location": '',
        "summary": '',
        "skills": [],
        "work_experience": [],
        "education": [],
        "certifications": [],
        "projects": []
    }
    current_section = None
    last_job = None
    last_education = None
    last_project = None
    lines = text.splitlines()
    location_found = False
    found_bullet = False
    company_name = ''
    last_job = {}
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        # Extract location preference if found in the contact information section

        if not location_found:
            location = extract_location(line)
            if location:
                sections['location'] = location
                location_found = True
                continue
        section = detect_section(line)
        # If this is a section header, update the current section
        if section:
            print(f"found section {section}")
            if current_section == 'work_experience':
                if last_job and last_job['title']:
                    sections['work_experience'].append(last_job.copy())
            current_section = section
            continue
        # if content found without header and after the location is found add to summary
        if not current_section and location_found:
            current_section = 'summary'
        # Handle the content based on the section
        if current_section == 'summary':
            sections['summary'] += line
        elif current_section == 'skills':
            values = line.split(':', 1)[1] if ':' in line else line
            skills_list = [v.strip() for v in values.split(',')]
            skills_list = list(filter(None, skills_list))
            sections['skills'].extend(skills_list)
        elif current_section == 'work_experience':
            if is_bullet(line) or found_bullet:
                if last_job:
                    bullet_str = re.sub(r'^[•●▪\-\s]*', '', line).strip()
                    if bullet_str in ['●\u200b', '\u200b']:
                        found_bullet = True
                        continue
                    elif found_bullet:
                        last_job['description'].append(line)
                        found_bullet = False
            else:
                company_date_match = SAME_LINE_DATE_PATTERN.match(line)
                if company_date_match:
                    company_name = company_date_match.group(1).strip()
                    date_info = company_date_match.group(2).strip()
                    location = extract_location(company_name)
                    if last_job and last_job['title']:
                        sections['work_experience'].append(last_job.copy())
                    if location:
                        # this is company name
                        last_job = {
                            'company_and_location': company_name,
                            'title': '',
                            'date': date_info,
                            'description': []
                        }
                    else:
                        # this is title in same company
                        last_job = {
                            'company_and_location': last_job.get('company_and_location', ""),
                            'title': company_name,
                            'date': date_info,
                            'description': []
                        }
        elif current_section == 'education':
            if is_bullet(line) or found_bullet:
                if last_education:
                    bullet = re.sub(r'^[•●▪\-\s]*', '', line).strip()
                    if bullet in ['●\u200b', '\u200b']:
                        found_bullet = True
                        continue
                    elif found_bullet:
                        last_education['description'].append(line)
                        found_bullet = False
            else:
                education_date_match = SAME_LINE_DATE_PATTERN.match(line)
                if not last_education:
                    if education_date_match:
                        education_name = education_date_match.group(1).strip()
                        date_info = education_date_match.group(2).strip()
                    else:
                        education_name = line
                        date_info = ''
                    last_education = {
                        'university_and_location': education_name,
                        'degree': '',
                        'date': date_info,
                        'description': []
                    }
                    sections['education'].append(last_education)
                elif is_date(line) and last_education:
                    # If the date is on a separate line
                    last_education['date'] = line
                else:
                    last_education['degree'] = line
        elif current_section == 'projects':
            if is_bullet(line) or found_bullet:
                if last_project:
                    bullet = re.sub(r'^[•●▪\-\s]*', '', line).strip()
                    if bullet in ['●\u200b', '\u200b']:
                        found_bullet = True
                        continue
                    elif found_bullet:
                        last_project['description'].append(line)
                        found_bullet = False
            else:
                project_date_match = SAME_LINE_DATE_PATTERN.match(line)
                if not last_project:
                    if project_date_match:
                        project_name = project_date_match.group(1).strip()
                        date_info = project_date_match.group(2).strip()
                    else:
                        project_name = line
                        date_info = ''
                    last_project = {
                        'project_name': project_name,
                        'date': date_info,
                        'description': []
                    }
                    sections['projects'].append(last_project)
                elif is_date(line) and last_project:
                    # If the date is on a separate line
                    last_project['date'] = line
                else:
                    last_project['degree'] = line
    return sections


def generate_html(sections):
    if not sections:
        return ""
    """
    {'location': (None, None),
    'summary': 'Backend software development engineer with more than 5 years of experience. Looking for a job.',
    'skills': [{'category': 'Programming Languages', 'skills': ['Python', 'C++', 'Java']},
    {'category': 'Tools/Databases', 'skills': ['GitHub', 'Kubernetes', 'Docker']},
    {'category': 'Operating Systems', 'skills': ['MacOS', 'Window', 'Linux']},
    {'category': 'Soft Skills', 'skills': ['Teamwork', 'Accountability']},
    {'category': 'Languages', 'skills': ['Proficient in English and Spanish']}],
    'work_experience': [
        {'company_and_location': 'TEST COMPANY | TEST LOCATION',
        'title': 'Software Engineer',
        'date': 'September 2020 - Current',
        'description': ['Built distributed python application', 'Let team meetings and sprint planning']}
    ],
    'education': [
        {'university_and_location': 'TEST UNIVERSITY | TEST LOCATION',
        'degree': 'Bachelor of Science in Computer Science', 'date': 'September 2016 - June 2020',
        'description': []}
    ],
    'projects': []}
    """


