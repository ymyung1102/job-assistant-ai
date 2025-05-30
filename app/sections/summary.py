# summary.py
import logging
from .base_sections import ResumeSection

logger = logging.getLogger('summary')

class SummarySection(ResumeSection):
    """
    A subclass of ResumeSection for parsing and storing the resume summary section.
    Typically accumulates summary lines without special processing.
    """

    def __init__(self):
        """
        Initializes the SummarySection.
        """
        super().__init__()
