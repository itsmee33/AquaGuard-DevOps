
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AquaGuard - Water Monitoring</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef5f9;
            padding: 30px;
        }
        .card {
            max-width: 600px;
            margin: auto;
            padding: 25px;
            background: white;
            border-radius: 15px;
        }
        .level {
            font-size: 45px;
            color: #087eaa;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>AquaGuard Water Monitoring</h1>
        <h2>Tank Water Level</h2>
        <div class="level"><span id="level">{{ level }}</span>%</div>
        <input id="slider" type="range" min="0" max="100"
               value="{{ level }}">
        <button onclick="updateLevel()">Update Level</button>
        <h3 id="status">{{ status }}</h3>
        <p id="advice">{{ advice }}</p>
        <hr>
        <p>Application: Running</p>
        <a href="/health">Check Application Health</a>
    </div>

    <script>
    async function updateLevel() {
        const level = Number(document.getElementById("slider").value);
        const response = await fetch("/api/level", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({level: level})
        });
        const data = await response.json();

        if (!response.ok) {
            alert(data.error);
            return;
        }

        document.getElementById("level").textContent = data.level;
        document.getElementById("status").textContent = data.status;
        document.getElementById("advice").textContent = data.advice;
    }
    </script>
</body>
</html>
"""

def classify_level(level):
    if level < 0 or level > 100:
        raise ValueError("Level must be between 0 and 100")

    if level < 20:
        return "LOW WATER ALERT", "Please schedule a refill."

    if level >= 90:
        return "OVERFLOW RISK", "Check the inlet and stop filling."

    return "NORMAL", "Water level is within the normal range."


@app.get("/")
def home():
    level = 65
    status, advice = classify_level(level)
    return render_template_string(
        HTML, level=level, status=status, advice=advice
    )


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "AquaGuard"
    })


@app.post("/api/level")
def update_level():
    data = request.get_json(silent=True) or {}

    try:
        level = int(data["level"])
        status, advice = classify_level(level)
    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Provide an integer level from 0 to 100"
        }), 400

    return jsonify({
        "level": level,
        "status": status,
        "advice": advice
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
