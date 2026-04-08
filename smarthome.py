import flet as ft

def main(page: ft.Page):
    # Window and Page Configuration
    page.title = "Ambient Smart Home"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505" 
    # Explicit Padding object to satisfy strict type checking
    page.padding = ft.Padding.all(30)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def cast_controls(items: list) -> list[ft.Control]:
        return items

    # --- Application State ---
    # Global state dictionary to track power, climate, security, and lighting
    state = {
        "power": True,
        "temp": 24.0,
        "playing": False,
        "security": "HOME",
        "lights": {"Living Room": True, "Kitchen": False, "Bedroom": True}
    }

    # --- Ambient Color Logic ---
    # Returns a hex color string based on temperature thresholds
    def get_ambient_color(temp: float) -> str:
        if temp < 19:
            return "#0D203A"      # Cold Deep Blue
        elif temp < 24:
            return "#1A1A2E"      # Neutral Twilight
        elif temp < 28:
            return "#331621"      # Warm Purple
        else:
            return "#4A0E17"      # Hot Crimson

    # --- UI Components ---
    power_status = ft.Text("SYSTEM ONLINE", size=12, weight=ft.FontWeight.BOLD, color="#34C759")
    temp_display = ft.Text("24°C", size=60, weight=ft.FontWeight.W_900, color="#FFFFFF")
    music_status = ft.Text("Paused", size=14, color="#8E8E93")
    security_text = ft.Text("HOME MODE", size=12, weight=ft.FontWeight.BOLD, color="#00D1FF")

    # Main Animated Container that changes color based on ambient state
    ambient_card = ft.Container(
        width=440,
        bgcolor=get_ambient_color(state["temp"]),
        border_radius=ft.BorderRadius.all(40), 
        padding=ft.Padding.all(35),            
        shadow=ft.BoxShadow(spread_radius=2, blur_radius=50, color="#60000000"),
        animate=ft.Animation(800, ft.AnimationCurve.EASE_OUT)
    )

    # --- Interactive Callbacks ---

    # Helper function to generate light control cards dynamically
    def create_light_card(name: str):
        is_on = state["lights"][name]
        
        # Define icons and labels for the card
        icon = ft.Icon(icon=ft.Icons.LIGHTBULB_OUTLINE, color="#000000" if is_on else "#8E8E93", size=24)
        label = ft.Text(name, size=12, weight=ft.FontWeight.BOLD, color="#000000" if is_on else "#8E8E93")
        
        # Internal click handler for individual lights
        def toggle_light(e):
            if not state["power"]: return
            
            state["lights"][name] = not state["lights"][name]
            new_on = state["lights"][name]
            
            # Visual feedback on toggle
            e.control.bgcolor = "#FFD700" if new_on else "#2C2C2E"
            icon.color = "#000000" if new_on else "#8E8E93"
            label.color = "#000000" if new_on else "#8E8E93"
            page.update()

        return ft.Container(
            content=ft.Column(controls=cast_controls([icon, label]), alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            bgcolor="#FFD700" if is_on else "#2C2C2E",
            width=110,
            height=85,
            border_radius=ft.BorderRadius.all(20),
            padding=ft.Padding.all(10),
            data=name, # Store reference name in the data property for safe retrieval
            ink=True,
            on_click=toggle_light,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        )

    # Pre-generate light cards and group them in a row
    light_cards = [create_light_card("Living Room"), create_light_card("Kitchen"), create_light_card("Bedroom")]
    
    lights_row = ft.Row(
        controls=cast_controls(light_cards), 
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # Handler for Security System Toggling
    def toggle_security(e):
        if not state["power"]: return
        
        if state["security"] == "HOME":
            state["security"] = "AWAY"
            security_text.value = "AWAY MODE"
            security_text.color = "#FF453A"
            security_btn.icon = ft.Icons.LOCK 
            security_btn.icon_color = "#FF453A"
        else:
            state["security"] = "HOME"
            security_text.value = "HOME MODE"
            security_text.color = "#00D1FF"
            security_btn.icon = ft.Icons.LOCK_OPEN 
            security_btn.icon_color = "#00D1FF"
            
        page.update()

    security_btn = ft.IconButton(
        icon=ft.Icons.LOCK_OPEN, 
        icon_color="#00D1FF",
        on_click=toggle_security
    )

    # Master Power Logic: Disables-Enables all subsystems
    def on_power_change(e):
        state["power"] = e.control.value
        
        if state["power"]:
            power_status.value = "SYSTEM ONLINE"
            power_status.color = "#34C759"
            ambient_card.bgcolor = get_ambient_color(state["temp"])
            temp_slider.disabled = False
            play_btn.disabled = False
            security_btn.disabled = False
            
            # Re-enable light card visuals based on stored state
            for card in light_cards:
                name = str(card.data) 
                is_on = state["lights"][name]
                card.bgcolor = "#FFD700" if is_on else "#2C2C2E"
        else:
            power_status.value = "SYSTEM OFFLINE"
            power_status.color = "#8E8E93"
            ambient_card.bgcolor = "#0A0A0A" # Dim the lights
            temp_slider.disabled = True
            play_btn.disabled = True
            security_btn.disabled = True
            
            # Auto pause media and dim lights on system shutdown
            if state["playing"]:
                toggle_music(None)
            for card in light_cards:
                card.bgcolor = "#121212"
                
        page.update()

    power_switch = ft.Switch(value=True, on_change=on_power_change, active_color="#34C759")

    # Update climate display and ambient background color
    def on_temp_change(e):
        val = e.control.value
        state["temp"] = val
        temp_display.value = f"{int(val)}°C"
        
        if state["power"]:
            ambient_card.bgcolor = get_ambient_color(val)
            
        page.update()

    temp_slider = ft.Slider(
        min=16, max=30, value=24, divisions=14,
        active_color="#FFFFFF",
        inactive_color="#40FFFFFF",
        on_change=on_temp_change
    )

    # Media playback logic
    def toggle_music(e):
        if not state["power"]: return 
            
        state["playing"] = not state["playing"]
        
        if state["playing"]:
            play_btn.icon = ft.Icons.PAUSE_CIRCLE_FILLED
            music_status.value = "Playing: Synthwave Radio"
            music_status.color = "#00D1FF"
        else:
            play_btn.icon = ft.Icons.PLAY_CIRCLE_FILLED
            music_status.value = "Paused"
            music_status.color = "#8E8E93"
            
        page.update()

    play_btn = ft.IconButton(
        icon=ft.Icons.PLAY_CIRCLE_FILLED, 
        icon_color="#FFFFFF",
        icon_size=40,
        on_click=toggle_music
    )

    # Media card assembly with semi-transparent background
    music_card = ft.Container(
        content=ft.Row(controls=cast_controls([
            ft.Icon(icon=ft.Icons.MUSIC_NOTE, color="#8E8E93"),
            ft.Column(controls=cast_controls([
                ft.Text("Living Room Audio", weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                music_status
            ]), spacing=2, expand=True),
            play_btn
        ])),
        bgcolor="#1A000000", 
        padding=ft.Padding.all(20),
        border_radius=ft.BorderRadius.all(20)
    )

    # --- Layout Assembly ---
    # Combine all segments into the primary animated ambient card
    ambient_card.content = ft.Column(
        controls=cast_controls([
            # Master Power Header
            ft.Row(controls=cast_controls([
                ft.Column(controls=cast_controls([
                    ft.Text("MASTER CONTROL", size=12, color="#8E8E93"),
                    power_status
                ]), spacing=2),
                power_switch
            ]), alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Container(height=25),
            
            # Security Status Panel
            ft.Row(controls=cast_controls([
                ft.Row(controls=cast_controls([
                    security_btn,
                    security_text
                ]), spacing=5)
            ]), alignment=ft.MainAxisAlignment.END),
            
            ft.Container(height=5),
            
            # Climate-Temperature Section
            ft.Column(controls=cast_controls([
                ft.Text("CLIMATE", size=12, color="#8E8E93"),
                temp_display,
                temp_slider,
                ft.Row(controls=cast_controls([
                    ft.Text("16°", size=12, color="#8E8E93"),
                    ft.Text("30°", size=12, color="#8E8E93")
                ]), alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]), spacing=5),
            
            ft.Container(height=30),
            
            # Smart Lighting Grid
            ft.Text("QUICK LIGHTS", size=12, color="#8E8E93"),
            ft.Container(height=5),
            lights_row,
            
            ft.Container(height=30),
            
            # Media Player Interface
            ft.Text("MEDIA", size=12, color="#8E8E93"),
            ft.Container(height=5),
            music_card
        ]),
        spacing=0
    )

    # Final Page injection
    page.add(ambient_card)

ft.run(main)