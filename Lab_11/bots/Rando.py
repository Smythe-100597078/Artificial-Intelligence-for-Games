from random import choice

class Rando(object):

    def update(self, gameinfo):
        if gameinfo.my_fleets:
            return
        if gameinfo.my_planets and gameinfo.not_my_planets:

            #dest = choice(list(gameinfo.not_my_planets.values()))
            #src = choice(list(gameinfo.my_planets.values()))

            src = max(gameinfo.my_planets.values(),key=lambda p: p.num_ships)
            dest = min(gameinfo.not_my_planets.values(),key=lambda p: p.num_ships)

            if src.num_ships > 10:
                gameinfo.planet_order(src,dest,int(src.num_ships * 0.75))

