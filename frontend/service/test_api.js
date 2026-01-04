import { login } from "./api_user.js";
import { getAllUser } from "./user.js";

async function run() {
    try{
        await login("1","1");
        const users = await getAllUser();
        console.log(users)
    }
    catch(err){
        let p = document.getElementById("message")
        p.textContent = err.message
        console.error(err.message)
    }
}

run();