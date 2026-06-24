setInterval(() => {
    fetch('/ping',
        {
        'headers' : { "X-Fetch-Request" : "t", "X-CSRFToken" : csrfToken }
        }
        ).catch((err) => {
            console.log('Ping failed: ' + err);
            success = 1;
        });
    }, 15000);