from Core.app import *
from Core.constructs import MenuItem
import pygame

class MainMenu(App):
	def __init__(self, width=800, height=480):
		"""
		Initialize the main menu with a given width and height.
		"""
		super().__init__(width, height)
		self.title = "Main Menu"
		self.id = "main_menu"
		self.background_color = (0, 0, 0)
		self.menu_items: list[MenuItem] = []

		# Scrolling state
		self.scroll_x = 0
		self.velocity_x = 0
		self.friction = 0.92
		self.dragging = False
		self.last_mouse_x = 0
		self.mouse_down_pos = (0, 0)
		self.drag_threshold = 5

		self.font = pygame.font.Font(None, 24)

	def tick(self, events: list[pygame.event.Event]) -> pygame.Surface:
		"""
		Process events and return the surface for the main menu.
		"""
		self.surface.fill(self.background_color)

		for event in events:
			if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN) and event.button == 1:
				self.dragging = True
				self.last_mouse_x = event.pos[0]
				self.mouse_down_pos = event.pos
				self.velocity_x = 0  # stop momentum when starting new drag

			elif (event.type == pygame.MOUSEBUTTONUP or event.type == pygame.FINGERUP) and event.button == 1:
				self.dragging = False

				# Check if it's a click (not a drag)
				dx = abs(event.pos[0] - self.mouse_down_pos[0])
				dy = abs(event.pos[1] - self.mouse_down_pos[1])
				if dx < self.drag_threshold and dy < self.drag_threshold:
					new_app_id = self.check_click(event.pos)
					if new_app_id is not None:
						return self.surface, new_app_id

			elif (event.type == pygame.MOUSEMOTION or event.type == pygame.FINGERMOTION) and self.dragging:
				dx = event.pos[0] - self.last_mouse_x
				self.scroll_x += dx
				self.velocity_x = dx  # for momentum after release
				self.last_mouse_x = event.pos[0]

		# Apply momentum when not dragging
		if not self.dragging:
			# get the position of the furthest right icon
			max_x = (self.width // 2 + ((len(self.menu_items) * 150) // 2) + 50) + self.scroll_x
			min_x = (self.width // 2 - ((len(self.menu_items) * 150) // 2) - 100) + self.scroll_x
			# draw lines on max_x and min_x
			# pygame.draw.line(self.surface, (255, 0, 0), (max_x, 0), (max_x, self.height))
			# pygame.draw.line(self.surface, (255, 0, 0), (min_x, 0), (min_x, self.height))
			# check if the max_x is outside the screen and we are scrolling right
			
			offset_scroll = self.scroll_x - 25
			if max_x > self.width and min_x > 0:
				self.velocity_x -= 1
			# check if the min_x is outside the screen and we are scrolling left
			elif min_x < 0 and max_x < self.width:
				self.velocity_x += 1

			# if both max x and min x are inside the screen, add velocity towards the center
			elif min_x > 0 and max_x < self.width and abs(offset_scroll) > 2:
				if offset_scroll > 0:
					self.velocity_x -= offset_scroll / 150
				else:
					self.velocity_x -= offset_scroll / 150
			
			self.scroll_x += self.velocity_x
			self.velocity_x *= self.friction  # slow down

		# Draw app bar
		spacing = 150
		start_x = self.width // 2 - ((len(self.menu_items) * spacing) // 2) + self.scroll_x
		y = self.height // 2 - 50

		self.icon_rects = []  # store positions for click detection

		for index, item in enumerate(self.menu_items):
			x = start_x + index * spacing

			# Draw logo (100x100)
			self.surface.blit(item.logo_image, (x, y))

			# Draw name below
			text_surface = self.font.render(item.name, True, (255, 255, 255))
			text_rect = text_surface.get_rect(center=(x + 50, y + 100 + 14))
			self.surface.blit(text_surface, text_rect)

			# Save bounding box for clicks
			self.icon_rects.append((pygame.Rect(x, y, 100, 100), item.app_id))

		return self.surface, None

	def check_click(self, mouse_pos):
		"""
		Check if an app icon was clicked.
		"""
		for rect, app_id in self.icon_rects:
			if rect.collidepoint(mouse_pos):
				return app_id
		
		return None

	def add_menu_item(self, item: MenuItem):
		"""
		Add a menu item to the main menu.
		"""
		self.menu_items.append(item)
