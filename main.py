import requests
from typing import Literal, Optional


PropertyType = Literal["all", "unit", "house"]


def fetch_properties(
    suburb: str = "Belmont North", property_type: PropertyType = "all"
) -> list:
    """Fetch properties for a given suburb from the microburbs API.

    Args:
        suburb: Name of the suburb to search
        property_type: Filter by 'all', 'unit', or 'house'

    Returns:
        A list of property dictionaries with details.
    """
    # Development mode: Return test data
    test_data = [
        {
            "address": f"{i} Smith Street, {suburb}",
            "price": f"${500000 + (i * 50000):,}",
            "property_type": "house" if i % 2 == 0 else "unit",
            "bedrooms": 3 + (i % 2),
            "bathrooms": 2,
            "parking": 1 + (i % 2),
            "description": f"Beautiful {'house' if i % 2 == 0 else 'unit'} in {suburb}",
        }
        for i in range(1, 6)
    ]

    # Filter by property type if not "all"
    if property_type != "all":
        test_data = [p for p in test_data if p["property_type"] == property_type]

    return test_data


def fetch_market_insights(suburb, property_type=None):
    """Fetch market insights (vacancy rate and median price) for a suburb.

    Args:
        suburb: Name of the suburb
        property_type: Optional filter for property type

    Returns:
        Dictionary with vacancy and price information
    """
    url = "https://www.microburbs.com.au/report_generator/api/suburb/market"
    headers = {"Authorization": "Bearer test", "Content-Type": "application/json"}

    try:
        # Fetch vacancy rate
        vacancy_params = {"suburb": suburb, "metric": "vacancy"}
        if property_type and property_type != "all":
            vacancy_params["property_type"] = property_type

        vacancy_response = requests.get(url, params=vacancy_params, headers=headers)
        vacancy_response.raise_for_status()
        vacancy_data = vacancy_response.json()["results"][0]

        # Fetch median price
        price_params = {"suburb": suburb, "metric": "price"}
        if property_type and property_type != "all":
            price_params["property_type"] = property_type

        price_response = requests.get(url, params=price_params, headers=headers)
        price_response.raise_for_status()
        price_data = price_response.json()["results"][0]

        # Process vacancy data
        latest_vacancy = vacancy_data[-1]
        prev_vacancy = vacancy_data[-2] if len(vacancy_data) > 1 else latest_vacancy

        current_rate = latest_vacancy["value"] * 100
        prev_rate = prev_vacancy["value"] * 100
        vacancy_trend = current_rate - prev_rate

        vacancy_trend_text = "Stable"
        if abs(vacancy_trend) > 0.1:
            vacancy_trend_text = "Increasing" if vacancy_trend > 0 else "Decreasing"
            vacancy_trend_text += " from last month"

        # Process price data
        latest_price = price_data[-1]
        prev_price = price_data[-2] if len(price_data) > 1 else latest_price

        current_price = latest_price["value"]
        prev_price_value = prev_price["value"]
        price_trend = ((current_price - prev_price_value) / prev_price_value) * 100

        price_trend_text = "Stable"
        if abs(price_trend) > 1:  # Only show trend if change is >1%
            price_trend_text = "Increasing" if price_trend > 0 else "Decreasing"
            price_trend_text += " from last month"

        return {
            "vacancy": {
                "rate": current_rate,
                "trend": vacancy_trend,
                "trend_text": vacancy_trend_text,
            },
            "price": {
                "value": current_price,
                "trend": price_trend,
                "trend_text": price_trend_text,
            },
        }

    except Exception as e:
        print(f"Error fetching market insights: {e}")
        return None


def main():
    """Command line interface for testing the API functions."""
    import sys

    suburb = sys.argv[1] if len(sys.argv) > 1 else "Belmont North"
    property_type = sys.argv[2] if len(sys.argv) > 2 else "all"

    if property_type not in ("all", "unit", "house"):
        print(f"Invalid property type: {property_type}")
        print("Valid options are: all, unit, house")
        sys.exit(1)

    print(f"Fetching data for {suburb} ({property_type})")
    properties = fetch_properties(suburb, property_type)
    insights = fetch_market_insights(suburb, property_type)

    print(
        "\nProperties found:",
        len(properties) if isinstance(properties, list) else "N/A",
    )
    if insights:
        print(f"\nVacancy rate: {insights['vacancy']:.1f}%")
        print(f"Trend: {insights['trend_text']}")


if __name__ == "__main__":
    main()
