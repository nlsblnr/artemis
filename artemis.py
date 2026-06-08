import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

screen_width = 1600
screen_height = round(screen_width/16*9)

dt = 0.001
G = 100000
threshold_x = 1
threshold_y = 1
planet_speed = 400
m_E = 500

class Planet:
    def __init__(self, mass, x, y, v_x, v_y, a_x, a_y):
        self.mass = mass
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.a_x = a_x
        self.a_y = a_y

def calculate_force(planet, other_planet):
    distance = math.sqrt((other_planet.y-planet.y)**2 + (other_planet.x-planet.x)**2)
    F = G*planet.mass*other_planet.mass/distance**2
    dx = other_planet.x-planet.x
    dy = other_planet.y-planet.y

    F_x = dx/distance*F
    F_y = dy/distance*F

    return (F_x, F_y)


def update_planet_data():
    for i, planet in enumerate(planets):
        planet.x = planet.x + dt*planet.v_x
        planet.y = planet.y + dt*planet.v_y
        planet.v_x = planet.v_x + dt*planet.a_x
        planet.v_y = planet.v_y + dt*planet.a_y
        # Kräfte bzgl. der anderen Körper berechnen
        F_x_new = 0
        F_y_new = 0
        for k, other_planet in enumerate(planets):
            if k != i:
                F_x_new += calculate_force(planet=planet, other_planet=other_planet)[0]
                F_y_new += calculate_force(planet=planet, other_planet=other_planet)[1]

        planet.a_x = F_x_new/planet.mass
        planet.a_y = F_y_new/planet.mass

alpha_x, alpha_y, beta_x, beta_y, gamma_x, gamma_y = [], [], [], [], [], []


planets = []
planets.append(Planet(m_E, 0, 0, 0, 0, 0, 0))
planets.append(Planet(1, 0, planets[0].y + G*planets[0].mass/planet_speed**2, planet_speed, 0, 0, 0))
planets.append(Planet(1, 0, planets[0].y - G*planets[0].mass/planet_speed**2, -planet_speed, 0, 0, 0))

for epoch in range(5000):
    if epoch%1000:
        print(epoch)
    update_planet_data()
    for i, planet in enumerate(planets):
        if i == 0:
            alpha_x.append(planet.x)
            alpha_y.append(planet.y)
        elif i == 1:
            beta_x.append(planet.x)
            beta_y.append(planet.y)
        elif i == 2:
            gamma_x.append(planet.x)
            gamma_y.append(planet.y)

plt.plot(alpha_x, alpha_y, label='alpha')
plt.plot(beta_x, beta_y, label='beta')
plt.plot(gamma_x, gamma_y, label='gamma')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Projectile Trajectories')
plt.legend()
plt.grid(True)
plt.show()

fig, ax = plt.subplots(figsize=(8, 8))

# Trajectory lines
line_a, = ax.plot([], [], label='alpha')
line_b, = ax.plot([], [], label='beta')
line_g, = ax.plot([], [], label='gamma')

# Moving markers
dot_a, = ax.plot([], [], 'o')
dot_b, = ax.plot([], [], 'o')
dot_g, = ax.plot([], [], 'o')

# Set limits based on all data
all_x = np.concatenate([alpha_x, beta_x, gamma_x])
all_y = np.concatenate([alpha_y, beta_y, gamma_y])
ax.set_xlim(all_x.min(), all_x.max())
ax.set_ylim(min(0, all_y.min()), all_y.max())
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Projectile Trajectories')
ax.legend()
ax.grid(True)

nframes = min(len(alpha_x), len(beta_x), len(gamma_x))

def update(i):
    line_a.set_data(alpha_x[:i+1], alpha_y[:i+1])
    line_b.set_data(beta_x[:i+1], beta_y[:i+1])
    line_g.set_data(gamma_x[:i+1], gamma_y[:i+1])

    dot_a.set_data([alpha_x[i]], [alpha_y[i]])
    dot_b.set_data([beta_x[i]], [beta_y[i]])
    dot_g.set_data([gamma_x[i]], [gamma_y[i]])

    return line_a, line_b, line_g, dot_a, dot_b, dot_g

anim = FuncAnimation(fig, update, frames=nframes, interval=0.1, blit=True)
plt.show()