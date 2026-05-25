states_full = {
    "in_progress": "Matchmaking in Progress",
    "team_selection": "Select 3 Pokemon to send into battle",
    "combat_fight_or_team": "FIGHT",
    # "combat_attack": "", # brauch ich das ueberhaupt? einfach random
    "combat_switch": "Moves & More",
    "continue": "Continue Battling",
}

states_cut = {
    "in_progress": "Matchmaking",
    "team_selection": "send into battle",
    "combat_fight_or_team": "Battle info",
    "combat_attack": "FIGHT",
    "combat_switch": "Moves",
    "continue": "Continue Battling",
}


def check_state(data_text):
    # ToDo: maybe use fuzzy search?
    for key, val in states_cut.items():
        if val in data_text:
            print("current state:", key)


if __name__ == "__main__":
    dummy_data = ['', '', '', '', '  ', ' ', '', ' ', '  ', '', '', '', '=', '', '', '', '—<—-', '', '', '', '=', '',
            'asceneue',
            '', '', '', 'on', '', '', '', 'Continue', 'Battling', '', '', '', 'a']
    data_text = " ".join(dummy_data)
    check_state(data_text)
