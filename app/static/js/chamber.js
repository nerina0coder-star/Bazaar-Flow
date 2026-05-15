const messagesContainer = document.getElementById('messages');
messagesContainer.scrollTop = messagesContainer.scrollHeight;


const socketio = io();
const submittable = document.getElementById('submittable');
const submitting = document.getElementById('submitting');

const messages = document.getElementById('messages');

socketio.on("message_from_server", (e) => {

    const dt_message = e.message;
    const dt_author = e.author;
    const dt_timehourminute = e.timehourminute;
    const dt_timemonthday = e.timemonthday;

    const message = document.createElement('div');
    const messageHeader = document.createElement('div');
    const messageText = document.createElement('div');

    const author = document.createElement('span');
    const timestamp = document.createElement('span');
    const timehourminute = document.createElement('span');
    const timemonthday = document.createElement('span');

    message.className = 'message';
    messageHeader.className = 'message-header';
    messageText.className = 'message-text';

    author.className = 'author';
    timestamp.className = 'timestamp';

    author.innerText = dt_author;
    messageText.innerText = dt_message;

    timehourminute.innerText = dt_timehourminute;
    timemonthday.innerText = dt_timemonthday;

    timestamp.appendChild(timemonthday);
    timestamp.appendChild(timehourminute);

    messageHeader.appendChild(author);
    messageHeader.appendChild(timestamp);

    message.appendChild(messageHeader);
    message.appendChild(messageText);

    messages.appendChild(message);

    messages.scrollTop = messages.scrollHeight;
});

submittable.addEventListener('submit', (e) => {
    e.preventDefault();
    if (submitting.value.trim() !== '') {
        socketio.emit('message_from_client', {
            message: submitting.value
        });
        submitting.value = "";
    };
});