const messageHistory = []

let message;

document.getElementById("submit").onclick = function() {
    message = document.getElementById("message-box").value;
    messageHistory.push(message);

}


