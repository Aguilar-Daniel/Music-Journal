import requests
import json

with open("config.json", "r") as f:
    key = json.load(f)


API_KEY = key["API_KEY"]
BASE_URL = "http://ws.audioscrobbler.com/2.0/"
confirm = "No"
i = 1



try:
    with open("Notes_and_Ratings.json", "r") as f:
        journal = json.load(f)
except FileNotFoundError:
    journal = {}


username = input("Please enter your username: ")


params = {
    "method": "user.getRecentTracks",
    "api_key": API_KEY,
    "user": username,
    "limit": 10,
    "format": "json"
}
response = requests.get(BASE_URL, params=params)
data = response.json()

tracks = data["recenttracks"]["track"]

for track in tracks:
    print(str(i) + "."  + track["name"] + " - " + track["artist"]["#text"])

    journal[tracks[i - 1]["name"]] = {
        "Notes": journal.get(tracks[i - 1]["name"], {}).get("Notes", "No notes"),
        "Rating": journal.get(tracks[i - 1]["name"], {}).get("Rating", "No rating")
    }

    i += 1
    with open("Songs.json", "w") as f:
        json.dump(data, f, indent=4)



while confirm == "no" or confirm == "No":
    print("Pick a song to rate or add notes to: ")
    select = int(input())
    i = select
    print("You chose: " + tracks[select - 1]["name"])
    confirm = input("Confirm? (Yes/No): ")


noteorrate = int(input("1.Add note\n2.Rate\n"))


while noteorrate != 1 and noteorrate != 2:
    noteorrate = int(input("Pick a valid option!\n 1.Add note\n 2.Rate\n"))


if noteorrate == 1:
    print("Notes: " + journal[tracks[i - 1]["name"]]["Notes"])
    note = input("Notes: ")
    journal[tracks[i - 1]["name"]]["Notes"] = note

elif noteorrate == 2:
    print("Current rating: " + journal[tracks[i - 1]["name"]]["Rating"])
    rating = input("Rate out of 10: ")
    journal[tracks[i - 1]["name"]]["Rating"] = rating


with open("Notes_and_Ratings.json", "w") as f:
    json.dump(journal, f, indent=4)




