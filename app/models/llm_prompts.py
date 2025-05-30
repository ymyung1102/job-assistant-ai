# llm_prompts.py
class Prompt:
    """
    A class to encapsulate prompt templates for resume processing and analysis.
    """
    def __init__(self, resume: str, job_description: str = ""):
        """
        Initializes the Prompt object.

        Args:
            resume (str): The resume content as text.
            job_description (str, optional): The job description content. Defaults to "".
        """
        self.resume = resume
        self.job_description = job_description

    def get_analyze_prompt(self) -> str:
        """
        Generates a prompt to analyze resume match with job descriptions.

        Returns:
            str: The formatted analysis prompt.
        """
        return f"""
            You are an expert HR assistant who matches resumes with job descriptions.
            Given the following resume and job description, your task is to analyze the match between them 
            and provide feedback on how well the candidate fits the role.
            Please rate the match on a scale from 0 to 10, where 0 means no match and 10 means perfect match.
            Additionally, provide a summary of the skills, experience, and qualifications from the resume that
            align with the job description.
            Provide the match score and detailed analysis in markdown format. Include:
            ## **Match Analysis**

            ### **Skills:** Strong match (Python, Docker, REST)
            ### **Experience:** Lacks team leadership
            ### **Suggestions:**
              - Add more metrics to achievements
              - Include recent cloud projects
              
            
            Resume:
            \"\"\"
            {self.resume}
            \"\"\"
    
            Job Description:
            \"\"\"
            {self.job_description}
            \"\"\"
            

            """
    # TODO: To be added for unparsable resume
    def get_format_resume_prompt(self) -> str:
        """
        Generates a prompt to format the resume in a structured way.

        Returns:
            str: The formatted resume prompt.
        """
        return (
            f"You are an extremely strict formatter, NOT a writer."
            f"\nFormat the following text into HTML and CSS for UI display, following these exact rules:"
            f"\n1. One HTML block that starts with ```html containing ONLY the HTML."
            f"\n2. One CSS block that starts with ```css containing ONLY the CSS."
            f"\n3. NO OTHER TEXT should be outside the code blocks."
            f"\n4. In HTML, wrap everything inside a single <div class='user-profile'>."
            f"\n5. Each section must start with an <h2> header and separated by an <hr>."
            f"\n6. Bullet points and nested bullet points should be marked accordingly."
            f"\n7. CSS must center the entire content nicely on the page."
            f"\n8. All text should be in same font style and non-header contents should be in same font size."
            f"\n\nIn the response there should be below sections. Do not include a section is not found in the text."
            f"\n1. Name and contact information: any personal links or address. "
            f"\n2. Summary: short paragraph describing about the person's bio. "
            f"\n3. Skills and Abilities: Technical or soft skills. "
            f"\n4. Work experience: Company name and duration of working along with detailed job description."
            f"\n5. Education: University and the major. "
            f"\n6. Projects: Any personal project and its description. "
            f"\n\nIMPORTANT RULES:"
            f"\n- DO NOT change, reword, or add ANY new text. Only use exactly what is in the input."
            f"\n- DO NOT assume anything. No guessing or imagination."
            f"\n- Follow structure strictly even if the input is messy."
            f"\n\nHere is the text to format:"
            f"\n\"\"\"{self.resume}\"\"\"")

