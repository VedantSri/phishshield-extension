const API_KEY = "AIzaSyBC9IB4UMLDW_MrEGdczZrUxGWoh4VCu4Q";

// function to check URL with Google Safe Browsing
async function checkURL(url) {

    const body = {
        client: {
            clientId: "phishshield",
            clientVersion: "1.0"
        },
        threatInfo: {
            threatTypes: ["MALWARE", "SOCIAL_ENGINEERING"],
            platformTypes: ["ANY_PLATFORM"],
            threatEntryTypes: ["URL"],
            threatEntries: [{ url: url }]
        }
    };

    try {
        const response = await fetch(
            `https://safebrowsing.googleapis.com/v4/threatMatches:find?key=${API_KEY}`,
            {
                method: "POST",
                body: JSON.stringify(body)
            }
        );

        const data = await response.json();

        // if matches found = phishing
        if (data && data.matches) {
            return true;
        } else {
            return false;
        }

    } catch (error) {
        console.error("API Error:", error);
        return false;
    }
}

// listen for message from content.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

    if (request.action === "checkURL") {
        checkURL(request.url).then(result => {
            sendResponse({ isPhishing: result });
        });
        return true; // required for async
    }

});
