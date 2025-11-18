/*
Golden Hour App Group 1
UMGC CMSC 495 7385
Shivam Patel, Raymond Rowland, Mariam Ahmed, Katrina Wilhelm, Paul Cooper
November 18, 2025

shared.js

The JavaScript file for the Golden Hour Flask application.
Defines functions for handling flashed messages and adding favorites.
Prevents DRY violations by centralizing shared functionality.
*/

/*
Function to parse flashed messages and display them in a dialog.
Parameters:
- flashedMessages: An array of flashed messages with their categories.
- dialog: The dialog element to display messages.
*/
function parseFlashedMessages(flashedMessages, dialog) {
    console.log("flashedMessages");
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

/*
Function to add a location to favorites via a POST request.
Parameters:
- url: The endpoint URL to send the POST request to.
- lat: Latitude of the location.
- lon: Longitude of the location.
- city_name: Name of the city.
- state: State of the location.
- country: Country of the location.
*/
function addToFavorites(url, lat, lon, city_name, state, country) {
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
            state: state,
            country: country 
        })
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    });
}
