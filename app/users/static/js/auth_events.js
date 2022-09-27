window.onload = function() {
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
};

function clear_validation_input(elem) {
    elem.classList.remove('is-valid')
    elem.classList.remove('is-invalid')
} 

function validate_register() {
    var result = true;

    // username, email, password
    const re_array = [
        /^[a-zA-Z0-9_\.]+$/,
        /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,16}$/
    ];

    const elem_array = [
        document.getElementById('register_user'),
        document.getElementById('register_email'),
        document.getElementById('register_pass1')
    ]

    // Regex validation
    for (let i = 0; i < re_array.length; i++) {
        if (re_array[i].test(elem_array[i].value)) {
            clear_validation_input(elem_array[i]);
            elem_array[i].classList.add('is-valid');
        } else {
            clear_validation_input(elem_array[i]);
            elem_array[i].classList.add('is-invalid');
            result = false;
        }
    }

    // Non-regex validation
    pass2 = document.getElementById('register_pass2');
    if (!elem_array[2].value){
        clear_validation_input(pass2);
    } else if (pass2.value == elem_array[2].value) {
        clear_validation_input(pass2);
        pass2.classList.add('is-valid');
    } else {
        clear_validation_input(pass2);
        pass2.classList.add('is-invalid');
        result = false;
    }

    company = document.getElementById('register_company');
    if (company.value) {
        clear_validation_input(company);
        company.classList.add('is-valid');
    } else {
<<<<<<< HEAD:app/users/static/js/auth_events.js
        clear_validation_input(password2);
    } 
}
=======
        clear_validation_input(company);
        company.classList.add('is-invalid');
        result = false;
    }

    return result;
}
>>>>>>> fdd9cc19713f0338fe0dfd29d47d6a3668a4c0a5:app/main_app/static/js/auth_events.js
