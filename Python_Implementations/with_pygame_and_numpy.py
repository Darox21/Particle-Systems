import pygame
import numpy as np
import math
from random import randint


## SETUP ##

pygame.init()

# Camera position for dragging particle positions
camera_pos = np.array([0,0])

# Size of window, and caption of it
w_dimentions = [1280, 720] # Description

screen = pygame.display.set_mode((w_dimentions))
pygame.display.set_caption("Physics_sims")

# Strength of the force of gravity
GRAVITY = 0.0003


class main(object):
	""" This aplication's package""" 
	def __init__(self):
		
		global camera_pos
		# Tells the class to use the global "camera_pos" 
		# instead of creating its own local variable

		camera_drag = False

		# Generation of particles
		for n in range(30):
			randompos = (randint(0,w_dimentions[0]),
						randint(0,w_dimentions[1]))

			Particle.array.append(Particle(randompos))
			# Append to the object array inside the object so it can
			# be accesed from methods inside the object


		## LOOP ##
		running = True
		while running:

			screen.fill((20,20,20)) # Fill the background

			mouse_pos = np.array(pygame.mouse.get_pos())
			# Check de mouse position and add it to an array

			# Check events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					print("Pressed: Mouse " + str(event.button))
					if event.button == 2: # if Middle click
						camera_drag = True
				
				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 2:
						camera_drag = False

			
			if camera_drag: # Move the "camera_pos" acordingly
				camera_pos += (mouse_pos - prev_mouse_pos)
			
			prev_mouse_pos = mouse_pos
			# Keep the last mouse position

			# Particles
			for p in Particle.array:
				p.update_acceleration()
			# For every particle in the array use its functions
			for p in Particle.array:
				p.update_pos()
				p.show()


			pygame.display.update()


class Particle(object):
	# The Particle object handles the particle related methods

	array = []
	# A array every particle is aware of, and has every particle created

	def __init__(self, pos, mass=100, vel=[0,0]):
		# Physics related things
		self.pos = np.array(list(map(float, pos)))
		# To explain this "list(map(float, pos))":
		# First apply the float() function to every value in the pos[] array
		# Then output it as a list, and finally make that into a np.array()
		# This is equivalent [float(pos[0]),float(pos[1])] but feels prettier
		self.mass = mass
		self.vel = np.array(list(map(float, vel)))

		# Drawing related things
		self.radius = int(math.sqrt(self.mass/ math.pi))
		# This makes a s
		self.size = (int(self.radius*2), int(self.radius*2))
		self.color = (255,255,128)


	def update_acceleration(self):
		"""Calculates acording to the force of gravity the other particles excert"""
		total_newtons = np.array([0.0,0.0])
		for p in self.array:
			distance = np.linalg.norm(self.pos - p.pos)
			if distance != 0: # To avoid infinities
				# Also avoids the particle excerting force to itself

				force_by_axys = np.array(self.pos - p.pos)

				# Gravity
				strength_of_force = ((GRAVITY * self.mass * p.mass) / 
											(distance ** 2))
				force_by_axys *= strength_of_force
				total_newtons += force_by_axys
			# Make a vector adding every force applied by every other particle

		self.vel -= total_newtons / self.mass
		# Add the total 


	def update_pos(self):
		"""Adds to position the velocity"""
		self.pos += self.vel

	def show(self):
		"""Makes a surface and calls screen.blit()"""
		# Draw and blit to screen
		relative_pos = self.pos + camera_pos

		surface = pygame.Surface(self.size)
		center = (self.radius, self.radius)
		pygame.draw.circle(surface, self.color, center, self.radius)


		screen.blit(surface,list(map(int, relative_pos)))
		

if __name__ == '__main__':
	# if this file is excecuted as the main file, do this:
	main()