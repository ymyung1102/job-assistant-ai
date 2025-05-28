// workExperience.js

class WorkExperience {
    constructor(resumeEditor) {
        this.resumeEditor = resumeEditor;
    }

    generateWorkExperience(workExperience) {
        if (!workExperience) return '';
        return workExperience.map((experience, index) => {
            const descriptionHTML = generateEditableBulletList(experience.description, index, "work_experience");
            return `
            <div class="job">
                <button class="delete-button">✖</button>
                <div class="company_and_location">
                    <label>Company:</label>
                    <input type="text" data-section="work_experience" data-field="company_and_location" data-index=${index} value="${experience.company_and_location}" />
                </div>
                <div class="title">
                    <label>Title:</label>
                    <input type="text" data-section="work_experience" data-field="title" data-index=${index} value="${experience.title}" />
                </div>
                <div class="date">
                    <label>Date Duration:</label>
                    <input type="text" data-section="work_experience" data-field="date" data-index=${index} value="${experience.date}" />
                </div>
                <div class="description">
                    <label>Description:</label>
                    ${descriptionHTML}
                </div>
            </div>
        `;
        }).join('');
    }

    addWorkExperience() {
        if (!this.resumeEditor.currentResume.work_experience)
            this.resumeEditor.currentResume.work_experience = [];
        const newExperience = {
            company_and_location: '',
            title: '',
            date: '',
            description: ['']
        };
        this.resumeEditor.currentResume.work_experience.push(newExperience);
        this.resumeEditor.render();
    }

    deleteWorkExperience(buttonElement) {
        const elementDiv = buttonElement.closest('.job');
        const allElements = Array.from(document.querySelectorAll('#work-experience-list .job'));
        const index = allElements.indexOf(elementDiv);
        if (index !== -1) {
            this.resumeEditor.currentResume.work_experience.splice(index, 1);
            this.resumeEditor.render();
        }
    }

    bindAddListeners() {
        document.getElementById('add-job-btn')?.addEventListener('click', () => {
            this.addWorkExperience();
        });
    }

    bindDeleteListeners() {
        const deleteButtons = document.querySelectorAll('#work-experience-list .delete-button');
        deleteButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.deleteWorkExperience(button);
            });
        });
    }
}
