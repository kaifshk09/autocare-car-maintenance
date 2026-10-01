import os


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
