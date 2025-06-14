from __future__ import annotations

"""github_pixel_art.py — v0.4.0
================================
• Poprawiono parsowanie nowego layoutu GitHuba (komórki `<td>` z klasą
  `ContributionCalendar-day`).  
• Usunięto nadmiarowy `print`, dodano wyraźne filtrowanie elementów z
  `data-date`.
"""

import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Tuple, List

import requests
import tkinter as tk
import tkinter.messagebox as mb
from bs4 import BeautifulSoup
from git import Repo

# Zgodność: pozwala wciąż pisać tk.messagebox.*
tk.messagebox = mb  # type: ignore[attr-defined]

# --- KONFIGURACJA -----------------------------------------------------------
REPO_PATH = Path.cwd()
BRANCH_NAME = "main"

GITHUB_COLORS = ["#161B22", "#0E4429", "#006D32", "#26A641", "#39D353"]
COMMIT_LEVELS = [1, 3, 6, 10]

SQUARE_SIZE = 15
PADDING_X = 40
PADDING_Y = 30

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "X-Requested-With": "XMLHttpRequest",
}

# ---------------------------------------------------------------------------


def _extract_int(value: str | None, default: int = 0) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


# --- POBIERANIE KONTRYBUCJI -------------------------------------------------

def fetch_github_contributions(username: str, year: int) -> Dict[str, Tuple[int, int]]:
    """Zwraca mapę `YYYY‑MM‑DD -> (level, count)` dla danego roku.

    Obsługuje zarówno stary SVG (`rect[data-date]`), jak i nowy układ tabeli
    (`td.ContributionCalendar-day`). Jeśli `data-count` nie istnieje, liczba
    commitów jest wyciągana z `aria-label` (np. "17 contributions on 2025‑01‑06").
    """

    url = (
        f"https://github.com/users/{username}/contributions"
        f"?from={year}-01-01&to={year}-12-31"
    )
    try:
        html = requests.get(url, headers=HEADERS, timeout=10)
        html.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"HTTP problem while fetching contributions: {e}") from e

    soup = BeautifulSoup(html.text, "html.parser")

    # Jeśli GitHub zwrócił <include-fragment>, pobierz jego zawartość
    frag = soup.find("include-fragment")
    if frag and frag.get("src"):
        try:
            html2 = requests.get("https://github.com" + frag["src"], headers=HEADERS, timeout=10)
            html2.raise_for_status()
            soup = BeautifulSoup(html2.text, "html.parser")
        except requests.RequestException:
            pass  # zostaje pierwotny soup

    # 1. Nowy układ (komórki <td> z klasą ContributionCalendar-day)
    elems = soup.select("[data-date].ContributionCalendar-day")
    # 2. Stary układ (rect w SVG)
    if not elems:
        elems = soup.select("rect[data-date]")

    contributions: Dict[str, Tuple[int, int]] = {}
    for el in elems:
        date = el.get("data-date")
        if not date:
            continue
        level = _extract_int(el.get("data-level") or el.get("data-activity-level"))

        if "data-count" in el.attrs:
            count = _extract_int(el["data-count"], 0)
        else:
            m = re.search(r"(\d+) contributions? on", el.get("aria-label", ""))
            count = int(m.group(1)) if m else 0

        contributions[date] = (level, count)

    return contributions


# --- COMMITOWANIE ----------------------------------------------------------

def commit_on_dates(dates: List[Tuple[str, int]]) -> None:
    repo = Repo(REPO_PATH)
    os.chdir(REPO_PATH)
    file_path = REPO_PATH / "pixel_art.txt"

    for date_str, level in dates:
        n = COMMIT_LEVELS[level - 1]
        for i in range(n):
            with file_path.open("a", encoding="utf-8") as f:
                f.write(f"Pixel-art {date_str} {i+1}/{n} lvl {level}\n")
            subprocess.run(["git", "add", str(file_path)], check=True)
            env = os.environ | {
                "GIT_AUTHOR_DATE": f"{date_str}T12:00:00",
                "GIT_COMMITTER_DATE": f"{date_str}T12:00:00",
            }
            subprocess.run(
                ["git", "commit", "-m", f"Pixel‑art {date_str} ({i+1}/{n})"],
                env=env,
                check=True,
            )
    subprocess.run(["git", "push", "-u", "origin", BRANCH_NAME], check=True)


# --- GUI --------------------------------------------------------------------

def draw(year: int, username: str) -> None:
    root = tk.Tk()
    root.title(f"GitHub Pixel Art – {year}")
    root.configure(bg="#0D1117")

    # Pobranie danych z GitHuba
    try:
        contributions = fetch_github_contributions(username, year)
    except Exception as exc:  # noqa: BLE001
        tk.messagebox.showerror("Błąd pobierania", f"Nie udało się pobrać danych:\n{exc}")
        root.destroy()
        return

    if not contributions:
        tk.messagebox.showinfo("Brak danych", "Użytkownik nie ma kontrybucji w tym roku.")

    # Obliczenia siatki
    first_day = datetime(year, 1, 1)
    start_day = first_day - timedelta(days=first_day.weekday())  # poniedziałek tygodnia‑0

    weeks_in_year = (datetime(year, 12, 31) - start_day).days // 7 + 1
    grid_width = PADDING_X + weeks_in_year * (SQUARE_SIZE + 2)
    grid_height = PADDING_Y + 7 * (SQUARE_SIZE + 2)

    # Strefy dodatkowe (legenda, przyciski)
    AUX_HEIGHT = 140

    root.geometry(f"{grid_width + 40}x{grid_height + AUX_HEIGHT}")
    root.resizable(False, False)

    canvas = tk.Canvas(root, bg="#0D1117", highlightthickness=0)
    canvas.place(x=0, y=0, width=grid_width + 20, height=grid_height + 20)

    grid: Dict[int, list] = {}

    # Etykiety miesięcy
    months_labels = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    ]
    for i, month in enumerate(months_labels):
        canvas.create_text(
            PADDING_X + (i * 4.36 * SQUARE_SIZE),
            10,
            text=month,
            fill="#FFFFFF",
            font=("Arial", 10, "bold"),
        )

    # Etykiety dni tygodnia (co drugi dzień, żeby było przejrzyście)
    for i, day in enumerate(["Mon", "Wed", "Fri"]):
        canvas.create_text(20, PADDING_Y + (i * 2 * (SQUARE_SIZE + 2)), text=day, fill="#FFFFFF", font=("Arial", 10))


    # Rysowanie siatki pikseli
    for week in range(weeks_in_year):
        for weekday in range(7):
            date = start_day + timedelta(weeks=week, days=weekday)
            if date.year == year:
                date_str = date.strftime("%Y-%m-%d")
                x = PADDING_X + week * (SQUARE_SIZE + 2)
                y = PADDING_Y + weekday * (SQUARE_SIZE + 2)
                level, count = contributions.get(date_str, (0, 0))
                rect = canvas.create_rectangle(
                    x,
                    y,
                    x + SQUARE_SIZE,
                    y + SQUARE_SIZE,
                    fill=GITHUB_COLORS[level],
                    outline="#30363D",
                )
                grid[rect] = [date_str, level, count]

    # --- Interakcja ---------------------------------------------------------
    selected_level = tk.IntVar(value=1)  # domyślnie 1 (jasny zielony)

    def on_click(event):
        item = canvas.find_closest(event.x, event.y)[0]
        if item in grid:
            date_str, *_ = grid[item]
            lvl = selected_level.get()
            grid[item][1] = lvl
            canvas.itemconfig(item, fill=GITHUB_COLORS[lvl])

    def on_right_click(event):
        item = canvas.find_closest(event.x, event.y)[0]
        if item in grid:
            grid[item][1] = 0
            canvas.itemconfig(item, fill=GITHUB_COLORS[0])

    def on_move(event):
        item = canvas.find_closest(event.x, event.y)[0]
        if item in grid:
            date_str, lvl, cnt = grid[item]
            status_label.config(text=f"{date_str}: {cnt} commit(s), level {lvl}")
        else:
            status_label.config(text="")

    canvas.bind("<Button-1>", on_click)
    canvas.bind("<B1-Motion>", on_click)
    canvas.bind("<Button-3>", on_right_click)
    canvas.bind("<Motion>", on_move)

    # --- Paleta kolorów -----------------------------------------------------
    palette = tk.Frame(root, bg="#0D1117")
    palette.place(x=PADDING_X, y=grid_height + 30)

    def make_level_btn(lvl: int, text: str | None = None):
        return tk.Button(
            palette,
            text=text,
            bg=GITHUB_COLORS[lvl],
            fg="white",
            width=3,
            relief=tk.RAISED,
            bd=1,
            command=lambda v=lvl: selected_level.set(v),
        )

    make_level_btn(0, "X").pack(side=tk.LEFT, padx=2)
    for lvl in range(1, 5):
        make_level_btn(lvl).pack(side=tk.LEFT, padx=2)

    # --- Legenda ------------------------------------------------------------
    legend = tk.Frame(root, bg="#0D1117")
    legend.place(x=PADDING_X, y=grid_height + 70)

    tk.Label(legend, text="Less", bg="#0D1117", fg="white").pack(side=tk.LEFT, padx=2)
    for color in GITHUB_COLORS:
        tk.Canvas(
            legend,
            width=SQUARE_SIZE,
            height=SQUARE_SIZE,
            bg=color,
            highlightthickness=1,
            highlightbackground="#30363D",
        ).pack(side=tk.LEFT, padx=1)
    tk.Label(legend, text="More", bg="#0D1117", fg="white").pack(side=tk.LEFT, padx=2)

    # --- Status & przycisk commit --------------------------------------------------
    status_label = tk.Label(root, text="", bg="#0D1117", fg="white")
    status_label.place(x=PADDING_X, y=grid_height + 110)

    def on_save():
        """Zbiera wszystkie wybrane kratki i wysyła do repozytorium."""
        dates_to_commit = [(d, lvl) for d, lvl, _ in grid.values() if lvl > 0]
        if not dates_to_commit:
            tk.messagebox.showinfo("Brak danych", "Nie wybrano żadnych " "dat do commitowania.")
            return
        root.destroy()
        commit_on_dates(dates_to_commit)
        print("Zakończono commitowanie! ✨")

    tk.Button(
        root,
        text="Commituj na GitHub",
        command=on_save,
        bg="#238636",
        fg="white",
        padx=10,
        pady=4,
    ).place(x=grid_width - 140, y=grid_height + 100)

    root.mainloop()


# --- Launcher ---------------------------------------------------------------

def main() -> None:  # noqa: D401
    """Uruchamia okienko wyboru roku i użytkownika."""

    sel = tk.Tk()
    sel.title("Wybierz rok i użytkownika")
    sel.configure(bg="#0D1117")
    sel.resizable(False, False)

    tk.Label(sel, text="Rok:", bg="#0D1117", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    year_ent = tk.Entry(sel)
    year_ent.insert(0, datetime.now().year)
    year_ent.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(sel, text="Użytkownik GitHub:", bg="#0D1117", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    user_ent = tk.Entry(sel)
    user_ent.grid(row=1, column=1, padx=5, pady=5)

    def _start():
        try:
            yr = int(year_ent.get())
            usr = user_ent.get().strip()
        except ValueError:
            tk.messagebox.showerror("Błąd", "Rok musi być liczbą całkowitą")
            return
        if not usr:
            tk.messagebox.showerror("Błąd", "Pole użytkownika nie może być puste")
            return
        sel.destroy()
        draw(yr, usr)

    tk.Button(sel, text="Rozpocznij", command=_start, bg="#238636", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

    sel.mainloop()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        draw(int(sys.argv[1]), sys.argv[2])
    else:
        main()
