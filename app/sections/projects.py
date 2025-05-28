from .base_sections import ResumeSection
from app.sections import *


class ProjectsSection(ResumeSection):
    def __init__(self):
        super().__init__()
        self.last_project = None
        self.found_bullet = False

    def add_content(self, line):
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


    def get_content(self):
        return self.content

    def add_last_project(self):
        if self.last_project:
            self.content.append(self.last_project.copy())
            self.last_project = None

    def finalize_section(self):
        if self.last_project:
            self.add_last_project()
