setInterval(() => {
	fetch('/ping').catch(err => console.log('ping failed: ' + err));
}, 30000);

document.getElementById('current-year').innerText = new Date().getFullYear();