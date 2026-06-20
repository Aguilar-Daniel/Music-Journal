import requests
import json


def save_journal(journal_data):
    with open("Notes_and_Ratings.json", "w") as file:
        json.dump(journal_data, file, indent=4)


with open("config.json", "r") as a:
    key = json.load(a)


API_KEY = key["API_KEY"]
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

def confirm_song():
    confirm = "no"
    select = None
    while confirm == "no":
        for x, track in enumerate(tracks, start=1):
            print(str(x) + "."  + track["name"] + " - " + track["artist"]["#text"])

        select = int(input("Pick a song to rate or add notes to: "))
        while select < 1 or select > len(tracks):
            select = int(input("Pick pick a valid song"))

        print("You chose: " + tracks[select - 1]["name"])
        confirm = input("Confirm? (Yes/No): ").lower()

    return select


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

old_journal = journal
journal = {}

for track in tracks:
    song = track["name"]

    journal[song] = old_journal.get(song, {
        "Notes": "No notes",
        "Rating": "No rating"
    })

for song in old_journal:
    if song not in journal:
        journal[song] = old_journal[song]

with open("Songs.json", "w") as f:
    json.dump(data, f, indent=4)

save_journal(journal_data=journal)

run = True
while run:

    i = confirm_song()

    song = tracks[i - 1]["name"]
    menu = int(input("MAIN MENU\n1.Edit note(s)\n2.Rate\n3.Pick another song\n4.Quit\n"))

    while menu not in [1, 2, 3, 4]:
        menu = int(input("Pick a valid option!\n 1.Edit note(s)\n 2.Rate\n"))

    while menu != 3 and menu != 4:

        if menu == 1:
            print("Current note(s): " + journal[song]["Notes"])
            note_Edit = int(input("1.Add to note\n2.Rewrite note\n3.Back\n"))

            while note_Edit not in [1, 2, 3]:
                print("Please select a valid option")
                note_Edit = int(input("1.Add to note\n2.Rewrite note\n3.Back\n"))
            if note_Edit == 1:
                new_Note = input("Add to note: ")
                journal[song]["Notes"] += " " + new_Note

                save_journal(journal_data=journal)

            elif note_Edit == 2:
                erase_confirm = input("This will erase your current note(s)\nConfirm? (yes/no)").lower()

                while erase_confirm != "yes" and erase_confirm != "no":
                    erase_confirm = input("Confirm? (yes/no)")

                if erase_confirm == "yes":
                    new_Note = input("New note: ")
                    journal[song]["Notes"] = new_Note

                    save_journal(journal_data=journal)

            else:
                menu = int(input("MAIN MENU\n1.Edit note(s)\n2.Rate\n3.Pick another song\n4.Quit\n"))

                while menu not in [1, 2, 3, 4]:
                    menu = int(input("Pick a valid option!\n 1.Edit note(s)\n 2.Rate\n3.Pick another song\n4.Quit\n"))



        elif menu == 2:
            print("Current rating: " + str(journal[song]["Rating"]))

            rating = input("Rate out of 10: ")
            journal[song]["Rating"] = rating
            save_journal(journal_data=journal)

            menu = int(input("MAIN MENU\n1.Edit note(s)\n2.Rate\n3.Pick another song\n4.Quit\n"))
            while menu not in [1, 2, 3, 4]:
                menu = int(input("Pick a valid option!\n 1.Edit note(s)\n 2.Rate\n3.Pick another song\n4.Quit\n"))

    if menu == 3:
        continue

    else:
        run = False

save_journal(journal_data=journal)

