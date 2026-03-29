import requests

DEFAULT_POSTCODE = "CB74DL"


def get_postcode():
    user_input = input(f"Enter postcode (press Enter to use default {DEFAULT_POSTCODE}): ").strip()
    postcode = user_input or DEFAULT_POSTCODE
    return postcode.replace(" ", "").upper()


def fetch_data(postcode):
    url = f"https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}"

    # headers since cloudflare blocking us :( #imnotabot
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