import random

from core.ai.brain import brain_process

from core.ai.memory_graph import (
    learn,
    top_topics
)

from core.platform.realtime import (
    live_emit
)


# =========================
# PROCESS
# =========================
def process(user_id, text):

    # =========================
    # LEARN
    # =========================
    learn(user_id, text)


    # =========================
    # BRAIN
    # =========================
    brain = brain_process(user_id, text)

    style = brain["style"]

    intent = brain["intent"]


    # =========================
    # MEMORY CONTEXT
    # =========================
    topics = top_topics(user_id)

    topic_text = ""

    if topics:

        best = topics[0][0]

        topic_text = f"(aklında en çok '{best}' var)"


    # =========================
    # RESPONSE
    # =========================
    if intent == "greeting":

        reply = random.choice([
            "Selam tekrar hoş geldin",
            "Seni görmek iyi oldu",
            "Buradayım 😄"
        ])


    elif intent == "emotion":

        reply = random.choice([
            "İçini dökmek ister misin?",
            "Bugün seni yoran bir şey var gibi.",
            "Biraz anlatabilirsin."
        ])


    elif intent == "fun":

        reply = random.choice([
            "Harbi iyi patladım 🤣",
            "O nasıl enerji dhdhdh",
            "Tam kaos ortamı 😎"
        ])


    elif intent == "question":

        reply = random.choice([
            "Bunu düşünelim.",
            "Güzel soru.",
            "Şöyle bakabiliriz:"
        ])


    else:

        reply = random.choice([
            "Seni dinliyorum.",
            "Devam et.",
            "İlginç geldi."
        ])


    final = f"{reply} {style} {topic_text}"


    # =========================
    # REALTIME EVENT
    # =========================
    live_emit("ai_reply", {
        "user_id": user_id,
        "text": text,
        "reply": final
    })


    return final
