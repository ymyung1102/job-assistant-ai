
from difflib import get_close_matches
import us as states
from geopy.geocoders import Nominatim
import fitz
import re

from app.utils.constants import SECTION_HEADERS


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


def find_date_pattern(line):
    return re.compile(
        r"^(.*?)((?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*)").match(line)


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
    state = None
    city = None
    try:
        geolocator = Nominatim(user_agent="location_extractor")

        state_names = [state.name for state in states.STATES]
        state_abbreviations = [state.abbr for state in states.STATES]

        state_pattern = r'\b(' + '|'.join(state_names + state_abbreviations) + r')\b'
        state_match = re.search(state_pattern, text)
        state = state_match.group(1) if state_match else None

        return state
        # TODO: Add location preference
        # if state:
        #     text_without_state = text.replace(state, '')
        #     location = geolocator.geocode(text_without_state, country_codes='US')
        #     city = location.raw['address']['city'] if location and 'city' in location.raw['address'] else None
        # elif geolocator.geocode(text, country_codes='US'):
        #     location = geolocator.geocode(text, country_codes='US')
        #     state = location.raw['address']['state'] if location and 'state' in location.raw['address'] else None
        #     city = location.raw['address']['city'] if location and 'city' in location.raw['address'] else None
        # if city is None:
        #     return state
        # return city, state
    except Exception as exc:
        print("Address not found")
        # if state and city:
        #     return city, state
        # elif state:
        #     return state
    return None
