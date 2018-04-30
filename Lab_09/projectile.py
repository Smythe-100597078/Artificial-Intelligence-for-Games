from vector2d import Vector2D
from time import clock
from math import sin, cos, radians
from random import random, randrange, uniform, randint
from graphics import egi, KEY


class projectile(object):

      def __init__(self, world=None, type="",speed="",inaccuracyVal="",scale=30.0,mass=1.0):
        self.world = world
        self.pos =  Vector2D(self.world.agents[0].pos.x,self.world.agents[0].pos.y)   
        dir = radians(random()*360)
        self.heading = Vector2D(sin(dir), cos(dir))
        self.vel = Vector2D()
        self.force = Vector2D()  
        self.accel = Vector2D()
        self.inaccuracy = Vector2D(randint(float(inaccuracyVal),float(inaccuracyVal)+20 ))
        self.side = self.heading.perp()
        self.max_force = 500.0
        self.scale = Vector2D(scale, scale)  
        self.max_speed = float(speed) * scale
        self.type = type
        self.mass = mass
        self.collided = False

      def render(self):
          if self.collided == False:
                  egi.set_pen_color(name = "WHITE")
                  egi.circle(self.pos,5)
              

      def shot(self):
          enemy = self.world.hunter
          target_pos = ((((enemy.pos - self.pos) - self.inaccuracy).normalise() * enemy.max_speed) * self.max_speed)
          self.heading = target_pos
          return target_pos


      def check_kill_zone(self):
          max_x, max_y = self.world.cx, self.world.cy
          if (self.pos.x > max_x) | (self.pos.x < 0) | (self.pos.y > max_y) | (self.pos.y < 0):
              self.world.agents[0].projects.remove(self)
          

      def update(self,delta):
          force = self.heading.normalise() * self.max_speed
          force.truncate(self.max_force)
          self.accel = force / self.mass  
          self.vel += self.accel * delta
          self.vel.truncate(self.max_speed)
          self.pos += self.vel * delta
          if self.vel.length_sq() > 0.00000001:
              self.heading = self.vel.get_normalised()
              self.side = self.heading.perp()
          self.check_kill_zone()
         