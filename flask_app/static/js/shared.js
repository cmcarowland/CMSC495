function parseFlashedMessages(flashedMessages, dialog) {
    if (flashedMessages.length > 0) {
        for (const [category, message] of flashedMessages) {
            if (category === 'error') {
                document.getElementById("dialogMessage").innerText = message;
                dialog.classList.remove('success');
                dialog.classList.add('error');
                dialog.showModal();
            }
            else if (category === 'success') {
                document.getElementById("dialogMessage").innerText = message;
                dialog.classList.remove('error');
                dialog.classList.add('success');
                dialog.showModal();
            }
        }
    }
}

function addToFavorites(url, lat, lon, city_name, country) {
    fetch(url, {
        method: "POST",
        headers: {
        "Content-Type": "application/json"
        },
        body: JSON.stringify(
        { 
            lat: lat, 
            lon: lon, 
            name: city_name, 
            country: country 
        })
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    });
}
