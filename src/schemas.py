BRIEF_SCHEMA ={
    "type": "object",
    "additionalProperties": False,
    "properties":{
        "level": {"type": "integer", "minimum": 1, "maximum": 3},
        "ability_method": {"type": "string", "enum": ["point_buy"]},
        "playstyle":{"type": "array", "items": {"type": "string"}},
        "preferred_classes": {"type": "array", "items": {"type": "string"}},
        "preferred_lineages": {"type":"array", "items":{"type":"string"}},
        "preferred_backgrounds": {"type":"array", "items":{"type":"string"}},
        "tone":{"type": "string"},
        "combat_focus": {"type": "string"},
        "roleplay_focus": {"type": "string"},
        "constraints": {"type": "array", "items": {"type": "string"}}
    },
    "required": [
        "level",
        "ability_method",
        "playstyle",
        "preferred_classes",
        "preferred_lineages",
        "preferred_backgrounds",
        "tone",
        "combat_focus",
        "roleplay_focus",
        "constraints"
    ]
}

CHARACTER_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "meta": {
            "type": "object",
            "additionalProperties": False,
            "properties":{
                "system": {"type": "string"},
                "level": {"type": "integer"},
                "ability_method": {"type": "string"},
                "sourcebooks": {"type": "array","items":{"type":"string"}},
                "playstyle": {"type": "array", "items": {"type": "string"}},
                "constraints": {"type": "array", "items":{"type": "string"}}
            },
            "required": ["system", "level", "ability_method", "sourcebooks", "playstyle", "constraints"]
        },
        "identity": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "name": {"type": "string"},
                "lineage": {"type": "string"},
                "class": {"type": "string"},
                "subclass": {"type": ["string", "null"]},
                "background": {"type": "string"},
                "alignment": {"type": "string", "enum": [
                    "Lawful Good", "Neutral Good", "Chaotic Good",
                    "Lawful Neutral", "Neutral", "Chaotic Neutral",
                    "Lawful Evil", "Neutral Evil", "Chaotic Evil"
                    ]}
            },
            "required": ["name", "lineage", "class", "subclass", "background", "alignment"]
        },
        "abilities": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "str": {"type": "integer"},
                "dex": {"type": "integer"},
                "con": {"type": "integer"},
                "int": {"type": "integer"},
                "wis": {"type": "integer"},
                "cha": {"type": "integer"}
            },
            "required": ["str", "dex", "con", "int", "wis", "cha"]
        },
        "proficiencies": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "skills": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                "tools": {"type": "array", "items": {"type": "string"}},
                "languages": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["skills", "tools", "languages"]
        },
        "combat": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "hp": {"type": "integer"},
                "ac": {"type": "integer"},
                "speed": {"type": "integer"},
                "attacks": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["hp", "ac", "speed", "attacks"]
        },
        "features": {"type": "array", "items":{"type":"string"}, "minItems" : 1},
           "spells": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "casting_ability": {"type": ["string", "null"]},
                    "cantrips": {"type": "array", "items": {"type": "string"}},
                    "known": {"type": "array", "items": {"type": "string"}},
                    "prepared": {"type": "array", "items": {"type": "string"}}
                    },
                "required": ["casting_ability", "cantrips", "known", "prepared"]
            },
        "equipment": {"type": "array", "items" :{"type": "string"}, "minItems": 1},
            "personality":{
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "traits": {"type": "array", "items": {"type": "string"},"minItems": 1},
                "ideals": {"type": "array", "items": {"type": "string"},"minItems": 1},
                "bonds": {"type": "array", "items": {"type": "string"},"minItems": 1},
                "flaws": {"type": "array", "items": {"type": "string"},"minItems": 1}
            },
            "required": ["traits", "ideals", "bonds", "flaws"]
        },
        "backstory": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "one_liner": {"type": "string"},
                "short": {"type": "string"}
            },
            "required": ["one_liner", "short"]
        },
            "rule_checks": {"type": "array", "items":{"type":"string"}}
    },

    "required": [
        "meta",
        "identity",
        "abilities",
        "proficiencies",
        "combat",
        "features",
        "spells",
        "equipment",
        "personality",
        "backstory",
        "rule_checks"
    ]
}

REVIEW_SCHEMA = {
    "type":"object",
    "additionalProperties": False,
    "properties":{
        "valid":{"type": "boolean"},
        "issues":{"type": "array", "items":{"type": "string"}},
        "suggested_fixes":{"type": "array", "items":{"type": "string"}}
    },
    "required":["valid", "issues", "suggested_fixes"]
}