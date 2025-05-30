import logging
import re
import us as states
from difflib import get_close_matches
from re import Match


from geopy.geocoders import Nominatim


from app.utils.constants import SECTION_HEADERS

logger = logging.getLogger("utils")


def find_date_pattern(line: str) -> Match[str] | None:
    """
    Detects a date pattern in a line and returns a match object.

    Args:
        line (str): A line from the resume.

    Returns:
        re.Match or None: Match object if a date pattern is found.
    """
    return re.compile(
        r"^(.*?)((?:January|February|March|April|May|June|July|August|September|October|November|December|"
        r"Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*)"
    ).match(line)


def detect_section(line: str) -> str | None:
    """
    Detects the resume section (e.g., skills, education) a line belongs to using fuzzy matching.

    Args:
        line (str): A line from the resume.

    Returns:
        str or None: Section name if detected, otherwise None.
    """
    line_lower = line.strip().lower()
    for section, keywords in SECTION_HEADERS.items():
        matches = get_close_matches(line_lower, keywords, n=1, cutoff=0.8)
        if matches:
            return section
    return None


def is_bullet(line: str) -> bool:
    """
    Checks if a line starts with a bullet point.

    Args:
        line (str): A line from the resume.

    Returns:
        bool: True if it's a bullet line, else False.
    """
    return line.strip().startswith(('-', '•', '●', '▪'))


def extract_location(text: str) -> str | None:
    """
    Extracts U.S. state from a string using fuzzy matching.

    Args:
        text (str): A text line likely containing a location.

    Returns:
        str or None: Extracted state name or abbreviation, or None if not found.
    """
    state = None
    city = None
    try:
        # geolocator = Nominatim(user_agent="location_extractor")

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
        logger.exception("Address not found", exc)
        # if state and city:
        #     return city, state
        # elif state:
        #     return state
    return None
