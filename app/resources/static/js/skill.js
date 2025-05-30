// skill.js

class Skill {
    constructor(resumeEditor) {
        this.resumeEditor = resumeEditor;
    }

    generateSkill(skillList) {
        const skills = skillList || [];
        return `
            <div id="skill-container">
                ${skills.map((skill, index) => `
                    <div class="skill-chip" data-index="${index}">
                        <span>${skill}</span>
                        <button class="skill-delete-button">✖</button>
                    </div>
                `).join('')}
                <div class="skill-input-wrapper">
                    <input type="text" id="new-skill-input" placeholder="Add a skill" />
                    <button id="add-skill-btn">Add</button>
                </div>
                <div id="skill-warning" class="skill-warning" style="color: red; margin-top: 5px;"></div>
            </div>
        `;
    }

    addSkill(skillValue) {
        if (!this.resumeEditor.currentResume.skills) this.resumeEditor.currentResume.skills = [];
        if (skillValue && !this.resumeEditor.currentResume.skills.includes(skillValue)) {
            this.resumeEditor.currentResume.skills.push(skillValue.trim());

            requestAnimationFrame(() => {
                const input = document.getElementById('new-skill-input');
                if (input) input.focus();
            });
            this.resumeEditor.render();
        }
        else {
            const warningEl = document.getElementById('skill-warning');
            if (warningEl) warningEl.textContent = `"${skillValue.trim()}" is already added.`;

        }
    }

    deleteSkill(buttonElement) {
        const elementDiv = buttonElement.closest('.skill-chip');
        const index = parseInt(elementDiv.getAttribute('data-index'));
        if (!isNaN(index)) {
            this.resumeEditor.currentResume.skills.splice(index, 1);
            this.resumeEditor.render();
        }
    }

    bindAddListeners() {
        document.getElementById('add-skill-btn')?.addEventListener('click', () => {
            const input = document.getElementById('new-skill-input');
            if (input && input.value.trim() !== '') {
                this.addSkill(input.value);
                input.value = '';
            }
        });
        document.getElementById('new-skill-input')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const input = e.target;
                if (input.value.trim() !== '') {
                    this.addSkill(input.value);
                    input.value = '';
                }
            }
        });
    }

    bindDeleteListeners() {
        const deleteButtons = document.querySelectorAll('#skill-container .skill-delete-button');
        deleteButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.deleteSkill(button);
            });
        });
    }
}
