const BACKEND_URL = "http://localhost:5000"


const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const messages = document.getElementById('messages');


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

  messageInput.value = '';
});

messageInput.addEventListener('keydown', async (event) => {
  if (event.keyCode === 13) { // Check if enter key was pressed
    moveImage()
    const message = messageInput.value.trim();
    if (message === '') {
      return;
    }
    addUserMessage(message);
    messageInput.value = ''; // Clear the message input field
    let resp = await getResponse(message);
    await addResponseMessage(resp);

  }
});

function moveImage() {
  let topPos = 0;
  let leftPos = 0;
  const img = document.getElementById('my-image');
  const interval = setInterval(frame, 20);

  function frame() {
    if (topPos >= window.innerHeight - img.height) {
      clearInterval(interval);
    } else {
      topPos++;
      img.style.top = topPos + 'px';
    }
  }
}

