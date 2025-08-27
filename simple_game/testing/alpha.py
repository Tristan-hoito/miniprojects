import random
import json
import time, sys, os

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
DARK_RED = "\033[31m"
DARK_BLUE = "\033[34m"
WHITE = "\033[37m"
BLUE = "\033[34m"
RESET = "\033[0m"

current_stock = None

class Typing:
    def clear_terminal():
        # Check the operating system and use the appropriate command
        if os.name == 'nt':  # For Windows
            _ = os.system('cls')

    def typingPrint(text):
        for character in text:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.10)

    def typingPrint05(text):
        for character in text:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.05)

    def typingPrint2(text):
        for character in text:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.20)

    def typingbackspace(text):
        for character in text:
            sys.stdout.write(character)  # Print the text
            sys.stdout.flush()      # Ensure it's displayed immediately
            time.sleep(0.20)           # Pause for a moment
        
        time.sleep(1)
        for character in text:
            sys.stdout.write('\b' + ' ' + '\b')  # backspace, overwrite with space, backspace again
            sys.stdout.flush()
            time.sleep(0.1)

    def typingInput(text):
        for character in text:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(0.05)
        value = input()  
        return value

# Constants for player stats
INITIAL_HP = 100
INITIAL_ATTACK = 10
INITIAL_DEFENSE = 5
LEVEL_UP_HP = 20
EXP_MULTIPLIER = 1.25

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = INITIAL_HP
        self.max_hp = INITIAL_HP
        self.attack = INITIAL_ATTACK
        self.defense = INITIAL_DEFENSE
        self.level = 1
        self.exp_required = int(20 * (EXP_MULTIPLIER * self.level))
        self.exp = 0
        self.gold = 10000
        self.inventory = []
        self.inventory_weapons = []
        self.inventory_armors = []
        self.equipped_weapon = None
        self.equipped_armor = None

    def to_dict(self):
        return {
            "name": self.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "attack": self.attack,
            "defense": self.defense,
            "level": self.level,
            "exp": self.exp,
            "exp_required": self.exp_required,
            "gold": self.gold,
            "inventory": self.inventory,
            "weapons": self.inventory_weapons,
            "armors": self.inventory_armors,
            "equipped weapon": self.equipped_weapon,
            "equipped armor": self.equipped_armor

        }

    @classmethod
    def from_dict(cls, data):
        player = cls(data["name"])
        player.hp = data["hp"]
        player.max_hp = data["max_hp"]
        player.attack = data["attack"]
        player.defense = data["defense"]
        player.level = data["level"]
        player.exp = data["exp"]
        player.exp_required = data["exp_required"]
        player.gold = data["gold"]
        player.inventory = data["inventory"]
        player.inventory_weapons = data["weapons"]
        player.inventory_armors = data["armors"]
        player.equipped_weapon = data["equipped weapon"]
        player.equipped_armor = data["equipped armor"]
        return player

    def gain_exp(self, amount):
        self.exp += amount
        Typing.typingPrint05(f"\n{BLUE}{self.name} has gained {amount} exp!{RESET}\n")
        time.sleep(0.5)

        if self.exp >= self.exp_required:  # simple level up rule
            self.level += 1
            self.exp = 0
            self.max_hp += 20
            self.hp = self.max_hp
            self.attack += 5
            self.defense += 2
            Typing.typingPrint05(f"\n{WHITE}{self.name} leveled up to {self.level}!{RESET}")
            Typing.typingPrint05(f"\n {GREEN}HP recovered!{RESET}")
            Typing.typingPrint05(f"\n {RED}+5 Attack!{RESET}")
            Typing.typingPrint05(f"\n {DARK_BLUE}+2 Defense!\n{RESET}")
            time.sleep(1)

    def gain_gold(self, amount):
        self.gold += amount
        Typing.typingPrint05(f"\n{YELLOW}{self.name} has gained {amount} gold!{RESET}")
        time.sleep(0.5)

    def rest_inn(self):
        """Allow player to rest at the inn to restore health for a cost."""
        while True:
            amount = max(10, int(30 * (self.level * 0.1)))
            if self.gold >= amount:
                Typing.clear_terminal()
                Typing.typingbackspace("Approaching Pandora's Inn.......")
                time.sleep(1)
                Typing.typingPrint05("Hello welcome at Pandora's Inn, how may I help you?")
                time.sleep(1)
                Typing.typingPrint05(f"\nHello, do you have a room for {YELLOW}{self.gold}{RESET} gold?\n")
                time.sleep(1)
                response = Typing.typingInput(f"\nAbsolutely! Do you want to rent a room at Pandora's Inn for {YELLOW}{amount}{RESET} gold? Y/N?\n > ").lower()
                
                if response == "y":
                    Typing.clear_terminal()
                    Typing.typingPrint05("Thank you for purchasing a room at Pandora's Inn!")
                    time.sleep(1)
                    Typing.typingbackspace("\nResting........")
                    time.sleep(2)
                    Typing.typingPrint05(f"{GREEN}HP FULLY RECOVERED!{RESET}")
                    Typing.typingPrint05("\nThank you for coming! Come back again!")
                    time.sleep(1)

                    self.gold -= amount 
                    self.hp = self.max_hp
                    global current_stock
                    current_stock = None

                    return show_menu(is_first_time=False)
                    
                elif response == "n":
                    Typing.typingPrint05("\nTsk... Why even bother? Goodbye...\n")
                    time.sleep(1)
                    return show_menu(is_first_time=False)
                        
                else:
                    Typing.clear_terminal()
                    Typing.typingbackspace("\nPlease only choose between Yes or No Adventurer!")
                    time.sleep(1)
                    continue
            
            else:
                Typing.clear_terminal()
                Typing.typingbackspace("\nApproaching Pandora's Inn.......")
                time.sleep(1)
                Typing.typingPrint05("Hello welcome at Pandora's Inn, how may I help you?")
                time.sleep(1)
                Typing.typingPrint05(f"\nHello, do you have a room for {YELLOW}{self.gold}{RESET} gold?")
                time.sleep(1)
                Typing.clear_terminal()
                Typing.typingbackspace("\n.................")
                Typing.typingPrint("GO AWAY! WE DON'T WELCOME BEGGARS!")
                time.sleep(1)
                Typing.typingbackspace("\n.................")
                time.sleep(1)
                Typing.typingPrint("Maybe I should get gold first.....\n")
                time.sleep(2)
                return show_menu(is_first_time=False)

    def show_status(self):
        print(f"{self.name} | HP: {GREEN}{self.hp}/{self.max_hp}{RESET} | ATK: {RED}{self.attack}{RESET} | DEF: {DARK_BLUE}{self.defense}{RESET}")

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0



class Enemy:
    def __init__(self, name, base_hp, base_attack, base_defense, base_exp_reward, player_level, gold_reward):
        self.name = name
        # Scale stats based on player level
        level_multiplier = 1 + (player_level - 1) * 0.3  # 30% increase per level
        self.hp = int(base_hp * level_multiplier)
        self.max_hp = self.hp
        self.attack = int(base_attack * level_multiplier)
        self.defense = int(base_defense * level_multiplier)
        self.exp_reward = base_exp_reward
        self.gold_reward = gold_reward

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

    def show_status(self):
        print(f"{self.name} | HP: {GREEN}{self.hp}/{self.max_hp}{RESET} | ATK: {RED}{self.attack}{RESET} | DEF: {DARK_BLUE}{self.defense}{RESET}")



class Item:
    def __init__(self, name, category, lvl_requirement, cost, durability, added_hp, added_def, added_atk):
        self.name = name
        self.category = category
        self.lvl_requirement = lvl_requirement
        self.cost = cost
        self.durability = durability
        self.max_durability = durability
        self.added_hp = added_hp
        self.added_def = added_def
        self.added_atk = added_atk

    def show_status(self):
        if self.category == "Weapon":
            print(f"{self.name} | {self.category} \nLVL Required: {self.lvl_requirement} | COST: {YELLOW}{self.cost}{RESET} \nDurability: {self.durability}/{self.max_durability} \n {RED}+ ATK: {self.added_atk}{RESET}")

        elif self.category == "Armor":
            print(f"{self.name} | {self.category} \nLVL Required: {self.lvl_requirement} | COST: {YELLOW}{self.cost}{RESET} \nDurability: {self.durability}/{self.max_durability} \n {GREEN}+ HP: {self.added_hp}{RESET}\n {DARK_BLUE}+ DEF: {self.added_def}{RESET}")

    def take_damage(self, durability_damage):
        self.durability -= durability_damage
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.durability > 0



def buying(item, player):
    Typing.clear_terminal()
    Typing.typingbackspace("Purchasing Item.....")
    global current_stock

    if player.gold >= item.cost and player.level >= item.lvl_requirement:
        player.gold -= item.cost

        if item.category == "Weapon":
            player.inventory_weapons.append(item)

        elif item.category == "Armor":
            player.inventory_armors.append(item)

        else:
            player.inventory.append(item)

        Typing.typingPrint05(f"{item.name} has been Successfully purchased!")
        time.sleep(0.5)
        Typing.typingPrint05(f"\nItem has been added into your Inventory!")
        time.sleep(1)
        Typing.clear_terminal()
        Typing.typingPrint05("Thank you for buying at Founty's! Please come back again!")
        time.sleep(1)

        current_stock = "Purchased"
        return current_stock, show_menu(is_first_time=False)
    
    else: 
        Typing.typingPrint05(f"Buying {item.name} has failed! Due to insufficient funds or did not reach the levl requirement!\n")
        time.sleep(1)
        Typing.clear_terminal()
        Typing.typingPrint05("Tsk..... Wasting my time. GO AWAY BEGGAR!")
        time.sleep(1)
        Typing.typingbackspace("\n.................")
        time.sleep(1)
        Typing.typingPrint("Maybe I should get gold first.....")
        time.sleep(2)
        return show_menu(is_first_time=False)

def stock(player):
    global current_stock

    if current_stock is None:
        ITEM_NAMES = ["Long Sword", "Dagger", "Chainmail", "None"]
        ITEM_WEIGHTS = [30, 30, 30, 10]

        encounter = random.choices(ITEM_NAMES, weights=ITEM_WEIGHTS, k=1)[0]

        Typing.clear_terminal()
        Typing.typingPrint05(f"Welcome to Founty's Shop! Where you can find the best items in the world!")
        Typing.typingbackspace(f"\nChecking Stocks..........")
        time.sleep(1)
        
        if encounter != "None":
            for item_data in item_types:
                if item_data[0] == encounter:
                    current_stock = Item(item_data[0], item_data[1], item_data[2], item_data[3],
                                    item_data[4], item_data[5], item_data[6], item_data[7])
                    break
        
        else:
            Typing.clear_terminal()
            Typing.typingPrint05("Unfortunately, There is no stocks at the moment.....\n Please come back again!")
            time.sleep(1)
            current_stock = "No Stock"
            return current_stock, show_menu(is_first_time=False)
    
    elif current_stock == "No Stock":
        Typing.clear_terminal()
        Typing.typingPrint05("Welcome back to Founty's Shop! Unfortunately, There is no stocks at the moment.....\n Please come back again!")
        time.sleep(1)
        return show_menu(is_first_time=False)
        
    elif current_stock == "Purchased":
        Typing.clear_terminal()
        Typing.typingPrint05(f"Welcome back to Founty's Shop! We don't have any more stock!\n Please come back again next time!")
        time.sleep(2)
        show_menu(is_first_time=False)

    else:
        Typing.clear_terminal()
        Typing.typingPrint05(f"Welcome back to Founty's Shop! The same items are still available!")
        time.sleep(1)
    
    if current_stock:
        shop(player, current_stock)

def response_purchasing(item, player):
    while True:
        response = Typing.typingInput(f"Do you want to purchase {item.name}? Y/N?\n > ").lower() 
        if response == "y":
            buying(item, player)

        elif response == "n": 
            Typing.clear_terminal()
            Typing.typingPrint05("Tsk..... Wasting my time.....")
            time.sleep(1)
            Typing.typingbackspace("\n.................")
            Typing.typingPrint05("Bruh")
            time.sleep(1)
            show_menu(is_first_time=False)
        
        else: 
            Typing.typingPrint05("\nPlease choose between Yes or No Adventurer!")
            time.sleep(1)
            return

def purchasing(item, player):
    while True:
        if item.category in ("Weapon", "Armor"):
            response_purchasing(item, player)

        else:
            amount = Typing.typingInput(int(f"\nHow many do you want to purchase? "))
            item.cost *= amount
            response_purchasing(item, player)   

def manage_item(player, item):
    Typing.clear_terminal()
    if item.category == "Weapon":
        if player.equipped_weapon == item:
            #unequip
            player.attack -= item.added_atk
            player.equipped_weapon = None
            Typing.typingPrint05(f"{item.name} unequipped!\n")
            Typing.typingPrint05(f" {RED}- {item.added_atk} ATK{RESET}\n")
            time.sleep(1)

        else:
            # Swap if another weapon is already equipped
            if player.equipped_weapon:
                player.attack -= player.equipped_weapon.added_atk
                Typing.typingPrint05(f"{item.name} unequipped!\n")
                Typing.typingPrint05(f" {RED}- {item.added_atk} ATK{RESET}\n")
                time.sleep(1)
                Typing.clear_terminal()

            player.equipped_weapon = item
            player.attack += item.added_atk
            Typing.typingPrint05(f"{item.name} equipped!\n")
            Typing.typingPrint05(f" {RED}+ {item.added_atk} ATK{RESET}\n")
            time.sleep(1)

    elif item.category == "Armor":
        if player.equipped_armor == item:
            # Unequip
            player.defense -= item.added_def
            player.max_hp -= item.added_hp
            if player.hp > player.max_hp:
                player.hp = player.max_hp
            player.equipped_armor = None
            Typing.typingPrint05(f"{item.name} unequipped!\n")
            Typing.typingPrint05(f" {GREEN}- {item.added_hp} ATK{RESET}\n")
            Typing.typingPrint05(f" {DARK_BLUE}- {item.added_def} ATK{RESET}\n")
            time.sleep(1)

        else:
            if player.equipped_armor:
                player.defense -= player.equipped_armor.added_def
                player.max_hp -= player.equipped_armor.added_hp
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
                Typing.typingPrint05(f"{item.name} unequipped!\n")
                Typing.typingPrint05(f" {GREEN}- {item.added_hp} ATK{RESET}\n")
                Typing.typingPrint05(f" {DARK_BLUE}- {item.added_def} ATK{RESET}\n")
                time.sleep(1)
            player.equipped_armor = item
            player.defense += item.added_def
            player.max_hp += item.added_hp
            Typing.typingPrint05(f"{item.name} equipped!\n")
            Typing.typingPrint05(f" {GREEN}+ {item.added_hp} ATK{RESET}\n")
            Typing.typingPrint05(f" {DARK_BLUE}+ {item.added_def} ATK{RESET}\n")
            time.sleep(1)

def inventory_menu(player,show=True):
    if show:
        Typing.clear_terminal()
        Typing.typingbackspace("Loading Inventory.......")
        time.sleep(1)

    else:
        pass
def inventory_weapons():
    Typing.clear_terminal()
    print("------ WEAPONS ------")

    if not player.inventory_weapons:
        Typing.clear_terminal()
        Typing.typingPrint05("Your inventory is empty!\n")
        time.sleep(1)
        return show_menu(is_first_time=False)

    for i, item in enumerate(player.inventory_weapons, start=1):
        equipped = ""

        if player.equipped_weapon == item:
            equipped = " (Equipped)"

        if item.category:
            print(f"[{i}] {item.name} - {RED}+ {item.added_atk}{RESET}{equipped}")
        
        if item.category == "Armor":
            print("\n----- ARMORS -----")
            print(f"[{i}] {item.name} - {RED}+ {item.added_atk}{RESET}{equipped}")

        print("[0] Exit Inventory")

    choice = input("\nSelect an item to Equip or Unequip: ").strip()

    if choice.isdigit():
        choice = int(choice)

        if 0:
            Typing.clear_terminal()
            Typing.typingbackspace("Going back to the main menu......")

        elif 1 <= choice <= len(player.inventory):
            manage_item(player, player.inventory[choice - 1])
            time.sleep(1)
            return inventory_menu(player, show=False)
        
    else:
        Typing.clear_terminal()
        Typing.typingbackspace("Please select properly.....")
        time.sleep(1)
        return inventory_menu(player, show=False)
        
    return show_menu(is_first_time=False)

def inventory():
    Typing.clear_terminal()
    print("------ INVENTORY ------")

    if not player.inventory:
        Typing.clear_terminal()
        Typing.typingPrint05("Your inventory is empty!\n")
        time.sleep(1)
        return show_menu(is_first_time=False)

    for i, item in enumerate(player.inventory, start=1):
        equipped = ""

        if player.equipped_weapon == item or player.equipped_armor == item:
            equipped = " (Equipped)"

        if item.category:
            print(f"[{i}] {item.name} - (Quantity){item.category}{equipped}")

        if item.category == "Weapon":
            print("----- WEAPONS -----")
            print(f"[{i}] {item.name} - {RED}+ {item.added_atk}{RESET}{equipped}")
        
        if item.category == "Armor":
            print("\n----- ARMORS -----")
            print(f"[{i}] {item.name} - {RED}+ {item.added_atk}{RESET}{equipped}")

        print("[0] Exit Inventory")

    choice = input("\nSelect an item to Equip or Unequip: ").strip()

    if choice.isdigit():
        choice = int(choice)

        if 0:
            Typing.clear_terminal()
            Typing.typingbackspace("Going back to the main menu......")

        elif 1 <= choice <= len(player.inventory):
            manage_item(player, player.inventory[choice - 1])
            time.sleep(1)
            return inventory_menu(player, show=False)
        
    else:
        Typing.clear_terminal()
        Typing.typingbackspace("Please select properly.....")
        time.sleep(1)
        return inventory_menu(player, show=False)
        
    return show_menu(is_first_time=False)

def shop(player, item):
    print("\n---------- STATS ----------")
    print(f"{player.name} | HP: {GREEN}{player.hp}/{player.max_hp}{RESET} |" 
            f"\nLVL: {player.level} | EXP: {BLUE}{player.exp}/{player.exp_required}{RESET}"
            f"\n ATK: {RED}{player.attack}{RESET}\n DEF: {DARK_BLUE}{player.defense}{RESET} "
            f"\n GOLD: {YELLOW}{player.gold}{RESET}")
    ("---------------------------")
    print("")
    print("---------- ITEMS ----------")
    item.show_status()
    print("")
    purchasing(item, player)

def adventure(player):
    global current_stock
    current_stock = None

    """Handle random enemy encounters during adventure."""
    ENEMY_NAMES = ["Goblin", "Orc", "Kobold", "Slime", "Troll", "None"]
    ENEMY_WEIGHTS = [25, 15, 20, 30, 5, 5]  # percentages
    
    encounter = random.choices(ENEMY_NAMES, weights=ENEMY_WEIGHTS, k=1)[0]

    if encounter != "None":
        # Find the enemy data by name
        for enemy_data in enemy_types:
            if enemy_data[0] == encounter:
                enemy = Enemy(enemy_data[0], enemy_data[1], enemy_data[2],
                            enemy_data[3], enemy_data[4], player.level, enemy_data[5])
                battle(player, enemy)
                break
    else:
        Typing.typingPrint05("\nThe area is peaceful... no enemies this time.")
        time.sleep(1)
        return show_menu(is_first_time=False)

def battle(player, enemy):
    Typing.clear_terminal()
    Typing.typingPrint05(f"\n{DARK_RED}A wild {enemy.name} appears!{RESET}\n")
    time.sleep(1)
    
    while player.is_alive() and enemy.is_alive():
        Typing.clear_terminal()
        print("--- Battle ---")
        player.show_status()
        enemy.show_status()

        print("\nChoose an action:")
        print("\n[1] Attack")
        print("[2] Defend")
        print("[3] Run Away")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            # New damage formula considering defense more significantly
            damage = max(1, int(player.attack * (100 / (100 + enemy.defense))))  # Defense reduces damage exponentially
            enemy.take_damage(damage)

            Typing.typingPrint05(f"\n{player.name} attacks {enemy.name} for {DARK_RED}{damage}{RESET} damage!\n")

        elif choice == "2":
            Typing.typingPrint05(f"\n{player.name} defends and reduces damage this turn.\n")

        elif choice == "3":
            damage = int(player.max_hp * 0.3) 
            player.take_damage(damage)
            Typing.typingPrint05(f"\n{player.name} runs away and loses 30% of his health!\n")
            time.sleep(1) 
            return show_menu(is_first_time=False)

        else:
            Typing.typingPrint05("\nInvalid choice, you lose your turn!\n")
            time.sleep(1)

        if enemy.is_alive():
            # New enemy damage formula
            damage = max(1, int(enemy.attack * (100 / (100 + player.defense))))
    
            if choice == "2":
                damage //= 2  # defending still halves the damage

            player.take_damage(damage)
            Typing.typingPrint05(f"{enemy.name} attacks {player.name} for {DARK_RED}{damage}{RESET} damage!\n")
            time.sleep(0.5)

    # End of battle
    if player.is_alive():
        Typing.typingPrint05(f"\n{GREEN}{player.name} defeated {enemy.name}!{RESET}\n")
        time.sleep(0.5)
        player.gain_exp(enemy.exp_reward)
        player.gain_gold(enemy.gold_reward)
        return show_menu(is_first_time=False)

    else:
        Typing.typingPrint(f"\n{RED}{player.name} has been defeated...{RESET}")
        return show_menu(is_first_time=False)
    
def save_game(player, filename="save.json"):
    with open(filename, "w") as f:
        json.dump(player.to_dict(), f, indent=4)
    Typing.clear_terminal()
    Typing.typingbackspace("Saving........")
    Typing.typingPrint05("Game saved!")
    time.sleep(1)
    Typing.clear_terminal()

def load_game(filename="save.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return Player.from_dict(data)
        
    except FileNotFoundError:
        Typing.typingPrint05("\nNo save file found. Starting new game...")
        return None

player = Player("Hero")

enemy_types = [("Goblin", 30, 8, 3, 10, 15),
         ("Orc", 100, 15, 5, 25, 20 ),
         ("Kobold", 25, 12, 2, 8, 10),
         ("Slime", 15, 5, 1, 5, 5),
         ("Troll", 150, 20, 8, 50, 40)]

item_types = [("Long Sword", "Weapon", 1, 40, 100, 0, 0, 20),
              ("Dagger", "Weapon", 1, 15, 50, 0, 0, 15),
              ("Chainmail Armor", "Armor", 1, 80, 200, 100, 20, 0)]

def settings():
    global player
    
    while True:
        Typing.clear_terminal()
        Typing.typingbackspace("Opening Settings..........")
        print("----- SETTINGS -----")
        print("[1] New Game!")
        print("[2] Save Game!")
        print("[3] Load Game!")
        print("[4] Go back to Main Menu!")
        print("--------------------")
        choice = int(input("Please choose a function from 1-4: "))
        
        try:
            match choice:
                case 1:
                    while True:
                        Typing.clear_terminal()
                        response = Typing.typingInput("Do you really want to make a new save? Y/N?\n > ").lower()

                        if response == "y":
                            player.name = player.name
                            player.hp = INITIAL_HP
                            player.max_hp = INITIAL_HP
                            player.attack = INITIAL_ATTACK
                            player.defense = INITIAL_DEFENSE
                            player.level = 1
                            player.exp_required = int(20 * (EXP_MULTIPLIER * player.level))
                            player.exp = 0
                            player.gold = 0
                            save_game(player)
                            return show_menu(is_first_time=False)

                        elif response == "n":
                            Typing.typingPrint05("\nGoing back to settings...")
                            time.sleep(1)
                            return settings()
                        
                        else:
                            Typing.typingPrint05("\nPlease choose between Yes or No.")
                            time.sleep(1)
                            return

                case 2:
                    while True:
                        Typing.clear_terminal()
                        response = Typing.typingInput("Do you really want to save? Y/N?\n > ").lower()

                        if response == "y":
                            save_game(player)
                            return show_menu(is_first_time=False)

                        elif response == "n":
                            Typing.typingPrint05("\nGoing back to settings...")
                            time.sleep(1)
                            return settings()
                        
                        else:
                            Typing.typingPrint05("\nPlease choose between Yes or No.")
                            time.sleep(1)
                            return 

                case 3:
                    while True:
                        Typing.clear_terminal()
                        response = Typing.typingInput("Do you really want to Load your previous save?\n You're going to lose your current file. Y/N?\n > ").lower()

                        if response == "y":
                            loaded = load_game()
                            if loaded:
                                player = loaded
                                Typing.clear_terminal()
                                Typing.typingbackspace("Loading........")
                                Typing.typingPrint05("Game loaded successfully!")
                                time.sleep(1)
                                return show_menu(is_first_time=False)

                        elif response == "n":
                            Typing.typingPrint05("\nGoing back to settings...")
                            time.sleep(1)
                            return settings()
                        
                        else:
                            Typing.typingPrint05("\nPlease choose between Yes or No.")
                            time.sleep(1)
                            return
                        
                case 4:
                    Typing.typingPrint05("\nGoing back to the Main Menu...")
                    time.sleep(1)
                    return show_menu(is_first_time=False)
        
        except ValueError:
            Typing.typingPrint05("\nPlease choose from 1-4 only.")
            print("")
            
def show_menu(is_first_time=True):
    while True:
        Typing.clear_terminal()

        if is_first_time:
            Typing.typingPrint05(f"Welcome to Wilderlands Adventure, {player.name}!\n")
            Typing.typingbackspace("Loading Menu..........")
        else:
            Typing.typingPrint05(f"Welcome Back from the Adventure, {player.name}!\n")
            Typing.typingPrint05("Make sure to rest up, before going back to your adventure!\n")

        print("")
        time.sleep(1)
        print("---------- STATS ----------")
        print(f"{player.name} | HP: {GREEN}{player.hp}/{player.max_hp}{RESET} |" 
              f"\nLVL: {player.level} | EXP: {BLUE}{player.exp}/{player.exp_required}{RESET}"
              f"\n ATK: {RED}{player.attack}{RESET}\n DEF: {DARK_BLUE}{player.defense}{RESET} "
              f"\n GOLD: {YELLOW}{player.gold}{RESET}")
        print("")
        print("[1] Adventure!")
        print("[2] Buy at a Shop!")
        print("[3] Rest at an Inn!")
        print("[4] Inventory")  
        print("[5] End Adventure")
        print("[6] Settings\n")

        try:
            choice = int(input("Please choose a move from 1-6: "))

            match choice:
                case 1:
                    if player.is_alive():
                        adventure(player)
                    else:
                        print(f"You are {DARK_RED}dead!{RESET} Ending adventure...")
                        print("")
                        exit()

                case 2:
                    stock(player)

                case 3:
                    player.rest_inn()

                case 4:
                    inventory_menu(player)
                
                case 5:
                    while True:
                        Typing.clear_terminal()
                        response = Typing.typingInput("Do you want to save and quit? Y/N\n > ").lower()

                        if response == "y":
                            print("")
                            save_game(player)
                            Typing.typingPrint("Ending adventure.....")
                            time.sleep(1)
                            Typing.typingPrint05("\nThank you for playing!")
                            print("")
                            time.sleep(1)
                            Typing.clear_terminal()
                            exit()

                        elif response == "n":
                            print("")
                            Typing.typingPrint("Ending adventure.....")
                            time.sleep(1)
                            Typing.typingPrint05("\nThank you for playing!")
                            print("")
                            time.sleep(1)
                            Typing.clear_terminal()
                            exit()
                        
                        else:
                            Typing.typingPrint05("\nPlease choose between Yes or No.")
                            time.sleep(1)
                            return

                case 6:
                    settings()

        except ValueError:
            Typing.typingPrint05("\nPlease choose from 1-6 only.")
            print("")

show_menu(is_first_time=True)