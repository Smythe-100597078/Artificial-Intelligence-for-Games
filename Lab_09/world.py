'''A 2d world that supports agents with steering behaviour

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from enviroObject import enviroObject
from matrix33 import Matrix33
from graphics import egi
from pyglet import window, clock


class World(object):
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.target = Vector2D(cx / 2, cy / 2)
        self.agents = []
        self.hunter = None
        self.paused = True
        self.show_info = True
        self.platform = window.get_platform()
        self.display = self.platform.get_default_display()      
        self.screen = self.display.get_default_screen()
        self.screen_width = self.screen.width
        self.screen_height = self.screen.height
        self.enviroObjs = []
        
    

    def update(self, delta):
        if not self.paused:
            for agent in self.agents:
                agent.update(delta)
        if self.agents[0].mode == "shooting":
            for bullet in self.agents[0].projects:
                    bullet.update(delta)
                    self.check_Collision(self.hunter,bullet)
        
        

    def check_Collision(self,enemy,projectile):
        if (projectile.pos.x > enemy.pos.x - 10) & (projectile.pos.x < enemy.pos.x + 10) & (projectile.pos.y > enemy.pos.y - 10) & (projectile.pos.y < enemy.pos.y + 10):
              enemy.collided = True 
              projectile.collided = True
              self.agents[0].projects.remove(projectile)
          
    def render(self):
        for agent in self.agents:
            agent.render()

        if self.agents[0].mode == "hide":
            for obj in self.enviroObjs:
                obj.render()
        
        if self.agents[0].mode == "shooting":
            for bullet in self.agents[0].projects:
                    bullet.render()
        if len(self.agents[0].projects) > 0:
            weaponType = self.agents[0].projects[len(self.agents[0].projects)-1].type
            inaccuracyValue = self.agents[0].projects[len(self.agents[0].projects)-1].inaccuracy
            egi.text_at_pos(self.screen_width-250,self.screen_height-100, "Current Weapon: "+str(weaponType) )
            egi.text_at_pos(self.screen_width-250,self.screen_height-125, "Current Weapon: "+str(inaccuracyValue) )
            
        

        if self.target:
            egi.red_pen()
            egi.cross(self.target, 10)

        if self.show_info:
            infotext = ', '.join(set(agent.mode for agent in self.agents))
            forcetext = agent.max_force
            aligntext = agent.AlignmentWeight
            cohetext = agent.CohesionWeight
            septext = agent.SeperationWeight
            egi.white_pen()

            egi.text_at_pos(0, 0, infotext)
            egi.text_at_pos(10,self.screen_height-100, "Max Force Value (Truncated): "+str(forcetext) +" ( Q : + , W : - )")
            egi.text_at_pos(10,self.screen_height-125, "Seperation Weight : "+str(septext) +" ( A : + , S : - )")
            egi.text_at_pos(10,self.screen_height-150, "Cohesion Weight : "+str(cohetext) +" ( T : + , Y : - )")
            egi.text_at_pos(10,self.screen_height-175, "Alignment Weight: "+str(aligntext) +" ( D : + , F : - )")

    def wrap_around(self, pos):
      
        max_x, max_y = self.cx, self.cy
        if pos.x > max_x:
            pos.x = pos.x - max_x
        elif pos.x < 0:
            pos.x = max_x - pos.x
        if pos.y > max_y:
            pos.y = pos.y - max_y
        elif pos.y < 0:
            pos.y = max_y - pos.y

    def transform_points(self, points, pos, forward, side, scale):
      
        wld_pts = [pt.copy() for pt in points]
        mat = Matrix33() 
        mat.scale_update(scale.x, scale.y)
        mat.rotate_by_vectors_update(forward, side)
        mat.translate_update(pos.x, pos.y)
        mat.transform_vector2d_list(wld_pts)
        
        return wld_pts

    def transform_point(self,point,pos,forward,side):

        wld_pt = point.copy()
        mat = Matrix33()

        mat.rotate_by_vectors_update(forward,side)
        mat.translate_update(pos.x,pos.y)
        mat.transform_vector2d(wld_pt)

        return wld_pt
    
    def fillEnviroObjects(self):
        for x in range (0,5):
            self.enviroObjs.append(enviroObject("circle",self))
