MEMORY_GRAPH = {}


# =========================
# INIT
# =========================
def ensure_user(user_id):

    if str(user_id) not in MEMORY_GRAPH:

        MEMORY_GRAPH[str(user_id)] = {
            "topics": {},
            "emotion_score": 0,
            "interaction_count": 0
        }


# =========================
# LEARN
# =========================
def learn(user_id, text):

    ensure_user(user_id)

    user = MEMORY_GRAPH[str(user_id)]

    user["interaction_count"] += 1


    words = text.lower().split()


    for word in words:

        if len(word) < 4:
            continue

        current = user["topics"].get(word, 0)

        user["topics"][word] = current + 1


    # emotional score
    emotional_words = [
        "üzgün",
        "yalnız",
        "mutlu",
        "sinir",
        "moral"
    ]

    for e in emotional_words:

        if e in text.lower():

            user["emotion_score"] += 1


# =========================
# TOPICS
# =========================
def top_topics(user_id, limit=5):

    ensure_user(user_id)

    topics = MEMORY_GRAPH[str(user_id)]["topics"]

    ordered = sorted(
        topics.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ordered[:limit]
