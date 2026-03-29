import requests

postcode = input("Enter postcode: ")

if postcode == "":
    postcode = "CB74DL"

postcode = postcode.replace(" ", "").upper()

print("Using postcode:", postcode)

url = "https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/" + postcode

print("Calling API ")
print(url)

# headers since cloudflare blocking us :( #imnotabot
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-GB,en;q=0.9",
    "Referer": "https://www.just-eat.co.uk/",
    "Origin": "https://www.just-eat.co.uk",
    "Connection": "keep-alive"
}

response = requests.get(url, headers=headers)
print("status code: ", response.status_code)

if response.status_code != 200:
    print("something went wrong")
    print(response.text[:200])
else:
    data = response.json()

    restaurants = data["restaurants"]

    print("number of restaurants returned:", len(restaurants))

    for r in restaurants[:10]:
        name = r["name"]

        cuisines = []
        for c in r["cuisines"]:
            cuisines.append(c["name"])

        cuisines_str = ", ".join(cuisines)

        rating = r["rating"]["starRating"]

        addr = r["address"]
        address = addr["firstLine"] + ", " + addr["city"] + ", " + addr["postalCode"]

        
        print("Name:", name)
        print("Cuisines:", cuisines_str)
        print("Rating:", rating)
        print("Address:", address)