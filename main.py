import pygame
import math
import random
from vehicle_config import *
from DQN import DQAgent
from rl_agent import RLAgent

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Cyclopic Balance')

# Load the rim image
rim_image_path = 'rim_1.png'  # Replace with your image file path
rim_image = pygame.image.load(rim_image_path)
rim_image = pygame.transform.scale(rim_image, (2 * rim_radius, 2 * rim_radius))

# Load the rim image
tire_image_path = 'tire_1.png'  # Replace with your image file path
tire_image = pygame.image.load(tire_image_path)
tire_image = pygame.transform.scale(tire_image, (2 * tire_radius, 2 * tire_radius))

# Define the size and position of the yellow box
box_height = 250  # The height of the box
box_width = base_length/2  # The width of the box (same as base length)

# Define the center of gravity properties
cog_length = 50  # Length of the CoG vector
cog_shift_per_degree = 1  # How many pixels the CoG shifts per degree of wheel angle difference
arrowhead_size = 8  # The size of the arrowhead

# Define the acceleration range (example values, adjust as needed)
min_acceleration = - 5  # minimum acceleration
max_acceleration =   5   # maximum acceleration

# Acceleration arrow properties
arrow_length_per_unit = 10  # Length of the arrow per unit of acceleration
arrow_width = 5             # Width of the arrow line
arrowhead_size = 10         # Size of the arrowhead


# Clock to control frame rate
clock = pygame.time.Clock()

def calculate_angle(p1, p2):
    """Calculate the angle between two points"""
    return math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))

 # Randomize the box's x-position on the platform
platform_left_edge = 100
platform_right_edge = 600
box_width_half = box_width / 2
random_x = random.randint(platform_left_edge + box_width_half, platform_right_edge - box_width_half)

# Randomly select an acceleration value within the defined range
acceleration = random.uniform(min_acceleration, max_acceleration)

# Resultant vector properties
resultant_arrow_width = 5
resultant_arrowhead_size = 10

# Rotation state
rotate_clockwise_1 = True
rotate_clockwise_2 = True
max_rotation = 90

# Game loop flag
running = True

# Main game loop
agent = RLAgent()
# =====================================================================
# the car class for the DQ
class Cyclopic:

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rim_angle_1 += rotation_speed_1
            elif event.key == pygame.K_RIGHT:
                rim_angle_1 -= rotation_speed_1
            elif event.key == pygame.K_a:
                rim_angle_2 += rotation_speed_2
            elif event.key == pygame.K_d:
                rim_angle_2 -= rotation_speed_2


        # Update environment state
        state = {
            'acceleration': acceleration,
            'rim_angle_1': rim_angle_1,
            'rim_angle_2': rim_angle_2,
            'resultant_angle': calculate_resultant_angle()  # Placeholder function
        }


        # Get action from RL agent
        action = agent.choose_action(state)

        # Apply the action to the rims (placeholder logic)
        # action could be a tuple like (change_in_rim_angle_1, change_in_rim_angle_2)
        rim_angle_1 += action[0]
        rim_angle_2 += action[1]

        # Calculate reward (placeholder logic)
        reward = calculate_reward(state)  # Function to calculate reward based on the state

        next_state, reward, done = env.step(action)
        agent.learn(state, action, reward, next_state)

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

        # Create a surface for the rim to rotate
        rim_surface_1 = pygame.Surface((2 * rim_radius, 2 * rim_radius), pygame.SRCALPHA)
        pygame.draw.circle(rim_surface_1, GREY, (rim_radius, rim_radius), rim_radius, rim_thickness)

        # Rotate the rim
        rotated_rim_1 = pygame.transform.rotate(rim_image, rim_angle_1)
        # Get the new rect for the rotated rim to blit at the correct position
        rotated_rim_rect_1 = rotated_rim_1.get_rect(center=tire_pos_1)

        rotated_rim_2 = pygame.transform.rotate(rim_image, rim_angle_2)
        # Get the new rect for the rotated rim to blit at the correct position
        rotated_rim_rect_2 = rotated_rim_2.get_rect(center=tire_pos_2)
        # Blit the rotated rim onto the screen
        screen.blit(rotated_rim_1, rotated_rim_rect_1.topleft)
        screen.blit(rotated_rim_2, rotated_rim_rect_2.topleft)

        pygame.draw.line(screen,METALLIC, (shaft_end_pos_1[0]- shaft_width/2,
                                shaft_end_pos_1[1]-base_width/2 ), (shaft_base_pos_2[0]+shaft_width/2,shaft_base_pos_2[1]- shaft_length-base_width/2),20)
        
        # Calculate the angle of the base plate
        base_plate_angle = calculate_angle(shaft_end_pos_1, shaft_end_pos_2)

        # Create a surface for the box
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)  # Use SRCALPHA for transparency
        box_surface.fill(YELLOW)  # Fill the surface with the box color

        # Rotate the box surface
        rotated_box = pygame.transform.rotate(box_surface, - base_plate_angle)  # Negative angle for correct rotation direction

        # Calculate the new position for the rotated box
        box_center_x = random_x # (shaft_end_pos_1[0] + shaft_end_pos_2[0]) / 2

        # Find the bottom of the rotated box
        rotated_box_rect = rotated_box.get_rect(center=(box_center_x, shaft_end_pos_1[1] - base_width))
        box_bottom_y = rotated_box_rect.bottom

        # Adjust y-position so the bottom of the box aligns with the top of the platform
        box_center_y = shaft_end_pos_1[1] - base_width - (rotated_box.get_height() / 2)

        # Update the rect for proper positioning
        rotated_box_rect = rotated_box.get_rect(center=(box_center_x, box_center_y))

        rotated_box_rect = rotated_box.get_rect(center=(box_center_x, box_center_y))

        # Blit the rotated box onto the screen
        screen.blit(rotated_box, rotated_box_rect.topleft)   
        box_position_y = shaft_end_pos_1[1] - box_height

        # Calculate the angle difference between the two wheels
        angle_difference = abs(rim_angle_1 - rim_angle_2)
        # Determine the direction of the CoG shift
        cog_shift_direction = 1 if rim_angle_1 < rim_angle_2 else -1
        # Calculate the CoG shift
        cog_shift = angle_difference * cog_shift_per_degree * cog_shift_direction

        cog_arrow_base_x = box_center_x  # CoG arrow base is at the mid-point of the box
        cog_arrow_base_y = box_position_y + box_height // 2  # CoG arrow base is at the vertical center of the box

        # Calculate the CoG arrow tip position
        cog_arrow_tip_x = cog_arrow_base_x + cog_shift
        cog_arrow_tip_y = cog_arrow_base_y + cog_length  # The arrow points downwards

        # Draw the CoG arrow
        pygame.draw.line(screen, RED, (cog_arrow_base_x, cog_arrow_base_y), (cog_arrow_tip_x, cog_arrow_tip_y), 5)

        # Draw the CoG arrowhead
        cog_arrow_tip = (cog_arrow_tip_x, cog_arrow_tip_y)
        cog_arrow_left = (cog_arrow_tip_x - arrowhead_size, cog_arrow_tip_y - arrowhead_size)
        cog_arrow_right = (cog_arrow_tip_x + arrowhead_size, cog_arrow_tip_y - arrowhead_size)
        pygame.draw.polygon(screen, RED, [cog_arrow_tip, cog_arrow_left, cog_arrow_right])

        # Acceleration Arrow
        # Determine the direction of movement
        direction = -1 if acceleration < 0 else 1  # Left for negative, right for positive

        # Calculate the acceleration arrow length
        accel_arrow_length = abs(acceleration) * arrow_length_per_unit

        # Set the start point of the acceleration arrow (same as the CoG arrow base)
        accel_arrow_start_x = cog_arrow_base_x
        accel_arrow_start_y = cog_arrow_base_y

        # Calculate the end point of the acceleration arrow
        accel_arrow_end_x = accel_arrow_start_x + (direction * accel_arrow_length)
        accel_arrow_end_y = accel_arrow_start_y

        # Draw the acceleration arrow
        pygame.draw.line(screen, RED, (accel_arrow_start_x, accel_arrow_start_y), (accel_arrow_end_x, accel_arrow_end_y), arrow_width)

        # Draw the acceleration arrowhead
        accel_arrowhead_left = (accel_arrow_end_x - direction * arrowhead_size, accel_arrow_end_y - arrowhead_size)
        accel_arrowhead_right = (accel_arrow_end_x - direction * arrowhead_size, accel_arrow_end_y + arrowhead_size)
        pygame.draw.polygon(screen, RED, [(accel_arrow_end_x, accel_arrow_end_y), accel_arrowhead_left, accel_arrowhead_right])

        # Resultant Arrow
        # Calculate the resultant arrow's end point
        resultant_arrow_end_x = cog_arrow_base_x + (cog_arrow_tip_x - cog_arrow_base_x) + (accel_arrow_end_x - cog_arrow_base_x)
        resultant_arrow_end_y = cog_arrow_base_y + (cog_arrow_tip_y - cog_arrow_base_y) + (accel_arrow_end_y - cog_arrow_base_y)

        # Draw the resultant arrow
        pygame.draw.line(screen, BLUE, (cog_arrow_base_x, cog_arrow_base_y), (resultant_arrow_end_x, resultant_arrow_end_y), resultant_arrow_width)

        # Draw the resultant arrowhead
        resultant_arrowhead_left = (resultant_arrow_end_x - resultant_arrowhead_size, resultant_arrow_end_y - resultant_arrowhead_size)
        resultant_arrowhead_right = (resultant_arrow_end_x - resultant_arrowhead_size, resultant_arrow_end_y + resultant_arrowhead_size)
        pygame.draw.polygon(screen, BLUE, [(resultant_arrow_end_x, resultant_arrow_end_y), resultant_arrowhead_left, resultant_arrowhead_right])

        pygame.display.flip()

        # Cap the frame rate
        clock.tick(10)

