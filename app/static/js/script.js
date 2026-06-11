const csrfToken = document.querySelector('meta[name="csrf"]').getAttribute('content');

setInterval(() => {
        console.log("Sending ping...")
	fetch('/ping',
        {
         'headers' : { "X-Fetch-Request" : "t", "X-CSRFToken" : csrfToken }
        }
        ).catch(err => console.log('ping failed: ' + err)); }, 15000);

document.getElementById('current-year').innerText = new Date().getFullYear();
