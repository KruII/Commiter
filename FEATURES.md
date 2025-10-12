# Commiter Dashboard - Features Documentation

## Overview
The Commiter Dashboard is a modern, widget-based application that provides multiple tools for tracking GitHub contributions, managing finances, and monitoring AI bot training.

## Architecture

### Modular Design
The application is built with a modular architecture that allows easy extension:

```
main.py         - Launcher and original GitHub pixel art
dashboard.py    - Main dashboard application with widget management
widgets.py      - Widget implementations (BaseWidget, FinanceWidget, AIBotWidget)
theme.py        - Theme system (light/dark mode)
```

### Theme System (`theme.py`)

The theme system provides two color schemes:
- **Dark Mode**: GitHub-inspired dark theme with green accents
- **Light Mode**: Clean, bright theme for daytime use

Key features:
- Toggle between modes with one click
- All colors centrally managed
- Automatic propagation to all widgets

```python
# Theme colors include:
- bg: Background color
- fg: Foreground/text color
- canvas_bg: Canvas background
- card_bg: Widget card background
- border: Border colors
- accent: Accent color (buttons, highlights)
- github_colors: GitHub contribution graph colors
```

### Widget System (`widgets.py`)

#### BaseWidget
Base class for all widgets with common functionality:
- Position management (x, y)
- Size management (width, height)
- Theme updates
- Drag and drop support
- Destroy/cleanup

#### FinanceWidget
Comprehensive finance tracking widget with:

**Categories:**
1. **All** - Overview of all assets
2. **Crypto** - Cryptocurrency investments
3. **Investment** - Stocks and traditional investments
4. **ETF** - Exchange-traded funds

**Features:**
- Balance display with formatting
- Category switching
- Portfolio connection:
  - Binance
  - Coinbase
  - Interactive Brokers
  - Vanguard
- Manual transaction entry
- Statistics display:
  - Today's Change
  - Monthly Gain
  - Total Assets
- Secure API key storage (encrypted in production)

**Usage:**
```python
finance_widget = FinanceWidget(parent, theme, x=50, y=50, width=400, height=500)
```

#### AIBotWidget
AI bot training monitor based on GEM (Global Entrepreneurship Monitor):

**Features:**
- Training status (Idle, Training, Complete, Stopped)
- Progress bar with percentage
- GEM-based metrics:
  - Entrepreneurial Activity
  - Innovation Score
  - Market Analysis
  - Model Accuracy
- Training controls (Start/Stop)
- Real-time progress updates

**Usage:**
```python
ai_widget = AIBotWidget(parent, theme, x=50, y=50, width=400, height=300)
```

### Dashboard (`dashboard.py`)

#### WidgetManager
Manages all widgets on the dashboard:
- Add widgets dynamically
- Drag and drop repositioning
- Remove widgets (right-click context menu)
- Save/load layout to JSON
- Theme propagation to all widgets

**Layout Persistence:**
Widget positions are saved to `dashboard_layout.json`:
```json
[
  {
    "type": "FinanceWidget",
    "x": 50,
    "y": 50,
    "width": 400,
    "height": 500
  },
  {
    "type": "AIBotWidget",
    "x": 500,
    "y": 50,
    "width": 400,
    "height": 300
  }
]
```

#### Dashboard Application
Main application window with:
- Top toolbar with title and controls
- Theme toggle button
- Add widget button
- Save layout button
- Main canvas for widgets
- Status bar with instructions

**Window Size:** 1400x900 (customizable)

## User Interactions

### Drag and Drop
- **Left-click + drag** on any widget to move it
- Widgets can be positioned anywhere on the canvas
- Position is automatically saved

### Context Menu
- **Right-click** on any widget to show options
- Select "Remove Widget" to delete it

### Adding Widgets
1. Click "➕ Add Widget" button
2. Select widget type from dialog:
   - 💰 Finance Widget
   - 🤖 AI Bot Monitor
3. Widget appears at default position
4. Drag to desired location

### Theme Toggle
- Click theme button in toolbar
- Switches between:
  - 🌙 Dark Mode
  - ☀️ Light Mode
- All widgets update instantly

### Finance Widget Usage
1. **Select Category**: Click radio button for All/Crypto/Investment/ETF
2. **Connect Portfolio**:
   - Click "Connect Portfolio"
   - Select platform
   - Enter API key
   - Choose category
   - Click "Connect"
3. **Add Transaction**:
   - Click "Add Transaction"
   - Enter amount
   - Select category
   - Click "Add"

### AI Bot Training
1. Click "Start Training" to begin
2. Watch progress bar fill
3. Monitor GEM metrics
4. Click "Stop Training" to halt

## Extensibility

### Adding New Widgets

To add a new widget type:

1. **Create widget class in `widgets.py`:**
```python
class MyCustomWidget(BaseWidget):
    def __init__(self, parent, theme, x=0, y=0, width=300, height=200):
        super().__init__(parent, theme, x, y, width, height)
    
    def create_widget(self):
        super().create_widget()
        # Add your UI elements here
        tk.Label(
            self.frame,
            text="My Custom Widget",
            bg=self.theme.get("card_bg"),
            fg=self.theme.get("fg")
        ).pack()
```

2. **Register in WidgetManager (`dashboard.py`):**
```python
widget_classes = {
    "finance": FinanceWidget,
    "ai_bot": AIBotWidget,
    "my_custom": MyCustomWidget,  # Add here
}
```

3. **Add to dialog:**
```python
def add_my_custom():
    self.widget_manager.add_widget("my_custom", 50, 50)
    dialog.destroy()

tk.Button(
    btn_frame,
    text="🎨 My Custom Widget",
    command=add_my_custom,
    width=20,
    pady=10,
).pack(pady=5)
```

### Customizing Themes

Edit `theme.py` to customize colors:

```python
DARK = {
    "bg": "#0D1117",        # Main background
    "fg": "#FFFFFF",        # Text color
    "accent": "#238636",    # Accent color
    # ... more colors
}
```

## Best Practices

1. **Widget Size**: Keep widgets between 300-500px for optimal display
2. **Layout**: Arrange widgets in a grid for clean organization
3. **Save Frequently**: Click "💾 Save Layout" after arranging widgets
4. **Theme Consistency**: Ensure all custom widgets support theme updates
5. **Extensibility**: Use BaseWidget as foundation for custom widgets

## Future Enhancements

Potential additions:
- GitHub commits widget (integrate original feature)
- Calendar/scheduler widget
- Notes/todo widget
- Weather widget
- Stock ticker widget
- Cryptocurrency price tracker
- News feed widget
- Custom widget creator UI
- Multiple dashboard tabs
- Export dashboard as image
- Collaborative dashboards
- Widget marketplace
