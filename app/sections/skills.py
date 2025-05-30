# skills.py
import logging
from .base_sections import ResumeSection

logger = logging.getLogger('skills')

class SkillsSection(ResumeSection):
    """
    A subclass of ResumeSection for parsing and structuring skills.

    This class extracts skills listed in resume lines, supporting
    formats like "Skills: Python, Java, SQL" or just comma-separated lists.
    """
    def __init__(self):
        """
        Initializes the SkillsSection.
        """
        super().__init__()

    def add_content(self, line: str):
        """
        Parses a line to extract skills and adds them to the content list.

        Args:
            line (str): A line from the resume containing skills.
        """
        values = line.split(':', 1)[1] if ':' in line else line
        skills = [v.strip() for v in values.split(',') if v.strip()]
        self.content.extend(skills)

    def get_content(self) -> list:
        """
        Returns the list of parsed skills.

        Returns:
            list: Parsed skills as a list of strings.
        """
        return self.content