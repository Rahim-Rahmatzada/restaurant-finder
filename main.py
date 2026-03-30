import requests
from typing import Dict, List, Optional, TypedDict

DEFAULT_POSTCODE: str = "CB74DL"


class Cuisine(TypedDict):
    name: str
    uniqueName: str


class Rating(TypedDict):
    count: int
    starRating: Optional[float]
    userRating: Optional[float]


class Address(TypedDict):
    city: str
    firstLine: str
    postalCode: str


class Restaurant(TypedDict):
    id: str
    name: str
    uniqueName: str
    address: Address
    rating: Rating
    cuisines: List[Cuisine]


class ApiResponse(TypedDict):
    restaurants: List[Restaurant]


def get_postcode() -> str:
    """
    Prompt user for a postcode.

    If no input is provided, default postcode is used.
    The result is normalised by removing spaces and converting to uppercase.
    """
    user_input: str = input(f"Enter postcode (press Enter to use default {DEFAULT_POSTCODE}): ").strip()
    postcode: str = user_input or DEFAULT_POSTCODE
    return postcode.replace(" ", "").upper()


def fetch_data(postcode: str) -> Optional[requests.Response]:
    """
    Fetch restaurant data from the JET API for a given postcode.

    Returns:
        requests.Response | None: HTTP response object if successful, otherwise None.
    """
    url: str = f"https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}"

    headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-GB,en;q=0.9",
        "Referer": "https://www.just-eat.co.uk/",
        "Origin": "https://www.just-eat.co.uk",
        "Connection": "keep-alive"
    }

    try:
        response: requests.Response = requests.get(url, headers=headers, timeout=5)
        return response
    except requests.RequestException:
        return None


def display_restaurants(data: ApiResponse) -> None:
    """
    Display the first 10 restaurants from the API response.

    Extracts and prints:
    - Name
    - Cuisines
    - Rating
    - Address
    """
    restaurants: List[Restaurant] = data.get("restaurants", [])[:10]

    if not restaurants:
        print("No restaurants found for this postcode.")
        return

    print(f"\nShowing {len(restaurants)} restaurants:\n")

    for r in restaurants:
        name: str = r["name"]

        cuisines: str = ", ".join(
            c["name"] for c in r["cuisines"] if c.get("name")
        )

        rating: Optional[float] = r["rating"]["starRating"]

        address: str = ", ".join(filter(None, [
            r["address"]["firstLine"],
            r["address"]["city"],
            r["address"]["postalCode"],
        ]))

        print("Name:", name)
        print("Cuisines:", cuisines)
        print("Rating:", rating if rating is not None else "N/A")
        print("Address:", address)
        print("=" * 80)


def main() -> None:
    """
    Main program flow:
    - Get postcode input
    - Fetch data from API
    - Handle errors
    - Display restaurant data
    """
    postcode: str = get_postcode()
    print("Using postcode:", postcode)

    response: Optional[requests.Response] = fetch_data(postcode)

    if not response:
        print("Request failed")
        return

    print("Status code:", response.status_code)

    if response.status_code != 200:
        print("Something went wrong")
        print(response.text[:200])
        return

    try:
        data: ApiResponse = response.json()
    except ValueError:
        print("Invalid response received")
        return

    display_restaurants(data)


if __name__ == "__main__":
    main()