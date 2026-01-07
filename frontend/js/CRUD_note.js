import { get_all, get_one, delete_task, create_task, modify_task } from "../api/task.js";

const note_list = document.getElementById("note-list");
var note_dialog = document.getElementById('note-dialog');
var dialog = document.getElementById('add-button-dialog');
var add_button = document.getElementById('floating-add-button');

let current_id = null
let data_set = [];

async function load_all_note() {
    const note_list = await get_all()
    note_list.forEach(note => {
        data_set.push({
            id: String(note.id),
            header: note.header,
            description: note.detail,
            is_important: note.is_important,
            date: note.exp_date,
            time: note.exp_time
        })
        console.log(note)
    });
}
//load on start


function add_note() {
    let new_note = {
        id: Math.random().toString(36).substring(2, 10),
        header: dialog.querySelector("#header").value,
        description: dialog.querySelector("#des").value,
        date: dialog.querySelector("#date").value,
        time: dialog.querySelector("#time").value
    }
    if (new_note.header == "" && new_note.des == "") return;
    data_set.push(new_note)
}

function refresh_note_list() {
    note_list.innerHTML = data_set.map(
        value => `
            <div  data-id="${value.id}" class="note">
                <h1 class="header">${value.header}</h1>
                <h2 class="des">${value.description}</h2>
                <ul>
                </ul>
                <div>
                    <h3 class="date">${value.date}</h3>
                    <h3 class="time">${value.time}</h3>
                </div>
            </div>
    `).join("");
}

function find_id(id) {
    var obj = data_set.find(item => item.id === id)
    return obj
}

function delete_by_id(id) {
    let index = data_set.findIndex(item => item.id === id)
    data_set.splice(index, 1)
}

function open_edit_dialog(id) {
    let obj = find_id(id)
    load_data_for_dialog(obj)
    note_dialog.showModal()
}


function deleteNoteAnimation(id) {
    const noteElm = note_list.querySelector(`.note[data-id="${id}"]`)
    if (!noteElm) return;

    noteElm.classList.add("removing");
    noteElm.addEventListener('transitionend', () => {
        delete_by_id(id); // splice trong data_set
    }, { once: true });
}

/* only document have getElementById*/
function load_data_for_dialog(obj) {
    note_dialog.querySelector("#note-header").value = obj.header
    note_dialog.querySelector("#note-des").value = obj.description
    note_dialog.querySelector("#note-date").value = obj.date
    note_dialog.querySelector("#note-time").value = obj.time
}



/*
        <dialog class="main-dialog" id="note-dialog">
            <form action="" class="form-dialog" method="dialog">
                <input id="note-header" placeholder="Header" type="text">
                <textarea id="note-des" placeholder="Description" rows="15"></textarea>
                <h2>deadline</h2>
                <div class="deadline-input">
                    <label for="date">select date</label>
                    <input id="note-date" name="date" type="date">
                    <label for="time">select time</label>
                    <input id="note-time" name="time" type="time">
                </div>
                <div>
                    <button id="save-button">Save</button>
                    <button id="cancle-button">Cancel</button>
                    <button id="delete">Delete</button>
                </div>
            </form>
        </dialog>
*/

dialog.querySelector('#add').addEventListener("click", () => {
    add_note()
    refresh_note_list()
})


//note-dialog
note_dialog.querySelector("#delete").addEventListener('click', () => {
    if (!current_id) return;
    note_dialog.close();
    deleteNoteAnimation(current_id);
});

note_dialog.querySelector("#save-button").addEventListener('click', async () => {
    if (!current_id) return;
    let obj = data_set.find(item => item.id === current_id)
    if (!obj) return;

    let update_obj = {
        header : note_dialog.querySelector("#note-header").value,
        description : note_dialog.querySelector("#note-des").value,
        is_important: false,
        date : note_dialog.querySelector("#note-date").value,
        time : note_dialog.querySelector("#note-time").value
    }
    try{
        var response = await modify_task(current_id,update_obj)
        Object.assign(obj,update_obj)
        refresh_note_list();
        console.log(response)
        console.log("update complete")
    }
    catch(err){
        console.error("update false",err)
        alert("update false")
    }
})

note_list.addEventListener('click', function (e) {
    let note_elm = e.target.closest('.note');
    if (!note_elm) return;
    let id = note_elm.dataset.id
    current_id = id
    open_edit_dialog(current_id)
})

add_button.addEventListener('click', function () {
    // dialog.showModal();
    dialog.querySelector("#header").value = ""
    dialog.querySelector("#des").value = ""
    dialog.querySelector("#date").value = null
    dialog.querySelector("#time").value = null
    dialog.showModal();
});


//init
await load_all_note()
refresh_note_list()
