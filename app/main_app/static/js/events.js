let modal = null;

// ---------- DATA FUNCTIONS ---------------

function edit_data(table_name) {
    modal = document.getElementById(`${table_name}-modal`);
    modal.style.display = 'block';
}

// ---------- OTHER FUNCTIONS ---------------

function close_modal() {
    if (!modal) { return; }
    else {
        modal.style.display = 'none';
        modal = null;
    }
}