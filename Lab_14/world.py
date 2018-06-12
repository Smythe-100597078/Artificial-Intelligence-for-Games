'''A 2d world that supports agents with steering behaviour

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from matrix33 import Matrix33
from graphics import egi
from pyglet import window, clock


class World(object):
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.target = Vector2D(cx / 2, cy / 2)
        self.hunter = None
        self.agents = []
        self.paused = True
        self.show_info = True

    def update(self, delta):
        if not self.paused:
            for agent in self.agents:
                agent.update(delta)
               

    def render(self):
        for agent in self.agents:
            agent.render()

        platform = window.get_platform()
        display = platform.get_default_display()      
        screen = display.get_default_screen()
        screen_width = screen.width
        screen_height = screen.height
      
        

        if self.target:
            egi.red_pen()
            egi.cross(self.target, 10)

        if self.show_info:
            infotext = ', '.join(set(agent.mode for agent in self.agents))
            forcetext = agent.max_force
            egi.white_pen()

            egi.text_at_pos(0, 0, infotext)
            egi.text_at_pos(10,screen_height-100, "Max Force Value (Truncated): "+str(forcetext))
 


    def wrap_around(self, pos):
        ''' Treat world as a toroidal space. Updates parameter object pos '''
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
        ''' Transform the given list of points, using the provided position,
            direction and scale, to object world space. '''
        # make a copy of original points (so we don't trash them)
        wld_pts = [pt.copy() for pt in points]
        # create a transformation matrix to perform the operations
        mat = Matrix33()
        # scale,
        mat.scale_update(scale.x, scale.y)
        # rotate
        mat.rotate_by_vectors_update(forward, side)
        # and translate
        mat.translate_update(pos.x, pos.y)
        # now transform all the points (vertices)
        mat.transform_vector2d_list(wld_pts)
        # done
        return wld_pts

    def transform_point(self,point,pos,forward,side):

        wld_pt = point.copy()
        mat = Matrix33()

        mat.rotate_by_vectors_update(forward,side)
        mat.translate_update(pos.x,pos.y)
        mat.transform_vector2d(wld_pt)

        return wld_pt