//import axios from "axios";

function createBubbleHTML(className, text) {
    return `
    <div class="${className}">
        <p class="speech-text">${text}</p>
    </div>
    `;

}



const api = axios.create({
    baseURL: "/"

})

export const postMessage = async (message) => {
    const response = await api.post(
        "/message",
        {
            "message": message
        }
        
    );

    const msg = response.data.message;

    return msg;
};


let message;
let response;
let bubble;

const container = document.getElementById("middle-container");

document.getElementById("submit").onclick = async function() {
    message = document.getElementById("message-box").value;
    
    bubble = createElement(createBubbleHTML("speechb1", message));
    container.appendChild(bubble);
    container.scrollTop = container.scrollHeight;

    response = await postMessage(message);

    bubble = createElement(createBubbleHTML("speechb2", response));
    container.appendChild(bubble);
    container.scrollTop = container.scrollHeight;

}

function createElement(html, parentClass) {
    const template = document.createElement("template");

    template.innerHTML = html.trim();

    return template.content.firstElementChild;
}
