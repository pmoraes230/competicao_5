const camp_passord = document.getElementById("password");
const eye_camp = document.getElementById("button_password");
const eye = document.getElementById("eye");

const camp_passord2 = document.getElementById("password2");
const eye_camp2 = document.getElementById("button_password2");
const eye2 = document.getElementById("eye2");

eye_camp.addEventListener("click", function() {
    if(camp_passord.type== "password") {
        camp_passord.type = "text",
        eye.src = "/static/icons/eye-slash.svg"
    } else [
        camp_passord.type = "password",
        eye.src = "/static/icons/eye.svg"
    ]
})

eye_camp2.addEventListener("click", function() {
    if(camp_passord2.type== "password") {
        camp_passord2.type = "text",
        eye2.src = "/static/icons/eye-slash.svg"
    } else [
        camp_passord2.type = "password",
        eye2.src = "/static/icons/eye.svg"
    ]
})