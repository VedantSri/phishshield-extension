console.log("PhishShield loaded on page");

function showModernWarning() {

    const overlay = document.createElement("div");
    overlay.id = "phishshield-overlay";

    overlay.innerHTML = `
    <div class="phishshield-box">

        <div class="phishshield-header">
            <div class="title">🛡️ PhishShield</div>
            <div class="badge">HIGH RISK</div>
        </div>

        <div class="phishshield-body">
            <p class="main-text">
                This page looks like a <b>phishing website</b>.
            </p>

            <p class="sub-text">
                Do NOT enter passwords, OTP, or banking details.
            </p>
        </div>

        <button id="phishshield-close">✔ I Understand</button>

    </div>
    `;

    document.body.appendChild(overlay);

    document.getElementById("phishshield-close").onclick = () => {
        overlay.remove();
    };
}


// 🔍 Detection Logic
function detectPhishing() {
    let url = window.location.href.toLowerCase();

    const suspicious = [
        "login", "verify", "bank", "update",
        "secure", "free", "gift", "@", "confirm"
    ];

    let score = 0;

    suspicious.forEach(word => {
        if (url.includes(word)) score++;
    });

    if (score >= 1) {
        showModernWarning();
    }
}

detectPhishing();


// 🎨 STYLE INJECTION
const style = document.createElement("style");
style.innerHTML = `

#phishshield-overlay {
    position: fixed;
    top: 25px;
    right: 25px;
    z-index: 999999;
    isolation: isolate;
    mix-blend-mode: normal;
    opacity: 1 !important;

    animation: slideIn 0.5s ease;
}


/* MAIN BOX */
.phishshield-box {
    width: 360px;
    border-radius: 16px;
    font-family: 'Segoe UI', sans-serif;

    background: linear-gradient(145deg, #020617, #0f172a);

    border: 1px solid #1e293b;

    box-shadow: 0 0 30px rgba(239,68,68,0.8),
                0 0 80px rgba(0,0,0,0.9);
}


/* HEADER */
.phishshield-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    padding: 14px 16px;

    background: linear-gradient(90deg, #ef4444, #dc2626);
    border-radius: 16px 16px 0 0;
}

.title {
    font-size: 16px;
    font-weight: bold;
    color: white;
}

.badge {
    background: white;
    color: #dc2626;
    font-size: 11px;
    font-weight: bold;
    padding: 4px 8px;
    border-radius: 999px;
}

/* BODY */
.phishshield-body {
    padding: 16px;
}

.main-text {
    font-size: 15px;
    color: #f1f5f9;
    margin-bottom: 6px;
}

.sub-text {
    font-size: 13px;
    color: #cbd5e1;
}

/* BUTTON */
#phishshield-close {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 0 0 16px 16px;
    font-weight: bold;
    cursor: pointer;

    background: linear-gradient(90deg, #22c55e, #16a34a);
    color: black;
    transition: 0.3s;
}

#phishshield-close:hover {
    opacity: 0.95;
    transform: scale(1.02);
}

/* ANIMATION */
@keyframes slideIn {
    from {
        transform: translateX(120%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

`;

document.head.appendChild(style);
