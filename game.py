import random
import time
import game_env
import game_string
import json
import os

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

def delay(sec): #ini fungsi delay, nanti penggunaannya delay(detik)
    time.sleep(sec)
    return ''

def set_in_combat(value): #ini buat ngubah "In Combat". fungsinya nanti biar ada beberapa perintah yang ga bisa dijalanin kalo lagi battle atau kebalikannya
    player1['Status']['In Combat'] = value

def dice(x): #ini randomize dadu aja 
    return random.randint(1, x) if x > 0 else 0

def modifier(mod): #ini modifier stats buat awal game. belom jadi
    if mod == 'con':
        pass

#------------------------Spawn functions----------------------

def spawn_enemy(): #ini tadi buat ngasih stats ke musuh
    name = random.choice(game_env.enemy_all)
    enemy['Name'] = name
    enemy['Health'] = game_env.enemy[name][0]
    enemy['DMG'] = game_env.enemy[name][1]
    enemy['SPD'] = game_env.enemy[name][2]
    enemy['Effect'] = 'None'

def spawn_fruit(): 
    fruit = random.choice(game_env.buah)
    player1['Buah'][fruit] += 1
    print(f'Kamu menemukan buah: {fruit}!')
    delay(1)
    print(f'Jumlah sekarang: {player1["Buah"][fruit]}')
    return True

def spawn_weapon():
    armor = random.choice(game_env.armor_all)
    print(f'Kamu menemukan armor: {armor}. Saat ini kamu memakai: {player1["Equipment"]["Armor"]}')
    delay(1)
    ans = input('Apakah ingin mengganti armor dengan yang ditemukan? (y/n) ').strip().lower()
    if ans and ans[0] == 'y':
        player1['Equipment']['Armor'] = armor
        print(f'Armor diganti menjadi {armor}.')
    return True

def spawn_armor():
    armor = random.choice(game_env.armor_all)
    print(f'Kamu menemukan armor: {armor}. Saat ini kamu memakai: {player1["Equipment"]["Armor"]}')
    delay(1)
    ans = input('Apakah ingin mengganti armor dengan yang ditemukan? (y/n) ').strip().lower()
    if ans and ans[0] == 'y':
        player1['Equipment']['Armor'] = armor
        print(f'Armor diganti menjadi {armor}.')
    return True

def spawn_scroll():
    spell = random.choice(game_env.spell_all)
    print(f'Kamu menemukan spell scroll: {spell}. Kamu bisa cast spell ini saat pertarunganmu nanti.')
    delay(1)
    player1['Spell'][spell] = game_env.spell[spell]
    return True

def spawn_potion(potion):
    match potion:
        case 'mana':
            player1['Status']['Mana'] += 4
            print('Kamu menemukan sebuah mana potion. +4 Mana.')
            delay(1)
            return True
        case 'health':
            # simple health potion
            player1['Status']['Health'] += 10
            print('Kamu menemukan sebuah health potion. +10 Health.')
            delay(1)
            return True

def spawn_loot(): #ini buat spawn loot random. palingan nanti tiap loot bakal dibikin fungsi baru lagi aja
    d_100 = random.randint(1, 100)
    # 30% fruit, 10% weapon, 10% armor, 10% spell scroll, 20% mana potion, 20% health potion
    if d_100 > 70:
        return spawn_fruit()
    elif d_100 >= 60:
        return spawn_weapon()
    elif d_100 >= 50:
        return spawn_armor()
    elif d_100 >= 40:
        return spawn_scroll()
    elif d_100 >= 20:
        return spawn_potion('mana')
    else:
        return spawn_potion('health')
        

#------------------------Handler functions----------------------
def death_handler(): #ini kalau player mati
    if player1['Status']['Health'] > 0:
        return 0
    else:
        print('Health kamu habis, kamu kalah dalam permainan!')
        delay(1)
        return 1

def jalan_handler(): #ini kalau player input jalan. niatnya setelah beberapa ratus/ribu meter nanti ganti
    #environment yang dimana musuh sama kondisinya ada yang beda
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
        

def exit_handler(): #buat keluar dari game
    print('Terimakasih telah bermain!')
    exit()
    

def cek_handler(category): #mirip mirip sama help_handler
    if category.capitalize() not in player1 :
        print('Kategori tidak ditemukan. ketik "help cek"')
        return 0
    print('---' + category.capitalize() + '---')
    for item, value in player1[category.capitalize()].items():
        print(f'{item}: {value}')
    return 0

def help_handler(category): #ini kalau player input "help"
    if category not in help_command :
        print('Kategori tidak ditemukan.')
        return 0
    for item in help_command[category]: #ngambil dari help_command sesuai kategori help nya
        print(item)

def serang_handler(): #ini kalau player nyerang
    if dice(20) > 9:
        damage = dice(d_weapon_damage) + player1['Ability']['Strength']
        enemy['Health'] -= damage
        print(f'Kamu menyerang musuh dan memberikan {damage} damage!')
        return 1
    else:
        print('Kamu gagal menyerang musuh!')
        return 1


def spell_handler(spell): #ini belom jadi. niatnya buat spell tadi.
    #jadi disini, spell bakalan ngasih efek berbeda tiap jenisnya
    spell = spell.capitalize()
    if spell not in player1['Spell']:
        print('Spell tidak diketahui.')
        return 0
    d_hit = dice(20)
    if d_hit > 9:
        print('Hit!')
        damage = game_env.spell[spell][1]
        enemy['Health'] -= damage
        enemy['Effect'] = game_env.spell[spell][2] #efek spell, kayaknya bakal gw ubah lagi nanti
        return 1
    else:
        print('Tidak hit!')
        return 1

def kabur_handler(): #ini buat player kabur pas combat
    d_kabur = dice(20)
    if d_kabur + player1['Ability']['Dexterity'] > 12 + enemy['SPD']:
        print('Kamu berhasil kabur dari musuh')
        set_in_combat(False)
        print('Masukan perintah cek, jalan, help, atau exit.')
        return 0
    else:
        print('Kamu gagal kabur dari musuh')
        return 1

def enemy_handler(): #ini buat ngejalanin musuh. jadi musuh nyerang sama mati ada disini. ini dipanggil pas combat
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
#jadi bakal ngejalanin fungsi sesuai input pemain
command_map = { #ini command saat ngga combat
    'jalan': jalan_handler,
    'exit': exit_handler,
    'cek': lambda arg= None: cek_handler(arg) if arg else print('Kategori harus disebutkan. ketik "help cek"'),
    'help': lambda arg= None: help_handler(arg) if arg else print('Kategori harus disebutkan.'),
}

combat_command = { #ini command saat combat
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
            enemy_handler() #disini dipanggilnya. jadi setelah giliran player, musuh juga jalan/aksi
        if death_handler() == 1:
            set_in_combat(False)
            return 1
    return 0

def input_handler(*args): #ini buat ngehandle input playernya
    if not args or args[0] == "": #ini pake *args biar bisa ngambil 2 kata
        #jadi player bisa masukin "cek" atau "cek status"
        print("Masukkan perintah.")
        return
    cmd = args[0]
    arg = args[1] if len(args) > 1 else None
    func = command_map.get(cmd) if not player1['Status']['In Combat'] else combat_command.get(cmd)
    #ini func buat ngambil command map yang dipake
    if func:
        if arg is not None:
            return func(arg)
        else:
            return func()
    else:
        print('Perintah tidak dikenal.')

def start(): #ini buat masukin base stats nya
    player1['Status']['Health'] = game_env.status_base['Health'] + player1['Ability']['Constitution'] * 3
    player1['Status']['AC'] = game_env.status_base['AC']\
        + player1['Ability']['Dexterity']\
        + game_env.armor[player1['Equipment']['Armor']]

def run_game(): #Ini fungsi buat ngejalanin game nya 
    print('Objective adalah tujuan utama dalam permainan ini, yaitu mengumpulkan buah-buahan tertentu sampai 5.\
        \nKamu akan berjalan menjauh dari rumahmu, dan menghadapi berbagai musuh serta mengumpulkan buah-buahan\
        \nMasukan perintah cek, jalan, help, atau exit untuk memulai permainan.')
    while True:
        input_player = input('>>>>>').lower()
        input_player = tuple(input_player.split(' '))
        result = input_handler(*input_player)
        if result == 1:
            break

def main(): #Ini fungsi buat main game nya. jadi bisa retry dan ngeloop terus kalo pengen retry.
    while True:
        set_in_combat(False)
        start()
        run_game()
        retry_answer = input('Kamu kalah! Ingin coba lagi? (y/n)').strip().lower()
        if retry_answer != 'y':
            print('Terimakasih telah bermain!')
            break

main()

#TO-DO:
# Spell Action
# Win condition

#okeoke
#bagian spell nya belom gw koding jadi error
