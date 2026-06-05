import requests

url = "https://en.wikipedia.org/w/api.php"
headers = {"User-Agent": "TravelPlannerApp/1.0 (contact@example.com)"}
params = {
    "action": "query",
    "list": "search",
    "srsearch": "tourist attractions Dubai",
    "format": "json",
    "srlimit": 5
}
response = requests.get(url, params=params, headers=headers)
print("Status:", response.status_code)
print("Response:", response.text[:400])