const camp_passord = document.getElementById("password");
const eye_camp = document.getElementById("button_password");
const eye = document.getElementById("eye");

eye_camp.addEventListener("click", function() {
    if(camp_passord.type== "password") {
        camp_passord.type = "text",
        eye.src = "/static/icons/eye-slash.svg"
    } else [
        camp_passord.type = "password",
        eye.src = "/static/icons/eye.svg"
    ]
})