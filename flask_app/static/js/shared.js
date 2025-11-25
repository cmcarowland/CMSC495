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

/*
Function to fetch and display a quip in a target HTML element.
Parameters:
- targetElementId: The ID of the HTML element to display the quip.
*/
async function getQuip(targetElementId) {
    try {
        const response = await fetch("/getQuip");
        const data = await response.json();
        document.getElementById(targetElementId).innerHTML = data.html;
    } catch (err) {
        console.error("Error fetching quip:", err);
    }
}

/*
Function to load city weather data with a loading animation.
Parameters:
- url: The endpoint URL to fetch weather data from.
- lat: Latitude of the location.
- lon: Longitude of the location.
- city: Name of the city.
- state: State of the location.
- country: Country of the location.
- targetElementId: The ID of the HTML element to display the weather data.
*/
async function loadCityWeatherData(url, lat, lon, city, state, country, targetElementId) {
    await getQuip(targetElementId);
    const weatherUnicode = [
        "\u26C5", "\u2614", "\u26A1", "\u26C4", "\u2746", "\u{1f308}"
    ];

    const startTime = performance.now();
    
    // Start the fetch without awaiting
    const fetchPromise = fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            latitude: lat,
            longitude: lon,
            city: city,
            state: state,
            country: country
        })
    }).then(res => res.json());
    
    let count = 0;
    let htmlData = null;
    const minWaitTime = 500;
    
    while (((performance.now() - startTime) < minWaitTime) || htmlData == null) {
        await new Promise(resolve => setTimeout(resolve, 100));
        const randomIndex = Math.floor(Math.random() * weatherUnicode.length);
        document.getElementById('ticker').innerText += weatherUnicode[randomIndex];
        count += 1;
        if (count > 10) {
            document.getElementById('ticker').innerText = '';
            count = 0;
        }
        
        // Check if fetch is complete
        htmlData = await Promise.race([
            fetchPromise,
            new Promise(resolve => setTimeout(() => resolve(null), 0))
        ]);
    }
    
    if (htmlData.status === 204) {
        document.getElementById(targetElementId).classList.add('error');
    }

    document.getElementById(targetElementId).innerHTML = htmlData.html;
}