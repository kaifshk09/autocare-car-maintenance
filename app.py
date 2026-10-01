import os

from flask import Flask, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "autocare-dev-secret-key")


def safe_int(value, default=0):
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return max(0, int(value))

    text = str(value).strip()
    if not text:
        return default

    try:
        return max(0, int(float(text)))
    except (TypeError, ValueError):
        return default


def default_payload():
    return {
        "age": 5,
        "mileage": 50000,
        "service": 7000,
        "usage": "Normal",
        "warning": "No",
        "condition": "Good",
        "fuel": "Petrol",
    }


def parse_form_data(form_data):
    return {
        "age": safe_int(form_data.get("age", 0)),
        "mileage": safe_int(form_data.get("mileage", 0)),
        "service": safe_int(form_data.get("service", 0)),
        "usage": form_data.get("usage", "Normal"),
        "warning": form_data.get("warning", "No"),
        "condition": form_data.get("condition", "Good"),
        "fuel": form_data.get("fuel", "Petrol"),
    }


def calculate_prediction(data):
    age = safe_int(data.get("age", 0))
    mileage = safe_int(data.get("mileage", 0))
    service = safe_int(data.get("service", 0))
    usage = data.get("usage", "Normal")
    warning = data.get("warning", "No")
    condition = data.get("condition", "Good")

    # Simple, transparent weighted scoring model for an academic project.
    score = 0
    score += min(25, age * 3)
    score += min(30, mileage / 5000)
    score += min(20, service / 500)
    score += 10 if usage == "Heavy" else (5 if usage == "Moderate" else 0)
    score += 15 if warning == "Yes" else 0
    score += 12 if condition == "Poor" else (6 if condition == "Average" else 0)
    score = int(round(min(100, score)))

    if score >= 70:
        level = "High Risk"
        tone = "high"
        window = "Within 7 days"
        action = "Immediate maintenance inspection is recommended."
        advice = [
            "Check engine and warning indicators",
            "Inspect brakes, tyres and fluids",
            "Review overdue service items",
        ]
    elif score >= 40:
        level = "Medium Risk"
        tone = "medium"
        window = "Within 30 days"
        action = "Schedule a preventive maintenance inspection soon."
        advice = [
            "Check service schedule",
            "Inspect fluids and filters",
            "Monitor warning indicators",
        ]
    else:
        level = "Low Risk"
        tone = "low"
        window = "Within 90 days"
        action = "Continue scheduled preventive maintenance."
        advice = [
            "Follow manufacturer service intervals",
            "Monitor tyre pressure and fluids",
            "Keep service records updated",
        ]

    return {
        "score": score,
        "level": level,
        "tone": tone,
        "window": window,
        "action": action,
        "advice": advice,
    }


@app.route("/", methods=["GET", "POST"])
def home():
    payload = default_payload()
    result = None

    if request.method == "POST":
        payload = parse_form_data(request.form)
        result = calculate_prediction(payload)

    return render_template("index.html", result=result, data=payload)


@app.get("/health")
def health():
    return {"status": "ok", "service": "AutoCare", "version": "1.0.0"}, 200


if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
    )
