# parser.py
from app.utils.utils import extract_location, detect_section
from app.sections.summary import SummarySection
from app.sections.skills import SkillsSection
from app.sections.work_experience import WorkExperienceSection
from app.sections.education import EducationSection
from app.sections.projects import ProjectsSection

class ResumeParser:
    def __init__(self, text):
        self.text = text
        self.sections = {
            'summary': SummarySection(),
            'skills': SkillsSection(),
            'work_experience': WorkExperienceSection(),
            'education': EducationSection(),
            'projects': ProjectsSection()
        }
        self.current_section = None
        self.location = ''
        self.location_found = False

    def parse(self):
        lines = self.text.splitlines()
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue

            if not self.location_found:
                location = extract_location(line)
                if location:
                    self.location = location
                    self.location_found = True
                    continue

            section = detect_section(line)
            if section:
                self.current_section = section
                continue

            if not self.current_section and self.location_found:
                self.current_section = 'summary'

            if self.current_section in self.sections:
                self.sections[self.current_section].add_content(line)
            else:
                print("Section not yet included.")

        # finalize each section before returning result

        resume_content = {}
        for key, section in self.sections.items():
            section.finalize_section()
            resume_content[key] = section.get_content()

        return {
            'location': self.location,
            **resume_content
        }