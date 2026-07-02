import requests
import json
from tkinter import *
from tkmacosx import Button
from tkinter import messagebox

with open("config.json", "r") as a:
    key = json.load(a)

API_KEY = key["API_KEY"]
BASE_URL = "http://ws.audioscrobbler.com/2.0/"
tracks = []
username = ""
song_buttons = []
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

    try:
        tracks = data["recenttracks"]["track"]

    except KeyError:
        messagebox.showerror(title="Error", message="Username not found")
        return

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
    username_frame.pack_forget()
    song_selection(False, None)

def save_journal(journal_data):
    with open("Notes_and_Ratings.json", "w") as file:
        json.dump(journal_data, file, indent=4)



def song_selection(active_frame, frame_name):
    global song_options
    if active_frame:
        frame_name.pack_forget()

    song_options = Frame(main_window, bg="#1e1e1e")
    song_select = Label(song_options, text="Pick a song to rate or add notes to", font=("Monaco", 13, "underline"),
                        bg="#1e1e1e", fg="white")
    song_select.pack(pady=10)


    for x, track in enumerate(tracks, start=1):
        song_choice = Button(song_options,text=str(x) + "."  + track["name"] + " - " + track["artist"]["#text"],
                             bg="#2e2e2e", fg="white", highlightbackground="#2e2e2e",
                             command=lambda t=track: main_menu(t["name"]))
        song_choice.pack(pady=3, padx=10, fill="x")
        song_buttons.append(song_choice)
    song_options.pack(pady=10)

def save_note(song):
    journal[song]["Notes"] = notes.get("1.0", END)
    save_journal(journal_data=journal)
    note_frame.pack_forget()
    main_menu(song)


def save_rating(song):
    try:
        value = float(rating.get())
        if value < 1 or value > 10:
            messagebox.showerror(title="Rating Error", message="Rating must be 1-10!")

        else:
            journal[song]["Rating"] = rating.get()
            save_journal(journal_data=journal)
            rate_frame.pack_forget()
            main_menu(song)
    except ValueError:
        messagebox.showerror(title="Rating Error", message="Please enter a number")

def edit_note(song):
    global notes, note_frame
    menu.pack_forget()
    note_frame = Frame(main_window, bg="#1e1e1e")
    note_label = Label(note_frame, text="Current note(s): " + journal[song]["Notes"],
                       bg="#1e1e1e", fg="white", font=("Monaco", 11), wraplength=450)
    notes = Text(note_frame, bg="#2e2e2e", fg="white", insertbackground="white",
                 height=8, width=50)

    button_frame = Frame(note_frame, bg="#1e1e1e")
    submit_note = Button(button_frame, text="Save", bg="#cc0000", fg="white",
                         highlightbackground="#cc0000", command=lambda: save_note(song))
    back_button = Button(button_frame, text="Back", bg="#2e2e2e", fg="white",
                         highlightbackground="#2e2e2e", command=lambda: back_to_menu(song, note_frame))
    submit_note.pack(side="left", padx=5)
    back_button.pack(side="left", padx=5)

    note_label.pack(pady=10, padx=10)
    notes.pack(pady=5, padx=10)
    button_frame.pack(pady=10)
    note_frame.pack()

def rate_song(song):
    global rating, rate_frame
    menu.pack_forget()
    rate_frame = Frame(main_window, bg="#1e1e1e")
    rating_label = Label(rate_frame, text="Current Rating: " + str(journal[song]["Rating"]),
                         bg="#1e1e1e", fg="white", font=("Monaco", 11))
    rating = Entry(rate_frame, bg="#2e2e2e", fg="white", insertbackground="white", width=10)
    button_frame = Frame(rate_frame, bg="#1e1e1e")
    submit_rating = Button(button_frame, text="Save", bg="#cc0000", fg="white",
                           highlightbackground="#cc0000", command=lambda: save_rating(song))
    back_button = Button(button_frame, text="Back", bg="#2e2e2e", fg="white",
                         highlightbackground="#2e2e2e", command=lambda: back_to_menu(song, rate_frame))
    submit_rating.pack(side="left", padx=5)
    back_button.pack(side="left", padx=5)

    rating_label.pack(pady=20)
    rating.pack(pady=5, padx=20, fill="x")
    button_frame.pack(pady=10)
    rate_frame.pack()

def main_menu(song):
    global menu
    song_options.pack_forget()
    menu = Frame(main_window, bg="#1e1e1e")
    current_song = Label(menu, text=song, font=("Monaco", 14), fg="#acb4b5", bg="#1e1e1e")
    edit_button = Button(menu, text="Edit Note", bg="#cc0000", fg="white",
                         highlightbackground="#cc0000", command=lambda: edit_note(song))
    rate_button = Button(menu, text="Rate Song", bg="#cc0000", fg="white",
                         highlightbackground="#cc0000", command=lambda: rate_song(song))
    different_song_button = Button(menu, text="Select Another Song", bg="#2e2e2e", fg="white",
                                   highlightbackground="#2e2e2e", command=lambda: song_selection(True, menu))
    current_song.pack(pady=20)
    edit_button.pack(pady=5, padx=20, fill="x")
    rate_button.pack(pady=5, padx=20, fill="x")
    different_song_button.pack(pady=5, padx=20, fill="x")
    menu.pack()

def back_to_menu(song, frame_name):
    frame_name.pack_forget()
    menu.pack_forget()
    main_menu(song)



main_window = Tk()
main_window.config(bg="#1e1e1e")
main_window.title("Music Journal")
username_frame = Frame(main_window, bg="#1e1e1e")
username_label = Label(username_frame, text="last.fm username", font=("Monaco", 15), bg="#1e1e1e", fg="white")
username_request = Entry(username_frame, bg="#2e2e2e", fg="white", insertbackground="white")
submit_button = Button(username_frame, text="Submit", command=submit, bg="#cc0000", fg="white", pady=10)
username_label.pack(anchor="w", padx=10, pady=5)
username_request.pack(anchor="w", padx=10)
submit_button.pack(pady=10)
username_frame.pack()
main_window.geometry("500x600")
main_window.mainloop()