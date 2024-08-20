import json

# Movimientos básicos que ambos personajes comparten
BASIC_MOVES = {
    "P": ("Puño", 1),
    "K": ("Patada", 1)
}

# Movimientos especiales para cada personaje
SPECIAL_MOVES = {
    "Tonyn": {
        "DSD+P": ("Taladoken", 3),
        "SD+K": ("Remuyuken", 2)
    },
    "Arnaldor": {
        "SA+K": ("Remuyuken", 3),
        "ASA+P": ("Taladoken", 2)
    }
}

# Texto para mostrar los movimientos de los personajes
MOVEMENTS_TEXT = {
    "Tonyn": {
        "D": "Tonyn avanza",
        "A": "Tonyn retrocede",
        "S": "Tonyn se agacha",
        "W": "Tonyn se salta"
    },
    "Arnaldor": {
        "D": "Arnaldor retrocede",
        "A": "Arnaldor avanza",
        "S": "Arnaldor se agacha",
        "W": "Arnaldor salta"
    }
}

MAX_ENERGY = 6


class Fighter:
    def __init__(self, name):
        self.name = name
        self.energy = MAX_ENERGY
        self.moves = self.get_moves()

    def get_moves(self):
        # Combina movimientos básicos con los movimientos especiales del personaje
        moves = BASIC_MOVES.copy()
        moves.update(SPECIAL_MOVES.get(self.name, {}))
        return moves

    def _get_special_attack(self, move_str):
        special_attack = None
        for special in self.moves:
            if '+' not in special:
                continue
            if special in move_str:
                return special
        # return special_attack

    def _format_battle_str(self, move_seq, attack):
        if move_seq and attack:
            return f"{move_seq}+{attack}"
        elif move_seq:
            return move_seq
        elif attack:
            return attack

    def _format_movements_output_text(self, movements, ):
        text = ''
        for move in movements:
            if move == '+':
                break
            text += f"{MOVEMENTS_TEXT[self.name][move]}. "

        return text

    def _format_attack_output_text(self, attack):
        if attack:
            return f"{self.name} ataca con {self.moves[attack][0]}(-{self.moves[attack][1]} de energía)"

        return ''

    def _format_output_text(self, movements, attack):
        movement_text = self._format_movements_output_text(movements)
        attack_text = self._format_attack_output_text(attack)
        if movement_text == '':
            return attack_text
        if attack_text == '':
            return movement_text
        return f"{movement_text} {attack_text}"

    def attack(self, movements, attack):
        move_str = self._format_battle_str(movements, attack)
        special_move = self._get_special_attack(move_str)

        if special_move:
            move_str = move_str.replace(special_move, "")
            movements = move_str.replace(special_move, "")
            attack = special_move

        print(self._format_output_text(movements, attack))

        if attack in self.moves:
            move_name, damage = self.moves[attack]
            return move_name, damage
        else:
            return None, 0


def determine_first_turn(player1_data, player2_data):
    # Determinamos quién tiene el primer turno
    p1_mov_count = len(list(filter(None, player1_data['movimientos'])))
    p1_atk_count = len(list(filter(None, player1_data['golpes'])))
    p1_total_moves = p1_mov_count + p1_atk_count

    p2_mov_count = len(list(filter(None, player2_data['movimientos'])))
    p2_atk_count = len(list(filter(None, player2_data['golpes'])))
    p2_total_moves = p2_mov_count + p2_atk_count

    if p2_total_moves < p1_total_moves:
        return 2
    elif p2_mov_count < p1_mov_count:
        return 2
    elif p2_atk_count < p1_atk_count:
        return 2
    else:
        return 1


def simulate_fight(player1_data, player2_data):
    tonyn = Fighter("Tonyn")
    arnaldor = Fighter("Arnaldor")

    turn = determine_first_turn(player1_data, player2_data)
    print(f'{"Tonyn" if turn == 1 else "Arnaldor"} comienza la pelea')

    while tonyn.energy > 0 and arnaldor.energy > 0:
        if turn == 1:
            # Tonyn ataca
            turn = 2
            move = player1_data['movimientos'].pop(0) if player1_data['movimientos'] else ""
            attack = player1_data['golpes'].pop(0) if player1_data['golpes'] else ""

            move_name, damage = tonyn.attack(move, attack)
            if move_name:
                arnaldor.energy -= damage
                if arnaldor.energy <= 0:
                    print(f"Tonyn Gana la pelea y aun le queda {tonyn.energy} de energía")
                    return
        else:
            # Arnaldor ataca
            turn = 1
            move = player2_data['movimientos'].pop(0) if player2_data['movimientos'] else ""
            attack = player2_data['golpes'].pop(0) if player2_data['golpes'] else ""
            move_name, damage = arnaldor.attack(move, attack)
            if move_name:
                tonyn.energy -= damage
                if tonyn.energy <= 0:
                    print(f"Arnaldor Gana la pelea y aun le queda {arnaldor.energy} de energía")
                    return


# read a json file
battle = json.load(open('data/battle.json'))
simulate_fight(battle["player1"], battle["player2"])
