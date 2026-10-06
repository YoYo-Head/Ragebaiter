import axios from "./node_modules/axios";

const api = axios.create({
    baseURL: "http://0.0.0.0:8000"

})

export const postMessage = async (message) => {
    const response = await api.post(
        url = "/message",
        data = {
            "message": message

        }

    );

    return response.data;
};


const messageHistory = []

let message;

document.getElementById("submit").onclick = function() {
    message = document.getElementById("message-box").value;
    messageHistory.push(message);
    response = postMessage(message);

    window.alert(response)




}


