// workExperience.js

class Projects {
    constructor(resumeEditor) {
        this.resumeEditor = resumeEditor;
    }

    generateProjects(projects) {
        return projects.map((experience, index) => {
            const descriptionHTML = generateEditableBulletList(experience.description, index, "projects");
            return `
            <div class="project">
                <button class="delete-button" onclick="deleteProject(this)">✖</button>
                <div class="name">
                    <label>Project:</label>
                    <input type="text" data-section="projects" data-field="name" data-index=${index} value="${experience.name}" />
                </div>
                <div class="date">
                    <label>Date Duration:</label>
                    <input type="text" data-section="projects" data-field="date" data-index=${index} value="${experience.date}" />
                </div>
                <div class="description">
                    <label>Description:</label>
                    ${descriptionHTML}
                </div>
            </div>
        `;
        }).join('');
    }

    addProject() {
        if (!this.resumeEditor.currentResume.projects) this.resumeEditor.currentResume.projects = [];
        const newProject = {
            name: '',
            date: '',
            description: ['']
        };
        this.resumeEditor.currentResume.projects.push(newProject);
        this.resumeEditor.render();
    }

    deleteProject(buttonElement) {
        const elementDiv = buttonElement.closest('.project');
        const allElements = Array.from(document.querySelectorAll('#project-list .project'));
        const index = allElements.indexOf(elementDiv);
        if (index !== -1) {
            this.resumeEditor.currentResume.projects.splice(index, 1);
            this.resumeEditor.render();
        }
    }

    bindAddListeners() {
        document.getElementById('add-project-btn')?.addEventListener('click', () => {
            this.addProject();
        });
    }

    bindDeleteListeners() {
        const deleteButtons = document.querySelectorAll('#project-list .delete-button');
        deleteButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.deleteProject(button);
            });
        });
    }

}
