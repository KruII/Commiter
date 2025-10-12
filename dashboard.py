"""Main dashboard application with widget management."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import List, Dict, Any, Optional
import json
from pathlib import Path

from theme import Theme
from widgets import BaseWidget, FinanceWidget, AIBotWidget


class WidgetManager:
    """Manages widgets on the dashboard."""

    def __init__(self, canvas: tk.Canvas, theme: Theme):
        self.canvas = canvas
        self.theme = theme
        self.widgets: List[BaseWidget] = []
        self.selected_widget: Optional[BaseWidget] = None
        self.drag_data = {"x": 0, "y": 0, "widget": None}

    def add_widget(self, widget_type: str, x: int = 50, y: int = 50) -> None:
        """Add a new widget to the dashboard."""
        widget_classes = {
            "finance": FinanceWidget,
            "ai_bot": AIBotWidget,
        }

        widget_class = widget_classes.get(widget_type)
        if widget_class:
            widget = widget_class(self.canvas, self.theme, x, y)
            self.widgets.append(widget)
            self.setup_widget_bindings(widget)

    def setup_widget_bindings(self, widget: BaseWidget) -> None:
        """Setup drag and drop for widget."""
        if widget.frame:
            widget.frame.bind("<Button-1>", lambda e, w=widget: self.on_widget_press(e, w))
            widget.frame.bind("<B1-Motion>", lambda e, w=widget: self.on_widget_drag(e, w))
            widget.frame.bind("<ButtonRelease-1>", lambda e, w=widget: self.on_widget_release(e, w))
            widget.frame.bind("<Button-3>", lambda e, w=widget: self.on_widget_right_click(e, w))

    def on_widget_press(self, event, widget: BaseWidget) -> None:
        """Handle widget press for dragging."""
        self.drag_data["widget"] = widget
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.selected_widget = widget

    def on_widget_drag(self, event, widget: BaseWidget) -> None:
        """Handle widget dragging."""
        if self.drag_data["widget"] == widget:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            new_x = widget.x + dx
            new_y = widget.y + dy
            widget.move(new_x, new_y)

    def on_widget_release(self, event, widget: BaseWidget) -> None:
        """Handle widget release."""
        self.drag_data["widget"] = None

    def on_widget_right_click(self, event, widget: BaseWidget) -> None:
        """Handle right click on widget (show context menu)."""
        menu = tk.Menu(self.canvas, tearoff=0)
        menu.add_command(label="Remove Widget", command=lambda: self.remove_widget(widget))
        menu.post(event.x_root, event.y_root)

    def remove_widget(self, widget: BaseWidget) -> None:
        """Remove a widget from the dashboard."""
        if widget in self.widgets:
            widget.destroy()
            self.widgets.remove(widget)

    def update_theme(self, theme: Theme) -> None:
        """Update theme for all widgets."""
        self.theme = theme
        for widget in self.widgets:
            widget.update_theme(theme)

    def save_layout(self, filepath: Path) -> None:
        """Save widget layout to file."""
        layout = []
        for widget in self.widgets:
            layout.append(
                {
                    "type": widget.__class__.__name__,
                    "x": widget.x,
                    "y": widget.y,
                    "width": widget.width,
                    "height": widget.height,
                }
            )
        with open(filepath, "w") as f:
            json.dump(layout, f, indent=2)

    def load_layout(self, filepath: Path) -> None:
        """Load widget layout from file."""
        if filepath.exists():
            with open(filepath, "r") as f:
                layout = json.load(f)
            for widget_info in layout:
                widget_type = widget_info.get("type", "").lower().replace("widget", "")
                self.add_widget(
                    widget_type, widget_info.get("x", 50), widget_info.get("y", 50)
                )


class Dashboard:
    """Main dashboard application."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Commiter Dashboard")
        self.theme = Theme("dark")
        self.root.configure(bg=self.theme.get("bg"))
        
        # Window size
        self.window_width = 1400
        self.window_height = 900
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        
        self.setup_ui()
        self.widget_manager = WidgetManager(self.canvas, self.theme)
        
        # Load saved layout or create default widgets
        self.layout_file = Path("dashboard_layout.json")
        if self.layout_file.exists():
            self.widget_manager.load_layout(self.layout_file)
        else:
            # Add default widgets
            self.widget_manager.add_widget("finance", 50, 50)
            self.widget_manager.add_widget("ai_bot", 500, 50)

    def setup_ui(self) -> None:
        """Setup the main UI."""
        # Top toolbar
        toolbar = tk.Frame(self.root, bg=self.theme.get("card_bg"), height=50)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Title
        tk.Label(
            toolbar,
            text="📊 Commiter Dashboard",
            font=("Arial", 16, "bold"),
            bg=self.theme.get("card_bg"),
            fg=self.theme.get("fg"),
        ).pack(side=tk.LEFT, padx=20, pady=10)

        # Theme toggle button
        self.theme_btn = tk.Button(
            toolbar,
            text="🌙 Dark Mode",
            bg=self.theme.get("button_bg"),
            fg=self.theme.get("fg"),
            command=self.toggle_theme,
            relief=tk.FLAT,
            padx=10,
            pady=5,
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=10, pady=10)

        # Add widget button
        add_widget_btn = tk.Button(
            toolbar,
            text="➕ Add Widget",
            bg=self.theme.get("accent"),
            fg="white",
            command=self.show_add_widget_dialog,
            relief=tk.FLAT,
            padx=10,
            pady=5,
        )
        add_widget_btn.pack(side=tk.RIGHT, padx=5, pady=10)

        # Save layout button
        save_btn = tk.Button(
            toolbar,
            text="💾 Save Layout",
            bg=self.theme.get("button_bg"),
            fg=self.theme.get("fg"),
            command=self.save_layout,
            relief=tk.FLAT,
            padx=10,
            pady=5,
        )
        save_btn.pack(side=tk.RIGHT, padx=5, pady=10)

        # Main canvas for widgets
        self.canvas = tk.Canvas(
            self.root,
            bg=self.theme.get("canvas_bg"),
            highlightthickness=0,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_bar = tk.Frame(self.root, bg=self.theme.get("card_bg"), height=30)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = tk.Label(
            self.status_bar,
            text="Ready | Drag widgets to reposition | Right-click to remove",
            bg=self.theme.get("card_bg"),
            fg=self.theme.get("text_secondary"),
        )
        self.status_label.pack(side=tk.LEFT, padx=10)

    def toggle_theme(self) -> None:
        """Toggle between light and dark theme."""
        self.theme.toggle()
        
        # Update main window
        self.root.configure(bg=self.theme.get("bg"))
        self.canvas.configure(bg=self.theme.get("canvas_bg"))
        
        # Update toolbar and status bar
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                self.update_frame_theme(widget)
        
        # Update theme button text
        if self.theme.mode == "dark":
            self.theme_btn.configure(text="🌙 Dark Mode")
        else:
            self.theme_btn.configure(text="☀️ Light Mode")
        
        # Update all widgets
        self.widget_manager.update_theme(self.theme)

    def update_frame_theme(self, frame: tk.Frame) -> None:
        """Recursively update frame and its children theme."""
        try:
            frame.configure(bg=self.theme.get("card_bg"))
        except:
            pass
        
        for child in frame.winfo_children():
            try:
                if isinstance(child, tk.Label):
                    child.configure(bg=self.theme.get("card_bg"), fg=self.theme.get("fg"))
                elif isinstance(child, tk.Button):
                    if "accent" in str(child.cget("bg")).lower() or "#238636" in str(child.cget("bg")):
                        child.configure(bg=self.theme.get("accent"))
                    else:
                        child.configure(bg=self.theme.get("button_bg"), fg=self.theme.get("fg"))
                elif isinstance(child, tk.Frame):
                    self.update_frame_theme(child)
            except:
                pass

    def show_add_widget_dialog(self) -> None:
        """Show dialog to add a new widget."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Widget")
        dialog.geometry("300x200")
        dialog.configure(bg=self.theme.get("bg"))

        tk.Label(
            dialog,
            text="Select Widget Type:",
            font=("Arial", 12, "bold"),
            bg=self.theme.get("bg"),
            fg=self.theme.get("fg"),
        ).pack(pady=20)

        btn_frame = tk.Frame(dialog, bg=self.theme.get("bg"))
        btn_frame.pack(pady=10)

        def add_finance():
            self.widget_manager.add_widget("finance", 50, 50)
            dialog.destroy()

        def add_ai_bot():
            self.widget_manager.add_widget("ai_bot", 50, 50)
            dialog.destroy()

        tk.Button(
            btn_frame,
            text="💰 Finance Widget",
            bg=self.theme.get("accent"),
            fg="white",
            command=add_finance,
            width=20,
            pady=10,
        ).pack(pady=5)

        tk.Button(
            btn_frame,
            text="🤖 AI Bot Monitor",
            bg=self.theme.get("accent"),
            fg="white",
            command=add_ai_bot,
            width=20,
            pady=10,
        ).pack(pady=5)

    def save_layout(self) -> None:
        """Save current widget layout."""
        self.widget_manager.save_layout(self.layout_file)
        messagebox.showinfo("Success", "Layout saved successfully!")

    def run(self) -> None:
        """Start the dashboard."""
        self.root.mainloop()


def main() -> None:
    """Main entry point for the dashboard."""
    dashboard = Dashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
