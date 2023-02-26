let modal = null;

window.onload = function() {
    default_schedule_hours_total();
    dates_of_week();
    weekdays_name();
    weekday_hours_total();
    week_hours_total();
}

function edit_data(table_name, id) {
    const data = document.querySelectorAll(`[id^="${id}-${table_name}"]`);
    const form = document.getElementById(`${table_name}_update_form`);
    const form_inputs = form.querySelectorAll("input[type=text], input[type=number], input[type=date], select");
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
            if (data.item(i).innerText == 'Off') {
                form_inputs.item(i).value = ''
            } else {
                form_inputs.item(i).value = data.item(i).innerText;
            }
        }
    }

    modal.style.display = 'block';
}

// --- ONLOAD FUNCTIONS ---

function default_schedule_hours_total() {
    const elements = document.querySelectorAll(`[id$="-default_schedule_total"]`);
    for (var i = 0; i < elements.length; i++) {
        hours = elements.item(i).getAttribute('schedule');
        elements.item(i).innerText = calc_schedule_total(hours);
    }
}

function dates_of_week() {
    const date = document.querySelector(`[id$="-schedule_profile_begin_date"`).innerText;
    const date_elemetns = document.getElementsByClassName('date_weekday');

    for (var i = 0; i < date_elemetns.length; i++) {
        format_date = convert_date_to_iso(date, i).split('-');
        date_elemetns.item(i).innerText = `${format_date[1]}/${format_date[2]}/${format_date[0]}`;
    }
}

function weekdays_name() {
    const date = document.querySelector(`[id$="-schedule_profile_begin_date"`).innerText;
    const date_elemetns = document.getElementsByClassName('weekday_name');

    for (var i = 0; i < date_elemetns.length; i++) {
        date_elemetns.item(i).innerText = convert_date_to_week_name(date, i);
    }
}

function weekday_hours_total() {
    const day_elements = document.getElementsByClassName('weekday');
    const weekday_total_elements = document.getElementsByClassName('weekday_total_hours');

    for (var i = 0; i < day_elements.length; i++) {
        var total = calc_schedule_total(day_elements.item(i).innerText);
        if (total > 0) {
            weekday_total_elements.item(i).innerText = `(${total})`;
        }
    }
}

function week_hours_total() {
    const day_elements = document.getElementsByClassName('weekday');
    const week_total_elements = document.querySelectorAll(`[id$="-week_total_hours"]`);
    
    let totals = [];
    var week_iter = 0;
    var total = 0;

    for (var i = 0; i < day_elements.length; i++) {
        total += calc_schedule_total(day_elements.item(i).innerText)
        week_iter += 1;
        if (week_iter == 7) {
            totals.push(total);
            total = 0;
            week_iter = 0;
        }
    }

    for (var i = 0; i < week_total_elements.length; i++) {
        if (totals[i] > 40) {
            week_total_elements.item(i).innerHTML = `<b>${totals[i]} <span class="text-danger">(OVERTIME)</span></b>`;
        } else {
            week_total_elements.item(i).innerHTML = `<b>${totals[i]}</b>`;
        }
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
    const format_date = new Date(date)
    format_date.setDate(format_date.getDate() + add_days_to_date);
    return format_date.toISOString().split('T')[0];
}

function convert_date_to_week_name(date, add_days_to_date = 0) {
    date = date.replace(/[.,]/g, "");
    const format_date = new Date(date)
    format_date.setDate(format_date.getDate() + add_days_to_date);
    return format_date.toLocaleDateString('en-US', { weekday: 'long' });
}

function get24from12(time) {
    const time_borders = time.split('-');
    var begin = time_borders[0];
    var end = time_borders[1];

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
    const begin = schedule[0];
    const end = schedule[1];

    var total = end - begin;
    if (total < 0) {
        total = end + (24 - begin);
    }

    return total;
}