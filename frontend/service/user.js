import { apiFetch } from "./api_user.js";

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