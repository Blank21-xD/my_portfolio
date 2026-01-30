// This handles the automatic year update in the footer
document.addEventListener('DOMContentLoaded', function () {
    const yearSpan = document.getElementById("year");
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
});

// You can add more JS logic here later, like form animations g!