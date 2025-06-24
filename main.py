import os
os.putenv('SDL_VIDEODRIVER', 'fbcon')  # Use framebuffer console
os.putenv('SDL_FBDEV', '/dev/fb0')     # Default framebuffer device
os.putenv('SDL_MOUSEDRV', 'TSLIB')     # Optional if using TSLib
os.putenv('SDL_MOUSEDEV', '/devices/platform/soc/fe205000.i2c/i2c-22/i2c-10/10-0038/input/input0')  # Replace with your touchscreen input

from Core.render import Render
from Core.mainmenu import MainMenu
from Apps.backup_camera import Backup_Camera
if __name__ == "__main__":
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