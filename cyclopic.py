import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Cyclopic Balance')

# Colors
BLACK = (0, 0, 0)
GREY = (192, 192, 192)
YELLOW = (255, 255, 0)  # Full METALLIC, full green, no blue
METALLIC = (192, 192, 224)  # A light grey-blue that might suggest a metallic sheen
RED = (100, 100, 100)

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


# Shaft properties
shaft_length = 120
shaft_width = 25

#base properties
base_length = 400
base_width = 25

# Rotation state
rotate_clockwise = True
max_rotation = 90

# Load the rim image
rim_image_path = 'rim_1.png'  # Replace with your image file path
rim_image = pygame.image.load(rim_image_path)
rim_image = pygame.transform.scale(rim_image, (2 * rim_radius, 2 * rim_radius))

# Load the rim image
tire_image_path = 'tire_1.png'  # Replace with your image file path
tire_image = pygame.image.load(tire_image_path)
tire_image = pygame.transform.scale(tire_image, (2 * tire_radius, 2 * tire_radius))

# Define the size and position of the yellow box
box_height = 150  # The height of the box
box_width = base_length/2  # The width of the box (same as base length)

# Define the center of gravity properties
cog_length = 50  # Length of the CoG vector
cog_shift_per_degree = 1  # How many pixels the CoG shifts per degree of wheel angle difference
arrowhead_size = 8  # The size of the arrowhead


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
    pygame.draw.rect(screen, METALLIC, shaft_rect_1)
    pygame.draw.rect(screen, METALLIC, shaft_rect_2)
    
    base_rect = pygame.Rect(shaft_end_pos_1[0],
                             shaft_end_pos_1[1] - base_width,
                             base_length,
                             base_width )
    



    # Blit the tire image onto the screen at the tire positions
    tire_rect_1 = tire_image.get_rect(center=tire_pos_1)
    tire_rect_2 = tire_image.get_rect(center=tire_pos_2)
    screen.blit(tire_image, tire_rect_1.topleft)
    screen.blit(tire_image, tire_rect_2.topleft)

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

    pygame.draw.line(screen,METALLIC, (shaft_end_pos_1[0]- shaft_width/2,
                             shaft_end_pos_1[1]-base_width/2 ), (shaft_base_pos_2[0]+shaft_width/2,shaft_base_pos_2[1]- shaft_length-base_width/2),20)
    
    # Position the box in the middle of the base
    mid_base_x = (shaft_base_pos_1[0] + shaft_base_pos_2[0]) / 2
    box_position_x = mid_base_x - (box_width // 2)
    box_position_y = shaft_end_pos_1[1] - base_width - box_height
    box_rect = pygame.Rect(box_position_x, box_position_y, box_width, box_height)
    pygame.draw.rect(screen, YELLOW, box_rect)
    

    # Blit the rotated rim onto the screen
    screen.blit(rotated_rim_1, rotated_rect_1.topleft)
    screen.blit(rotated_rim_2, rotated_rect_2.topleft)

    # Calculate the angle difference between the two wheels
    angle_difference = abs(rim_angle_1 - rim_angle_2)
    # Determine the direction of the CoG shift
    cog_shift_direction = 1 if rim_angle_1 > rim_angle_2 else -1
    # Calculate the CoG shift
    cog_shift = angle_difference * cog_shift_per_degree * cog_shift_direction
    # Calculate the CoG position
    arrow_base_x = mid_base_x  # Arrow base is at the mid-point of the box
    arrow_base_y = box_position_y + box_height // 2  # Arrow base is at the vertical center of the box

    # Calculate the position of the arrow tip based on the CoG shift
    arrow_tip_x = arrow_base_x + cog_shift
    arrow_tip_y = arrow_base_y + cog_length  # The arrow points downwards

    # Draw the CoG vector as a line from the base to the tip
    pygame.draw.line(screen, RED, (arrow_base_x, arrow_base_y), (arrow_tip_x, arrow_tip_y), 5)

    # Calculate the arrowhead points for the CoG vector
    # The arrowhead will be drawn at the tip
    arrow_tip = (arrow_tip_x, arrow_tip_y)
    arrow_left = (arrow_tip_x - arrowhead_size, arrow_tip_y - arrowhead_size)
    arrow_right = (arrow_tip_x + arrowhead_size, arrow_tip_y - arrowhead_size)
    pygame.draw.polygon(screen, RED, [arrow_tip, arrow_left, arrow_right])


    #pygame.draw.rect(screen, YELLOW, base_rect)
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(10)

# Quit Pygame
pygame.quit()
