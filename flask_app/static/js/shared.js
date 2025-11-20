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
Function to add/remove a location to favorites via a POST request.
Parameters:
- url: The endpoint URL to send the POST request to.
- lat: Latitude of the location.
- lon: Longitude of the location.
- city_name: Name of the city.
- state: State of the location.
- country: Country of the location.
*/
async function updateFavorites(url, lat, lon, name, state, country) {
    try {
        // Send update
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                lat: lat,
                lon: lon,
                name: name,
                state: state,
                country: country
            })
        });

        const data = await response.json();
        const favButton = document.getElementById("favorite-button");
        const favLocationsDiv = document.getElementById("favorite-locations");

        if (favButton) {

            favButton.src = 
                data.action === "removed"
                ? "./static/resources/icon_star_round_outline.png"
                : "./static/resources/icon_star_round.png";

            return;   
        } else if (favLocationsDiv) {
            const res = await fetch("/renderFavorites");
            const htmlData = await res.json();
            favLocationsDiv.innerHTML = htmlData.html;
        }
    } catch (err) {
        console.error("Error:", err);
    }
}
