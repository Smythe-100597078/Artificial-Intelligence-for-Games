
#variables
fStamina = 25
fHealth = 50
fDamage = 5

states = ['attacking','defending','surrender']
current_state = 'defending'

alive = True
running = True
defence_counter = 0

while running and alive:
    # defending: if health < 25, then defend.  Each defence removes 5 Health.
    # Two defences in a row returns 5 Stamina
    if current_state is 'defending':	
        print("Defending against Attack (-_-)")
        fHealth -= 5
        defence_counter += 1
    if defence_counter == 2:
       fStamina += 5
       defence_counter = 0
        # Check for change state
    if fStamina > 0:
        current_state = 'attacking'
    if fHealth == 0:
        current_state = 'surrender'
   
    # attacking: attacks imaginary enemy, each attack deals 5 damage
    elif current_state is 'attacking':
        print("Attacking the enemy (~_~)  ")
        fStamina -= 5
       
        # Check for change state
    if fStamina == 0:
        current_state = 'defending'
        
            
    # surrender: you are out of health and stamina, the game is over
    elif current_state is 'surrender':
       print("The enemy has slain you (°-°)")
       print("Game Over!")
       alive = False
       running = False
       

