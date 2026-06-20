setInterval(() => {
    var success = 1;
    console.log("Ping...")
    fetch('/ping',
        {
        'headers' : { "X-Fetch-Request" : "t", "X-CSRFToken" : csrfToken }
        }
        ).catch((err) => {
            console.log('Ping failed: ' + err);
            success = 1;
        });
        if (success == 1) { console.log("Pong..."); }
    }, 15000);