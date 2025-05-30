# projects.py
import logging
from .base_sections import ResumeSection
from app.sections import *

logger = logging.getLogger('projects')

class ProjectsSection(ResumeSection):
    """
    A subclass of ResumeSection for parsing and structuring project history.

    This class extracts project_name, date, and descriptive bullet points
    from resume lines based on detected date patterns and bullet formats.
    """
    def __init__(self):
        """
        Initializes the ProjectsSection with state variables to track
        the most recent project entry and bullet formatting context.
        """
        super().__init__()
        self.last_project = None
        self.found_bullet = False

    def add_content(self, line):
        """
        Parses a line of text and adds it to the appropriate
        field in the current or new project entry.

        Args:
            line (str): A line from the resume assumed to be part of the Project section.
        """
        line = line.strip()
        if not line:
            return
        date_match = find_date_pattern(line)
        if date_match:
            if self.last_project:
                self.add_last_project()
            project_name = date_match.group(1).strip()
            date_info = date_match.group(2).strip()
            self.last_project = {
                'project_name': project_name,
                'date': date_info,
                'description': []
            }
        elif is_bullet(line):
            if self.last_project:
                self.found_bullet = True
                bullet_str = re.sub(r'^[•●▪\-\s]*', '', line).strip()
                if bullet_str not in ['●\u200b', '\u200b']:
                    if self.last_project:
                        self.last_project['description'].append(line)
        elif not self.found_bullet and self.last_project.get('description'):
            self.last_project['description'][-1] += ' ' + line
            self.found_bullet = False
        else:
            self.last_project['description'].append(line)
            self.found_bullet = False


    def get_content(self) -> list:
        """
        Retrieves the structured project content.

        Returns:
            list: A list of parsed project entries (dicts).
        """
        return self.content

    def add_last_project(self):
        """
        Appends the currently built project entry to the content list
        and resets the temporary holder.
        """
        if self.last_project:
            self.content.append(self.last_project.copy())
            self.last_project = None

    def finalize_section(self):
        """
        Finalizes the section by saving any in-progress project entry.
        """
        if self.last_project:
            self.add_last_project()
