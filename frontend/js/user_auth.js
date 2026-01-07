import { login } from "../api/auth.js"

const password = document.getElementById("password")
const username = document.getElementById("username")
const check_button = document.getElementById("checkbox")


document.getElementById("login_btn").addEventListener("click",async () => {
    try{
        const response = await login(username.value, password.value)
        window.location.replace("index.html");
    }
    catch{
        console.log("invalid credental")
    }     
});
