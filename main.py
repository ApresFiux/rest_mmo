import os
import random

from flask import Flask, request, jsonify, abort, redirect, session

from charecter import Character

"""
 Define Characters
"""
magic_gladiator = Character(500, 800, 400, 50, '1', 'Magic Gladiator')
super_knight = Character(600, 50, 350, 40, '2', 'Super Knight')
evil_elf = Character(800, 600, 250, 30, '3', 'Evil Elf')

characters_list = [magic_gladiator, super_knight, evil_elf]
characters = {
    char.id: char.name for char in characters_list
}

magic_gladiator = {'id': 1, 'name': 'Magic Gladiator'}

welcome_msg = 'Welcome, '
api = Flask(__name__)
api.config.update({
    'SECRET_KEY': os.urandom(32)
})

main_data = {}


@api.route('/start_game', methods=['GET', 'POST'])
def start_new_game():
    if request.method == 'GET':
        if 'user_chose' not in session and 'game_began' not in session:
            session['initial'] = True
            session['_id'] = os.urandom(12)
            return jsonify({'Please select Charecter': characters})
        elif 'user_chose' in session and 'game_began' not in session:
            session['enemy_chose'] = True
            return jsonify({'Please select Enemy': globals()['enemies']})
        elif 'game_began' in session and 'began_get' not in session:
            session['began_get'] = True
            return jsonify('you can start posing attacks')
        elif 'began_get' in session:
            return jsonify({'current state':
                                {'your char':
                                     {'hp': main_data[session['_id']]['char'].hp,
                                      'mp': main_data[session['_id']]['char'].mp
                                      },
                                 'enemy':
                                     {'hp': main_data[session['_id']]['enemy'].hp,
                                      'mp': main_data[session['_id']]['enemy'].mp
                                      }
                                 }
                            })
    elif request.method == 'POST' and request.content_type == 'application/json':
        if 'initial' not in session:
            return redirect('/start_game')

        if 'user_chose' not in session:
            json_data = request.data.decode()
            user_chose = [char for char in characters_list if json_data == char.id or json_data == char.name]
            if not user_chose:
                return jsonify('Bad Choice! Try again!')
            else:
                user_chose = user_chose[0]
            session['user_chose'] = user_chose.id
            main_data[session['_id']] = {'char': Character(user_chose.hp, user_chose.mp,
                                                           user_chose.armor, user_chose.power,
                                                           user_chose.id, user_chose.name)
                                         }

            globals()['enemies'] = {
                char.id: char.name for char in characters_list if char != user_chose
            }
            return jsonify(
                f"Great! you choose {user_chose.name}! Now, please choose your enemy: {globals()['enemies']}")

        elif 'user_chose' in session and 'enemy' not in session:
            if 'enemy_chose' not in session or 'game_began' in session:
                return redirect('/start_game')

            json_data = request.data.decode()
            enemy = [char for char in characters_list if
                     (json_data == char.id or json_data == char.name) and char.id != session['user_chose']]
            if not enemy:
                return jsonify('Bad Choice! Try again!')
            else:
                enemy = enemy[0]
            session['game_began'] = True
            session['enemy'] = True
            main_data[session['_id']].update({'enemy': Character(enemy.hp, enemy.mp,
                                                                 enemy.armor, enemy.power,
                                                                 enemy.id, enemy.name)
                                              })
            session['enemy_chose'] = True
            return jsonify(f"Cool! your enemy is {enemy.name}!")

        elif 'game_began' in session:
            json_data = request.data.decode()
            if json_data == 'attack':
                session_data = main_data[session['_id']]
                char_attack = random.randint(session_data['char'].power - 30, session_data['char'].power)
                char_hit = random.randint(session_data['enemy'].power - 30, session_data['enemy'].power)
                dmg_received = session_data['char'].receive_hit(char_hit)
                dmg_done = session_data['enemy'].receive_hit(char_attack)
                if dmg_received == 'Character Dead':
                    return jsonify(f'Your character: Character Dead')
                if dmg_done == 'Character Dead':
                    return jsonify('enemy is dead! you won!')
                return jsonify(f"your hit power was {dmg_done}, enemy's - ${dmg_received}.")
            else:
                return jsonify("type 'attack'")
    else:
        abort(405)


if __name__ == '__main__':
    api.run
