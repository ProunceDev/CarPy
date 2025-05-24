from Core.app import *
from Core.constructs import MenuItem
import cv2

class Backup_Camera(App):
	def __init__(self, width=800, height=480):
		"""
		Initialize the app with a given width and height.
		"""
		super().__init__(width, height)
		self.title = "Backup Camera"
		self.id = "backup_camera"
		self.background_color = (0, 0, 0)
		self.menu_items: list[MenuItem] = []

		self.camera = cv2.VideoCapture(0)
		if not self.camera.isOpened():
			print("Error: Camera not found.")
			self.camera = None

	def tick(self, events: list[pygame.event.Event]) -> pygame.Surface:
		"""
		Process events and return the surface for the main menu.
		"""
		if self.camera is not None:
			# Read a frame from the camera
			ret, frame = self.camera.read()
			if ret:
				# Convert the frame to RGB format
				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				# Convert the frame to a pygame surface
				frame = cv2.resize(frame, (self.width, self.height))
				frame = pygame.surfarray.make_surface(frame)
				self.surface.blit(frame, (0, 0))
			else:
				self.surface.fill(self.background_color)
				font = pygame.font.Font(None, 36)
				text = font.render("Error: could not read from camera", True, (255, 0, 0))
				text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
				self.surface.blit(text, text_rect)
		else:
			self.surface.fill(self.background_color)
			font = pygame.font.Font(None, 36)
			text = font.render("Camera not found", True, (255, 0, 0))
			text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
			self.surface.blit(text, text_rect)

		return self.surface, None
	
	def get_menu_item(self):
		"""
		Get the menu item for the backup camera.
		"""
		# load the image to a surface from assets/backup_camera.png
		logo_image = pygame.image.load("Assets/backup_camera.png").convert_alpha()
		return MenuItem(self.title, self.id, logo_image)