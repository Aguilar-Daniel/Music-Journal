# 🎵 Music Journal

A personal music journal that connects to your Last.fm account, fetches your 10 most recently played songs, and lets you save notes and ratings for each one.

---

## Features

- Fetches your 10 most recently played tracks from Last.fm
- Add and edit notes for any song
- Rate songs on a scale of 1–10
- Notes and ratings are saved locally and persist between sessions
- Previously noted songs are preserved even after they leave your recent 10
- Clean dark-themed GUI built with Tkinter

---

## Requirements

- Python 3.x
- A [Last.fm](https://www.last.fm) account with scrobbling enabled
- A Last.fm API key (free at [last.fm/api](https://www.last.fm/api))

### Python Libraries

Install the required libraries with:

```bash
pip install requests tkmacosx
```

---

## Setup

1. **Clone the repository**
```bash
git clone https://github.com/Aguilar-Daniel/Music-Journal.git
cd Music-Journal
```

2. **Create a `config.json` file** in the project folder with your Last.fm API key:
```json
{
    "API_KEY": "your_api_key_here"
}
```

3. **Run the program**
```bash
python Main.py
```

---

## How to Use

1. Enter your Last.fm username and click **Submit**
2. Your 10 most recently played songs will appear — click one to select it
3. From the main menu you can:
   - **Edit Note** — add or rewrite notes for the song
   - **Rate Song** — give the song a rating from 1–10
   - **Select Another Song** — go back to the song list
4. Notes and ratings are saved automatically

---

## File Structure

```
Music-Journal/
├── Main.py                  # Main application
├── config.json              # Your API key (not tracked by Git)
├── Notes_and_Ratings.json   # Your saved journal data (not tracked by Git)
├── Songs.json               # Raw Last.fm track data (not tracked by Git)
└── README.md
```

---

## Notes

- `config.json` and `Notes_and_Ratings.json` are listed in `.gitignore` and will not be pushed to GitHub — your data stays on your machine
- Journal entries are preserved across sessions — even if a song leaves your recent 10, its notes and rating are saved and will reappear if you listen to it again

---

## Built With

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) — GUI framework
- [tkmacosx](https://github.com/Saadmairaj/tkmacosx) — Mac-compatible Tkinter widgets
- [Last.fm API](https://www.last.fm/api) — music data
- [requests](https://pypi.org/project/requests/) — HTTP requests
