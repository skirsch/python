import pygame
import time

def create_blinking_square(size):
  """
  Creates a blinking white square with brightness control and exit functionality.

  Args:
    size: Size of the window (width, height).
  """

  pygame.init()
  screen = pygame.display.set_mode(size)
  pygame.display.set_caption("Blinking Square")

  black = (0, 0, 0)
  brightness = 255  # Initial brightness
  blinking = True

  square_size = 50  # Adjust square size as needed

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          brightness = min(brightness + 10, 255)
        elif event.key == pygame.K_RIGHT:
          brightness = min(brightness + 1, 255)
        elif event.key == pygame.K_DOWN:
          brightness = max(brightness - 10, 0)
        elif event.key == pygame.K_LEFT:
          brightness = max(brightness - 1, 0)
        elif event.key == pygame.K_SPACE:
          running = False

    screen.fill(black)

    square_x = (size[0] - square_size) // 2
    square_y = (size[1] - square_size) // 2

    if blinking:
      pygame.draw.rect(screen, (brightness, brightness, brightness), (square_x, square_y, square_size, square_size))

    # Display brightness level
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Brightness: {brightness}", True, (255, 255, 255))
    text_rect = text.get_rect(center=(size[0] // 2, size[1] - 20))
    screen.blit(text, text_rect)

    pygame.display.flip()
    time.sleep(0.5)  # Adjust blink rate here
    blinking = not blinking

  pygame.quit()

# Example usage:
create_blinking_square((1920, 1080))

## this creates a new window and pops it up.
# Cursor keys to change brightness
# Space key terminates it


