"""Widget system for the dashboard."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional
from datetime import datetime
import json


class BaseWidget:
    """Base class for all dashboard widgets."""

    def __init__(self, parent: tk.Widget, theme: Any, x: int = 0, y: int = 0, width: int = 300, height: int = 200):
        self.parent = parent
        self.theme = theme
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.frame = None
        self.create_widget()

    def create_widget(self) -> None:
        """Create the widget UI. Must be implemented by subclasses."""
        self.frame = tk.Frame(
            self.parent,
            bg=self.theme.get("card_bg"),
            highlightbackground=self.theme.get("border"),
            highlightthickness=1,
        )
        self.frame.place(x=self.x, y=self.y, width=self.width, height=self.height)

    def update_theme(self, theme: Any) -> None:
        """Update widget colors based on theme."""
        self.theme = theme
        if self.frame:
            self.frame.configure(bg=self.theme.get("card_bg"), highlightbackground=self.theme.get("border"))

    def destroy(self) -> None:
        """Remove the widget."""
        if self.frame:
            self.frame.destroy()

    def move(self, x: int, y: int) -> None:
        """Move widget to new position."""
        self.x = x
        self.y = y
        if self.frame:
            self.frame.place(x=x, y=y)


class FinanceWidget(BaseWidget):
    """Widget for tracking finances and statistics."""

    def __init__(self, parent: tk.Widget, theme: Any, x: int = 0, y: int = 0, width: int = 400, height: int = 500):
        self.categories = ["All", "Crypto", "Investment", "ETF"]
        self.current_category = tk.StringVar(value="All")
        self.portfolios: Dict[str, Dict[str, Any]] = {}
        self.data: Dict[str, float] = {
            "All": 0.0,
            "Crypto": 0.0,
            "Investment": 0.0,
            "ETF": 0.0,
        }
        super().__init__(parent, theme, x, y, width, height)

    def create_widget(self) -> None:
        """Create the finance widget UI."""
        super().create_widget()

        # Title
        title = tk.Label(
            self.frame,
            text="💰 Finance Dashboard",
            font=("Arial", 14, "bold"),
            bg=self.theme.get("card_bg"),
            fg=self.theme.get("fg"),
        )
        title.pack(pady=10)

        # Category selector
        cat_frame = tk.Frame(self.frame, bg=self.theme.get("card_bg"))
        cat_frame.pack(pady=5, fill=tk.X, padx=10)

        tk.Label(cat_frame, text="Category:", bg=self.theme.get("card_bg"), fg=self.theme.get("fg")).pack(side=tk.LEFT)

        for cat in self.categories:
            btn = tk.Radiobutton(
                cat_frame,
                text=cat,
                variable=self.current_category,
                value=cat,
                bg=self.theme.get("card_bg"),
                fg=self.theme.get("fg"),
                selectcolor=self.theme.get("button_bg"),
                command=self.update_display,
            )
            btn.pack(side=tk.LEFT, padx=5)

        # Balance display
        self.balance_frame = tk.Frame(self.frame, bg=self.theme.get("card_bg"))
        self.balance_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)

        self.balance_label = tk.Label(
            self.balance_frame,
            text="$0.00",
            font=("Arial", 24, "bold"),
            bg=self.theme.get("card_bg"),
            fg=self.theme.get("accent"),
        )
        self.balance_label.pack(pady=10)

        # Statistics
        self.stats_frame = tk.Frame(self.balance_frame, bg=self.theme.get("card_bg"))
        self.stats_frame.pack(fill=tk.BOTH, expand=True)

        # Portfolio management
        portfolio_frame = tk.Frame(self.frame, bg=self.theme.get("card_bg"))
        portfolio_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Label(
            portfolio_frame,
            text="Portfolio Management",
            font=("Arial", 10, "bold"),
            bg=self.theme.get("card_bg"),
            fg=self.theme.get("fg"),
        ).pack()

        btn_frame = tk.Frame(portfolio_frame, bg=self.theme.get("card_bg"))
        btn_frame.pack(pady=5)

        tk.Button(
            btn_frame,
            text="Connect Portfolio",
            bg=self.theme.get("accent"),
            fg="white",
            command=self.connect_portfolio,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Add Transaction",
            bg=self.theme.get("button_bg"),
            fg=self.theme.get("fg"),
            command=self.add_transaction,
        ).pack(side=tk.LEFT, padx=5)

        self.update_display()

    def update_display(self) -> None:
        """Update the display based on selected category."""
        category = self.current_category.get()
        balance = self.data.get(category, 0.0)
        self.balance_label.configure(text=f"${balance:,.2f}")

        # Clear and update stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        stats = [
            ("Today's Change", "+$0.00 (+0.0%)", self.theme.get("accent")),
            ("Monthly Gain", "+$0.00", self.theme.get("fg")),
            ("Total Assets", f"${balance:,.2f}", self.theme.get("fg")),
        ]

        for label, value, color in stats:
            row = tk.Frame(self.stats_frame, bg=self.theme.get("card_bg"))
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=label + ":", bg=self.theme.get("card_bg"), fg=self.theme.get("text_secondary")).pack(
                side=tk.LEFT
            )
            tk.Label(row, text=value, bg=self.theme.get("card_bg"), fg=color, font=("Arial", 10, "bold")).pack(
                side=tk.RIGHT
            )

    def connect_portfolio(self) -> None:
        """Open dialog to connect a portfolio."""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Connect Portfolio")
        dialog.geometry("400x300")
        dialog.configure(bg=self.theme.get("bg"))

        tk.Label(dialog, text="Portfolio Connection", font=("Arial", 12, "bold"), bg=self.theme.get("bg"), fg=self.theme.get("fg")).pack(
            pady=10
        )

        # Form
        form_frame = tk.Frame(dialog, bg=self.theme.get("bg"))
        form_frame.pack(pady=10, padx=20, fill=tk.BOTH)

        tk.Label(form_frame, text="Platform:", bg=self.theme.get("bg"), fg=self.theme.get("fg")).grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )
        platform_var = tk.StringVar()
        platform_combo = ttk.Combobox(
            form_frame, textvariable=platform_var, values=["Binance", "Coinbase", "Interactive Brokers", "Vanguard"]
        )
        platform_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="API Key:", bg=self.theme.get("bg"), fg=self.theme.get("fg")).grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        api_entry = tk.Entry(form_frame, show="*")
        api_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Category:", bg=self.theme.get("bg"), fg=self.theme.get("fg")).grid(
            row=2, column=0, sticky="e", padx=5, pady=5
        )
        category_var = tk.StringVar(value="Crypto")
        category_combo = ttk.Combobox(form_frame, textvariable=category_var, values=self.categories[1:])
        category_combo.grid(row=2, column=1, padx=5, pady=5)

        def save_portfolio():
            platform = platform_var.get()
            api_key = api_entry.get()
            category = category_var.get()
            if platform and api_key:
                self.portfolios[platform] = {"api_key": api_key, "category": category}
                tk.messagebox.showinfo("Success", f"Portfolio connected: {platform}")
                dialog.destroy()

        tk.Button(
            dialog, text="Connect", bg=self.theme.get("accent"), fg="white", command=save_portfolio
        ).pack(pady=10)

    def add_transaction(self) -> None:
        """Open dialog to add a transaction."""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add Transaction")
        dialog.geometry("350x250")
        dialog.configure(bg=self.theme.get("bg"))

        tk.Label(dialog, text="New Transaction", font=("Arial", 12, "bold"), bg=self.theme.get("bg"), fg=self.theme.get("fg")).pack(
            pady=10
        )

        form_frame = tk.Frame(dialog, bg=self.theme.get("bg"))
        form_frame.pack(pady=10, padx=20)

        tk.Label(form_frame, text="Amount:", bg=self.theme.get("bg"), fg=self.theme.get("fg")).grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )
        amount_entry = tk.Entry(form_frame)
        amount_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Category:", bg=self.theme.get("bg"), fg=self.theme.get("fg")).grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        category_var = tk.StringVar(value="Crypto")
        category_combo = ttk.Combobox(form_frame, textvariable=category_var, values=self.categories[1:])
        category_combo.grid(row=1, column=1, padx=5, pady=5)

        def save_transaction():
            try:
                amount = float(amount_entry.get())
                category = category_var.get()
                self.data[category] = self.data.get(category, 0.0) + amount
                self.data["All"] = sum(self.data[cat] for cat in self.categories[1:])
                self.update_display()
                tk.messagebox.showinfo("Success", f"Added ${amount:,.2f} to {category}")
                dialog.destroy()
            except ValueError:
                tk.messagebox.showerror("Error", "Please enter a valid amount")

        tk.Button(
            dialog, text="Add", bg=self.theme.get("accent"), fg="white", command=save_transaction
        ).pack(pady=10)


class AIBotWidget(BaseWidget):
    """Widget for monitoring AI bot training based on GEM."""

    def __init__(self, parent: tk.Widget, theme: Any, x: int = 0, y: int = 0, width: int = 400, height: int = 300):
        self.training_status = "Idle"
        self.progress = 0
        super().__init__(parent, theme, x, y, width, height)

    def create_widget(self) -> None:
        """Create the AI bot training monitor UI."""
        super().create_widget()

        # Title
        title = tk.Label(
            self.frame,
            text="🤖 AI Bot Training Monitor",
            font=("Arial", 14, "bold"),
            bg=self.theme.get("card_bg"),
            fg=self.theme.get("fg"),
        )
        title.pack(pady=10)

        # Status
        status_frame = tk.Frame(self.frame, bg=self.theme.get("card_bg"))
        status_frame.pack(pady=10, fill=tk.X, padx=20)

        tk.Label(
            status_frame,
            text="Status:",
            bg=self.theme.get("card_bg"),
            fg=self.theme.get("text_secondary"),
        ).pack(side=tk.LEFT)

        self.status_label = tk.Label(
            status_frame,
            text=self.training_status,
            font=("Arial", 10, "bold"),
            bg=self.theme.get("card_bg"),
            fg=self.theme.get("accent"),
        )
        self.status_label.pack(side=tk.RIGHT)

        # Progress bar
        progress_frame = tk.Frame(self.frame, bg=self.theme.get("card_bg"))
        progress_frame.pack(pady=5, fill=tk.X, padx=20)

        tk.Label(progress_frame, text="Progress:", bg=self.theme.get("card_bg"), fg=self.theme.get("fg")).pack(
            anchor="w"
        )

        self.progress_bar = ttk.Progressbar(progress_frame, length=300, mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=5)

        self.progress_label = tk.Label(
            progress_frame, text="0%", bg=self.theme.get("card_bg"), fg=self.theme.get("fg")
        )
        self.progress_label.pack(anchor="e")

        # GEM Metrics
        metrics_frame = tk.Frame(self.frame, bg=self.theme.get("card_bg"))
        metrics_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        tk.Label(
            metrics_frame,
            text="GEM-based Metrics:",
            font=("Arial", 10, "bold"),
            bg=self.theme.get("card_bg"),
            fg=self.theme.get("fg"),
        ).pack(anchor="w", pady=5)

        metrics = [
            ("Entrepreneurial Activity", "0%"),
            ("Innovation Score", "0.0"),
            ("Market Analysis", "Pending"),
            ("Model Accuracy", "0%"),
        ]

        for label, value in metrics:
            row = tk.Frame(metrics_frame, bg=self.theme.get("card_bg"))
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=label + ":", bg=self.theme.get("card_bg"), fg=self.theme.get("text_secondary")).pack(
                side=tk.LEFT
            )
            tk.Label(row, text=value, bg=self.theme.get("card_bg"), fg=self.theme.get("fg")).pack(side=tk.RIGHT)

        # Controls
        btn_frame = tk.Frame(self.frame, bg=self.theme.get("card_bg"))
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Start Training",
            bg=self.theme.get("accent"),
            fg="white",
            command=self.start_training,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Stop Training",
            bg=self.theme.get("button_bg"),
            fg=self.theme.get("fg"),
            command=self.stop_training,
        ).pack(side=tk.LEFT, padx=5)

    def start_training(self) -> None:
        """Start AI bot training simulation."""
        self.training_status = "Training"
        self.status_label.configure(text="Training", fg=self.theme.get("accent"))
        self.progress = 0
        self.update_progress()

    def stop_training(self) -> None:
        """Stop AI bot training."""
        self.training_status = "Stopped"
        self.status_label.configure(text="Stopped", fg="#F85149")

    def update_progress(self) -> None:
        """Update training progress."""
        if self.training_status == "Training" and self.progress < 100:
            self.progress += 1
            self.progress_bar["value"] = self.progress
            self.progress_label.configure(text=f"{self.progress}%")
            if self.progress < 100:
                self.frame.after(100, self.update_progress)
            else:
                self.training_status = "Complete"
                self.status_label.configure(text="Complete", fg=self.theme.get("accent"))
