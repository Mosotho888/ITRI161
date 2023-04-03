import pygame
import random
import math

# Define some constants
WIDTH, HEIGHT = 800, 600
MAX_VELOCITY = 5
MAX_FORCE = 0.1
ALIGNMENT_RADIUS = 50
COHESION_RADIUS = 100
SEPARATION_RADIUS = 50
OBSTACLE_RADIUS = 20
BORDER_SIZE = 100

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define some helper functions
def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def limit_vector(vector, limit):
    magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
    if magnitude > limit:
        return [vector[0] / magnitude * limit, vector[1] / magnitude * limit]
    else:
        return vector

class Boid:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def update(self, boids, obstacles):
        alignment = [0, 0]
        cohesion = [0, 0]
        separation = [0, 0]
        count_alignment = 0
        count_cohesion = 0
        count_separation = 0

        for boid in boids:
            distance_to_boid = distance(self.position, boid.position)
            if 0 < distance_to_boid < ALIGNMENT_RADIUS:
                alignment[0] += boid.velocity[0]
                alignment[1] += boid.velocity[1]
                count_alignment += 1
            if 0 < distance_to_boid < COHESION_RADIUS:
                cohesion[0] += boid.position[0]
                cohesion[1] += boid.position[1]
                count_cohesion += 1
            if 0 < distance_to_boid < SEPARATION_RADIUS:
                separation_vector = [self.position[0] - boid.position[0], self.position[1] - boid.position[1]]
                separation_vector = limit_vector(separation_vector, MAX_FORCE)
                separation[0] += separation_vector[0]
                separation[1] += separation_vector[1]
                count_separation += 1

        if count_alignment > 0:
            alignment[0] /= count_alignment
            alignment[1] /= count_alignment
            alignment = limit_vector(alignment, MAX_VELOCITY)
            self.velocity[0] += alignment[0]
            self.velocity[1] += alignment[1]

        if count_cohesion > 0:
            cohesion[0] /= count_cohesion
            cohesion[1] /= count_cohesion
            cohesion_vector = [cohesion[0] - self.position[0], cohesion[1] - self.position[1]]
            if cohesion_vector == [0, 0]:
                # if boid is at the same position as the current boid, give a random cohesion vector
                cohesion_vector = [random.uniform(-1, 1), random.uniform(-1, 1)]
            else:
                # normalize the cohesion vector and multiply it by the maximum velocity
                cohesion_vector = limit_vector(cohesion_vector, MAX_FORCE)
            self.velocity[0] += cohesion_vector[0]
            self.velocity[1] += cohesion_vector[1]

        if count_separation > 0:
            separation[0] /= count_separation
            separation[1] /= count_separation
            separation = limit_vector(separation, MAX_VELOCITY)
            self.velocity[0] += separation[0]
            self.velocity[1] += separation[1]

        self.velocity = limit_vector(self.velocity, MAX_VELOCITY * 0.1)
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Avoid obstacles
        for obstacle in obstacles:
            distance_to_obstacle = distance(self.position, obstacle)
            if distance_to_obstacle < OBSTACLE_RADIUS:
                avoidance_vector = [self.position[0] - obstacle[0], self.position[1] - obstacle[1]]
                avoidance_vector = limit_vector(avoidance_vector, MAX_FORCE)
                self.velocity[0] += avoidance_vector[0]
                self.velocity[1] += avoidance_vector[1]

        if self.position[0] < BORDER_SIZE:
            self.velocity[0] += MAX_FORCE
        elif self.position[0] > WIDTH - BORDER_SIZE:
            self.velocity[0] -= MAX_FORCE
        if self.position[1] < BORDER_SIZE:
            self.velocity[1] += MAX_FORCE
        elif self.position[1] > HEIGHT - BORDER_SIZE:
            self.velocity[1] -= MAX_FORCE

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Wrap position around screen boundaries
        if self.position[0] < 0:
            self.position[0] = WIDTH
        elif self.position[0] > WIDTH:
            self.position[0] %= WIDTH
        if self.position[1] < 0:
            self.position[1] = HEIGHT
        elif self.position[1] > HEIGHT:
            self.position[1] %= HEIGHT


    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position[0]), int(self.position[1])), 5)

boids = []
obstacles = []
n = 50
running = True

for i in range(n):
         boids.append(Boid([random.uniform(0, WIDTH), random.uniform(0, HEIGHT)], [random.uniform(-1, 1), random.uniform(-1, 1)]))


while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                boids.append(Boid(list(event.pos), [random.uniform(-1, 1), random.uniform(-1, 1)]))
            elif event.button == 3: # right click
                obstacles.append(event.pos)

    # Update the boids
    for boid in boids:
        boid.update(boids, obstacles)

    # Draw the boids and obstacles
    screen.fill((0, 0, 0))
    for boid in boids:
        boid.draw()
    for obstacle in obstacles:
        pygame.draw.circle(screen, (255, 0, 0), obstacle, OBSTACLE_RADIUS, 1)
    pygame.display.flip()

pygame.quit()
