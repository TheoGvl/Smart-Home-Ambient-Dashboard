# Ambient Smart Home Dashboard

A premium, interactive smart home control panel built with **Python** and the **Flet** framework. The application focuses on an "Ambient UX", where visual changes smoothly reflect the state of the environment in real-time.

## Key Features

* **Ambient Theming Engine**: The background color smoothly transitions based on the selected temperature:
    * **Cold Blue** (<19°C)
    * **Twilight Dark** (24°C)
    * **Warm Purple** (28°C)
    * **Hot Crimson** (>28°C)
* **Smart Lighting System**: Interactive lighting cards for individual rooms, featuring independent state management and visual confirmation.
* **Security Interface**: Toggle seamlessly between "Home Mode" and "Away Mode" with dynamic icon and status color changes.
* **Master Power Control**: A central system switch that disables all subsystems like lights, climate, media and dims the entire application into a standby state.
* **Pylance Optimized**: The code is written with strict typing and utilizes the latest Flet API (0.80+), completely eliminating static type checker errors and deprecation warnings.

## Tech Stack

* **Language**: Python 3.8+
* **Framework**: Flet (v0.80.0+)
* **Key Concepts**: 
    * Global State Management
    * Asynchronous UI Updates
    * Implicit Animations & Transitions
    * Custom Component Generators

## How to Run

1.  **Install Flet**:
    ```bash
    pip install flet
    ```
2.  **Run the application**:
    ```bash
    python smarthome.py
    ```

## How to Use

1.  Drag the **Climate Slider** to see the background dynamically change color based on the heat level.
2.  Click the cards in the **Quick Lights** section to turn the lights on or off in specific rooms.
3.  Use the **Security Icon** to lock the house into "Away Mode".
4.  Toggle the **Master Control** switch to see the entire system go into a dark standby mode, locking all other controls.
