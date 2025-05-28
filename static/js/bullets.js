function generateEditableBulletList(description = [], index, section_name) {
    // TODO: Ctrl-Z is not working as expected
    if (!Array.isArray(description)) {
        description = [description];
    }
    // let bulletText = (description.length > 0)
    //     ? description.map(item => `• ${item}`).join('\n')
    //     : '• ';
    return `<textarea data-section="${section_name}" data-field="description" data-index="${index}"
            oninput="handleInput(this, ${index})"
            onkeydown="handleEnter(event, this)"></textarea>`;
    // return `<textarea data-section=${section_name} data-field="description" data-index=${index}
    //         oninput="handleInput(this, ${index})"
    //         onkeydown="handleEnter(event, this)">${bulletText}</textarea>`;
}

function populateTextareas() {
    const descriptions = document.querySelectorAll('textarea[data-field="description"]');
    descriptions.forEach(textarea => {
        const section = textarea.dataset.section;
        const index = textarea.dataset.index;
        const value = resumeEditor.currentResume[section][index].description;

        if (Array.isArray(value)) {
            textarea.value = value.map(item => `• ${item}`).join('\n');
        } else {
            textarea.value = `• ${value}`;
        }

        // Also trigger resize
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    });
}

// When new line, add a bullet point
function handleInput(textarea, index) {
    const lines = textarea.value.split('\n').map(line => {
        // If the line doesn't start with a bullet, add it
        if (line.trim() !== '' && !line.trim().startsWith('•')) {
            return '• ' + line.trim();
        }
        return line;
    });
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
    // Rejoin the lines
    const newText = lines.join('\n');
    if (textarea.value !== newText) {
        textarea.value = newText;

        // Optional: move cursor to end
        textarea.selectionStart = textarea.selectionEnd = textarea.value.length;
    }
}

// When user presses Enter in bullet mode
function handleEnter(event, textarea) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent default new line
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;

        const value = textarea.value;
        const before = value.substring(0, start);
        const after = value.substring(end);

        // Insert a newline and bullet
        const newValue = before + '\n• ' + after;
        textarea.value = newValue;

        // Move the cursor after the bullet
        const newCursorPos = start + 3; // 1 for \n, 2 for bullet + space
        textarea.setSelectionRange(newCursorPos, newCursorPos);

        // Trigger input event manually
        textarea.dispatchEvent(new Event('input'));
    }
}
