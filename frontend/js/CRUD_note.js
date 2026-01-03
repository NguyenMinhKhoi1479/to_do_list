const note_list = document.getElementById("note-list");
var note_dialog = document.getElementById('note-dialog')
let current_id = null
let data_set = [
    {
        id: "1",
        header: "header 1",
        des: "description 1",
        date: "2024-10-01",
        time: "10:00"
    },
    {
        id: "2",
        header: "header 2",
        des: "description 2",
        date: "2024-10-02",
        time: "11:00"
    },
    {
        id: "8",
        header: "header 8",
        des: "awdadasdddddddddddddddawdasdawdasdasddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd 2",
        date: "2024-10-02",
        time: "11:00"
    },
    {
        id: "3",
        header: "header 3",
        des: "description 2",
        date: "2024-10-02",
        time: "11:00"
    },
    {
        id: "4",
        header: "header 4",
        des: "description 2",
        date: "2024-10-02",
        time: "11:00"
    },
    {
        id: "6",
        header: "header 6",
        des: "",
        date: "2024-10-02",
        time: "11:00"
    },

    {
        id: "7",
        header: "header 7",
        des: "description 2",
        date: "2024-10-02",
        time: "11:00"
    }
    ,

    {
        id: "8",
        header: "header 7",
        des: "description 2",
        date: "2024-10-02",
        time: "11:00"
    }
];

function refresh_note_list() {
    note_list.innerHTML = data_set.map(
        value => `
            <div data-id="${value.id}" class="note">
                <h1 class="header">${value.header}</h1>
                <h2 class="des">${value.des}</h2>
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
    note_dialog.querySelector("#note-des").value = obj.des
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

note_dialog.querySelector("#delete").addEventListener('click', () => {
    if (!current_id) return;

    note_dialog.close();
    deleteNoteAnimation(current_id);
});

note_dialog.querySelector("#save-button").addEventListener('click', () => {
    if (!current_id) return;
    obj = data_set.find(item => item.id === current_id)
    if (!obj) return;

    obj.header = note_dialog.querySelector("#note-header").value
    obj.des = note_dialog.querySelector("#note-des").value
    obj.date = note_dialog.querySelector("#note-date").value
    obj.time = note_dialog.querySelector("#note-time").value
    refresh_note_list()
})

note_list.addEventListener('click', function (e) {
    let note_elm = e.target.closest('.note');
    if (!note_elm) return;
    let id = note_elm.dataset.id
    current_id = id
    open_edit_dialog(id)
})


refresh_note_list()
/*
<div data-id="" class="note">
    <h1 class="header">header</h1>
    <h2 class="des">des</h2>
    <ul>
    </ul>
    <div>
        <h3 class="date">date</h3>
        <h3 class="time">time</h3>
    </div>
</div>
*/