from flask import Flask, jsonify, render_template, request

from planner import generate_company_plan

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/plan")
def create_plan():
    payload = request.get_json(silent=True) or request.form
    industry = str(payload.get("industry", "")).strip()
    country = str(payload.get("country", "")).strip()

    if not industry or not country:
        return jsonify({"error": "Both industry and country are required."}), 400

    plan = generate_company_plan(industry=industry, country=country)
    return jsonify(plan)


if __name__ == "__main__":
    app.run(debug=True)
