import os
import subprocess
import requests
import tkinter as tk
from datetime import datetime, timedelta
from git import Repo
from bs4 import BeautifulSoup

# KONFIGURACJA
REPO_PATH = os.getcwd()
BRANCH_NAME = "main"
GITHUB_COLORS = ["#161B22", "#0E4429", "#006D32", "#26A641", "#39D353"]
COMMIT_LEVELS = [1, 3, 6, 10]
SQUARE_SIZE = 15

# FUNKCJE

def fetch_github_contributions(username, year):
    url = f"https://github.com/users/{username}/contributions?from={year}-01-01&to={year}-12-31"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    days = soup.find_all('rect', {'class': 'ContributionCalendar-day'})
    contributions = {}
    for day in days:
        date = day['data-date']
        level = int(day['data-level'])
        contributions[date] = level
    return contributions

def commit_on_dates(dates):
    repo = Repo(REPO_PATH)
    os.chdir(REPO_PATH)

    for date, level in dates:
        num_commits = COMMIT_LEVELS[level - 1]
        for _ in range(num_commits):
            file_path = os.path.join(REPO_PATH, "file.txt")
            with open(file_path, "a") as f:
                f.write(f"Commit dla {date} (level {level})\n")

            subprocess.run(["git", "add", "file.txt"])

            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = f"{date}T12:00:00"
            env["GIT_COMMITTER_DATE"] = f"{date}T12:00:00"

            subprocess.run(["git", "commit", "-m", f"Commit dla {date} (level {level})"], env=env)

    subprocess.run(["git", "push", "origin", BRANCH_NAME])

# GUI

def draw(year, username):
    root = tk.Tk()
    root.title(f"GitHub Pixel Art ({year})")
    canvas = tk.Canvas(root, bg="#0D1117")
    canvas.pack(fill=tk.BOTH, expand=True)

    first_day = datetime(year, 1, 1)
    start_day = first_day - timedelta(days=first_day.weekday()+1)

    contributions = fetch_github_contributions(username, year)

    grid = {}

    months_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    days_labels = ["Mon", "Wed", "Fri"]

    # Miesiące
    for i, month in enumerate(months_labels):
        canvas.create_text(50 + (i * 4.4 * SQUARE_SIZE), 10, text=month, fill="#FFFFFF", font=("Arial", 10))

    # Dni tygodnia
    for i, day in enumerate(days_labels):
        canvas.create_text(20, 50 + (i * 2 * SQUARE_SIZE), text=day, fill="#FFFFFF", font=("Arial", 10))

    # Siatka
    for week in range(53):
        for weekday in range(7):
            date = start_day + timedelta(weeks=week, days=weekday)
            if date.year == year:
                date_str = date.strftime("%Y-%m-%d")
                x = 40 + week * (SQUARE_SIZE + 2)
                y = 30 + weekday * (SQUARE_SIZE + 2)
                level = contributions.get(date_str, 0)
                rect = canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE,
                                               fill=GITHUB_COLORS[level], outline="#30363D")
                grid[rect] = [date_str, level]

    selected_level = [1]

    def click(event):
        item = canvas.find_closest(event.x, event.y)[0]
        if item in grid:
            grid[item][1] = selected_level[0]
            canvas.itemconfig(item, fill=GITHUB_COLORS[selected_level[0]])

    def select_level(level):
        selected_level[0] = level

    palette_frame = tk.Frame(root, bg="#0D1117")
    palette_frame.pack(pady=5)

    for idx, color in enumerate(GITHUB_COLORS[1:], start=1):
        btn = tk.Button(palette_frame, bg=color, width=3, command=lambda lvl=idx: select_level(lvl))
        btn.pack(side=tk.LEFT, padx=2)

    canvas.bind("<B1-Motion>", click)
    canvas.bind("<Button-1>", click)

    def save():
        dates = [(d, lvl) for d, lvl in grid.values() if lvl > 0]
        root.destroy()
        commit_on_dates(dates)

    tk.Button(root, text="Commituj na GitHub", command=save, bg="#238636", fg="white").pack(pady=10)

    root.mainloop()

# WYBÓR ROKU i UŻYTKOWNIKA
if __name__ == "__main__":
    root_select = tk.Tk()
    root_select.title("Wybierz rok i użytkownika")

    tk.Label(root_select, text="Wpisz rok:").pack(pady=5)
    entry_year = tk.Entry(root_select)
    entry_year.insert(0, datetime.now().year)
    entry_year.pack(pady=5)

    tk.Label(root_select, text="Nazwa użytkownika GitHub:").pack(pady=5)
    entry_user = tk.Entry(root_select)
    entry_user.pack(pady=5)

    def start():
        year = int(entry_year.get())
        username = entry_user.get()
        root_select.destroy()
        draw(year, username)

    tk.Button(root_select, text="Rozpocznij", command=start).pack(pady=10)

    root_select.mainloop()
