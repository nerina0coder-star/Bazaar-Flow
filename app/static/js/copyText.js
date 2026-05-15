async function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
    } else {
        copyFallback(text);
    }
}

copybtn = document.getElementById('copy');

copybtn.addEventListener('click', () => {
    socketio.emit('get_entrance_code')
});

socketio.on('entrance_code', (e) => {
    copyText(e.code)
});