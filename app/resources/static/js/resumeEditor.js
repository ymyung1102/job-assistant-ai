class ResumeEditor {
    constructor(resume) {
        this.currentResume = resume;
        this.container = document.querySelector('.resume-container');
        this.skill = new Skill(this);
        this.workExperience = new WorkExperience(this);
        this.education = new Education(this);
        this.projects = new Projects(this);
    }

    render() {
        const editableHTML = this.generateEditableHTML(this.currentResume);
        this.container.innerHTML = editableHTML;
        this.skill.bindDeleteListeners();
        this.skill.bindAddListeners();
        this.workExperience.bindDeleteListeners();
        this.workExperience.bindAddListeners();
        this.education.bindDeleteListeners();
        this.education.bindAddListeners();
        this.projects.bindDeleteListeners();
        this.projects.bindAddListeners();
        this.autoResizeAllTextareas();
        populateTextareas();
    }

    generateEditableHTML(resume) {
        let skillHTML = this.skill.generateSkill(resume.skills)
        let workExperienceHTML = this.workExperience.generateWorkExperience(resume.work_experience);
        let educationHTML = this.education.generateEducation(resume.education);
        let projectsHTML = this.projects.generateProjects(resume.projects);

        return `
            <div class="section location"><h2>Location</h2><hr><input type="text" data-section="location" data-field="description" data-index="0" value="${resume.location}" /></div>
            <div class="section summary"><h2>Summary</h2><hr><input type="text" data-section="summary" data-field="description" data-index="0" value="${resume.summary}" /></div>
            <div class="section skills">
                <h2>Skills</h2><hr>
                <div class="skill-list">${skillHTML}</div>
            </div>

            <div class="section work-experience">
                <h2>Work Experience</h2><hr>
                <div id="work-experience-list">${workExperienceHTML}</div>
                <div class="button-wrapper"><button id="add-job-btn">Add Job</button></div>
            </div>
            <div class="section education">
                <h2>Education</h2><hr>
                <div id="education-list">${educationHTML}</div>
                <div class="button-wrapper"><button id="add-education-btn">Add Education</button></div>
            </div>
            <div class="section projects">
                <h2>Projects</h2><hr>
                <div id="project-list">${projectsHTML}</div>
                <div class="button-wrapper"><button id="add-project-btn">Add Project</button></div>
            </div>
        `;
    }

    collectResumeData() {
        const resumePane = document.querySelector('.resume-pane');
        const inputs = resumePane.querySelectorAll('input, textarea');

        const resume = {
            location: '',
            summary: '',
            skills: [],
            work_experience: [],
            education: [],
            projects: []
        };

        inputs.forEach(input => {
            const section = input.dataset.section;
            const field = input.dataset.field;
            const index = parseInt(input.dataset.index, 10);

            if (!section) return;
            const cleanValue = DOMPurify.sanitize(input.value);
            if (section === 'location' || section === 'summary') {
                resume[section] = cleanValue;
            } else if (Array.isArray(resume[section])) {
                if (!resume[section][index]) resume[section][index] = {};
                resume[section][index][field] = cleanValue;
            }
        });
        const skillChips = resumePane.querySelectorAll('#skill-container .skill-chip span');
        resume.skills = Array.from(skillChips).map(chip => DOMPurify.sanitize(chip.textContent.trim()));

        resumeEditor.currentResume = resume;
        return resume;
    }

    autoResizeAllTextareas() {
        document.querySelectorAll('textarea').forEach(textarea => {
            textarea.style.height = 'auto';
            textarea.style.height = textarea.scrollHeight + 'px';
        });
    }
}

// Initialize everything
const initialResumeData = {
    location: '',
    summary: '',
    skills: [],
    work_experience: [{ company_and_location: '', title: '', date: '', description: [] }],
    education: [{ college: '', degree: '', date: '' }],
    certifications: [{name:''}],
    projects: [{ project_name: '', description: [''] }]
};

let resumeEditor = new ResumeEditor(initialResumeData);
resumeEditor.render();


document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const backendURL = 'http://127.0.0.1:5000';
    const formData = new FormData();
    const fileInput = document.getElementById('resume');
    formData.append('resume', fileInput.files[0]);
    document.getElementById('uploadResume').style.visibility = 'hidden';
    document.getElementById('resume-loading').style.display = 'flex';

    fetch(`${backendURL}/upload`, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            // Initialize ResumeEditor with uploaded resume
            resumeEditor = new ResumeEditor(data);
            resumeEditor.render();  // This handles DOM updates

        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('resume-editor').innerHTML = 'An error occurred. Please try again.';
        })
        .finally(() => {
            document.getElementById('resume-loading').style.display = 'none';
            document.getElementById('uploadResume').style.visibility = 'visible';
        });
});

document.getElementById('analyzeMatch').addEventListener('click', async function (e) {
    // Prevent default form submission behavior if this button is inside a form
    e.preventDefault();
    const resume = resumeEditor.collectResumeData();
    // Extract job description (from textarea)
    const jobDesc = DOMPurify.sanitize(document.getElementById('jobDescription').value);

    // Check if all required fields are filled
    console.log(resume)
    if (!resume.skills || !resume.work_experience || !resume.education || !jobDesc) {
        alert('Please fill in all resume sections and provide the job description.');
        return;
    }

    // Show loading indicator
    document.getElementById('analyzeMatch').style.visibility = 'hidden';
    document.getElementById('loading').style.display = 'flex';

    // Make the POST request to the backend
    try {
        const response = await fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                resume: resume,
                job_description: jobDesc
            })
        });

        if (response.ok) {
            const data = await response.json();
            // Handle the result (e.g., display it in the UI)
            if (data.result) {
                document.getElementById('result-container').innerHTML = DOMPurify.sanitize(marked.parse(data.result));
            }
        } else {
            console.error('Error:', response.statusText);
            document.getElementById('result-container').innerHTML = 'An error occurred. Please try again.';
        }

    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = 'An error occurred. Please try again.';
    } finally {
        // Hide loading indicator after request is complete
        document.getElementById('loading').style.display = 'none';
        document.getElementById('analyzeMatch').style.visibility = 'visible';
    }
});

// function collectResumeData() {
//     const resumePane = document.querySelector('.resume-pane');
//     const inputs = resumePane.querySelectorAll('input, textarea');
//
//     const resume = {
//         location: '',
//         summary: '',
//         skills: '',
//         work_experience: [],
//         education: [],
//         projects: []
//     };
//
//     inputs.forEach(input => {
//         const section = input.dataset.section;
//         const field = input.dataset.field;
//         const index = parseInt(input.dataset.index, 10);
//
//         if (!section) return;
//
//         if (section === 'location' || section === 'summary' || section === 'skills') {
//             resume[section] = input.value;
//         } else if (Array.isArray(resume[section])) {
//             if (!resume[section][index]) resume[section][index] = {};
//             resume[section][index][field] = input.value;
//         }
//     });
//     resumeEditor.currentResume = resume;
//     return resume;
// }
