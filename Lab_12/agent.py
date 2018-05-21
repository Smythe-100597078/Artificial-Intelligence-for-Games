
from graphics import egi


class Agent(object):

      def __init__(self, x,y,radius):
          self.dx = x
          self.dy = y
          self.radius = radius


      def update(self,src,dest):
        src_box = src 
        dest_box = dest
        scale = 0.5
        self.dx = src.x + (dest.x - src.x) * scale
        self.dy = src.y + (dest.y - src.y) * scale

      def render(self):
          egi.set_pen_color("Red")
          egi.circle(self.dx,self.dy,True,20)

