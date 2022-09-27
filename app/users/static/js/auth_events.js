window.onload = function() {
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))
};

function check_user_avaliability() {
    // const username = document.getElementById('register_user');
    // username.classList.add('is-valid');
}

function clear_validation_input(elem) {
    if (!elem.value) { 
        elem.classList.remove('is-valid')
        elem.classList.remove('is-invalid')
    }
} 

function password_matching() {
    const password1 = document.getElementById('register_pass1');
    const password2 = document.getElementById('register_pass2');
    if (password1.value) {
        if (password1.value != password2.value) {
            password2.classList.remove('is-valid');
            password2.classList.add('is-invalid');
        } else {
            password2.classList.remove('is-invalid');
            password2.classList.add('is-valid');
        }
    } else {
        clear_validation_input(password2);
    } 
}
