var client_id = Date.now()
document.querySelector("#ws-id").textContent = client_id;
var ws = new WebSocket(`ws://localhost/ws/${1}`);

var url_backend = "http://localhost/chatrooms/1"

// var xhr = new HttpRequest();
// xhr.open('GET', url_backend, true);
// xhr.setRequestHeader('Content-Type', 'application/json');
const loadApp = () => {
    fetch(url_backend)
        .then(response => response.json())
        .then(
            data => {
                let messagesHTML = ''
                for (let entry of data.slice().reverse()){
                    console.log(JSON.stringify(entry))
                    messagesHTML += createMessage(JSON.stringify(entry))
                }
                document.getElementById('message-stack').innerHTML = messagesHTML
            }
        );
}
const createMessage = (message) =>{
    var data = `
    <div class="message">
        <p><b>from:</b> {{message.transmitter}} at: {{message.time}}</p>
        <p>${message}</p>
    </div>`;
    return data;
}

async function sendMessage(event) {
    var input = document.getElementById("messageText")
    ws.send(`{"message":"${input.value}", "client_id":"${client_id}"}`)
    input.value = ''
    event.preventDefault()
};

ws.onmessage = function(event) {
    let messagesHTML = document.getElementById('message-stack').innerHTML;
    messagesHTML += createMessage(event.data);
    document.getElementById('message-stack').innerHTML = messagesHTML
};