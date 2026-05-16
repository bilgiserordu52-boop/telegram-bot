from core.features.registry import register_feature


def evolve_feature(name, response_text=None):
    name = name.strip().lower()

    if response_text is None:
        response_text = f"AI generated response for '{name}'"

    def dynamic_feature():
        return {
            "status": "ok",
            "response": response_text,
            "feature": name,
            "evolved": True
        }

    register_feature(name, dynamic_feature)

    return {
        "status": "evolved",
        "feature": name
    }
