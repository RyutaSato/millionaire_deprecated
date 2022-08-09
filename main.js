let client_id = '01G657TC2NK9RSCWC977J1PBQG';
document.querySelector("#ws-id").textContent = client_id.toString();

let onSubmit = document.getElementById("submit")
let url = new URL(`ws://localhost:8000/ws/`)
url.searchParams.set('token', client_id)
console.log(url.toString())
let ws = new WebSocket(url);
ws.onmessage = function(event) {
    let messages = document.getElementById('messages');
    let message = document.createElement('li');
    let content = document.createTextNode(event.data);
    console.log(content);
    let jsonMessage = JSON.parse(event.data);

    if(jsonMessage["status"]==="online"){
        let onlineTag = "<a class=\"online\">online</a>"
        messages.insertAdjacentHTML("beforebegin", onlineTag)
    }
    message.appendChild(content);
    messages.appendChild(message);
};
function sendMessage(event) {
    let messageContext = document.getElementById("messageText")
    let messageDict = {
        "status" : "online",
        "id": client_id,
        "date": new Date().toString(),
        "message": messageContext.value
    };
    console.log(messageDict);
    let messageJson = JSON.stringify(messageDict);
    ws.send(messageJson);
    messageContext.value = '';
    event.preventDefault();
}

function loginPost(event) {
    let loginJson = {
        "username": document.forms.namedItem("email"),
        "password": document.forms.namedItem("password")
    }
    let response = fetch("/user/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: loginJson
    });
    if (response.ok) {
        alert(formData.toString())
    } else {
        alert("Error" + response.headers.get("body"))
    }

}
