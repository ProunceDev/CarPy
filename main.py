import os
import threading
import asyncio
from evdev import InputDevice, ecodes, UInput

# Set SDL video driver before importing your app modules
os.putenv('SDL_VIDEODRIVER', 'kmsdrm')

from Core.render import Render
from Core.mainmenu import MainMenu
from Apps.backup_camera import Backup_Camera

# Touchscreen config - adjust device and screen size if needed
TOUCH_DEV = '/dev/input/event5'
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

# Clamp helper
def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

# State variables for touch position and touch status
abs_x = 0
abs_y = 0
touch_down = False

# Create uinput device to emit mouse events
ui = UInput()

async def input_loop():
    global abs_x, abs_y, touch_down
    device = InputDevice(TOUCH_DEV)
    print(f"Listening on {TOUCH_DEV} for touch input...")

    async for event in device.async_read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:
                abs_x = clamp(event.value, 0, SCREEN_WIDTH)
            elif event.code == ecodes.ABS_Y:
                abs_y = clamp(event.value, 0, SCREEN_HEIGHT)

            # If touch is down, send relative movement based on deltas
            if touch_down:
                # For simplicity send absolute coords as relative movements (can improve)
                ui.write(ecodes.EV_REL, ecodes.REL_X, abs_x)
                ui.write(ecodes.EV_REL, ecodes.REL_Y, abs_y)
                ui.syn()

        elif event.type == ecodes.EV_KEY and event.code == ecodes.BTN_TOUCH:
            if event.value == 1:
                touch_down = True
                ui.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 1)
                ui.syn()
            elif event.value == 0:
                touch_down = False
                ui.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 0)
                ui.syn()

def start_input_loop():
    asyncio.run(input_loop())

if __name__ == "__main__":
    # Start touchscreen input translator in a background thread
    threading.Thread(target=start_input_loop, daemon=True).start()

    # Your existing app code
    render = Render(width=800, height=480, title="CarPy")
    render.initialize()
    main_menu = MainMenu()
    backup_camera = Backup_Camera()
    main_menu.add_menu_item(backup_camera.get_menu_item())
    render.add_app(main_menu)
    render.add_app(backup_camera)
    render.set_active_app("main_menu")

    # Main loop
    running = True
    while running:
        running = render.tick()
    render.quit()
