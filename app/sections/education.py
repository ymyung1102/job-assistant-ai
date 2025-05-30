# education.py
import logging
from .base_sections import ResumeSection
from app.sections import *

logger = logging.getLogger('education')

class EducationSection(ResumeSection):
    """
    A subclass of ResumeSection for parsing and structuring education history.

    This class extracts university, degree, date, and descriptive bullet points
    from resume lines based on detected date patterns and bullet formats.
    """
    def __init__(self):
        """
        Initializes the EducationSection with state variables to track
        the most recent education entry and bullet formatting context.
        """
        super().__init__()
        self.last_education = None
        self.found_bullet = False

    def add_content(self, line):
        """
        Processes a single line of text and adds it to the appropriate
        field in the current or new education entry.

        Args:
            line (str): A line from the resume assumed to be part of the Education section.
        """
        line = line.strip()
        if not line:
            return
        date_match = find_date_pattern(line)
        if date_match:
            education_name = date_match.group(1).strip()
            date_info = date_match.group(2).strip()
            location = extract_location(education_name)
            if location:
                if self.last_education:
                    self.add_last_education()
                self.last_education = {
                    'university_and_location': education_name,
                    'degree': '',
                    'date': date_info,
                    'description': []
                }
            else:
                self.last_education['description'].append(line)
        elif is_bullet(line):
            self.found_bullet = True
            bullet_str = re.sub(r'^[•●▪\-\s]*', '', line).strip()
            if bullet_str not in ['●\u200b', '\u200b']:
                if self.last_education:
                    self.last_education['description'].append(bullet_str)
        elif self.found_bullet and self.last_education:
            self.last_education['description'].append(line)
            self.found_bullet = False
        elif self.last_education and not self.last_education.get('degree'):
            self.last_education['degree'] = line
        elif self.last_education.get('description'):
            self.last_education['description'][-1] += ' ' + line
            self.found_bullet = False
        else:
            self.last_education['description'].append(line)
            self.found_bullet = False

    def get_content(self) -> list:
        """
        Retrieves the structured education content.

        Returns:
            list: A list of parsed education entries (dicts).
        """
        return self.content

    def add_last_education(self):
        """
        Appends the currently built education entry to the content list
        and resets the temporary holder.
        """
        if self.last_education:
            self.content.append(self.last_education.copy())
            self.last_education = None

    def finalize_section(self):
        """
        Finalizes the section by saving any in-progress education entry.
        """
        if self.last_education:
            self.add_last_education()
