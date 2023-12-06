import random
# Colors
BLACK = (0, 0, 0)
GREY = (192, 192, 192)
YELLOW = (255, 255, 0)  # Full METALLIC, full green, no blue
METALLIC = (192, 192, 224)  # A light grey-blue that might suggest a metallic sheen
RED = (100, 100, 100)
BLUE = (0, 0, 255)  # Full blue color


# Tire properties
tire_pos_1 = (200, 400)
tire_pos_2 = (600, 400)
tire_radius = 100

# Rim properties
rim_radius = 85
rim_thickness = 15
# Rim properties with random starting angles
rim_angle_1 = random.uniform(0, 90)  # Random starting angle for rim 1
rim_angle_2 = random.uniform(0, 90)  # Random starting angle for rim 2
rotation_speed_1 = 1  # Degrees per frame
rotation_speed_2 = 0.5  # Degrees per frame


# Shaft properties
shaft_length = 120
shaft_width = 25

#base properties
base_length = 400
base_width = 25