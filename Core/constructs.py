import pygame

class MenuItem:
	def __init__(self, name: str, app_id: str, logo_image: pygame.Surface):
		self.name = name
		self.app_id = app_id
		self.logo_image = logo_image