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
        "Content-Type": "application/json",
        ...options.headers
    }

    if(token){
        headers["Authorization"] = `Bearer ${token}`
    }

    const response = await fetch(API_BASE + url,{
        ...options,
        headers
    });


    if(response.status === 403 || response.status === 401){
        localStorage.removeItem("token")

        //return to login menu
        window.location.href = "/login"
        throw new Error(unauthorized)
    }

    if(!response.ok){
        const err = await response.json();
        throw err;
    }

    return response
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

