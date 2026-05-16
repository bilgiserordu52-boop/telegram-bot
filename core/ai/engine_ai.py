import random


RESPONSES = {
    "selam": ["👋 Selam", "👋 Hey", "👋 Buradayım"],
    "nasılsın": ["İyiyim 👍", "Fena değil", "Gayet stabilim"],
}


def generate(text):

    text = text.lower().strip()

    if "selam" in text:
        return random.choice(RESPONSES["selam"])

    if "nasıl" in text:
        return random.choice(RESPONSES["nasılsın"])

    return random.choice([
        "Bunu anlayamadım",
        "Biraz daha açık yazar mısın?",
        "İlginç..."
    ])
