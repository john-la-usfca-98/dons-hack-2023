document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('scheduleForm');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        addClassToSchedule();
    });
});

function addClassToSchedule() {
    const classNum = document.getElementById('classNum').value;
    const classTime = document.getElementById('classTime').value; // POSSIBLY REMOVE CLASS TIME
    
    if (!classNum || !classTime) {
        alert('Please fill in both class number and time.');
        return;
    }

    const table = document.querySelector('.calendar-container');
    let existingRow = null;

    // Check if a row with the same time exists
    for (const row of table.rows) {
        if (row.cells[0].innerText === classTime) {
            existingRow = row;
            break;
        }
    }

    if (!existingRow) {
        // If the row with the given time doesn't exist, create a new row
        existingRow = table.insertRow(-1);
        existingRow.insertCell(0).innerText = classTime;
    }

    const newCell = existingRow.insertCell(-1);
    newCell.innerText = classNum;

    // Clear input fields
    document.getElementById('classNum').value = '';
    document.getElementById('classTime').value = '';
}
