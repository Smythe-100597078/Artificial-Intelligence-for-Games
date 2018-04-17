'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from enviroObject import enviroObject
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform, randint
from path import Path

AGENT_MODES = {
    KEY._1: 'seek',
    KEY._2: 'arrive_slow',
    KEY._3: 'arrive_normal',
    KEY._4: 'arrive_fast',
    KEY._5: 'flee',
    KEY._6: 'pursuit',
    KEY._7: 'follow_path',
    KEY._8: 'wander',
    KEY._9: 'flocking',
    KEY._0: 'hide'

}

class Agent(object):

    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        'normal' : 0.5,
        'fast' : 0.2
        # ...
    }

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='seek'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        # where am i and where am i going? random start pos
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()  # current steering force
        self.accel = Vector2D() # current acceleration due to force
        self.mass = mass
        self.tagged = False
        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-0.25,  0.15),
            Point2D( 0.25,  0.0),
            Point2D(-0.25, -0.15)
        ]
        ### path to follow?
        self.path = Path()
        self.randomise_path()
        self.waypoint_threshold = 50.0
        ### wander details
        self.wander_target = Vector2D(1,0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = 1.0 * scale
        self.wander_jitter = 10.0 * scale
        self.bRadius = scale
        self.neighbourR = 50;
        self.enviroObjs = []
        self.fillEnvirObjects()
        self.neighbours = []

        self.CohesionWeight = 0
        self.SeperationWeight = 2.0
        self.AlignmentWeight = 0

        # limits?
        self.max_speed = 20.0 * scale
        self.max_force = 500.0
        
        # debug draw info?
        self.show_info = False






    def randomise_path(self):
        cx = self.world.cx
        cy = self.world.cy
        margin = min(cx,cy) * (1/6)
        self.path.create_random_path(10,margin,margin,cx-margin,cy-margin)

    def follow_path(self):
        if self.path.is_finished():
            self.arrive(self.path.current_pt(),'slow')
        else:
            if self.pos.distance(self.path.current_pt()) < self.waypoint_threshold:
                self.path.inc_current_pt()
        
        return self.seek(self.path.current_pt())

    def fillEnvirObjects(self):
        for x in range (0,5):
            self.enviroObjs.append(enviroObject("circle",self.world))

       

    def calculate(self,delta):

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
            force = self.pursuit(self.world.hunter)
        elif mode == 'wander':
            force = self.wander(delta)
        elif mode == 'follow_path':
            force = self.follow_path()
        elif mode == 'flocking':
            force = self.sumBehaviours(delta)
        else:
            force = Vector2D()
        self.force = force
        return force
    
    def update(self, delta):
       
        force = self.calculate(delta)  # <-- delta needed for wander
        force.truncate(self.max_force)
      
        self.accel = force / self.mass  # not needed if mass = 1.0
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
        ''' Draw the triangle agent with color'''
        # draw the path if it exists and the mode is follow
        if self.mode == 'follow_path':
            self.path.render()
        
        if self.mode == "wander":
            wnd_pos = Vector2D(self.wander_dist,0)
            wld_pos = self.world.transform_point(wnd_pos,self.pos,self.heading,self.side)

            if self.tagged :
                 self.color = 'GREEN'
            else:
                self.color = 'ORANGE'
            wnd_pos = (self.wander_target + Vector2D(self.wander_dist,0))
            wld_pos = self.world.transform_point(wnd_pos,self.pos,self.heading,self.side)
          
        if self.mode == "hide":
            for x in self.enviroObjs:
                x.render()
            
                

        # draw the ship
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        
        # draw it!
        egi.closed_shape(pts)


        # add some handy debug drawing info lines - force and velocity
        if self.show_info:
            s = 0.5 # <-- scaling factor
            # force
            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)
            # velocity
            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)
            # net (desired) change
            egi.white_pen()
            egi.line_with_arrow(self.pos+self.vel * s, self.pos+ (self.force+self.vel) * s, 5)
            egi.line_with_arrow(self.pos, self.pos+ (self.force+self.vel) * s, 5)

    def speed(self):
        return self.vel.length()

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos):
        ''' move away from hunter position '''
        ## add panic distance (second)
        # ...
        ## add flee calculations (first)
        # ...
        return Vector2D()

    def arrive(self, target_pos, speed):
        
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist > 0:
            speed = dist / decel_rate
           
            speed = min(speed, self.max_speed)
         
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

    
    
    def tagNeighbours(self,bots,radius) :
        self.neighbours.clear();
       
        for bot in bots :
            egi.red_pen()
            egi.circle(bot.pos,radius)
            if bot != self :
                bot.tagged = False
                to = self.pos - bot.pos
                gap = radius + bot.bRadius
                if to.length_sq() < gap**2 :
                    bot.tagged = True
                    egi.white_pen()
                    egi.text_at_pos(bot.pos.x,bot.pos.y,"Tagged")    
                    self.neighbours.append(bot)
               
       

    def Seperation(self,group):
        SteeringForce = Vector2D()
        for bot in group:
            if bot != self and bot.tagged:
                ToBot = self.pos - bot.pos
                SteeringForce += ToBot.normalise() / ToBot.length()
        return SteeringForce
             
    def Alignment(self,group):
        AvgHeading = Vector2D()
        AvgCount = 0

        for bot in group:
            if bot != self and bot.tagged:
                AvgHeading += bot.heading
                AvgCount +=1
        if AvgCount > 0:
            AvgHeading /= float(AvgCount)
            AvgHeading -= self.heading
        return AvgHeading

    def Cohesion(self,group):
        CentreMass = Vector2D()
        SteeringForce = Vector2D()
        AvgCount = 0

        for bot in group:
            if bot != self and bot.tagged :
                CentreMass += bot.pos
                AvgCount += 1
        if AvgCount > 0 :
            CentreMass /= float(AvgCount)
            SteeringForce = self.seek(CentreMass)
        return SteeringForce
    

    def wander(self, delta):
       wt = self.wander_target

       jitter_tts = self.wander_jitter * delta
       wt += Vector2D(uniform(-1,1) * jitter_tts, uniform(-1,1) * jitter_tts)

       wt.normalise()
       wt *= self.wander_radius

       target = wt + Vector2D(self.wander_dist,0)

       wld_target = self.world.transform_point(target,self.pos,self.heading,self.side)
      
       
       for agent in self.world.agents :
           print(len(agent.neighbours))
       return self.seek(wld_target)

    def sumBehaviours(self,delta):
       self.tagNeighbours(self.world.agents,self.neighbourR)
       if len(self.neighbours) == 0 :
          return self.wander(delta)
       cohesion = self.Cohesion(self.neighbours) * self.CohesionWeight
       alignment = self.Alignment(self.neighbours) * self.AlignmentWeight
       seperation = self.Seperation(self.neighbours) * self.SeperationWeight

       return cohesion + alignment + seperation
       
   
           

   
    
           

