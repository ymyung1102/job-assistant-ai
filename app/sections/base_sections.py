# base_sections.py
class ResumeSection:
    """
    Base class for all resume sections.

    This class provides basic functionality to store and retrieve
    section content. Intended to be subclassed for specific resume sections
    like Education, Experience, Skills, etc.
    """


    def __init__(self):
        """
        Initializes an empty content list for the resume section.
        Subclasses may extend this to add section-specific initialization.
        """
        self.content = []

    def add_content(self, line: str):
        """
        Adds a line of text to the section.
        Can be overridden if line processing is needed.
        Args:
            line (str): A line of content belonging to the resume section.
        """
        self.content.append(line)

    def get_content(self) -> str:
        """
        Retrieves the complete section content as a single string.
        Subclasses may override this to format content differently.
        Returns:
            str: The concatenated content of the section.
        """
        return '\n'.join(self.content)

    def finalize_section(self):
        """
        Final processing step for the section.

        Can be overridden by subclasses to perform cleanup.
        """
        pass