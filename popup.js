document.getElementById("scanBtn").addEventListener("click", () => {

    const result = document.getElementById("result");

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {

        let url = tabs[0].url.toLowerCase();

        let score = 0;
        const keywords = ["login", "verify", "bank", "free", "gift", "update", "@"];

        keywords.forEach(word => {
            if (url.includes(word)) score++;
        });

        result.classList.remove("safe", "warning", "danger");

        if (score >= 4) {
            result.innerText = "🚨 High Risk Website";
            result.classList.add("danger");
        } else if (score >= 2) {
            result.innerText = "⚠️ Suspicious Website";
            result.classList.add("warning");
        } else {
            result.innerText = "✅ Safe Website";
            result.classList.add("safe");
        }

    });

});
