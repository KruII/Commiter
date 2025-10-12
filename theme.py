"""Theme management for light and dark mode."""
from __future__ import annotations

from typing import Dict


class Theme:
    """Theme configuration for the application."""

    DARK = {
        "bg": "#0D1117",
        "fg": "#FFFFFF",
        "canvas_bg": "#0D1117",
        "card_bg": "#161B22",
        "border": "#30363D",
        "accent": "#238636",
        "accent_hover": "#2EA043",
        "text_secondary": "#8B949E",
        "button_bg": "#21262D",
        "button_hover": "#30363D",
        "input_bg": "#0D1117",
        "input_border": "#30363D",
        "github_colors": ["#161B22", "#0E4429", "#006D32", "#26A641", "#39D353"],
    }

    LIGHT = {
        "bg": "#FFFFFF",
        "fg": "#24292F",
        "canvas_bg": "#F6F8FA",
        "card_bg": "#FFFFFF",
        "border": "#D0D7DE",
        "accent": "#1F883D",
        "accent_hover": "#1A7F37",
        "text_secondary": "#57606A",
        "button_bg": "#F6F8FA",
        "button_hover": "#EAEEF2",
        "input_bg": "#FFFFFF",
        "input_border": "#D0D7DE",
        "github_colors": ["#EBEDF0", "#9BE9A8", "#40C463", "#30A14E", "#216E39"],
    }

    def __init__(self, mode: str = "dark"):
        self.mode = mode
        self.colors = self.DARK if mode == "dark" else self.LIGHT

    def toggle(self) -> None:
        """Toggle between light and dark mode."""
        self.mode = "light" if self.mode == "dark" else "dark"
        self.colors = self.DARK if self.mode == "dark" else self.LIGHT

    def get(self, key: str) -> str:
        """Get a color value from the current theme."""
        return self.colors.get(key, "#000000")
