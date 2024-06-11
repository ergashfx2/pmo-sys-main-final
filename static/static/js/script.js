function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue
}




document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('add-task').addEventListener('click', function () {
        var form = document.getElementById('phase-form')
        form.insertAdjacentHTML('beforeend', `<div><label> Task nomini yozing :
            <input class="form-control mb-4 task-inputs" type="text" name="task">
            </label><br></div>`);
    })

    document.getElementById('save-all-data').addEventListener('click', function () {
        var data = {}
        var tasks = []
        data['phase_name'] = document.getElementById('phase-input').value
        document.querySelectorAll('.task-inputs').forEach(task => {
            tasks.push(task.value)

        })
        data['tasks'] = tasks
        var ref = window.location.href
        var token = getCookie('csrftoken')
        fetch(`${ref}/add-phase/`, {
            method: "POST",
            headers: {
                "Content-type": "application/json",
                "X-CSRFToken": token
            },
            body: JSON.stringify(data),
        }).then(res => {
            location.reload()
        });

    })

})

    var select = document.getElementById('input-select');
    var array = []
    var button = document.getElementById('do-button')
    var confirm_delete = document.getElementById('confirm')
    var delete_button = document.getElementById('delete-button')
    var all_delete_buttons = document.querySelectorAll('.delete-button')
    var delButton = document.getElementById('del-confirm')
    var selectedFiles = document.querySelectorAll('.del-files')
    var delFiles = []


    delButton.addEventListener('click', function () {
        selectedFiles.forEach(file => {
            file.addEventListener('change', function () {
                if (file.checked === true) {
                    delFiles.push(file.id)
                }
                if (file.checked === false) {
                    delFiles = delFiles.filter(item => item !== file.id)
                }
            })


        all_delete_buttons.forEach(value => {
            value.addEventListener('click', function () {
                confirm_delete.addEventListener('click', function () {
                    fetch(`delete/${value.id}`).then(res => {
                        location.reload()
                    })

                })
            })
        })


        document.querySelectorAll("input[type='checkbox']").forEach(value => {
            value.addEventListener('change', function () {
                if (value.checked === true) {
                    console.log(value.id)
                    array.push(value.id)
                }

            })
        })


        delete_button.addEventListener('click', function () {
            for (i = 0; i < array.length; i++) {
                fetch(`delete-user/${array[i]}`).then(res => {
                    console.log(res)
                    location.reload()
                })
            }

        })

        button.addEventListener('click', function () {
            console.log('clicked')
            if (select.value === 'Bloklash') {
                for (i = 0; i < array.length; i++) {
                    fetch(`block/${array[i]}`).then(res => {
                        location.reload()
                    })
                }
            }
            if (select.value === 'Blokdan ochish') {
                for (i = 0; i < array.length; i++) {
                    fetch(`unblock/${array[i]}`).then(res => {
                        location.reload()
                    })
                }
            }
        })
    })
})

document.addEventListener('DOMContentLoaded', function () {
    var trash_id
    document.querySelectorAll('.trash-icon').forEach(value => {
        value.addEventListener('click', function () {
            trash_id = value.id
        })
    })
    document.getElementById('delete-icon-confirm').addEventListener('click', function () {
        fetch(`/projects/my-projects/delete-phase/${trash_id}`).then(res => {
            location.reload()
        })
    })
})

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.chevron').forEach(value => {
        var icon_class
        value.addEventListener('click', function () {
            if (!value.id) {
                icon_class = document.getElementById('chevron' + value.classList[4]).classList
                console.log(icon_class)
            } else {
                icon_class = document.getElementById(value.id).classList
            }

            if (icon_class[1] === 'fa-chevron-right') {
                icon_class.replace('fa-chevron-right', "fa-chevron-down")
            } else {
                icon_class.replace('fa-chevron-down', "fa-chevron-right")
            }
        })
    })
})


document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('icon-buttons')) {
            var phase_id = event.target.classList[3];
            var element = document.getElementById('phase' + phase_id).textContent.toString()
            document.getElementById('phase' + phase_id).innerHTML = `<input type="text" value="${element}"/>`
            document.getElementById('icons-panel' + phase_id).innerHTML = `<i id="icon-save" class="fa-solid fa-circle-check" style="color: green;cursor: pointer"></i>`
                document.getElementById('icon-save').addEventListener('click', function () {
            var new_input = document.getElementById('phase' + phase_id).children.item(0).value
            var token = getCookie('csrftoken')
            fetch(`update-phase/${phase_id}`, {
                method: "POST",
                headers: {
                    "Content-type": "application/json",
                    "X-CSRFToken": token
                },
                body: JSON.stringify({'phase_name': new_input}),


            }).then(res => {
                location.reload()
            })
        })
        }

        document.addEventListener('keypress', function (event) {
            var new_input = document.getElementById('phase' + phase_id).children.item(0).value
            var token = getCookie('csrftoken')
            if (event.key === 'Enter') {
                fetch(`update-phase/${phase_id}`, {
                    method: "POST",
                    headers: {
                        "Content-type": "application/json",
                        "X-CSRFToken": token
                    },
                    body: JSON.stringify({'phase_name': new_input}),


                }).then(res => {
                    location.reload()
                })
            }

        })

    });
});

document.addEventListener('DOMContentLoaded', function () {
    var task_id
    var label
    var label_text
    document.querySelectorAll('.edit-task-icon').forEach(task => {
        task.addEventListener('click', function () {
            task_id = task.classList[3];
            label = document.getElementById('label' + task_id)
            label_text = document.getElementById('label' + task_id).innerText
            label.innerHTML = `<input id="input${task_id}" type="text" value="${label_text}"/>`
        })

        document.addEventListener('keypress', function (event) {
            if (event.key === 'Enter') {
                var token = getCookie('csrftoken')
                var new_value = document.getElementById('input' + task_id).value
                fetch(`update-task/${task_id}`, {
                    method: "POST",
                    headers: {
                        "Content-type": "application/json",
                        "X-CSRFToken": token
                    },
                    body: JSON.stringify({'task_name': new_value}),


                }).then(res => {
                    location.reload()
                })
            }
        })
    })
})


document.addEventListener('DOMContentLoaded', function () {
    var taskId
    document.querySelectorAll('.delete-task-icon ').forEach(task => {
        task.addEventListener('click', function () {
            taskId = task.id
        })

    })
    document.getElementById('delete-task-confirm').addEventListener('click', function () {
        fetch(`/projects/my-projects/delete-task/${taskId}`).then(res => {
            location.reload()
        })

    })
})


document.addEventListener('DOMContentLoaded', function () {
    var t_id
    document.querySelectorAll('.task-finish').forEach(value => {
        value.addEventListener('click', function () {
            t_id = value.classList[3]
        })
    })
    var new_val
    document.getElementById('task-done').addEventListener('change',function (e){
        new_val = e.target.value
    })
    document.getElementById('finish-task-confirm').addEventListener('click', function () {
        var token = getCookie('csrftoken')
        fetch(`update-task-percentage/${t_id}`, {
            method: "POST",
            headers: {
                "Content-type": "application/json",
                "X-CSRFToken": token
            },
            body: JSON.stringify({'task_done_percentage': new_val}),


        }).then(res => {
            location.reload()
        })
    })

})

document.addEventListener('DOMContentLoaded',function (){
    document.getElementById('url-input').style.display = 'none'
    document.getElementById('add-url').addEventListener('click',function (){
        document.getElementById('url-input').style.display = 'block'
    })

    var form = document.getElementById('add-file-form');
    form.addEventListener('submit',function (){
        window.location.replace('/projects/my-projects/detail/')
    })

})

document.addEventListener('DOMContentLoaded',function (){
    var detfiles = document.querySelectorAll('.del-files');
    var datas = []
        document.getElementById('del-confirm').addEventListener('click',function (e){
        location.reload()
    })

    detfiles.forEach(value => {
        value.addEventListener('change',function (e){
            var checked = e.target.checked
            if (checked){
                datas.push(value.id)
            }else {
                datas = datas.filter(item => item !== value.id);
            }
        })
    })



    document.getElementById('del-confirm').addEventListener('click',function (){
                        var token = getCookie('csrftoken')
                fetch(`delete-files/`, {
                    method: "POST",
                    headers: {
                        "Content-type": "application/json",
                        "X-CSRFToken": token
                    },
                    body: JSON.stringify({'datas': datas }),


                }).then(res => {
                    console.log(res)
                })

    })

})

document.addEventListener('DOMContentLoaded', function () {
    var archive_button = document.getElementById('archive');
    var p_id = archive_button.name;
    archive_button.addEventListener('click', function (e) {
        console.log(p_id);
        fetch(`/projects/my-projects/create-archive/${p_id}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to download archive');
                }
                return response.blob();
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = `${p_id}.zip`;
                link.click();
                window.URL.revokeObjectURL(url);
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    });
});


