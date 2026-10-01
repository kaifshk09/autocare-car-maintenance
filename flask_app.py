import os

from flask import Flask, render_template, request

from logic import calculate_prediction, default_payload, parse_form_data

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "autocare-dev-secret-key")


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
