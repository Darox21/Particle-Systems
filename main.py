import pygame
import numpy as np
import math


class main(object):
	""" This aplication's package
	""" 

    ## SETUP ##
	pygame.init()

	# Camera position for dragging particle positions
	camera_pos = np.array([0,0], dtype=np.int32)
	camera_scale = 1.0

	# Size of window, and caption of it
	w_dimentions = np.array([1280, 720], dtype=np.int16) # Description

	screen = pygame.display.set_mode((w_dimentions))
	pygame.display.set_caption("Physics_sims")
	icon = pygame.image.load("assets\window_icon.png")
	pygame.display.set_icon(icon)

	# Strength of the forces
	GRAVITY = 0.005
	ELECTROMAGNETISM = 2000

	def __init__(self):

		camera_drag = False

		# Generation of particles	
		self.generate_particles(50)
	

		## LOOP ##
		running = True
		while running:

			self.screen.fill((20,20,20)) # Fill the background

			mouse_pos = np.array(pygame.mouse.get_pos(), dtype=np.int16)
			# Check de mouse position and add it to an array

			# Check events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 2: # if Middle click
						camera_drag = True
					
					if event.button == 4:
						main.camera_scale *= (1/0.9)
						print(f"Scale: {round(self.camera_scale, 4)}")
						main.camera_pos = main.camera_pos + ((mouse_pos - (mouse_pos * 1/0.9)) / self.camera_scale)
					if event.button == 5:
						main.camera_scale *= 0.9
						print(f"Scale: {round(self.camera_scale, 4)}")
						main.camera_pos = main.camera_pos + ((mouse_pos - (mouse_pos * 0.9)) / self.camera_scale)
				
				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 2:
						camera_drag = False
						print(f"New Camera Position: {list(map(int, self.camera_pos))}")

			
			if camera_drag: # Move the "camera_pos" acordingly
				main.camera_pos = self.camera_pos + ((mouse_pos - prev_mouse_pos)/ main.camera_scale)
			
			prev_mouse_pos = mouse_pos
			# Keep the last mouse position

			# Particles
			for p in Particle.array:
				p.update_acceleration()
			# For every particle in the array use its functions

			for p in Particle.array:
				p.update_pos()
				p.show()

			i = len(Particle.array) - 1
			while i >= 0:
				p = Particle.array[i]
				# Check if it is out of bounds
				if p.pos[0] < -9999 or p.pos[1] < -9999 or p.pos[0] > 9999 or p.pos[1] > 9999:
					print("Particle Out of bounds")
					del Particle.array[i]
				i -= 1
			del i


			pygame.display.update()
	

	def generate_particles(self, num, mass=(100,30), charge="rand", vel=[0.0,0.0], 
						   size=(5000, 5000), offset=(-2500,-2500)):
		"""Generates Particles 

			Parameters
			------------
			num: int
			Quantity of generated particles
			
			mass: tuple
			  Uses the numpy funcion of numpy.random.normal()
				first number is the mean of a gaussian distribution
				second number is the standard deviation
			charge: int
			  A signed int
			vel: list
			  velocity
			size: tuple
			  Size of the spawning area
			offset: tuple
			  Offset of the spawning area
		"""
		for n in range(num):
			p_pos = np.random.rand(2)
			p_pos = (p_pos * size) + offset

			p_mass = np.random.normal(mass[0],mass[1])

			if charge == "rand":
				p_charge = np.random.randint(-1,2)
			else:
				p_charge = charge
			
			p_vel = vel

			# print(f"Particle( Pos: {p_pos}, Mass:{p_mass}, Charge: {p_charge}, Vel: {p_vel})")
			Particle.array.append(Particle(p_pos, p_mass, p_charge, p_vel))
			# Append to the object array inside the object so it can
			# be accesed from methods inside the object


class Particle(object):
	"""The Particle object handles the particle related methods
	"""
	array = []
	# A array every particle is aware of, and has every particle created

	def __init__(self, pos, mass=100, charge=1, vel=[0,0]):
		# Physics related things
		self.pos = np.array(list(map(float, pos)), dtype=np.float32)
		# "list(map(float, pos))": is equivalent [float(pos[0]),float(pos[1])] 
		# but feels prettier
		self.mass = mass
		self.charge = charge
		self.vel = np.array(list(map(float, vel)), dtype=np.float32)

		# Drawing related things
		try:
			self.radius = int(math.sqrt(self.mass / math.pi)) * 10
		except e as exception:
			# I have a bug related to this, I still don't find out why
			print(f"Mass: {self.mass} \nMass divided by Pi: {self.mass / math.pi}")
			Print(e)
		
		# This makes the area directly proportional to its mass
		self.size = np.array((self.radius*2, self.radius*2))

		red = abs(self.charge - 1) * 127
		green = abs(self.charge + 1) * 127
		self.color = (red,green,128)


	def update_acceleration(self):
		"""Calculates acording to the force the other particles excert"""
		total_newtons = np.zeros(2)
		for p in self.array:
			distance = np.linalg.norm(self.pos - p.pos)
			if distance != 0: # To avoid infinities
				# Also avoids the particle excerting force to itself

				force_by_axys = np.array(self.pos - p.pos)
				dist_sqrd = (distance ** 2)

				# Gravity
				strength_of_force = ((main.GRAVITY * self.mass * p.mass) / dist_sqrd)
				added_vector = force_by_axys * strength_of_force
				total_newtons += added_vector

				#Electromagnetism
				if self.charge != 0 and p.charge != 0:
					strength_of_force = (-(main.ELECTROMAGNETISM * self.charge * p.charge) 
										/ dist_sqrd)
					added_vector = force_by_axys * strength_of_force
					total_newtons += added_vector
			# Make a vector adding every force applied by every other particle

		self.vel -= total_newtons / self.mass
		# Add the total 


	def update_pos(self):
		"""Adds to position the velocity"""
		self.pos += self.vel


	def show(self):
		"""Makes a surface and calls screen.blit()"""

		relative_size = self.size * main.camera_scale
		relative_radius = int(self.radius * main.camera_scale)
		relative_pos = (self.pos + main.camera_pos) * main.camera_scale

		if relative_radius >= 1:
			surface = pygame.Surface(relative_size)
			center = (relative_radius, relative_radius)
			pygame.draw.circle(surface, self.color, center, relative_radius)
		else:
			# Anything below a radius of 1 will will be drawn as a radius of 1
			surface = pygame.Surface((2,2))
			pygame.draw.circle(surface, self.color, (1,1), 1)

		main.screen.blit(surface,list(map(int, relative_pos)))


if __name__ == '__main__':
	# if this file is excecuted as the main file, do this:
	main()