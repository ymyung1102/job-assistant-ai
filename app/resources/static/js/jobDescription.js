function resizeTextarea(textarea) {
    // Reset height to auto to shrink if the content is deleted
    textarea.style.height = 'auto';
    // Set the height to match the scrollHeight (content height)
    textarea.style.height = `${textarea.scrollHeight}px`;
}

// For when the content is pasted
document.getElementById('jobDescription').addEventListener('paste', function () {
    // Wait for the paste to complete and trigger resize
    setTimeout(() => resizeTextarea(this), 0);
});