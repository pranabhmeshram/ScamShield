async function scanURL() {
    const input = document.getElementById("urlInput");
    const resultBox = document.getElementById("resultBox");

    const url = input.value.trim();

    if (url === "") {
        alert("Please enter a URL first.");
        return;
    }

    resultBox.classList.add("show");
    resultBox.innerHTML = `
        <div class="result-title">
            🔄 Analyzing URL...
        </div>
        <p>Please wait while ScamShield checks the URL.</p>
    `;

    try {
        const response = await fetch("/scan", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: url
            })
        });

        const data = await response.json();

        if (!response.ok) {
            resultBox.innerHTML = `
                <div class="result-title">❌ Error</div>
                <p>${data.error || "Unable to analyze URL."}</p>
            `;
            return;
        }

        // Risk status
        let emoji = "🟢";
        let cssClass = "low-risk";

        if (data.status === "Medium Risk") {
            emoji = "🟡";
            cssClass = "medium-risk";
        }

        if (data.status === "High Risk") {
            emoji = "🔴";
            cssClass = "high-risk";
        }

        // Reasons
        const reasonList = data.reasons
            .map(reason => `<li>${reason}</li>`)
            .join("");

        // Domain information
        const domain = data.domain_info?.domain || "Not available";
        const ip = data.domain_info?.ip_address || "Not available";
        const protocol = data.domain_info?.protocol || "Not available";
        const dnsStatus = data.domain_info?.status || "Not available";

        resultBox.innerHTML = `
            <div class="result-title">
                ${emoji} Scan Result
            </div>

            <div class="risk-score">
                ${data.score}/100
            </div>

            <div class="result-status ${cssClass}">
                ${data.status}
            </div>

            <h3>🔎 Security Analysis</h3>

            <ul>
                ${reasonList}
            </ul>

            <h3 style="margin-top:25px;">
                🌐 Domain Information
            </h3>

            <div style="
                margin-top:15px;
                padding:18px;
                background:#f8fafc;
                border-radius:12px;
                line-height:2;
            ">
                <div>
                    <strong>Domain:</strong>
                    ${domain}
                </div>

                <div>
                    <strong>IP Address:</strong>
                    ${ip}
                </div>

                <div>
                    <strong>Protocol:</strong>
                    ${protocol}
                </div>

                <div>
                    <strong>DNS Status:</strong>
                    ${dnsStatus}
                </div>
            </div>

            <p style="margin-top:20px; color:#64748b;">
                URL:
                <strong>${escapeHTML(data.url)}</strong>
            </p>

            <p style="
                margin-top:15px;
                color:#64748b;
                font-size:14px;
            ">
                🔐 This analysis uses rule-based security indicators
                for educational purposes. A low-risk result does not
                guarantee that a website is safe.
            </p>
        `;

        resultBox.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    } catch (error) {

        resultBox.innerHTML = `
            <div class="result-title">
                ❌ Connection Error
            </div>

            <p>
                Unable to connect to the Flask server.
                Make sure the server is running.
            </p>
        `;
    }
}


// Prevent HTML from being inserted through the displayed URL
function escapeHTML(value) {
    return value
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
