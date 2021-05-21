const usernameField = document.querySelector('#usernameField');
const feedbackArea = document.querySelector('.invalid_feedback');
const usernameSuccess = document.querySelector('.usernameSuccess');

const emailField = document.querySelector('#emailField');
const emailFeedbackArea = document.querySelector('.emailFeedbackArea');
const emailSuccess = document.querySelector('.emailSuccess');

const passwordField = document.querySelector('#passwordField');
const passwordField2 = document.querySelector('#passwordField2');
const passwordFeedbackArea = document.querySelector('.passwordFeedbackArea');
const passwordSuccess = document.querySelector('.passwordSuccess');

const showPasswordToggle = document.querySelector('.showPasswordToggle');
const submitBtn = document.querySelector('.submit-btn');


//Checking username against database and displaying success and error messages
usernameField.addEventListener('keyup', e => {
    const usernameVal = e.target.value;

    if(usernameVal.length > 0) {
        usernameSuccess.style.display = 'block';
        usernameSuccess.textContent = `Checking ${usernameVal}`;
        usernameField.classList.remove('is-invalid');
        feedbackArea.style.display = 'none';

        fetch("/authentication/validate-username", {
            body: JSON.stringify({username: usernameVal}),
            method: "POST"
        })
        .then(res => res.json())
        .then(data => {
            // console.log(data);
            usernameSuccess.style.display = 'none';
            if(data.username_error){
                submitBtn.disabled = true;
                usernameField.classList.add('is-invalid');
                feedbackArea.style.display = 'block';
                feedbackArea.innerHTML=`<p>${data.username_error}</p>`;
            } else{
                submitBtn.removeAttribute('disabled');
            }
        });
    }
});


//Checking email against database and displaying success and error messages
emailField.addEventListener('keyup', e => {
    const emailVal = e.target.value;

    if(emailVal.length > 0) {
        emailSuccess.style.display = 'block';
        emailSuccess.textContent = `Checking ${emailVal}`;
        emailField.classList.remove('is-invalid');
        emailFeedbackArea.style.display = 'none';

        fetch("/authentication/validate-email", {
            body: JSON.stringify({email: emailVal}),
            method: "POST"
        })
        .then(res => res.json())
        .then(data => {
            // console.log(data);
            emailSuccess.style.display = 'none';
            if(data.email_error){
                submitBtn.disabled = true;
                emailField.classList.add('is-invalid');
                emailFeedbackArea.style.display = 'block';
                emailFeedbackArea.innerHTML=`<p>${data.email_error}</p>`;
            } else {
                submitBtn.removeAttribute('disabled');
            }
        });
    }
});



//Checking password against database and displaying success and error messages
passwordField.addEventListener('keyup', e => {
    const passwordVal = e.target.value;

    
    if(passwordVal.length > 0) {
        passwordSuccess.style.display = 'block';
        passwordSuccess.textContent = `Checking ${passwordVal}`;
        passwordField.classList.remove('is-invalid');
        passwordFeedbackArea.style.display = 'none';

        fetch("/authentication/validate-password", {
            body: JSON.stringify({password: passwordVal}),
            method: "POST"
        })
        .then(res => res.json())
        .then(data => {
            // console.log(data);
            passwordSuccess.style.display = 'none';
            if(data.password_error){
                submitBtn.disabled = true;
                passwordField.classList.add('is-invalid');
                passwordFeedbackArea.style.display = 'block';
                passwordFeedbackArea.innerHTML=`<p>${data.password_error}</p>`;
            } else {
                submitBtn.removeAttribute('disabled');
            }
        });
    }
});

showPasswordToggle.addEventListener('click', toggleHandler)

function toggleHandler(e) {
    if(showPasswordToggle.textContent === 'SHOW') {
        showPasswordToggle.textContent = 'HIDE';
        passwordField.setAttribute('type', 'text')
        passwordField2.setAttribute('type', 'text')
    } else {
        showPasswordToggle.textContent = 'SHOW';
        passwordField.setAttribute('type', 'password')
        passwordField2.setAttribute('type', 'password')
    }
}