
// Confirm before deleting a student
function confirmDelete() {
    return confirm("Are you sure you want to delete this student record?");
}

// Show a welcome message when the dashboard loads
document.addEventListener("DOMContentLoaded", function () {
    console.log("Student Management System loaded successfully.");
});


document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("studentSearch");
    const table = document.getElementById("studentsTable");

    if (searchInput && table) {
        searchInput.addEventListener("keyup", function () {
            const searchValue = searchInput.value.toLowerCase();
            const rows = table.getElementsByTagName("tr");

            for (let i = 1; i < rows.length; i++) {
                const rowText = rows[i].textContent.toLowerCase();

                rows[i].style.display =
                    rowText.includes(searchValue) ? "" : "none";
            }
        });
    }
});
document.addEventListener("DOMContentLoaded", function () {
    if (window.lucide) {
        lucide.createIcons();
    }
});
