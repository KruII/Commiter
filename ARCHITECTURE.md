# Commiter Dashboard - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                              │
│                    Application Launcher                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  1. Dashboard Mode (New)                            │   │
│  │  2. GitHub Pixel Art Mode (Original)                │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
              │                              │
              │                              │
              ▼                              ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│     dashboard.py         │    │   Original GitHub         │
│   Dashboard Application  │    │   Pixel Art Feature       │
└──────────────────────────┘    └──────────────────────────┘
              │
              ├─────────────────┬─────────────────┐
              ▼                 ▼                 ▼
      ┌──────────────┐  ┌─────────────┐  ┌─────────────┐
      │  theme.py    │  │ widgets.py  │  │   JSON      │
      │              │  │             │  │  Storage    │
      │ Theme System │  │   Widgets   │  │  (Layout)   │
      └──────────────┘  └─────────────┘  └─────────────┘
```

## Component Hierarchy

```
Dashboard
    ├── WidgetManager
    │   ├── List[BaseWidget]
    │   │   ├── FinanceWidget
    │   │   ├── AIBotWidget
    │   │   └── [Custom Widgets...]
    │   └── Layout Management
    │       ├── Save Layout
    │       └── Load Layout
    │
    ├── Theme
    │   ├── Dark Mode Colors
    │   └── Light Mode Colors
    │
    └── UI Components
        ├── Toolbar
        │   ├── Title
        │   ├── Theme Toggle
        │   ├── Add Widget Button
        │   └── Save Layout Button
        ├── Canvas (Widget Container)
        └── Status Bar
```

## Widget Structure

```
BaseWidget (Abstract)
    ├── Properties
    │   ├── parent: tk.Widget
    │   ├── theme: Theme
    │   ├── x, y: Position
    │   ├── width, height: Size
    │   └── frame: tk.Frame
    │
    ├── Methods
    │   ├── create_widget()
    │   ├── update_theme(theme)
    │   ├── destroy()
    │   └── move(x, y)
    │
    └── Implementations
        ├── FinanceWidget
        │   ├── Categories System
        │   ├── Balance Display
        │   ├── Portfolio Manager
        │   └── Transaction System
        │
        └── AIBotWidget
            ├── Status Display
            ├── Progress Bar
            ├── GEM Metrics
            └── Training Controls
```

## Data Flow

### Theme Toggle
```
User clicks theme button
    ↓
Dashboard.toggle_theme()
    ↓
Theme.toggle() → Update theme.colors
    ↓
WidgetManager.update_theme(theme)
    ↓
For each widget: widget.update_theme(theme)
    ↓
UI updates with new colors
```

### Add Widget
```
User clicks "Add Widget"
    ↓
Dashboard.show_add_widget_dialog()
    ↓
User selects widget type
    ↓
WidgetManager.add_widget(type, x, y)
    ↓
Create widget instance
    ↓
Setup drag/drop bindings
    ↓
Add to widgets list
    ↓
Widget appears on canvas
```

### Save Layout
```
User clicks "Save Layout"
    ↓
WidgetManager.save_layout(filepath)
    ↓
For each widget: collect {type, x, y, width, height}
    ↓
Save to dashboard_layout.json
    ↓
Success message
```

### Load Layout
```
Dashboard starts
    ↓
Check if dashboard_layout.json exists
    ↓
WidgetManager.load_layout(filepath)
    ↓
For each saved widget: create and position
    ↓
Widgets restored to saved positions
```

## File Structure

```
/home/runner/work/Commiter/Commiter/
├── main.py                    # Application entry point & launcher
├── dashboard.py               # Dashboard application
├── widgets.py                 # Widget implementations
├── theme.py                   # Theme system
├── dashboard_layout.json      # Saved widget layout (generated)
├── file.txt                   # Temp file for commits
├── requiremnts.txt           # Dependencies
├── README.md                  # User documentation
├── FEATURES.md               # Feature documentation
├── ARCHITECTURE.md           # This file
└── LICENSE                    # MIT License
```

## Class Diagram

```
┌─────────────────────┐
│      Theme          │
├─────────────────────┤
│ - mode: str         │
│ - colors: Dict      │
├─────────────────────┤
│ + toggle()          │
│ + get(key)          │
└─────────────────────┘
         △
         │ uses
         │
┌────────┴────────────────────────────┐
│           BaseWidget                │
├─────────────────────────────────────┤
│ - parent: tk.Widget                 │
│ - theme: Theme                      │
│ - x, y: int                         │
│ - width, height: int                │
│ - frame: tk.Frame                   │
├─────────────────────────────────────┤
│ + create_widget()                   │
│ + update_theme(theme)               │
│ + destroy()                         │
│ + move(x, y)                        │
└─────────────────────────────────────┘
         △
         │ inherits
         │
    ┌────┴─────┐
    │          │
┌───┴───┐  ┌──┴────┐
│Finance│  │AIBot  │
│Widget │  │Widget │
└───────┘  └───────┘

┌─────────────────────────────────────┐
│        WidgetManager                │
├─────────────────────────────────────┤
│ - canvas: tk.Canvas                 │
│ - theme: Theme                      │
│ - widgets: List[BaseWidget]         │
│ - selected_widget: BaseWidget       │
│ - drag_data: Dict                   │
├─────────────────────────────────────┤
│ + add_widget(type, x, y)            │
│ + remove_widget(widget)             │
│ + update_theme(theme)               │
│ + save_layout(filepath)             │
│ + load_layout(filepath)             │
│ + on_widget_press(event, widget)    │
│ + on_widget_drag(event, widget)     │
│ + on_widget_release(event, widget)  │
└─────────────────────────────────────┘
         △
         │ uses
         │
┌────────┴────────────────────────────┐
│          Dashboard                  │
├─────────────────────────────────────┤
│ - root: tk.Tk                       │
│ - theme: Theme                      │
│ - widget_manager: WidgetManager     │
│ - canvas: tk.Canvas                 │
│ - window_width, height: int         │
├─────────────────────────────────────┤
│ + setup_ui()                        │
│ + toggle_theme()                    │
│ + show_add_widget_dialog()          │
│ + save_layout()                     │
│ + run()                             │
└─────────────────────────────────────┘
```

## Event Flow

### Drag and Drop
```
Mouse Down on Widget
    ↓
on_widget_press()
    ├── Store drag_data (x, y, widget)
    └── Set selected_widget
    ↓
Mouse Move (B1-Motion)
    ↓
on_widget_drag()
    ├── Calculate delta (dx, dy)
    ├── Calculate new position
    └── widget.move(new_x, new_y)
    ↓
Mouse Up
    ↓
on_widget_release()
    └── Clear drag_data
```

### Right-Click Menu
```
Right-Click on Widget
    ↓
on_widget_right_click()
    ↓
Create context menu
    └── "Remove Widget" option
    ↓
User clicks remove
    ↓
remove_widget(widget)
    ├── widget.destroy()
    └── Remove from widgets list
```

## Extension Points

### 1. New Widget Types
Add new widgets by:
1. Extending `BaseWidget` in `widgets.py`
2. Registering in `WidgetManager.widget_classes`
3. Adding to "Add Widget" dialog

### 2. Custom Themes
Add themes by:
1. Extending `Theme.DARK` and `Theme.LIGHT` dictionaries
2. Adding theme selection UI
3. Saving theme preference

### 3. Data Persistence
Current: JSON file for layout
Future options:
- SQLite database for widget data
- Cloud sync for multi-device
- Export/import configurations

### 4. Widget Communication
Future feature:
- Event bus for inter-widget communication
- Shared data store
- Widget linking (e.g., finance updates trigger alerts)

## Performance Considerations

1. **Widget Count**: Recommended max 10-15 widgets per dashboard
2. **Update Frequency**: Theme updates affect all widgets
3. **Layout Saves**: Triggered manually, not on every move
4. **Memory**: Each widget maintains its own state

## Security Considerations

1. **API Keys**: Currently stored in memory
   - Future: Encrypt and store securely
   - Use system keychain/vault
2. **Portfolio Data**: Local only
   - Future: Optional cloud backup with encryption
3. **File Permissions**: Check write permissions for layout file

## Testing Strategy

1. **Unit Tests**: Individual widget functionality
2. **Integration Tests**: Widget manager operations
3. **UI Tests**: Theme switching, drag-drop
4. **Layout Tests**: Save/load functionality
5. **Manual Tests**: Visual appearance, user interactions
