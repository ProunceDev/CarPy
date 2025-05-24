import pygame
from Core.app import App
import datetime

class Render:
	def __init__(self, width=800, height=480, title="Render"):
		self.width = width
		self.height = height
		self.title = title
		self.screen = None
		self.clock = None
		self.apps: list[App] = []
		self.active_app_id = "none"

	def initialize(self):
		pygame.init()
		self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
		pygame.display.set_caption(self.title)
		self.clock = pygame.time.Clock()

	def tick(self) -> bool:
		events = pygame.event.get()

		if self.active_app_id != "none":
			for app in self.apps:
				if app.id == self.active_app_id:
					surface, new_app_id = app.tick(events)
					if new_app_id != None:
						self.active_app_id = new_app_id
					self.screen.blit(surface, (0, 0))
					break

		font = pygame.font.Font(None, 36)
		current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
		text = font.render(current_time, True, (255, 255, 255))
		text_rect = text.get_rect(center=(self.width // 2, self.height - 30))
		self.screen.blit(text, text_rect)

		# if the app is not the main menu, draw the back button
		if self.active_app_id != "main_menu":
			# Button size and position
			button_width, button_height = 100, 40
			padding = 10
			x = self.width - button_width - padding
			y = padding

			# Draw button background
			pygame.draw.rect(self.screen, (50, 50, 50), (x, y, button_width, button_height), border_radius=8)

			# Draw text
			back_text = font.render("Back", True, (255, 255, 255))
			back_text_rect = back_text.get_rect(center=(x + button_width // 2, y + button_height // 2))
			self.screen.blit(back_text, back_text_rect)


		
		for event in events:
			if event.type == pygame.QUIT:
				return False
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if self.active_app_id != "main_menu":
					# Updated back button rect (matches new size and position)
					button_width, button_height = 100, 40
					padding = 10
					x = self.width - button_width - padding
					y = padding
					back_button_rect = pygame.Rect(x, y, button_width, button_height)
					
					if back_button_rect.collidepoint(event.pos):
						self.active_app_id = "main_menu"
						break


		pygame.display.flip()
		if self.clock:
			self.clock.tick(60)

		return True

	def add_app(self, app):
		"""
		Add an application to the render loop.
		"""
		self.apps.append(app)

	def set_active_app(self, app_id):
		"""
		Set the active application by its ID.
		"""
		self.active_app_id = app_id

	def quit(self):
		pygame.quit()