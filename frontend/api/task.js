import { apiFetch } from "./auth.js";

export async function get_all() {
    const res = await apiFetch("/task/");
    return res.json()
}

export async function get_one(id) {
    const res = await apiFetch(`/task/${id}`)
    return res.json()
}

export async function create_task(task) {
    const res = await apiFetch("/task",{
        method :"POST",
        body: JSON.stringify({
            id: task.id,
            header: task.header,
            detail: task.description,
            is_important: false,
            exp_date: task.date,
            exp_time: task.time
        })
    })
    return res.json()
}

export async function delete_task(id) {
    const res = await apiFetch(`/task/${id}`,{method: "DELETE"})
    return res.json()
}

export async function modify_task(id, task){
    const res = await apiFetch(`/task/${id}`,{
        method: "PATCH",
        body: JSON.stringify({
            header: task.header,
            detail: task.description,
            is_important: false,
            exp_date: task.date,
            exp_time: task.time
        })
    })
    return res.json()
}

