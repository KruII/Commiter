import os
import random
import subprocess
import tkinter as tk
from tkcalendar import Calendar
from git import Repo

# Automatycznie wykrywa ścieżkę do repozytorium
CURRENT_PATH = os.getcwd()

# Sprawdza, czy w obecnym katalogu jest repozytorium Git
if not os.path.exists(os.path.join(CURRENT_PATH, ".git")):
    raise Exception(f"🚨 Nie znaleziono repozytorium Git w: {CURRENT_PATH}")

REPO_PATH = CURRENT_PATH
BRANCH_NAME = "main"  # Możesz zmienić, jeśli używasz innej gałęzi
COMMITS_PER_DAY = (1, 3)  # Zakres commitów na dzień

# Inicjalizacja repozytorium
repo = Repo(REPO_PATH)

# Funkcja do commitowania w wybranych dniach
def commit_on_dates(dates):
    os.chdir(REPO_PATH)

    for date in dates:
        num_commits = random.randint(*COMMITS_PER_DAY)
        for i in range(num_commits):
            file_path = os.path.join(REPO_PATH, "file.txt")
            with open(file_path, "a") as f:
                f.write(f"Commit {i+1} z dnia {date}\n")

            subprocess.run(["git", "add", "file.txt"])

            commit_message = f"Commit {i+1} z dnia {date}"

            # Tworzymy zmienne środowiskowe
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = f"{date}T12:00:00"
            env["GIT_COMMITTER_DATE"] = f"{date}T12:00:00"

            # Uruchamiamy commit z poprawnym env
            subprocess.run(["git", "commit", "-m", commit_message], env=env, check=True)
            print(f"✅ Commit {i+1} dodany dla {date}")

    print("\n📤 Wysyłanie commitów na GitHub...")
    subprocess.run(["git", "push", "origin", BRANCH_NAME])
    print("✅ Wysłano na GitHub!")

# GUI do wybierania wielu dni w kalendarzu
def open_calendar():
    def toggle_date():
        date = cal.get_date()
        if date in selected_dates:
            selected_dates.remove(date)
            listbox.delete(selected_dates.index(date))
        else:
            selected_dates.append(date)
            listbox.insert(tk.END, date)

    def confirm_dates():
        if selected_dates:
            root.destroy()
            commit_on_dates(selected_dates)

    root = tk.Tk()
    root.title("Wybierz dni do commitowania")

    label = tk.Label(root, text="Klikaj daty w kalendarzu, aby je wybrać", font=("Arial", 12))
    label.pack(pady=5)

    cal = Calendar(root, selectmode="day", date_pattern="yyyy-MM-dd")
    cal.pack(pady=5)

    selected_dates = []

    button_toggle = tk.Button(root, text="Dodaj/Usuń datę", command=toggle_date)
    button_toggle.pack(pady=5)

    listbox = tk.Listbox(root, height=10)
    listbox.pack(pady=5)

    button_confirm = tk.Button(root, text="Zatwierdź", command=confirm_dates)
    button_confirm.pack(pady=10)

    root.mainloop()

# Uruchomienie kalendarza
open_calendar()
