const BACKEND_URL = "http://localhost:5000/chat"


const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const messages = document.getElementById('messages');

function addMessage(side, text) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message');
  messageElement.classList.add(`message-${side}`);
  messageElement.innerHTML = `<p>${text}</p>`;
  messages.appendChild(messageElement);
  messages.scrollTop = messages.scrollHeight;
}

async function processUserMessage(message) {
  let r = await fetch(BACKEND_URL, { method: 'POST',
    headers: { 
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ msg: message })
  });
  r = await r.json();
  console.log(r);
  let response = r["msg"];
  return response;
}

sendButton.addEventListener('click', async () => {
  const message = messageInput.value.trim();
  if (message === '') {
    return;
  }
  addMessage('right', message);

  let resp = await processUserMessage(message);
  addMessage('left', resp);

  messageInput.value = '';
});
