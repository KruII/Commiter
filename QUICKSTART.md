# Quick Start Guide

Get up and running with Commiter Dashboard in 5 minutes!

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/KruII/Commiter.git
cd Commiter
```

2. **Install dependencies:**
```bash
pip install -r requiremnts.txt
```

3. **Launch the application:**
```bash
python main.py
```

## First Launch

When you first run the application, you'll see a launcher with two options:

### Option 1: Dashboard Mode (Recommended for New Features)
Click **"📊 Open Dashboard (New!)"** to access:
- Finance tracking widget
- AI bot training monitor
- Customizable widget layout
- Light/dark theme toggle

### Option 2: GitHub Pixel Art Mode (Original Feature)
- Enter a year (e.g., 2025)
- Enter your GitHub username
- Click "Open Pixel Art"

## Dashboard Quick Tour

### 1. Understanding the Interface

```
┌─────────────────────────────────────────────────┐
│  Title              [Buttons]          [Theme]  │  ← Toolbar
├─────────────────────────────────────────────────┤
│                                                 │
│  [Widget 1]          [Widget 2]                 │  ← Canvas
│                                                 │  ← (Drag widgets here)
│                                                 │
├─────────────────────────────────────────────────┤
│  Status: Ready | Instructions                   │  ← Status Bar
└─────────────────────────────────────────────────┘
```

### 2. Working with Widgets

**Add a Widget:**
1. Click "➕ Add Widget" button
2. Choose "💰 Finance Widget" or "🤖 AI Bot Monitor"
3. Widget appears in the top-left corner
4. Drag it to your preferred position

**Move a Widget:**
- Click and hold on the widget
- Drag to new position
- Release mouse button

**Remove a Widget:**
- Right-click on the widget
- Select "Remove Widget"

### 3. Using the Finance Widget

**Track Your Finances:**
1. Select a category (All, Crypto, Investment, ETF)
2. View your current balance
3. See statistics (Today's Change, Monthly Gain, etc.)

**Add a Transaction:**
1. Click "Add Transaction"
2. Enter amount (e.g., 1000)
3. Select category
4. Click "Add"
5. Balance updates automatically

**Connect a Portfolio:**
1. Click "Connect Portfolio"
2. Select platform (Binance, Coinbase, etc.)
3. Enter API key
4. Choose category
5. Click "Connect"

### 4. Using the AI Bot Monitor

**Start Training:**
1. Click "Start Training" button
2. Watch progress bar fill
3. Monitor GEM metrics
4. Wait for completion or click "Stop Training"

**View Metrics:**
- Entrepreneurial Activity
- Innovation Score
- Market Analysis
- Model Accuracy

### 5. Customizing the Theme

**Toggle Theme:**
- Click the theme button (🌙 Dark Mode or ☀️ Light Mode)
- Entire dashboard updates instantly
- All widgets adapt to new theme

### 6. Saving Your Layout

**Manual Save:**
1. Arrange widgets as desired
2. Click "💾 Save Layout"
3. Layout saved to `dashboard_layout.json`

**Automatic Restore:**
- Next time you open the dashboard
- Widgets appear in saved positions

## Common Tasks

### Task 1: Set Up Finance Tracking
```
1. Launch dashboard
2. Click "Add Widget" → "Finance Widget"
3. Click "Add Transaction"
4. Enter: Amount: 5000, Category: Investment
5. Click "Add"
6. View updated balance
```

### Task 2: Monitor AI Training
```
1. Launch dashboard
2. Add "AI Bot Monitor" widget
3. Click "Start Training"
4. Observe progress and metrics
5. Click "Stop Training" when done
```

### Task 3: Create Custom Dashboard Layout
```
1. Launch dashboard
2. Add 2-3 widgets
3. Drag them to preferred positions
4. Toggle theme to preferred mode
5. Click "Save Layout"
6. Close and reopen - layout persists!
```

## Keyboard Shortcuts (Future Feature)

Currently, all interactions are mouse-based. Future versions will include:
- `Ctrl+N` - Add new widget
- `Ctrl+S` - Save layout
- `Ctrl+T` - Toggle theme
- `Delete` - Remove selected widget

## Tips and Tricks

1. **Organize by Purpose:**
   - Group related widgets together
   - Finance widgets on left, monitoring on right

2. **Use Color Coding:**
   - Light mode for daytime work
   - Dark mode for evening sessions

3. **Save Frequently:**
   - Save layout after major changes
   - Prevents loss of arrangement

4. **Start Simple:**
   - Begin with 1-2 widgets
   - Add more as you become comfortable

5. **Experiment:**
   - Try different layouts
   - Test both themes
   - Add and remove widgets freely

## Troubleshooting

### Dashboard Won't Open
```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install -r requiremnts.txt

# Try direct launch
python dashboard.py
```

### Widgets Not Appearing
- Check that you clicked "Add Widget"
- Look for widgets in top-left corner
- Try maximizing window
- Restart dashboard

### Layout Not Saving
- Check write permissions in directory
- Look for `dashboard_layout.json` file
- Try manual save with "Save Layout" button

### Theme Not Changing
- Click theme button in toolbar
- Check that all widgets support theme updates
- Restart dashboard if needed

## Next Steps

Once you're comfortable with the basics:

1. **Read Full Documentation:**
   - `README.md` - Overview and usage
   - `FEATURES.md` - Detailed feature list
   - `ARCHITECTURE.md` - System design

2. **Customize Further:**
   - Edit `theme.py` to add custom colors
   - Create new widgets in `widgets.py`
   - Extend functionality

3. **Contribute:**
   - Report issues on GitHub
   - Suggest new widget types
   - Submit pull requests

## Getting Help

- **Documentation:** Read `README.md` and `FEATURES.md`
- **Demo:** Run `python demo.py` to see features
- **Issues:** Open an issue on GitHub
- **Code:** Check `ARCHITECTURE.md` for code structure

## Quick Reference Card

```
┌─────────────────────────────────────────────────┐
│              DASHBOARD CONTROLS                 │
├─────────────────────────────────────────────────┤
│  Add Widget          ➕ Button in toolbar      │
│  Remove Widget       Right-click → Remove      │
│  Move Widget         Click and drag            │
│  Toggle Theme        🌙/☀️ Button             │
│  Save Layout         💾 Button in toolbar      │
├─────────────────────────────────────────────────┤
│            FINANCE WIDGET                       │
├─────────────────────────────────────────────────┤
│  Switch Category     Click radio button        │
│  Add Money           "Add Transaction" button  │
│  Connect Account     "Connect Portfolio" button│
├─────────────────────────────────────────────────┤
│           AI BOT MONITOR                        │
├─────────────────────────────────────────────────┤
│  Start Training      "Start Training" button   │
│  Stop Training       "Stop Training" button    │
│  View Progress       Progress bar              │
│  Check Metrics       GEM-based stats           │
└─────────────────────────────────────────────────┘
```

Happy dashboarding! 🎉
