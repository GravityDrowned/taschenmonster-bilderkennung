states_cut = {
    "in_progress": "Matchmaking",
    "team_selection": "send into battle",
    "combat_fight_or_team": "Battle info",
    "mega_evolve": "MEGA EVOLVE",
    "combat_attack": "FIGHT",
    "combat_switch": "Moves",
    "continue": "Continue Battling",
}


def get_states(data_text):
    keys = []
    for key, val in states_cut.items():
        if val in data_text:
            keys.append(key)
            #print("current state:", key)
    return keys
