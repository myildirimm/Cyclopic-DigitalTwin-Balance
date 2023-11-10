import pygame
import math

# Initialize Pygame
pygame.init()



# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tire with Oscillating Rim and L-Shaft')

# Colors
BLACK = (0, 0, 0)
GREY = (192, 192, 192)
RED = (155, 100, 50)
YELLOW = (100, 100, 100)

# Tire properties
tire_pos_1 = (200, 400)
tire_pos_2 = (600, 400)
tire_radius = 100

# Rim properties
rim_radius = 85
rim_thickness = 15
rim_angle_1 = 0  # Starting angle
rim_angle_2 = 20  # Starting angle
rotation_speed_1 = 1  # Degrees per frame
rotation_speed_2 = 0.5  # Degrees per frame

# Load the rim image
rim_image_path = 'rim_1.png'  # Replace with your image file path
rim_image = pygame.image.load(rim_image_path)
rim_image = pygame.transform.scale(rim_image, (2 * rim_radius, 2 * rim_radius))

# Shaft properties
shaft_length = 120
shaft_width = 25

#base properties
base_length = 400
base_width = 25

# Rotation state
rotate_clockwise = True
max_rotation = 90

# Game loop flag
running = True

# Clock to control frame rate
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen
    screen.fill((255, 255, 255))

    # Draw the tire (outer circle)
    pygame.draw.circle(screen, BLACK, tire_pos_1, tire_radius, 5)
    pygame.draw.circle(screen, BLACK, tire_pos_2, tire_radius, 5)

    # Rotate the rim
    if rotate_clockwise:
        rim_angle_1 += rotation_speed_1
        if rim_angle_1 >= max_rotation:
            rotate_clockwise = False
    else:
        rim_angle_1 -= rotation_speed_1
        if rim_angle_1 <= -max_rotation:
            rotate_clockwise = True

        # Rotate the rim
    if rotate_clockwise:
        rim_angle_2 += rotation_speed_2
        if rim_angle_2 >= max_rotation:
            rotate_clockwise = False
    else:
        rim_angle_2 -= rotation_speed_2
        if rim_angle_2 <= -max_rotation:
            rotate_clockwise = True

    # Create a surface for the rim to rotate
    rim_surface_1 = pygame.Surface((2 * rim_radius, 2 * rim_radius), pygame.SRCALPHA)
    pygame.draw.circle(rim_surface_1, GREY, (rim_radius, rim_radius), rim_radius, rim_thickness)

    # Rotate the rim
    rotated_rim_1 = pygame.transform.rotate(rim_image, rim_angle_1)
    rotated_rim_2 = pygame.transform.rotate(rim_image, rim_angle_2)

    # Get the new rect for the rotated rim to blit at the correct position
    rotated_rect_1 = rotated_rim_1.get_rect(center=tire_pos_1)

    # Get the new rect for the rotated rim to blit at the correct position
    rotated_rect_2 = rotated_rim_2.get_rect(center=tire_pos_2)

    # Blit the rotated rim onto the screen
    screen.blit(rotated_rim_1, rotated_rect_1.topleft)
    screen.blit(rotated_rim_2, rotated_rect_2.topleft)


    shaft_base_pos_1 = (tire_pos_1[0] - (math.cos(math.radians((rim_angle_1))) * rim_radius)+10, tire_pos_1[1] + (math.sin(math.radians((rim_angle_1))) * rim_radius))
    shaft_base_pos_2 = (tire_pos_2[0] - (math.cos(math.radians((rim_angle_2))) * rim_radius)+10, tire_pos_2[1] + (math.sin(math.radians((rim_angle_2))) * rim_radius))

    shaft_end_pos_1 = (shaft_base_pos_1[0],shaft_base_pos_1[1]- shaft_length)
    shaft_end_pos_2 = (shaft_base_pos_2[0],shaft_base_pos_2[1]- shaft_length)

    # Draw the shaft
    shaft_rect_1 = pygame.Rect(shaft_base_pos_1[0] - shaft_width // 2,
                             shaft_base_pos_1[1] - shaft_length,
                             shaft_width,
                             shaft_length)
    shaft_rect_2 = pygame.Rect(shaft_base_pos_2[0] - shaft_width // 2,
                             shaft_base_pos_2[1] - shaft_length,
                             shaft_width,
                             shaft_length)
    base_rect = pygame.Rect(shaft_end_pos_1[0],
                             shaft_end_pos_1[1] - base_width,
                             base_length,
                             base_width )
    pygame.draw.line(screen,YELLOW, (shaft_end_pos_1[0]- shaft_width/2,
                             shaft_end_pos_1[1]-base_width/2 ), (shaft_base_pos_2[0]+shaft_width/2,shaft_base_pos_2[1]- shaft_length-base_width/2),20)
    pygame.draw.rect(screen, RED, shaft_rect_1)
    pygame.draw.rect(screen, RED, shaft_rect_2)
    #pygame.draw.rect(screen, YELLOW, base_rect)
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(10)

# Quit Pygame
pygame.quit()
