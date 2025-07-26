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
            
            Your task is to analyze the match between the following resume and job description. Provide feedback on how well the candidate's resume fits the job description.
            
            Instructions:
            - Rate the match on a scale from 0 to 10 (0 = no match, 10 = perfect match).
            - Base your evaluation strictly on the job description.
            - Do **not** penalize for skills or experience not mentioned in the job description.
            - Provide a detailed analysis summarizing how the candidate’s skills, experience, and qualifications align with the job description.
            - Suggest only relevant improvements based on the job description.

            ## **Match Analysis**
            ### **Score:** <match_score>/10
            ### **Skills:**
            - <Skill 1: matched/missing>
            - <Skill 2: matched/missing>
            ...
            ### **Experience:**
            - <Summary of relevant experience>
            - <Any critical gaps>
            
            ### **Suggestions:**
            - <Suggestion 1>
            - <Suggestion 2>
            
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

