from flask import Flask, jsonify, render_template, request

from planner import COUNTRY_OPTIONS, INDUSTRY_OPTIONS, LEANNESS_OPTIONS, generate_company_plan

app = Flask(__name__)


@app.get("/")
def index():
    return render_template(
        "index.html",
        industry_options=INDUSTRY_OPTIONS,
        country_options=COUNTRY_OPTIONS,
        leanness_options=LEANNESS_OPTIONS,
    )


@app.post("/api/plan")
def create_plan():
    payload = request.get_json(silent=True) or request.form
    industry = str(payload.get("industry", "")).strip()
    country = str(payload.get("country", "")).strip()
    leanness = str(payload.get("leanness", "balanced")).strip() or "balanced"

    if not industry or not country:
        return jsonify({"error": "Industry and country are required."}), 400

    plan = generate_company_plan(industry=industry, country=country, leanness=leanness)
    return jsonify(plan)


if __name__ == "__main__":
    app.run(debug=True)
