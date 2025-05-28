from .base_sections import ResumeSection


class SkillsSection(ResumeSection):
    def __init__(self):
        super().__init__()

    def add_content(self, line):
        values = line.split(':', 1)[1] if ':' in line else line
        skills = [v.strip() for v in values.split(',') if v.strip()]
        self.content.extend(skills)

    def get_content(self):
        return self.content