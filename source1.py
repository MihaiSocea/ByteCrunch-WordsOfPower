import requests
from time import sleep
import random

host = ""
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5

# Word list with costs
word_list = [
    ("Feather", 1), ("Coal", 1), ("Pebble", 1), ("Leaf", 2), ("Paper", 2),
    ("Rock", 2), ("Water", 3), ("Twig", 3), ("Sword", 4), ("Shield", 4),
    ("Gun", 5), ("Flame", 5), ("Rope", 5), ("Disease", 6), ("Cure", 6),
    ("Bacteria", 6), ("Shadow", 7), ("Light", 7), ("Virus", 7), ("Sound", 8),
    ("Time", 8), ("Fate", 8), ("Earthquake", 9), ("Storm", 9), ("Vaccine", 9),
    ("Logic", 10), ("Gravity", 10), ("Robots", 10), ("Stone", 11), ("Echo", 11),
    ("Thunder", 12), ("Karma", 12), ("Wind", 13), ("Ice", 13), ("Sandstorm", 13),
    ("Laser", 14), ("Magma", 14), ("Peace", 14), ("Explosion", 15), ("War", 15),
    ("Enlightenment", 15), ("Nuclear Bomb", 16), ("Volcano", 16), ("Whale", 17),
    ("Earth", 17), ("Moon", 17), ("Star", 18), ("Tsunami", 18), ("Supernova", 19),
    ("Antimatter", 19), ("Plague", 20), ("Rebirth", 20), ("Tectonic Shift", 21),
    ("Gamma-Ray Burst", 22), ("Human Spirit", 23), ("Apocalyptic Meteor", 24),
    ("Earth’s Core", 25), ("Neutron Star", 26), ("Supermassive Black Hole", 35),
    ("Entropy", 45)
]

# Convert word list into a dictionary with IDs
word_dict = {word.lower(): (idx + 1, cost) for idx, (word, cost) in enumerate(word_list)}

# Predefined counter words
sys_word_map = {
    "lion": "Gun", "mirror": "Rock", "fire": "Water", "darkness": "Light",
    "virus": "Vaccine", "earthquake": "Tectonic Shift", "storm": "Thunder",
    "war": "Peace", "disease": "Cure"
}

# Fallback logic: simple keyword matching
keywords = {
    "fire": "Water", "heat": "Ice", "cold": "Flame", "darkness": "Light",
    "flood": "Tsunami", "weapon": "Shield", "war": "Peace", "attack": "Defense",
    "earth": "Earthquake", "storm": "Thunder", "disease": "Cure"
}

def find_best_weapon(sys_word):
    """Finds the best weapon using predefined logic or simple keyword matching."""
    sys_word = sys_word.lower()

    # If there's a predefined counter, use it
    if sys_word in sys_word_map:
        return word_dict[sys_word_map[sys_word].lower()][0]

    # Check if sys_word contains a keyword
    for key, counter in keywords.items():
        if key in sys_word:
            return word_dict[counter.lower()][0]

    # Fallback: return the cheapest weapon
    return min(word_dict.values(), key=lambda x: x[1])[0]

def play_game(player_id):
    """Main function to play the game."""
    for round_id in range(1, NUM_ROUNDS + 1):
        try:
            # Fetch system word
            while True:
                response = requests.get(get_url)
                response_data = response.json()

                sys_word = response_data['word']
                round_num = response_data['round']

                if round_num == round_id:
                    break  # Exit loop when correct round

                sleep(1)  # Wait before retrying

            print(f"Round {round_id} | System Word: {sys_word}")

            # Fetch game status (optional)
            if round_id > 1:
                status_response = requests.get(status_url)
                print(status_response.json())

            # Choose the best counter word
            chosen_word_id = find_best_weapon(sys_word)

            # Submit response
            data = {"player_id": player_id, "word_id": chosen_word_id, "round_id": round_id}
            post_response = requests.post(post_url, json=data)
            print(f"Response: {post_response.json()}")

            sleep(random.uniform(1, 3))  # Random delay to avoid instant responses

        except Exception as e:
            print(f"Error: {e}")

# Example usage
player_id = "Player123"
play_game(player_id)
