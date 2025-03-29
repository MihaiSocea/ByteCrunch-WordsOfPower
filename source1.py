import requests
from time import sleep
import random

# ====================== 🔗 API Config ======================

host = "172.18.4.158"  # 👈 Replace with your actual game host URL
post_url = f"http://172.18.4.158:8000/submit-word"
get_url = f"http://172.18.4.158:8000/get-word"
status_url = f"http://172.18.4.158:8000/status"
NUM_ROUNDS = 5

# ====================== 💰 Word List & Cost ======================

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

# ====================== 🧠 Tool Theme (Player Words Grouped) ======================

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

# ====================== 🔍 Reaction Themes (What to Look for in System Words) ======================

reaction_theme = {
    "living": [
        "human", "animal", "life", "man", "woman", "child", "creature", "beast", "lion", "bird",
        "tiger", "organism", "flesh", "mammal", "predator", "person", "baby", "boy", "girl", "adult",
        "parent", "people", "body", "soul", "heart", "being", "citizen", "farmer", "worker", "soldier",
        "villager", "hunter", "native"
    ],
    "pebble-beatable": [
        "glass", "mirror", "vase", "bottle", "window", "screen", "lens", "tablet", "phone"
    ],
    "disease": [
        "virus", "bacteria", "plague", "infection", "pandemic", "flu", "illness", "fever",
        "contagion", "epidemic", "sickness", "parasite", "germ", "outbreak", "cough", "cancer",
        "diabetes", "cold", "rash", "vomit", "symptom", "tumor", "pain", "headache", "wound"
    ],
    "emotion": [
        "anger", "fear", "love", "hate", "rage", "grief", "sorrow", "joy", "pain", "despair", "hope",
        "desire", "lust", "envy", "guilt", "shame", "trust", "pride", "jealousy", "sadness", "happiness",
        "stress", "shock", "loneliness", "confusion", "anxiety", "emotion"
    ],
    "chaos": [
        "collapse", "entropy", "chaos", "anarchy", "disorder", "ruin", "confusion", "frenzy", "havoc",
        "descent", "chaotic", "blackhole", "madness", "turmoil", "disarray", "breakdown", "panic", "riot",
        "storm", "rebellion", "revolt", "eruption", "blast", "explosion"
    ],
    "weapon": [
        "gun", "sword", "bomb", "tank", "missile", "blade", "cannon", "grenade", "sniper", "rifle",
        "pistol", "axe", "dagger", "projectile", "artillery", "mace", "club", "torpedo", "bullet",
        "nuke", "shotgun", "bow", "arrow", "knife"
    ],
    "magic": [
        "karma", "fate", "spirit", "enlightenment", "soul", "ghost", "mystic", "sorcery", "ritual",
        "curse", "blessing", "divine", "supernatural", "phantom", "magic", "spell", "hex", "charm",
        "witch", "wizard", "miracle", "destiny"
    ],
    "time": [
        "time", "clock", "era", "timeline", "future", "past", "eternity", "history", "century", "second",
        "hour", "moment", "age", "minute", "instant", "decade", "epoch", "lifetime", "countdown"
    ],
    "space": [
        "star", "moon", "planet", "galaxy", "universe", "void", "nebula", "cosmos", "comet", "blackhole",
        "supernova", "astral", "orbit", "vacuum", "meteor", "asteroid", "satellite", "telescope",
        "dimension", "space", "gravity"
    ],
    "technology": [
        "robot", "machine", "android", "cyber", "ai", "mechanical", "drone", "technology", "server",
        "network", "circuit", "data", "device", "computer", "screen", "keyboard", "code", "software",
        "hardware", "console", "sensor", "program"
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
    ]
}



# ====================== 🔁 Bind Theme (reaction → tool themes) ======================

bind_theme = {
    "disease": ["anti_disease", "healing"],
    "living": ["anti_living"],
    "emotion": ["stability", "defense"],
    "chaos": ["stability", "defense"],
    "weapon": ["defense", "force"],
    "magic": ["logic", "stability"],
    "time": ["stability"],
    "space": ["stability"],
    "technology": ["chaos", "force"],
    "nature": ["force", "defense", "anti_nature"],
    "breakable": ["breaking"],
    "pebble_beatable":["just_a_pebble"],
    "misery": ["cleaning"],
    "eternal": ["cheapest"]
}


# ====================== ♻️ Fallback (if no match) ======================

fallback_theme = ["Time"]

# ====================== 🤖 what_beats() Logic ======================

def what_beats(system_word):
    sys_lower = system_word.lower()
    matched_themes = []

    # Step 1: Check which themes match the system word
    for theme, keywords in reaction_theme.items():
        if any(kw in sys_lower for kw in keywords):
            matched_themes.append(theme)

    print(f"🧠 Matched themes for '{system_word}': {matched_themes}")

    candidate_words = []

    # Step 2: Gather tools from matched counter-themes
    for mt in matched_themes:
        counter_categories = bind_theme.get(mt, [])
        for cc in counter_categories:
            candidate_words.extend(tool_theme.get(cc, []))

    # Step 3: If no matches, randomly choose from fallback
    if not candidate_words:
        print("⚠️ No theme match — choosing randomly from fallback options.")
        best = random.choice(fallback_theme)
        print(f"🎯 Fallback response: '{best}' (${word_cost[best]})\n")
        return word_id_map[best]

    # Step 4: Choose cheapest valid word from matched candidates
    valid = [w for w in candidate_words if w in word_cost]
    best = min(valid, key=lambda w: word_cost[w])
    print(f"🎯 Chosen response: '{best}' (${word_cost[best]})\n")
    return word_id_map[best]

# ====================== 🎮 Game Loop ======================

def play_game(player_id):
    for round_id in range(1, NUM_ROUNDS + 1):
        round_num = -1
        while round_num != round_id:
            response = requests.get(get_url)
            data = response.json()
            # print(f"⏳ Waiting for Round {round_id} | Server says: Round {data['round']} - Word: {data['word']}")
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
    play_game("ePUaEHrl5J")  # replace with your player_id

