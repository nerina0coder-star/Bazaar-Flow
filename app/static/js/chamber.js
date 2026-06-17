
const messagesContainer = document.getElementById('messages');
messagesContainer.scrollTop = messagesContainer.scrollHeight;
const token = document.querySelector('meta[name=T]').content;
const vertoken = document.querySelector('meta[name=VT]').content;

const socketio = io({
    auth: { token: vertoken }
});
const submittable = document.getElementById('submittable');
const submitting = document.getElementById('submitting');

const messages = document.getElementById('messages');

let isPrepending = false;

let added = 1;

let canPrepend = true;

socketio.on("message_from_server", (e) => {

    const dt_message = e.message;
    const dt_author = e.author;
    const dt_timehourminute = e.timehourminute;
    const dt_timemonthday = e.timemonthday;
    const dt_token = e.token;

    const message = document.createElement('div');
    const messageHeader = document.createElement('div');
    const messageText = document.createElement('div');

    const author = document.createElement('span');
    const timestamp = document.createElement('span');
    const timehourminute = document.createElement('span');
    const timemonthday = document.createElement('span');

    if (dt_token === token) {
        message.className = 'message message-self';
    } else { message.className = 'message'; }

    messageHeader.className = 'message-header';
    messageText.className = 'message-text';

    author.className = 'author';
    timestamp.className = 'timestamp mx-6';

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
    added += 1;
});
socketio.on("server_send_more", (e) => {

    const dt_nomore = e.nomore;
    if (dt_nomore) { canPrepend = false; return; }

    isPrepending = true

    const dt_message = e.message;
    const dt_author = e.author;
    const dt_timehourminute = e.timehourminute;
    const dt_timemonthday = e.timemonthday;
    const dt_token = e.token;
    const dt_islast = e.islast;

    const message = document.createElement('div');
    const messageHeader = document.createElement('div');
    const messageText = document.createElement('div');

    const author = document.createElement('span');
    const timestamp = document.createElement('span');
    const timehourminute = document.createElement('span');
    const timemonthday = document.createElement('span');

    if (dt_token === token) {
        message.className = 'message message-self';
    } else { message.className = 'message'; }

    messageHeader.className = 'message-header';
    messageText.className = 'message-text';

    author.className = 'author';
    timestamp.className = 'timestamp mx-6';

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
    
    const beforePrepend = messages.scrollHeight;
    const topBeforePrepend = messages.scrollTop;

    messages.prepend(message)

    const afterPrepend = messages.scrollHeight;

    dif = afterPrepend - beforePrepend;
    messages.scrollTop = topBeforePrepend + dif;
    
    if (dt_islast) {
        isPrepending = false;
    }
    added += 1;
})

submittable.addEventListener('submit', (e) => {
    e.preventDefault();
    if (submitting.value.trim() !== '') {
        socketio.emit('message_from_client', {
            message: submitting.value
        });
        submitting.value = "";
    };
});
messages.addEventListener('scroll', () => {
    // Check if the user has reached the top (with a small 5px threshold for reliability)
    if (canPrepend && messages.scrollTop <= 5 && !isPrepending) {
                
        isPrepending = true;

        // Store the current scroll height to prevent the view from jumping after prepending
        const previousScrollHeight = messages.scrollHeight;

        // Add the message to the top of the div
        socketio.emit('client_ask_more',
            {
                after: added
            }
        );
    }
});
