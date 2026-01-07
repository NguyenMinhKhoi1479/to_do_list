import { apiFetch } from "./auth.js";

export async function getAllUser() {
    const res = await apiFetch("/user/");
    return res.json();
}

export async function getUser(username) {
    const res = await apiFetch(`"/user/${username}"`)
    return res.json();
}

export async function deleteUser(username) {
    const res = await apiFetch(`"/user/${username}"`,{
        method: "DELETE"
    })
    return res.json();
}

export async function createUser(user) {
    const res = await apiFetch("/user/",{
        method: "POST",
        body: {
            username: user.username,
            hashed_pwd: user.password,
            email: user.email
        }
    })
}