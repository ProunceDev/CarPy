import pygame

class App:
	def __init__(self, width=800, height=480):
		"""
		Initialize the application with a given width and height.
		"""
		self.width = width
		self.height = height
		self.surface = pygame.Surface((self.width, self.height))
		self.id = "none"

	def tick(self, events: list[pygame.event.Event]) -> pygame.Surface:
		"""
		Process events and return the surface.
		"""

		# Placeholder: fill the screen with a color (black)

		self.surface.fill((0, 0, 0))
		return self.surface