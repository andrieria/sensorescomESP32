
import pygame
from pygame.locals import *
import sys
import math

import serial
import re
# Define the COM port and baud rate
com_port = 'COM13'
baud_rate = 9600

# Initialize Pygame

ser = serial.Serial(com_port, baud_rate)
print(f"Reading from {com_port} at {baud_rate} baud...")
pygame.init()
xp,yp=0,0
# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (0, 0, 0)
CUBE_COLOR = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Cube")

# Define the vertices of the cube
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

# Define the edges that connect the vertices
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
]

# Initialize rotation angles
angle_x = 0
angle_y = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Clear the screen
    screen.fill(BG_COLOR)

    # Rotate the cube around the X and Y axes
    rotated_vertices = []
    for vertex in vertices:
        x, y, z = vertex

        # Rotate around X-axis
        new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
        new_z = y * math.sin(angle_x) + z * math.cos(angle_x)

        # Rotate around Y-axis
        new_x = x * math.cos(angle_y) + z * math.sin(angle_y)

        rotated_vertices.append([new_x, new_y, new_z])

    # Draw the edges
    for edge in edges:
        start = rotated_vertices[edge[0]]
        end = rotated_vertices[edge[1]]
        pygame.draw.line(screen, CUBE_COLOR, (start[0] * 100 + WIDTH // 2, start[1] * 100 + HEIGHT // 2),
                         (end[0] * 100 + WIDTH // 2, end[1] * 100 + HEIGHT // 2), 2)

    pygame.display.flip()
    data = ser.readline().decode('utf-8', errors='ignore').strip()
    datax=list(map(int,data.split()))
    xpos,ypos=datax[0],datax[1]
    if abs(xp-xpos)>=5:
        if xpos-xp>=0:
            angle_x+=0.05
        elif xpos-xp<=0:
            angle_x-=0.05
        xp=xpos
        print("X is changing")
    if abs(yp-ypos)>=5:
        if ypos-yp>=0:
            angle_y-=0.05
        elif ypos-yp<=0:
            angle_y+=0.05
        yp=ypos
        print("Y is changing")
    print(xpos,ypos)
    # Update rotation angles

    # Limit the frame rate
    pygame.time.delay(10)

# Quit Pygame
pygame.quit()
sys.exit()


'''import pygame
from pygame.locals import *
import sys
import math
import serial

# Define the COM port and baud rate
com_port = 'COM13'  # Substitua pela porta correta
baud_rate = 115200

# Initialize Pygame
ser = serial.Serial(com_port, baud_rate)
print(f"Reading from {com_port} at {baud_rate} baud...")
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (0, 0, 0)
CUBE_COLOR = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Cube")

# Define the vertices of the cube
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

# Define the edges that connect the vertices
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
]

# Initialize rotation angles
angle_x = 0.0
angle_y = 0.0
angle_z = 0.0

# Define a scale factor to control rotation speed
scale_factor = 0.01

def interpolate_angle(current_angle, target_angle, speed=0.1):
    return current_angle + (target_angle - current_angle) * speed

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Clear the screen
    screen.fill(BG_COLOR)

    # Read and parse the MPU6050 data
    data = ser.readline().decode('utf-8', errors='ignore').strip()
    try:
        datax = list(map(float, data.split()))
        if len(datax) == 3:
            # Scale the received data to control rotation speed
            target_angle_x = (datax[0] - 128) * scale_factor
            target_angle_y = (datax[1] - 128) * scale_factor
            target_angle_z = (datax[2] - 128) * scale_factor

            # Smoothly interpolate angles
            angle_x = interpolate_angle(angle_x, target_angle_x)
            angle_y = interpolate_angle(angle_y, target_angle_y)
            angle_z = interpolate_angle(angle_z, target_angle_z)
    except ValueError:
        continue

    rotated_vertices = []
    for vertex in vertices:
        x, y, z = vertex

        # Apply rotation around X-axis
        new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
        new_z = y * math.sin(angle_x) + z * math.cos(angle_x)

        # Apply rotation around Y-axis
        new_x = x * math.cos(angle_y) + new_z * math.sin(angle_y)
        new_z = -x * math.sin(angle_y) + new_z * math.cos(angle_y)

        # Apply rotation around Z-axis
        x = new_x * math.cos(angle_z) - new_y * math.sin(angle_z)
        y = new_x * math.sin(angle_z) + new_y * math.cos(angle_z)

        rotated_vertices.append([x, y, z])

    # Draw the edges
    for edge in edges:
        start = rotated_vertices[edge[0]]
        end = rotated_vertices[edge[1]]
        pygame.draw.line(screen, CUBE_COLOR, (start[0] * 100 + WIDTH // 2, start[1] * 100 + HEIGHT // 2),
                         (end[0] * 100 + WIDTH // 2, end[1] * 100 + HEIGHT // 2), 2)

    pygame.display.flip()
    pygame.time.delay(10)

# Quit Pygame
pygame.quit()
sys.exit()'''





'''import pygame
from pygame.locals import *
import sys
import math
import serial

# Define the COM port and baud rate
com_port = 'COM13'
baud_rate = 115200

# Initialize Pygame
ser = serial.Serial(com_port, baud_rate)
print(f"Reading from {com_port} at {baud_rate} baud...")
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (0, 0, 0)
CUBE_COLOR = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Cube")

# Define the vertices of the cube
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

# Define the edges that connect the vertices
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
]

# Initialize rotation angles
angle_x = 0.0
angle_y = 0.0
angle_z = 0.0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Clear the screen
    screen.fill(BG_COLOR)

    # Read and parse the MPU6050 data
    data = ser.readline().decode('utf-8', errors='ignore').strip()
    try:
        datax = list(map(float, data.split()))
        if len(datax) == 3:
            # Adjust the sensitivity if necessary
            angle_x += math.radians(datax[0] - 128) / 256.0
            angle_y += math.radians(datax[1] - 128) / 256.0
            angle_z += math.radians(datax[2] - 128) / 256.0
    except ValueError:
        continue

    rotated_vertices = []
    for vertex in vertices:
        x, y, z = vertex

        # Apply rotation around X-axis
        new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
        new_z = y * math.sin(angle_x) + z * math.cos(angle_x)

        # Apply rotation around Y-axis
        new_x = x * math.cos(angle_y) + new_z * math.sin(angle_y)
        z = -x * math.sin(angle_y) + new_z * math.cos(angle_y)

        # Apply rotation around Z-axis
        x = new_x * math.cos(angle_z) - new_y * math.sin(angle_z)
        y = new_x * math.sin(angle_z) + new_y * math.cos(angle_z)

        rotated_vertices.append([x, y, z])

    # Draw the edges
    for edge in edges:
        start = rotated_vertices[edge[0]]
        end = rotated_vertices[edge[1]]
        pygame.draw.line(screen, CUBE_COLOR, (start[0] * 100 + WIDTH // 2, start[1] * 100 + HEIGHT // 2),
                         (end[0] * 100 + WIDTH // 2, end[1] * 100 + HEIGHT // 2), 2)

    pygame.display.flip()
    pygame.time.delay(10)

# Quit Pygame
pygame.quit()
sys.exit()'''


'''import pygame
from pygame.locals import *
import sys
import math
import serial

# Define the COM port and baud rate
com_port = 'COM13'
baud_rate = 115200

# Initialize Pygame
ser = serial.Serial(com_port, baud_rate)
print(f"Reading from {com_port} at {baud_rate} baud...")
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (0, 0, 0)
CUBE_COLOR = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Cube")

# Define the vertices of the cube
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

# Define the edges that connect the vertices
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
]

# Initialize rotation angles
angle_x = 0.0
angle_y = 0.0
angle_z = 0.0

def interpolate_angle(current_angle, target_angle, speed=0.05):
    return current_angle + (target_angle - current_angle) * speed

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Clear the screen
    screen.fill(BG_COLOR)

    # Rotate the cube based on the latest MPU6050 data
    data = ser.readline().decode('utf-8', errors='ignore').strip()
    try:
        datax = list(map(float, data.split()))
        if len(datax) == 3:
            target_angle_x = math.radians(datax[0] - 128) / 256.0 * math.pi
            target_angle_y = math.radians(datax[1] - 128) / 256.0 * math.pi
            target_angle_z = math.radians(datax[2] - 128) / 256.0 * math.pi

            angle_x = interpolate_angle(angle_x, target_angle_x)
            angle_y = interpolate_angle(angle_y, target_angle_y)
            angle_z = interpolate_angle(angle_z, target_angle_z)
    except ValueError:
        continue

    rotated_vertices = []
    for vertex in vertices:
        x, y, z = vertex

        # Apply rotation around X-axis
        new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
        new_z = y * math.sin(angle_x) + z * math.cos(angle_x)

        # Apply rotation around Y-axis
        new_x = x * math.cos(angle_y) + new_z * math.sin(angle_y)
        new_z = -x * math.sin(angle_y) + new_z * math.cos(angle_y)

        # Apply rotation around Z-axis
        x = new_x * math.cos(angle_z) - new_y * math.sin(angle_z)
        y = new_x * math.sin(angle_z) + new_y * math.cos(angle_z)
        z = new_z

        rotated_vertices.append([x, y, z])

    # Draw the edges
    for edge in edges:
        start = rotated_vertices[edge[0]]
        end = rotated_vertices[edge[1]]
        pygame.draw.line(screen, CUBE_COLOR, (start[0] * 100 + WIDTH // 2, start[1] * 100 + HEIGHT // 2),
                         (end[0] * 100 + WIDTH // 2, end[1] * 100 + HEIGHT // 2), 2)

    pygame.display.flip()
    pygame.time.delay(10)

# Quit Pygame
pygame.quit()
sys.exit()'''



