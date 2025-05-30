# work_experience.py
import logging
from .base_sections import ResumeSection
from app.sections import *

logger = logging.getLogger('work_experience')

class WorkExperienceSection(ResumeSection):
    """
    A subclass of ResumeSection for parsing and structuring work experiences.

    This class extracts structured job data such as company and location,
    job title, dates, and description bullet points from resume lines.
    """
    def __init__(self):
        """
        Initializes the WorkExperienceSection with state variables to track
        the most recent job entry and bullet formatting context.
        """
        super().__init__()
        self.last_company = ""
        self.last_job = {}
        self.found_bullet = False

    def add_content(self, line: str):
        """
        Processes a single line of text and adds it to the appropriate
        field in the current or new job entry.
        Args:
            line (str): A line from the resume assumed to be part of
                the Work Experience section.

        """
        line = line.strip()
        if not line:
            return
        date_match = find_date_pattern(line)
        if date_match:
            if self.last_job and self.last_job.get('title') != '':
                self.add_last_job()
            company_or_title = date_match.group(1).strip()
            date_info = date_match.group(2).strip()
            location = extract_location(company_or_title)
            if location:
                self.last_company = company_or_title
                self.last_job = {
                    'company_and_location': company_or_title,
                    'title': '',
                    'date': date_info,
                    'description': []
                }
            else:
                self.last_job = {
                    'company_and_location': self.last_company,
                    'title': company_or_title,
                    'date': date_info,
                    'description': []
                }
        elif is_bullet(line):
            self.found_bullet = True
            bullet_str = re.sub(r'^[•●▪\-\s]*', '', line).strip()
            if bullet_str not in ['●\u200b', '\u200b']:
                if self.last_job:
                    self.last_job['description'].append(bullet_str)
        elif self.found_bullet and self.last_job:
            self.last_job['description'].append(line)
            self.found_bullet = False
        elif self.last_job and not self.last_job.get('title'):
            self.last_job['title'] = line
        elif self.last_job.get('description'):
            self.last_job['description'][-1] += ' ' + line
            self.found_bullet = False
        else:
            self.last_job['description'].append(line)
            self.found_bullet = False

    def get_content(self) -> list:
        """
        Retrieves the structured work experience content.

        Returns:
            list: A list of parsed job entries (dicts).
        """
        return self.content

    def add_last_job(self):
        """
        Appends the currently built job entry to the content list
        and resets the temporary holder.
        """
        if self.last_job:
            self.content.append(self.last_job.copy())
            self.last_job = {}

    def finalize_section(self):
        """
        Finalizes the section by saving any in-progress job entry.
        """
        if self.last_job:
            self.add_last_job()