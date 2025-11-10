from flask import Flask, render_template, request
from main import fetch_properties, fetch_market_insights, PropertyType

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/", methods=["GET", "POST"])
def index():
    # Get suburb from form or query params, with fallback
    suburb = (request.form.get("suburb") or request.args.get("suburb") or "").strip()
    if not suburb:
        suburb = "Belmont North"

    # Get and validate property_type
    property_type = (
        request.form.get("property_type") or request.args.get("property_type") or "all"
    )
    if property_type not in ("all", "unit", "house"):
        property_type = "all"

    data = None
    market_data = None
    error = None

    try:
        data = fetch_properties(suburb, property_type)
        market_data = fetch_market_insights(suburb, property_type)
    except Exception as exc:
        error = str(exc)
        data = None
        market_data = None

    return render_template(
        "index.html",
        suburb=suburb,
        property_type=property_type,
        data=data,
        market_data=market_data,
        error=error,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
