
class Simple(object):
    def update(self, gameinfo):
         if gameinfo.my_fleets:
            return
         if gameinfo.my_planets and gameinfo.not_my_planets:
            self.findClosest(gameinfo)
            self.findWeakest(gameinfo)
            self.findStrongest(gameinfo)

    def findWeakest(self,gameinfo):
         src = list(gameinfo.my_planets.values())[0]
         dest = min(gameinfo.not_my_planets.values(),key=lambda p: p.num_ships)
         if (src.num_ships > dest.num_ships):
             gameinfo.planet_order(src,dest,int(src.num_ships*0.75))

    def findStrongest(self,gameinfo):
         src = list(gameinfo.my_planets.values())[0]
         dest = max(gameinfo.not_my_planets.values(),key=lambda p: p.num_ships)

         if (src.num_ships > dest.num_ships):
             gameinfo.planet_order(src,dest,int(src.num_ships))

    def findClosest(self,gameinfo):
         src = list(gameinfo.my_planets.values())[0]
         dest = list(gameinfo.not_my_planets.values())
         selectedDest = dest[0]
         distance = src.distance_to(dest[0])
         for x in dest:
             temp = x.distance_to(src)
             if temp < distance:
                 distance = temp
                 selectedDest = x

         if (src.num_ships > selectedDest.num_ships):
             gameinfo.planet_order(src,selectedDest,int(src.num_ships))
         

      
