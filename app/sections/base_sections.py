class ResumeSection:
    """Base class for all resume sections."""

    def __init__(self):
        self.content = []

    def add_content(self, line):
        self.content.append(line)

    def get_content(self):
        return '\n'.join(self.content)

    def finalize_section(self):
        pass