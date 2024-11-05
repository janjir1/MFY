import pygame
import math

# Constants
G = 6.67430e-11  # Gravitational constant
WIDTH, HEIGHT = 800, 600  # Screen dimensions
FPS = 60  # Frames per second

# Initial scale factor for visibility; can be changed with the slider
SCALE = 1e6 
SPEED = 1e4

class Body:
    def __init__(self, mass, position, velocity, color, radius):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.color = color
        self.radius = radius

    def calculate_gravitational_force(self, other):
        # Calculate the distance between the two bodies
        dx = other.position[0] - self.position[0]
        dy = other.position[1] - self.position[1]
        distance = math.sqrt(dx**2 + dy**2)

        # Avoid division by zero or extremely small distances
        if distance < 1:
            distance = 1

        # Calculate force magnitude
        force_magnitude = G * self.mass * other.mass / distance**2

        # Calculate force components
        force_x = force_magnitude * dx / distance
        force_y = force_magnitude * dy / distance

        return force_x, force_y

    def update_position(self, force, dt):
        # Calculate acceleration
        ax = force[0] / self.mass
        ay = force[1] / self.mass

        # Update velocity
        self.velocity[0] += ax * dt
        self.velocity[1] += ay * dt

        # Update position
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

    def draw(self, screen):
        # Convert scaled position to display coordinates
        display_x = int(self.position[0] / SCALE + WIDTH / 2)
        display_y = int(self.position[1] / SCALE + HEIGHT / 2)
        pygame.draw.circle(screen, self.color, (display_x, display_y), self.radius)

    def get_velocity_text(self):
        # Return the velocity as a formatted string
        velocity_magnitude = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        return f"Velocity: {velocity_magnitude:.2f} m/s"

class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, 20)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.knob_x = x + (initial_val - min_val) / (max_val - min_val) * width
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Move the knob within slider bounds
            self.knob_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
            # Update the slider's value based on the knob's position
            self.value = self.min_val + (self.knob_x - self.rect.x) / self.rect.width * (self.max_val - self.min_val)

    def draw(self, screen):
        # Draw the slider track
        pygame.draw.rect(screen, (180, 180, 180), self.rect)
        # Draw the knob
        pygame.draw.circle(screen, (0, 0, 255), (int(self.knob_x), self.rect.y + 10), 10)

    def get_value(self):
        return self.value

class Simulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Gravitational Movement of Two Bodies with Scale Control")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)

        # Define two bodies with initial properties
        self.body1 = Body(
            mass=5.972e24,
            position=[-1.5e8, 0],  # Positioned to the left of the screen center
            velocity=[0, 0],    # Increased velocity for visibility
            color=(0, 0, 255),
            radius=20
        )
        self.body2 = Body(
            mass=7.348e22,
            position=[1.5e8, 0],  # Positioned to the right of the screen center
            velocity=[0, 1000],    # Increased velocity for visibility
            color=(255, 0, 0),
            radius=10
        )

        # Initialize a slider for the scale variable
        self.scale_slider = Slider(10, HEIGHT - 40, 200, 1e4, 1e6, SPEED)

    def draw_origin_cross(self):
        # Draw a cross at the center of the screen (0,0 coordinates in simulation space)
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        cross_size = 10

        # Draw horizontal and vertical lines to form the cross
        pygame.draw.line(self.screen, (255, 255, 255), (center_x - cross_size, center_y), (center_x + cross_size, center_y), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (center_x, center_y - cross_size), (center_x, center_y + cross_size), 2)

    def display_velocity(self):
        # Render velocity text for each body
        body1_velocity_text = self.font.render(self.body1.get_velocity_text(), True, (255, 255, 255))
        body2_velocity_text = self.font.render(self.body2.get_velocity_text(), True, (255, 255, 255))

        # Display the text on the screen
        self.screen.blit(body1_velocity_text, (10, 10))  # Top-left corner for body1 velocity
        self.screen.blit(body2_velocity_text, (10, 30))  # Below body1 velocity text for body2

    def display_scale(self):
        # Display the current scale value
        scale_text = self.font.render(f"Speed: {SPEED:.1e}", True, (255, 255, 255))
        self.screen.blit(scale_text, (10, HEIGHT - 60))

    def run(self):
        global SPEED
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Pass events to the slider
                self.scale_slider.handle_event(event)

            # Update the SCALE based on the slider's value
            SPEED = self.scale_slider.get_value()

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Draw the origin cross at the center
            self.draw_origin_cross()

            # Calculate gravitational force on each body
            force_on_body1 = self.body1.calculate_gravitational_force(self.body2)
            force_on_body2 = (-force_on_body1[0], -force_on_body1[1])

            # Update positions of both bodies
            dt = 1 / FPS * SPEED
            self.body1.update_position(force_on_body1, dt)
            self.body2.update_position(force_on_body2, dt)

            # Draw the bodies
            self.body1.draw(self.screen)
            self.body2.draw(self.screen)

            # Display velocity and scale on the screen
            self.display_velocity()
            self.display_scale()

            # Draw the scale slider
            self.scale_slider.draw(self.screen)

            # Update display and tick clock
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    pygame.init()
    simulation = Simulation()
    simulation.run()
