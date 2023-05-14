const BACKEND_URL = "http://localhost:5000"


const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const messages = document.getElementById('messages');
const clearButton = document.getElementById('clear-button');


function addUserMessage(text) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message');
  messageElement.classList.add(`message-right`);
  messageElement.innerHTML = `<p>${text}</p>`;
  messages.appendChild(messageElement);
  messages.scrollTop = messages.scrollHeight;
}

async function getResponse(message) {
  let r = await fetch(BACKEND_URL + "/chat", { method: 'POST',
    headers: { 
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ msg: message })
  });
  return await r.json();
}

async function addResponseMessage(response) {
  resp = response["response"];
  console.log(response);

  if (response["task"] === "undefined" ) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(`message-left`);
    messageElement.innerHTML = `<p>${resp}</p>`;
    messages.appendChild(messageElement);
    messages.scrollTop = messages.scrollHeight;
    return;
  }

  let container = document.createElement('div');
  container.classList.add('image-container');
  
  const imgElement = document.createElement('img');
  imgElement.src = `data:image/jpeg;base64,${resp["image"]}`;

  const forecastElement = document.createElement('img');
  forecastElement.src = `data:image/jpeg;base64,${resp["forecast_image"]}`;

  const messageElement = document.createElement('div');
  messageElement.classList.add('message');
  messageElement.classList.add(`message-left`);
  messageElement.innerHTML = `<p>${resp["model_response"]}</p>`;
  
  container.appendChild(messageElement);
  container.appendChild(imgElement);
  container.appendChild(forecastElement);

  messages.appendChild(container);
  messages.scrollTop = messages.scrollHeight;
}

sendButton.addEventListener('click', async () => {
  const message = messageInput.value.trim();
  if (message === '') {
    return;
  }
  addUserMessage(message);
  messageInput.value = '';
  let resp = await getResponse(message);
  await addResponseMessage(resp);
});

messageInput.addEventListener('keydown', async (event) => {
  if (event.keyCode === 13) {
    const message = messageInput.value.trim();
    if (message === '') {
      return;
    }
    addUserMessage(message);
    messageInput.value = '';
    let resp = await getResponse(message);
    await addResponseMessage(resp);
  }
});

clearButton.addEventListener('click', () => {
  messages.innerHTML = '';
  messageInput.value = '';
});

