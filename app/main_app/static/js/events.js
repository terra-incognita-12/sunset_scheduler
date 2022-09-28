let modal = null;

window.onload = function() {
    default_schedule_hours_total();
}

function edit_data(table_name, id) {
    const data = document.querySelectorAll(`[id^="${id}-${table_name}"]`);
    const form = document.getElementById(`${table_name}_update_form`);
    let form_inputs = form.querySelectorAll("input[type=text], input[type=number], input[type=date], select");
    modal = document.getElementById(`${table_name}_modal`);

    const hidden_id = document.createElement("input");
    hidden_id.type = "hidden";
    hidden_id.value = id
    hidden_id.name = "hidden_id";

    form.appendChild(hidden_id);

    for (var i = 0; i < form_inputs.length; i++){
        if (form_inputs.item(i).type == 'select-one') {
            options = form_inputs.item(i);
            for (var j = 0; j < options.length; j++) {
                if (options.item(j).innerText == data.item(i).innerText) {
                    options.item(j).selected = true;
                }
            }
        } else if (form_inputs.item(i).type == 'date') {
            form_inputs.item(i).value = convert_date_to_iso(data.item(i).innerText);
        } else {
            form_inputs.item(i).value = data.item(i).innerText;
        }
    }

    modal.style.display = 'block';
}

// --- ONLOAD FUNCTIONS ---

function default_schedule_hours_total() {
    let elements = document.querySelectorAll(`[id$="-default_schedule_total"]`);
    for (var i = 0; i < elements.length; i++) {
        hours = elements.item(i).getAttribute('schedule');
        elements.item(i).innerText = calc_schedule_total(hours);
    }
}

// --- MODAL ---

function close_modal() {
    if (!modal) { return; }
    else {
        modal.style.display = 'none';
        modal = null;
    }
}

// --- OTHER FUNCTIONS ---

function convert_date_to_iso(date, add_days_to_date = 0) {
    // Get rid of punctuation marks in date (origin format: Aug. 1, 2022)
    date = date.replace(/[.,]/g, "");
    // Convert to yyyy-mm-dd
    // format_date = new Date(date).toISOString().split('T')[0];
    format_date = new Date(date)
    format_date.setDate(format_date.getDate() + add_days_to_date);
    return format_date.toISOString().split('T')[0];
}

function get24from12(time) {
    time_borders = time.split('-');
    begin = time_borders[0];
    end = time_borders[1];

    if (begin.includes('p') && parseInt(begin) != 12){
        begin = parseInt(begin) + 12;
    } else if (begin.includes('a') && parseInt(begin) == 12) {
        begin = 0;
    } else {
        begin = parseInt(begin);
    }

    if (end.includes('p') && parseInt(end) != 12){
        end = parseInt(end) + 12;
    } else if (end.includes('a') && parseInt(end) == 12) {
        begin = 0;
    } else {
        end = parseInt(end);
    }

    return [begin, end];
}

function calc_schedule_total(schedule) {
    if (schedule == 'Off') {
        return 0;
    }

    schedule = get24from12(schedule);
    begin = schedule[0];
    end = schedule[1];

    total = end - begin;
    if (total < 0) {
        total = end + (24 - begin);
    }

    return total;
}