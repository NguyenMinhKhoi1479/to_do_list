// api_post_test = "https://jsonplaceholder.typicode.com/posts"
// //test
// fetch(api_post_test)
//     .then(function(response){
//         return response.json();
//     })
//     .then(function(json){
//         console.log(json)
//     })

const API_BASE = "http://127.0.0.1:8000";

export async function apiFetch(url, options = {}) { //param url is the api url, option
    const token = localStorage.getItem("token");

    const headers = {
        ...options.headers
    }

    if(token){
        headers["Authorization"] = `Bearer ${token}`
    }

    return fetch(API_BASE+url,{
        ...options,
        headers
    });
}

export async function login(username, pwd) {
    const response = await fetch("http://127.0.0.1:8000/user/token",{
        method: "POST",
        headers: {
            "Content-Type" : "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            username: username,
            password: pwd
        })
    });

    if(!response.ok){
        throw new Error("invalid credental")
    }

    const data = await response.json();

    localStorage.setItem("token" , data.access_token)

    return data;
}

