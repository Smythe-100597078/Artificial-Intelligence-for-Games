
from random import randint
import itertools
import copy

player = {
    'HP' : 30,
    'Damage' : 5,
    'Heal' : 10
    }

enemy = {
    'HP' : 30,
    'Damage': 5,
    'Heal' : 5
    }

actions = {
    'attack',
    'heal',
    'damageBoost'
    }


def update(action,attacker,defender):
        if action == 'attack':
            defender['HP'] = defender['HP'] - attacker['Damage']
        if action == 'heal': 
            attacker['HP'] =  attacker['HP'] + attacker["Heal"]
        if action == 'damageBoost':
            attacker['Damage'] = attacker['Damage'] + 4



def lookAhead(plan):
    copyPlayer = copy.deepcopy(player)
    copyEnemy = copy.deepcopy(enemy)
    for p in plan:
        update(p, copyPlayer, copyEnemy)
        update('action', copyEnemy, copyPlayer)
        if copyPlayer['HP'] <= 0 and copyEnemy['HP'] <= 0:
            return copyPlayer, copyEnemy
    return copyPlayer, copyEnemy

def generate_possible_plans(depth):
    
    return list(itertools.product(actions, repeat=depth)) ## Equivilant to a nested for-loop, returns every possible action combination

def call_best_move_player():
    plannedActions = generate_possible_plans(3) ## Repeat 3 times
    bestOption = None
    for p in plannedActions:
        if not bestOption:
            tempPlayer, tempEnemy = lookAhead(p)
            if tempPlayer['HP'] > 0:
                bestOption = p       
    print('>> BEST PLAYER PLAN: ', bestOption)
    print(">> PLAYER CHOOSES TO: ", bestOption[0])
    return bestOption[0]

def call_best_move_enemy():
    plannedActions = generate_possible_plans(3) ## Repeat 3 times
    bestOption = None
    for p in plannedActions:
        if not bestOption:
            tempPlayer, tempEnemy = lookAhead(p)
            if tempEnemy['HP'] > 0:
                  bestOption = p    
    print('>> BEST ENEMY PLAN: ', bestOption)
    print(">> ENEMY CHOOSES TO: ", bestOption[0])
    return bestOption[0]

def genereate_uninformed_enemy_move():
    action = ''
    if randint(1, 6) == 2:
        action = 'damageBoost'
    elif randint(1, 6) == 4:
        action = 'damageBoost'
    else:
        action = 'attack'
    print("ENEMY CHOOSES TO ", action)
    return action


def run_game():
    HR = '-'*50
    
    print(">> SPIKE: 'THE PLANNING' IN GOAP")
    print(HR)
    running = True
    while running:
        print(">> PLAYER: ", player)
        print(">> ENEMY: ", enemy)

        print(HR)
        update(call_best_move_player(), player, enemy)
        update(genereate_uninformed_enemy_move(), enemy, player)
        print(HR)

        if player['HP'] <= 0 or enemy['HP'] <= 0:
            running = False
            print('>> GAME OVER')
            if player['HP'] <= 0:
                print(">> ENEMY WON!")
            else:
                print(">> PLAYER WON!!")

if __name__ == '__main__':
    run_game()




    