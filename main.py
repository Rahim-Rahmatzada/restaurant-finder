import requests

DEFAULT_POSTCODE = "CB74DL"


def get_postcode():
    """
    Prompt user for a postcode.

    If no input is provided, default postcode is used.
    The result is normalised by removing spaces and converting to uppercase.
    """
    user_input = input(f"Enter postcode (press Enter to use default {DEFAULT_POSTCODE}): ").strip()
    postcode = user_input or DEFAULT_POSTCODE
    return postcode.replace(" ", "").upper()


def fetch_data(postcode):
    """
    Fetch restaurant data from the JET API for a given postcode.

    Returns:
        requests.Response | None: HTTP response object if successful, otherwise None.
    """
    url = f"https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}"

    # required headers to avoid Cloudflare blocking non-browser requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-GB,en;q=0.9",
        "Referer": "https://www.just-eat.co.uk/",
        "Origin": "https://www.just-eat.co.uk",
        "Connection": "keep-alive"
    }

    try:
        response = requests.get(url, headers=headers)
        return response
    except requests.RequestException:
        return None


def display_restaurants(data):
    """
    Display the first 10 restaurants from the API response.

    Extracts and prints:
    - Name
    - Cuisines
    - Rating
    - Address
    """
    restaurants = data.get("restaurants", [])[:10]

    print(f"\nShowing {len(restaurants)} restaurants:\n")

    for r in restaurants:
        name = r.get("name", "N/A")

        cuisines = ", ".join(
            c.get("name", "") for c in r.get("cuisines", [])
        )

        rating = r.get("rating", {}).get("starRating", "N/A")

        addr = r.get("address", {})
        address = ", ".join(filter(None, [
            addr.get("firstLine"),
            addr.get("city"),
            addr.get("postalCode"),
        ]))

        print("Name:", name)
        print("Cuisines:", cuisines)
        print("Rating:", rating)
        print("Address:", address)
        print("=" * 80)


def main():
    """
    Main program flow:
    - Get postcode input
    - Fetch data from API
    - Handle errors
    - Display restaurant data
    """
    postcode = get_postcode()
    print("Using postcode:", postcode)

    response = fetch_data(postcode)

    if not response:
        print("Request failed")
        return

    print("Status code:", response.status_code)

    if response.status_code != 200:
        print("Something went wrong")
        print(response.text[:200])
        return

    try:
        data = response.json()
    except ValueError:
        print("Invalid response received")
        return

    display_restaurants(data)


if __name__ == "__main__":
    main()