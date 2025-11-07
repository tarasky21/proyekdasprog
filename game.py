import random
import time
import game_env
import game_string
import json
import os

#tes

player1 = {
    'Ability' : {
        'Strength' : 2,
        'Dexterity' : 3,
        'Constitution' : 2,
        'Wisdom' : 3
    },
    'Status' : {
        'Health' : 0,
        'AC' : 0,
        'Position' : 0,
        'Mana' : 0,
        'In Combat' : False
    },
 
    'Buah' : {
        'Jeruk' : 0,
        'Naga' : 0,
        'Pepaya' : 0,
        'Mangga' : 0
    },
    'Equipment' : {
        'Armor' : 'Cloth',
        'Weapon' : 'Shortsword',
    },
    'Spell' : dict()
}

json_path = os.path.join(os.path.dirname(__file__), "savefiles", "current_progress.json") #JSON save path
enemy = dict()
d_weapon_damage = game_env.weapon[player1['Equipment']['Weapon']]
help_command = game_string.help_command
#------------------------Else functions----------------------

def delay(sec):
    time.sleep(sec)
    return ''

def set_in_combat(value):
    player1['Status']['In Combat'] = value

def dice(x):
    return random.randint(1, x) if x > 0 else 0

def modifier(mod):
    if mod == 'con':
        pass

#------------------------Spawn functions----------------------

def spawn_enemy():
    name = random.choice(game_env.enemy_all)
    enemy['Name'] = name
    enemy['Health'] = game_env.enemy[name][0]
    enemy['DMG'] = game_env.enemy[name][1]
    enemy['SPD'] = game_env.enemy[name][2]
    enemy['Effect'] = 'None'

def spawn_loot():
    d_100 = random.randint(1, 100)
    # 30% fruit, 10% weapon, 10% armor, 10% spell scroll, 20% mana potion, 20% health potion
    if d_100 > 70:
        fruit = random.choice(game_env.buah)
        player1['Buah'][fruit] += 1
        print(f'Kamu menemukan buah: {fruit}!')
        delay(1)
        print(f'Jumlah sekarang: {player1["Buah"][fruit]}')
        return True
    elif d_100 >= 60:
        weapon = random.choice(game_env.weapon_all)
        print(f'Kamu menemukan senjata: {weapon}. Saat ini kamu memakai: {player1["Equipment"]["Weapon"]}')
        delay(1)
        ans = input('Apakah ingin mengganti senjata dengan yang ditemukan? (y/n) ').strip().lower()
        if ans and ans[0] == 'y':
            player1['Equipment']['Weapon'] = weapon
            print(f'Senjata diganti menjadi {weapon}.')
        return True
    elif d_100 >= 50:
        armor = random.choice(game_env.armor_all)
        print(f'Kamu menemukan armor: {armor}. Saat ini kamu memakai: {player1["Equipment"]["Armor"]}')
        delay(1)
        ans = input('Apakah ingin mengganti armor dengan yang ditemukan? (y/n) ').strip().lower()
        if ans and ans[0] == 'y':
            player1['Equipment']['Armor'] = armor
            print(f'Armor diganti menjadi {armor}.')
        return True
    elif d_100 >= 40:
        spell = random.choice(game_env.spell_all)
        print(f'Kamu menemukan spell scroll: {spell}. Kamu bisa cast spell ini saat pertarunganmu nanti.')
        delay(1)
        player1['Spell'][spell] = game_env.spell[spell]
        return True
    elif d_100 >= 20:
        # simple mana potion
        player1['Status']['Mana'] += 4
        print(f'Kamu menemukan sebuah mana potion. +4 Mana.')
        delay(1)
        return True
    else:
        # simple health potion
        player1['Status']['Health'] += 10
        print(f'Kamu menemukan sebuah health potion. +10 Health.')
        delay(1)
        return True

#------------------------Handler functions----------------------
def death_handler():
    if player1['Status']['Health'] > 0:
        return 0
    else:
        print(f'Health kamu habis, kamu kalah dalam permainan!{delay(1)}\n')
        return 1

def jalan_handler():
    if player1['Status']['In Combat'] == True:
        print('Kamu tidak dapat melanjutkan perjalanan saat dalam pertarungan\
            \nSelesaikan pertarungan ini atau ketik "help combat"')
        return 0
    player1['Status']['Position'] += 75
    print('Kamu berjalan sejauh 75 meter.')
    print('Jarak dari rumahmu sekarang adalah', player1['Status']['Position'], 'meter.')
    d_10 = dice(10)
    if d_10 < 4:
        result = combat_handler()
        if result == 1:
            return 1
    if d_10 > 6:
        spawn_loot()
        

def exit_handler():
    print('Terimakasih telah bermain!')
    exit()
    

def cek_handler(category):
    if category.capitalize() not in player1 :
        print('Kategori tidak ditemukan. ketik "help cek"')
        return 0
    print('---' + category.capitalize() + '---')
    for item, value in player1[category.capitalize()].items():
        print(f'{item}: {value}')
    return 0

def help_handler(category):
    if category not in help_command :
        print('Kategori tidak ditemukan.')
        return 0
    for item in help_command[category]:
        print(item)

def serang_handler():
    if dice(20) > 9:
        damage = dice(d_weapon_damage) + player1['Ability']['Strength']
        enemy['Health'] -= damage
        print(f'Kamu menyerang musuh dan memberikan {damage} damage!')
        return 1
    else:
        print('Kamu gagal menyerang musuh!')
        return 1


def spell_handler(spell):
    spell = spell.capitalize()
    if spell not in player1['Spell']:
        print('Spell tidak diketahui.')
        return 0
    d_hit = dice(20)
    if d_hit > 9:
        print('Hit!')
        damage = game_env.spell[spell][1]
        enemy['Health'] -= damage
        enemy['Effect'] = game_env.spell[spell][2]
        return 1
    else:
        print('Tidak hit!')
        return 1

def kabur_handler():
    d_kabur = dice(20)
    if d_kabur + player1['Ability']['Dexterity'] > 12 + enemy['SPD']:
        print('Kamu berhasil kabur dari musuh')
        set_in_combat(False)
        print('Masukan perintah cek, jalan, help, atau exit.')
        return 0
    else:
        print('Kamu gagal kabur dari musuh')
        return 1

def enemy_handler():
    if enemy['Health'] <= 0:
        print(f'Kamu mengalahkan {enemy["Name"]}!')
        delay(1)
        if dice(2) == 1:
            spawn_loot()
        set_in_combat(False)
        enemy.clear()
        print('Masukan perintah cek, jalan, help, atau exit.')
        return
    d_20 = dice(20)
    if d_20 >= player1['Status']['AC']:
        print(f'Kamu terkena damage {enemy['DMG']} serangan musuh!')
        player1['Status']['Health'] -= enemy['DMG']
    else:
        print(f'{enemy['Name']} mencoba menyerang kamu, tetapi tidak kena!')

#------------------------Command maps----------------------

command_map = {
    'jalan': jalan_handler,
    'exit': exit_handler,
    'cek': lambda arg= None: cek_handler(arg) if arg else print('Kategori harus disebutkan. ketik "help cek"'),
    'help': lambda arg= None: help_handler(arg) if arg else print('Kategori harus disebutkan.'),
}

combat_command = {
    'cek': lambda arg= None: cek_handler(arg) if arg else print('Kategori harus disebutkan. ketik "help cek"'),
    'exit': exit_handler,
    'help': lambda arg= None: help_handler(arg) if arg else print('Kategori harus disebutkan.'),
    'serang' : serang_handler,
    'kabur' : kabur_handler,
    'spell' : spell_handler,
    'jalan' : jalan_handler
}

#------------------------ Main handlers----------------------

def combat_handler():
    spawn_enemy()
    print(f"{enemy['Name']} muncul dari semak-semak!\nKetik serang, spell, atau kabur.")
    set_in_combat(True)
    while player1['Status']['In Combat'] == True and player1['Status']['Health'] > 0:
        input_player = input('>>>>>').lower()
        input_player = tuple(input_player.split(' '))
        if input_handler(*input_player) == 1:
            enemy_handler()
        if death_handler() == 1:
            set_in_combat(False)
            return 1
    return 0

def input_handler(*args):
    if not args or args[0] == "":
        print("Masukkan perintah.")
        return
    cmd = args[0]
    arg = args[1] if len(args) > 1 else None
    func = command_map.get(cmd) if not player1['Status']['In Combat'] else combat_command.get(cmd)
    if func:
        if arg is not None:
            return func(arg)
        else:
            return func()
    else:
        print('Perintah tidak dikenal.')

def start():
    player1['Status']['Health'] = game_env.status_base['Health'] + player1['Ability']['Constitution'] * 3
    player1['Status']['AC'] = game_env.status_base['AC']\
        + player1['Ability']['Dexterity']\
        + game_env.armor[player1['Equipment']['Armor']]

def run_game():
    print('Objective adalah tujuan utama dalam permainan ini, yaitu mengumpulkan buah-buahan tertentu sampai 5.\
        \nKamu akan berjalan menjauh dari rumahmu, dan menghadapi berbagai musuh serta mengumpulkan buah-buahan\
        \nMasukan perintah cek, jalan, help, atau exit untuk memulai permainan.')
    while True:
        input_player = input('>>>>>').lower()
        input_player = tuple(input_player.split(' '))
        result = input_handler(*input_player)
        if result == 1:
            break

def main():
    while True:
        set_in_combat(False)
        start()
        run_game()
        retry_answer = input('Kamu kalah! Ingin coba lagi? (y/n)').strip().lower()
        if retry_answer != 'y':
            print('Terimakasih telah bermain!')
            break


main()
