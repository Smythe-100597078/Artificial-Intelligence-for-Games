
class Complex(object):
   
    def update(self, gameinfo):
        fleets = list(gameinfo.enemy_fleets.values())
        self.findClosest(gameinfo)
        self.attackVulnurable(gameinfo,fleets)

    def findClosest(self,gameinfo):
        if gameinfo.my_planets and gameinfo.not_my_planets:
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
         

    def attackVulnurable(self,gameinfo,fleets):
        if gameinfo.enemy_fleets:
            src = list(gameinfo.my_planets.values())[0]
            for fleet in fleets:
                dest = fleet.src
                if src.num_ships > dest.num_ships:
                    gameinfo.planet_order(src,dest,int(src.num_ships))

    
