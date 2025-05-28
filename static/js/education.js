// workExperience.js

class Education {
    constructor(resumeEditor) {
        this.resumeEditor = resumeEditor;
    }

    generateEducation(education) {
        return education.map((experience, index) => {
            const descriptionHTML = generateEditableBulletList(experience.description, index, "education");
            return `
            <div class="college">
                <button class="delete-button" onclick="deleteEducation(this)">✖</button>
                <div class="university_and_location">
                    <label>University and Location:</label>
                    <input type="text" data-section="education" data-field="university_and_location" data-index=${index} value="${experience.university_and_location}" />
                </div>
                <div class="degree">
                    <label>Degree:</label>
                    <input type="text" data-section="education" data-field="degree" data-index=${index} value="${experience.degree}" />
                </div>
                <div class="date">
                    <label>Date Duration:</label>
                    <input type="text" data-section="education" data-field="date" data-index=${index} value="${experience.date}" />
                </div>
                <div class="description">
                    <label>Description:</label>
                    ${descriptionHTML}
                </div>
            </div>
        `;
        }).join('');
    }

    addEducation() {
        if (!this.resumeEditor.currentResume.education) this.resumeEditor.currentResume.education = [];

        const newEducation = {
            university_and_location: '',
            degree: '',
            date: '',
            description: ['']
        };

        this.resumeEditor.currentResume.education.push(newEducation);
        this.resumeEditor.render();
    }

    deleteEducation(buttonElement) {
        const elementDiv = buttonElement.closest('.college');
        const allElements = Array.from(document.querySelectorAll('#education-list .college'));
        const index = allElements.indexOf(elementDiv);
        if (index !== -1) {
            this.resumeEditor.currentResume.education.splice(index, 1);
            this.resumeEditor.render();
        }
    }

    bindAddListeners() {
        document.getElementById('add-education-btn')?.addEventListener('click', () => {
            this.addEducation();
        });
    }

    bindDeleteListeners() {
        const deleteButtons = document.querySelectorAll('#education-list .delete-button');
        deleteButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.deleteEducation(button);
            });
        });
    }
}
