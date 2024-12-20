import pygame
from pygame.math import Vector2
import math


class PhysicsObject:
    def __init__(self, mass = 1, pos =(0,0), vel =(0,0), momi = 0):
        self.mass = mass
        self.pos = Vector2(pos) #need to make pos a vector2, and a new one
        self.vel = Vector2(vel)
        self.force = Vector2(0,0)
        self.momi = momi
        def set(self, pos=None, angle=None):
         if pos is not None:
            self.pos = Vector2(pos)
         if angle is not None:
            self.angle = angle
    def clear_force(self):
         self.force = Vector2(0,0)
        

    def add_force(self, force):
        self.force +=force
   # def grav_force(self, force, )
    def impulse(self,impulse, point = None):
        self.vel +=Vector2(impulse)/self.mass
        #add the part to change angular velocity if point is not none
        if point is not None:
            s = point - self.pos
            self.avel += math.degrees(Vector2(s, impulse)/self.momi)
    def update(self, dt):
        
        # update velocity using the current force
        self.vel += self.force/self.mass *dt
        # update position using the newly updated velocity
        self.pos += self.vel *dt

class Circle(PhysicsObject):
    def __init__(self, radius=100, color=(255,255,255), width=0, **kwargs):#width = 0 means fill
        self.radius = radius
        self.color = color
        self.width = width
        self.contact_type = "Circle"
        super().__init__(**kwargs)
    def draw(self, window):
        pygame.draw.circle(window, self.color, self.pos, self.radius, self.width)
class Ball(PhysicsObject):

    def __init__(self, x, y,radius, screen, x_speed=2, y_speed=2):
        self.x = x
        self.y = y
        self.radius = radius
        self.screen = screen
        self.color = pygame.Color("grey")
        self.x_speed = x_speed
        self.y_speed = y_speed

    def move(self):
        pygame.draw.circle(self.screen, self.color, [self.x, self.y], self.radius)
        self.y -= self.y_speed
        self.x -= self.x_speed

    def bounce_x(self):
        self.x_speed *= -1

    def bounce_y(self):
        self.y_speed *= -1

    def check_for_contact_on_x(self):
        if self.x - self.radius <= 0 or self.x + self.radius >= self.screen.get_width():
            self.bounce_x()

    def check_for_contact_on_y(self):
        if self.y + self.radius <= 0:
            self.bounce_y()


class Polygon(PhysicsObject):
 def __init__(self, point1=(0,0), point2=(0,0), color=(255,255,255), width=1):
        super().__init__(mass=math.inf)
        self.color = color
        self.width = width
        self.set_points(point1, point2)  # this also sets self.pos and self.normal
        self.contact_type = "Polygon"

class Wall(PhysicsObject):
    def __init__(self, point1=(0,0), point2=(0,0), color=(255,255,255), width=1):
        super().__init__(mass=math.inf)
        self.color = color
        self.width = width
        self.set_points(point1, point2)  # this also sets self.pos and self.normal
        self.contact_type = "Wall"

    def draw(self, window):
        pygame.draw.line(window, self.color, self.point1, self.point2, self.width)
        #pygame.draw.line(window, self.color, self.pos, self.pos + 100*self.normal) # normal

    def update(self, dt):
        super().update(dt)
        self.point1 += self.vel * dt
        self.point2 += self.vel * dt

    def set_points(self, point1=None, point2=None):
        if point1 is not None:
            self.point1 = Vector2(point1)
        if point2 is not None:
            self.point2 = Vector2(point2)
        self.pos = (self.point1 + self.point2)/2
        self.update_normal()

    def update_normal(self):
        self.normal = (self.point2 - self.point1).normalize().rotate(90)

''' Copy this into your physics_objects.py file! '''

# class UniformCircle(Circle):
#     def __init__(self, radius=100, density=None, mass=None, **kwargs):
#         if mass is not None and density is not None:
#             raise("Cannot specify both mass and density.")
#         if mass is None and density is None:
#             mass = 1 # if neither mass or density is specified, default to mass = 1

#         # if mass is not defined, calculate it based on density*area               
#         if mass is None:
#             mass = density * math.pi * radius **2
        
        
#         # calculate moment of inertia
#         momi = 0.5 * mass * radius **2

#         super().__init__(mass=mass, momi=momi, radius=radius, **kwargs)


# class UniformPolygon(Polygon):
#     def __init__(self, density=None, local_points=[], pos=[0,0], angle=0, shift=True, mass=None, **kwargs):
#         if mass is not None and density is not None:
#             raise("Cannot specify both mass and density.")
#         if mass is None and density is None:
#             mass = 1 # if neither mass or density is specified, default to mass = 1
#             density = 1 # it must be defined, but its value doesn't matter when mass is specified
        
#         # Calculate mass, moment of inertia, and center of mass based on density
#         # by looping over all "triangles" of the polygon
#         total_mass = 0
#         center_of_mass_numerator = Vector2(0,0)
#         total_momi = 0
#         for i in range(len(local_points)):
            
#             s0 = Vector2(local_points[i])
#             s1 = Vector2(local_points[i - 1])
#             tri_area = 0.5 * s0.cross(s1)
#             tri_mass = density * abs(tri_area)
#             tri_com = (s0 + s1) / 3
#             tri_momi = tri_mass * (s0.distance_to(tri_com)**2 + s1.distance_to(tri_com)**2) / 6

#             total_mass += tri_mass
#             total_momi += tri_momi
#             center_of_mass_numerator += tri_com * tri_mass
            
        
#         # calculate total center of mass by dividing numerator by denominator (total mass)
#         com = center_of_mass_numerator / total_mass
#         # if mass is specified, then scale total_mass and total_momi
#         if mass is not None:
#             total_momi *= mass/total_mass
#             total_mass = mass

#         # Usually we shift local_points origin to center of mass
#         if shift:
#             com = Vector2(10,5)

#             # Shift all local_points by subtracting com
#             for p in local_points:
#                 p -= com
#             # Shift pos by adding com
#             for i in range(len(local_points)):
#                 local_points[i] -= com

#             local_points = [p-com for p in local_points]
#             # Use parallel axis theorem to correct the moment of inertia (total_momi)
#            # i = i(center_of_mass_numerator) - total_momi * math.abs(density)**2      

#         # Then call super().__init__() with those correct values
#         super().__init__(mass=abs(total_mass), momi=abs(total_momi), local_points=local_points, pos=pos, angle=angle, **kwargs) 

# # Test UniformPolygon
# shape = UniformPolygon(density=0.01, local_points=[[0,0],[20,0],[20,10],[0,10]])
# print(f"Check mass: {shape.mass} = {0.01*10*20}")  # check mass
# print(f"Check momi: {shape.momi} = {shape.mass/12*(10**2+20**2)}")  # check moment of inertia
# print([shape.local_points]) # check if rectangle is centered (checks center of mass)
# print([[-10,-5],[10,-5],[10,5],[-10,5]])  
