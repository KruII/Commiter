# Commiter

A comprehensive dashboard application with multiple features including GitHub commit visualization, finance tracking, and AI bot training monitoring.

## Features

### 🎨 Modern Dashboard (NEW!)
- **Widget-based system**: Add, remove, and reposition widgets freely
- **Light/Dark mode**: Toggle between themes with one click
- **Persistent layout**: Your widget arrangement is automatically saved

### 💰 Finance Widget
Track your investments and finances with multiple categories:
- **All**: Overview of all your assets
- **Crypto**: Cryptocurrency investments
- **Investment**: Stock and other investments
- **ETF**: Exchange-traded funds

Features:
- Connect multiple portfolio accounts (Binance, Coinbase, Interactive Brokers, Vanguard)
- Add manual transactions
- Real-time balance tracking
- Statistics and performance metrics

### 🤖 AI Bot Training Monitor
Monitor your AI bot training based on GEM (Global Entrepreneurship Monitor):
- Training status and progress tracking
- GEM-based metrics (Entrepreneurial Activity, Innovation Score, Market Analysis, Model Accuracy)
- Start/stop training controls
- Real-time progress visualization

### 📊 GitHub Pixel Art (Original Feature)
Generate GitHub commits to create pixel art on your contribution graph:
- Displays a calendar based on your previous contributions
- Mark squares with different activity levels
- Automatically creates and pushes commits to your repository

## Requirements

- Python 3.8 or newer
- Dependencies listed in `requiremnts.txt`

Install them with:
```bash
pip install -r requiremnts.txt
```

## Usage

### Launch the Application

```bash
python main.py
```

This will show a launcher with two options:
1. **Open Dashboard**: Launch the new widget-based dashboard
2. **GitHub Pixel Art Mode**: Use the original commit visualization tool

### Dashboard Mode

In dashboard mode, you can:
- **Add Widgets**: Click the "➕ Add Widget" button to add new widgets
- **Reposition Widgets**: Drag widgets to move them around the canvas
- **Remove Widgets**: Right-click on a widget to remove it
- **Toggle Theme**: Click the theme button to switch between light and dark modes
- **Save Layout**: Click "💾 Save Layout" to persist your widget arrangement

### Command Line Options

```bash
# Launch dashboard directly
python main.py --dashboard

# Launch GitHub Pixel Art directly
python main.py 2025 your-github-username
```

## Files

- `main.py`: Main launcher and GitHub pixel art functionality
- `dashboard.py`: Dashboard application with widget management
- `widgets.py`: Widget implementations (Finance, AI Bot)
- `theme.py`: Theme configuration for light/dark modes
- `dashboard_layout.json`: Saved widget layout (auto-generated)
- `file.txt`: Temporary storage for commit contents

## Warning

The GitHub Pixel Art feature rewrites repository history. Use it carefully.

## License

This project is licensed under the [MIT License](LICENSE).
