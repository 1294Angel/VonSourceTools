"""
Static data and constants used throughout VonSourceTools.
"""

MODEL_TYPE_CATEGORY_MAP = {
    "NPC": [
        "Basic", "Movement", "Combat", "Gestures",
        "NPC_Reactions", "Signals_Commands", "Interaction",
        "Swimming", "Vehicles", "Scripted_Sequences"
    ],
    "CHARACTER": [
        "Basic", "Movement", "Combat", "Gestures",
        "NPC_Reactions", "Signals_Commands", "Interaction",
        "Swimming", "Vehicles", "Scripted_Sequences"
    ],
    "VIEWMODEL": ["Viewmodel"],
    "PROP": [],
    "WORLDMODEL": []
}

NONE_ENUM = ("NONE", "None", "")