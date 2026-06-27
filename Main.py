import requests
import json
from tkinter import *
from tkmacosx import Button

with open("config.json", "r") as a:
    key = json.load(a)

API_KEY = key["API_KEY"]
BASE_URL = "http://ws.audioscrobbler.com/2.0/"
tracks = []
username = ""

try:
    with open("Notes_and_Ratings.json", "r") as f:
        journal = json.load(f)
except FileNotFoundError:
    journal = {}


def submit():
    global username, journal, tracks

    username = username_request.get()

    params = {
        "method": "user.getRecentTracks",
        "api_key": API_KEY,
        "user": username,
        "limit": 10,
        "format": "json"
    }
    values = requests.get(BASE_URL, params=params)
    data = values.json()

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

    with open("Songs.json", "w") as g:
        json.dump(data, g, indent=4)

    save_journal(journal_data=journal)
    username_label.pack_forget()
    username_request.pack_forget()
    submit_button.pack_forget()


def save_journal(journal_data):
    with open("Notes_and_Ratings.json", "w") as file:
        json.dump(journal_data, file, indent=4)

def valid_input(prompt, valid_options):
    while True:
        try:
            choice = int(input(prompt))
            if choice in valid_options:
                return choice
            else:
                print("Pick a valid option.")
        except ValueError:
            print("Pick a valid option.")








main_window = Tk()
main_window.config(bg="#1e1e1e")
username_label = Label(main_window, text="last.fm username", font=("Monaco", 15), bg="#1e1e1e", fg="white")
username_request = Entry(main_window, bg="#2e2e2e", fg="white", insertbackground="white")
submit_button = Button(main_window, text="Submit", command=submit, bg="#cc0000", fg="white")
username_label.pack(anchor="w", padx=10, pady=5)
username_request.pack(anchor="w", padx=10)
submit_button.pack(pady=10)


main_window.mainloop()


run = True

while run:

    i = confirm_song()

    song = tracks[i - 1]["name"]
    menu = valid_input("MAIN MENU\n1.Edit note(s)\n2.Rate\n3.Pick another song\n4.Quit\n", [1, 2, 3, 4])


    while menu != 3 and menu != 4:

        if menu == 1:
            print("Current note(s): " + journal[song]["Notes"])
            note_Edit = valid_input("1.Add to note\n2.Rewrite note\n3.Back\n", [1, 2, 3])

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
                menu = valid_input("MAIN MENU\n1.Edit note(s)\n2.Rate\n3.Pick another song\n4.Quit\n", [1, 2, 3, 4])




        elif menu == 2:
            print("Current rating: " + str(journal[song]["Rating"]))

            rating = valid_input("Rate out of 10: ", list(range(1, 11)))
            journal[song]["Rating"] = rating
            save_journal(journal_data=journal)

            menu = valid_input("MAIN MENU\n1.Edit note(s)\n2.Rate\n3.Pick another song\n4.Quit\n", [1, 2, 3, 4])

    if menu == 3:
        continue

    else:
        run = False

save_journal(journal_data=journal)

