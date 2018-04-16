'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import *
from graphics import egi


AGENT_MODES = {
    KEY._1: 'seek',
    KEY._2: 'arrive_slow',
    KEY._3: 'arrive_normal',
    KEY._4: 'arrive_fast',
    KEY._5: 'flee',
    KEY._6: 'pursuit'
}


class Agent(object):

    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        'normal':0.05,
        'fast': 0.002
        ### ADD 'normal' and 'fast' speeds here
    }

    def random_color():
        rgbl=[255,0,0]
        random.shuffle(rgbl)
        return tuple(rgbl)

    def __init__(self, world=None, scale=30.0, mass=2.0, mode='seek'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        # where am i and where am i going? random
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.accel = Vector2D()  # current steering force
        self.force = Vector2D()  # current steering force
        self.mass = mass
  
        self.id = len(world.agents)+1
        # limits?
        self.max_speed = 5000.0
        # data for drawing this agent
        self.color = choice(["WHITE","RED","GREEN","BLUE","GREY","PINK","PINK","YELLOW","ORANGE","PURPLE","BROWN","AQUA","DARK_GREEN","LIGHT_BLUE","LIGHT_GREY","LIGHT_PINK"])
      
       
        self.vehicle_shape = [
            Point2D(-1.25,0.0),
            Point2D(-1.0,0.0),
            Point2D(-1.0,0.25),
            Point2D(-0.75,0.25),
            Point2D(-0.75,0.5),
            Point2D(-0.5,0.5),
            Point2D(-0.25,0.25),
            Point2D(-0.25,0.0),
            Point2D(-0.5,0.0),
            Point2D(-0.5,0.25),
            Point2D(-0.25,0.25),
            Point2D(-0.5,0.5),
            Point2D(-0.5,0.75),
            Point2D(-0.75,0.75),
            Point2D(-0.75,1.0),
            Point2D(-0.5,1.0),
            Point2D(-0.5,0.75),
            Point2D(-0.25,0.75),
            Point2D(-0.25,0.5),
            Point2D(0.5,0.5),
            Point2D(0.5,0.75),
            Point2D(0.75,0.75),
            Point2D(0.75,1.0),
            Point2D(1.0,1.0),
            Point2D(1.0,0.75),
            Point2D(0.75,0.75),
            Point2D(0.75,0.5),
            Point2D(0.5,0.25),
            Point2D(0.75,0.25),
            Point2D(0.75,0.0),
            Point2D(0.5,0.0),
            Point2D(0.5,0.25),
            Point2D(0.75,0.5),
            Point2D(1.0,0.5),
            Point2D(1.0,0.25),
            Point2D(1.25,0.25),
            Point2D(1.25,0.0),
            Point2D(1.5,0.0),
            Point2D(1.5,-0.75),
            Point2D(1.25,-0.75),
            Point2D(1.25,-0.25),
            Point2D(1.0,-0.25),
            Point2D(1.0,-0.75),
            Point2D(0.75,-0.75),
            Point2D(0.75,-1.0),
            Point2D(0.25,-1.0),
            Point2D(0.25,-0.75),
            Point2D(0.75,-0.75),
            Point2D(0.75,-0.5),
            Point2D(-0.5,-0.5),
            Point2D(-0.5,-0.75),
            Point2D(0.0,-0.75),
            Point2D(0.0,-1.0),
            Point2D(-0.5,-1.0),
            Point2D(-0.5,-0.75),
            Point2D(-0.75,-0.75),
            Point2D(-0.75,-0.25),
            Point2D(-1.0,-0.25),
            Point2D(-1.0,-0.75),
            Point2D(-1.25,-0.75),
            Point2D(-1.25,0.0)


        ]

    def calculate(self):
        # calculate the current steering force
        mode = self.mode
        if mode == 'seek':
            force = self.seek(self.world.target)
        elif mode == 'arrive_slow':
            force = self.arrive(self.world.target, 'slow')
        elif mode == 'arrive_normal':
            force = self.arrive(self.world.target, 'normal')
        elif mode == 'arrive_fast':
            force = self.arrive(self.world.target, 'fast')
        elif mode == 'flee':
            force = self.flee(self.world.target)
        elif mode == 'pursuit':
            if self == self.world.hunter:
                force = self.flee(self.world.target)
            else:
                force = self.pursuit(self.world.hunter)
        #elif mode == 'wander':
        #    force = self.wander(delta)
        #elif mode == 'follow_path':
        #    force = self.follow_path()
        else:
            force = Vector2D()
        self.force = force
        return force

    def update(self,delta):
        ''' update vehicle position and orientation '''
       
        force = self.calculate()  
        
        self.accel = force / self.mass
        # new velocity
        self.vel += self.accel * delta
        # check for limits of new velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta
        # update heading is non-zero velocity (moving)
        if self.vel.length_sq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        # treat world as continuous space - wrap new position if needed
        self.world.wrap_around(self.pos)

    def render(self, color=None):
        print(self.id)
        ''' Draw the triangle agent with color'''
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
      
        egi.closed_shape(pts)
      

    def speed(self):
        return self.vel.length()

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos):
       panic_range = 100
       if self.pos.distance(hunter_pos) > panic_range:
           return Vector2D() #(0,0)
  
       desired_vel = (self.pos - hunter_pos).normalise() * self.max_speed
       return (desired_vel - self.vel)

    def arrive(self, target_pos, speed):
        ''' this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity'''
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist > 0:
            # calculate the speed required to reach the target given the
            # desired deceleration rate
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max
            speed = min(speed, self.max_speed)
            # from here proceed just like Seek except we don't need to
            # normalize the to_target vector because we have already gone to the
            # trouble of calculating its length for dist.
            desired_vel = to_target * (speed / dist)
            return (desired_vel - self.vel)
        return Vector2D(0, 0)

    def pursuit(self, evader):
        toEvader = evader.pos - self.pos
        relativeHeading = self.heading.dot(evader.heading)
       
        if (toEvader.dot(self.heading)> 0) and (relativeHeading < 0.95):
            return self.arrive(evader.pos,'slow')

        lookAheadTime = toEvader.length()/(self.max_speed+evader.speed())
        lookAheadTime += (1 - self.heading.dot(evader.heading)) * -1

        
        lookAheadPos = evader.pos + evader.vel*lookAheadTime
        return self.arrive(lookAheadPos, 'slow')

    
