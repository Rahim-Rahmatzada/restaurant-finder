## Getting Started

### 1. Clone repository
```bash
git clone https://github.com/<your-username>/restaurant-finder.git
cd restaurant-finder
```

## Setup

### Create virtual environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

## Run application
```bash
python main.py
```

You will be prompted:
```
Enter postcode (press Enter to use default CB74DL):
```

## Example
```
Enter postcode (press Enter to use default CB74DL):
Using postcode: CB74DL

Showing 10 restaurants:

Name: Example Restaurant
Cuisines: Pizza, Italian
Rating: 4.5
Address: 123 High Street, London, CB74DL
================================================================================
```

## Assumptions

- Just Eat API endpoint is publicly accessible and does not require authentication
- The API response structure remains consistent
- Address fields (`firstLine`, `city`, `postalCode`) are sufficient for display

## Notes

- The API is protected by Cloudflare, so request headers are required to simulate a browser request
- Postcode validation is not enforced locally due to the complexity of UK postcode formats

## Improvements

If given more time, the following improvements could be made:

- Add postcode validation using a dedicated API instead of messy regex
- Add sorting (e.g. by rating)
- Add filtering (e.g. by cuisine)
- Implement a web interface (e.g. using Flask or React)
- Add unit tests for core logic
- Add logging instead of print statements
- Implement retry logic for failed API requests

## Tech Stack

- Python 3
- `requests` library

## Project Structure
```
justeat-restaurant-finder/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Assessment Criteria Coverage

- ✔ Displays required restaurant data (name, cuisines, rating, address)
- ✔ Limits results to first 10 restaurants
- ✔ Clear instructions to build and run
- ✔ Assumptions documented
- ✔ Improvements outlined
