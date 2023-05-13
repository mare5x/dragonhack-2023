const BACKEND_URL = "http://localhost:5000/chat"


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
  let r = await fetch(BACKEND_URL, { method: 'POST',
    headers: { 
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ msg: message })
  });
  return await r.json();
}

async function addResponseMessage({ msg, img }) {
  console.log(msg, img);
  
  let container = document.createElement('div');
  container.classList.add('image-container');
  
  const imgElement = document.createElement('img');
  // imgElement.src = URL.createObjectURL(new Blob([atob(img)], {type: 'image/jpeg'}));
  imgElement.src = `data:image/jpeg;base64,${img}`;

  const messageElement = document.createElement('div');
  messageElement.classList.add('message');
  messageElement.classList.add(`message-left`);
  messageElement.innerHTML = `<p>${msg}</p>`;
  
  container.appendChild(messageElement);
  container.appendChild(imgElement);

  messages.appendChild(container);
  messages.scrollTop = messages.scrollHeight;
}

sendButton.addEventListener('click', async () => {
  const message = messageInput.value.trim();
  if (message === '') {
    return;
  }
  addUserMessage(message);
  let resp = await getResponse(message);
  await addResponseMessage(resp);

  messageInput.value = '';
});
