// script.js
document.addEventListener('DOMContentLoaded', function() {
    fetchModels();
    setupEventListeners();
});

function fetchModels() {
    fetch('/models')
        .then(response => response.json())
        .then(models => {
            let select = document.getElementById('modelSelect');
            models.forEach(model => {
                let option = document.createElement('option');
                option.value = model;
                option.text = model;
                select.appendChild(option);
            });
        });
}

function setupEventListeners() {
    document.getElementById("input").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevent the default action to stop from creating a new line
            send();
        }
    });
}

function updateChat(userMessage, botMessage, modelName) {
    var chat = document.getElementById("chat");
    if (userMessage) {
        chat.innerHTML += '<div class="chat-entry user"><p>' + userMessage + '</p></div>';
    }
    if (botMessage) {
        chat.innerHTML += '<div class="chat-entry bot"><p>' + modelName + ': ' + botMessage + '</p></div>';
    }
    chat.scrollTop = chat.scrollHeight; // Auto-scroll to the latest message
}

function send() {
    var input = document.getElementById("input");
    var context = document.getElementById("contextArea").value;
    var model = document.getElementById("modelSelect").value;
    var stream = document.getElementById("streamSelect").value;
    var text = input.value.trim();
    if (!text) return; // Don't send empty messages
    input.value = ''; // Clear the input after sending
    updateChat(text, null, null); // Display user message immediately

    var fullPrompt = context ? context + ". " + text : text;

    fetch('/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            model: model,
            prompt: fullPrompt,
            stream: stream === 'true'
        })
    })
    .then(response => response.json())
    .then(data => {
        updateChat(null, data.response || 'Error: No response from the bot', model);
    })
    .catch(error => {
        console.error('Error:', error);
        updateChat(null, 'Error: ' + error.message, model);
    });
}
