import requests
from time import sleep
import random


host = "172.18.4.158"  
post_url = f"http://172.18.4.158:8000/submit-word"
get_url = f"http://172.18.4.158:8000/get-word"
status_url = f"http://172.18.4.158:8000/status"
NUM_ROUNDS = 5

word_cost = {
    "Feather": 1, "Coal": 1, "Pebble": 1, "Leaf": 2, "Paper": 2, "Rock": 2,
    "Water": 3, "Twig": 3, "Sword": 4, "Shield": 4, "Gun": 5, "Flame": 5,
    "Rope": 5, "Disease": 6, "Cure": 6, "Bacteria": 6, "Shadow": 7, "Light": 7,
    "Virus": 7, "Sound": 8, "Time": 8, "Fate": 8, "Earthquake": 9, "Storm": 9,
    "Vaccine": 9, "Logic": 10, "Gravity": 10, "Robots": 10, "Stone": 11,
    "Echo": 11, "Thunder": 12, "Karma": 12, "Wind": 13, "Ice": 13,
    "Sandstorm": 13, "Laser": 14, "Magma": 14, "Peace": 14, "Explosion": 15,
    "War": 15, "Enlightenment": 15, "Nuclear Bomb": 16, "Volcano": 16,
    "Whale": 17, "Earth": 17, "Moon": 17, "Star": 18, "Tsunami": 18,
    "Supernova": 19, "Antimatter": 19, "Plague": 20, "Rebirth": 20,
    "Tectonic Shift": 21, "Gamma-Ray Burst": 22, "Human Spirit": 23,
    "Apocalyptic Meteor": 24, "Earth’s Core": 25, "Neutron Star": 26,
    "Supermassive Black Hole": 35, "Entropy": 45
}

word_id_map = {word: idx + 1 for idx, word in enumerate(word_cost)}

tool_theme = {
    "defense": ["Shield"],
    "healing": ["Cure", "Vaccine", "Rebirth", "Human Spirit"],
    "anti_disease": ["Cure", "Vaccine", "Bacteria"],
    "force": ["Gun", "Sword", "Rope", "Explosion"],
    "anti_living": ["Gun"],
    "stability": ["Logic", "Time", "Karma", "Gravity"],
    "nature": ["Leaf", "Twig", "Whale", "Moon"],
    "chaos": ["Magma", "Earthquake"],
    "just_a_pebble": ["Pebble"],
    "breaking": ["Rock"],
    "cleaning": ["Water"],
    "cheapest": ["Feather"]
}


reaction_theme = {
    "living": [
        "human", "animal", "life", "man", "woman", "child", "creature", "beast", "lion", "bird",
        "tiger", "organism", "flesh", "mammal", "predator", "person", "baby", "boy", "girl", "adult",
        "parent", "people", "body", "soul", "heart", "being", "citizen", "farmer", "worker", "soldier",
        "villager", "hunter", "native", "family", "friend", "dog", "cat", "fish", "insect"
    ],
    "pebble-beatable": [
        "glass", "mirror", "vase", "bottle", "window", "screen", "lens", "tablet", "phone", "cup", "plate"
    ],
    "disease": [
        "virus", "bacteria", "plague", "infection", "pandemic", "flu", "illness", "fever",
        "contagion", "epidemic", "sickness", "parasite", "germ", "outbreak", "cough", "cancer",
        "diabetes", "cold", "rash", "vomit", "symptom", "tumor", "pain", "headache", "wound", "health", "medicine"
    ],
    "emotion": [
        "anger", "fear", "love", "hate", "rage", "grief", "sorrow", "joy", "pain", "despair", "hope",
        "desire", "lust", "envy", "guilt", "shame", "trust", "pride", "jealousy", "sadness", "happiness",
        "stress", "shock", "loneliness", "confusion", "anxiety", "emotion", "laughter"
    ],
    "chaos": [
        "collapse", "entropy", "chaos", "anarchy", "disorder", "ruin", "confusion", "frenzy", "havoc",
        "descent", "chaotic", "blackhole", "madness", "turmoil", "disarray", "breakdown", "panic", "riot",
        "storm", "rebellion", "revolt", "eruption", "blast", "explosion", "traffic"
    ],
    "weapon": [
        "gun", "sword", "bomb", "tank", "missile", "blade", "cannon", "grenade", "sniper", "rifle",
        "pistol", "axe", "dagger", "projectile", "artillery", "mace", "club", "torpedo", "bullet",
        "nuke", "shotgun", "bow", "arrow", "knife"
    ],
    "magic": [
        "karma", "fate", "spirit", "enlightenment", "soul", "ghost", "mystic", "sorcery", "ritual",
        "curse", "blessing", "divine", "supernatural", "phantom", "magic", "spell", "hex", "charm",
        "witch", "wizard", "miracle", "destiny", "dream"
    ],
    "time": [
        "time", "clock", "era", "timeline", "future", "past", "eternity", "history", "century", "second",
        "hour", "moment", "age", "minute", "instant", "decade", "epoch", "lifetime", "countdown", "calendar"
    ],
    "space": [
        "star", "moon", "planet", "galaxy", "universe", "void", "nebula", "cosmos", "comet", "blackhole",
        "supernova", "astral", "orbit", "vacuum", "meteor", "asteroid", "satellite", "telescope",
        "dimension", "space", "gravity", "sun", "sky", "clouds", "earth"
    ],
    "technology": [
        "robot", "machine", "android", "cyber", "ai", "mechanical", "drone", "technology", "server",
        "network", "circuit", "data", "device", "computer", "screen", "keyboard", "code", "software",
        "hardware", "console", "sensor", "program", "internet", "tv", "remote", "phone", "charger"
    ],
    "nature": [
        "tree", "leaf", "branch", "animal", "river", "whale", "flower", "plant", "ocean", "desert",
        "wind", "storm", "forest", "earth", "sun", "sky", "grass", "root", "mountain", "hill",
        "rain", "sand", "snow", "fog", "volcano", "lake", "cliff", "island"
    ],
    "breakable": [
        "cup", "broom", "glove", "chalk", "glass", "mirror", "plate", "bottle", "window", "screen",
        "shell", "egg", "ice", "vase", "phone", "crystal", "twig", "stick"
    ],
    "misery": [
        "dust", "drought", "thirst", "parched", "arid", "scorched", "barren", "famine", "wilted", "cracked",  
        "desert", "heat", "dryness", "brittle", "sere", "withered", "blistered", "lifeless", "ash", "ember",  
        "charred", "smoke", "fire", "flame", "cinders", "inferno", "burning", "suffocation", "heatwave",  
        "mirage", "dehydration", "hardness", "rigidity", "baking", "sunburn", "desolation", "sandy", "grit",  
        "crumbling", "eroding", "choking", "desiccation", "fractured", "tinder", "kindling", "pyre",  
        "embers", "ashes", "soot", "crusty", "unquenched", "lifelessness", "scorch", "calcified", 
        "scalding", "petrified", "sandstorm", "starvation", "suffering", "poverty", "dusty"
    ],
    "eternal": [
        "immortal", "god", "legend", "phoenix", "eternal", "legacy", "myth", "deity", "infinity", 
        "undying", "resurrection", "everlasting", "timeless", "unchanging", "perpetual", "forever",
        "immortality", "divine", "eternity", "faith", "afterlife"
    ],
    "daily_objects": [
        "chair", "table", "bed", "sofa", "stool", "cupboard", "pillow", "blanket", "spoon", "fork", "knife",
        "plate", "glass", "mirror", "towel", "soap", "pen", "pencil", "paper", "notebook", "book", "bookcase",
        "desk", "whiteboard", "bag", "wallet", "keys", "door", "window", "clock", "trash", "recycling", 
        "tv", "remote", "phone", "charger", "calendar", "computer", "cup", "sink", "stove", "pot", "dish", 
        "fridge", "washing", "machine", "lamp"
    ],
    "food": [
        "food", "coffee", "tea", "milk", "salt", "sugar", "meat", "fruit", "vegetables"
    ],
    "transport": [
        "car", "bike", "bicycle", "bus", "train", "road", "traffic", "map", "helmet"
    ],
    "school": [
        "school", "language", "number", "letter", "question", "answer", "game", "art", "glue", "ruler", "backpack"
    ],
    "noise": [
        "music", "noise", "silence"
    ],
    "sleep": [
        "sleep", "dream", "bed", "pillow", "blanket"
    ],
    "work": [
        "work", "money", "job", "wallet"
    ],
}





bind_theme = {
    "disease": ["anti_disease", "healing"],
    "living": ["anti_living"],
    "emotion": ["stability", "defense"],
    "chaos": ["stability", "defense"],
    "weapon": ["defense", "force"],
    "magic": ["stability"],
    "time": ["stability"],
    "space": ["stability"],
    "technology": ["chaos", "force"],
    "nature": ["force", "defense"],
    "breakable": ["breaking"],
    "pebble_beatable": ["just_a_pebble"],
    "misery": ["cleaning"],
    "eternal": ["cheapest"],

 
    "daily_objects": ["breaking", "cleaning"],
    "food": ["cleaning", "cheapest"],
    "transport": ["chaos", "force"],
    "school": ["stability"],
    "noise": ["stability"],
    "sleep": ["light", "sound"],
    "work": ["stability"]
}




fallback_theme = ["Time"]



def what_beats(system_word):
    sys_lower = system_word.lower()
    matched_themes = []

    for theme, keywords in reaction_theme.items():
        if any(kw in sys_lower for kw in keywords):
            matched_themes.append(theme)

    print(f"🧠 Matched themes for '{system_word}': {matched_themes}")

    candidate_words = []
    for mt in matched_themes:
        counter_categories = bind_theme.get(mt, [])
        for cc in counter_categories:
            candidate_words.extend(tool_theme.get(cc, []))

    if not candidate_words:
        print("⚠️ No theme match — choosing randomly from fallback options.")
        best = random.choice(fallback_theme)
        print(f"🎯 Fallback response: '{best}' (${word_cost[best]})\n")
        return word_id_map[best]

    valid = [w for w in candidate_words if w in word_cost]
    best = min(valid, key=lambda w: word_cost[w])
    print(f"🎯 Chosen response: '{best}' (${word_cost[best]})\n")
    return word_id_map[best]



def play_game(player_id):
    for round_id in range(1, NUM_ROUNDS + 1):
        round_num = -1
        while round_num != round_id:
            response = requests.get(get_url)
            data = response.json()
            sys_word = data['word']
            round_num = data['round']
            sleep(1)

        print(f"\n🌀 Round {round_id} — System Word: {sys_word}")

        if round_id > 1:
            status = requests.get(status_url)
            print("📊 Previous round result:", status.json())

        chosen_word_id = what_beats(sys_word)
        data = {"player_id": player_id, "word_id": chosen_word_id, "round_id": round_id}
        response = requests.post(post_url, json=data)
        print("✅ Submission:", response.json())

if __name__ == "__main__":
    play_game("ePUaEHrl5J")

