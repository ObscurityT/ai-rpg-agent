from typing import Any, Dict, List

def sanitize_character(ch: Dict[str,Any], rules_obj, rules_raw: Dict[str,Any]) -> Dict[str,Any]:
    identity = ch.setdefault("identity", {})
    prof = ch.setdefault("proficiencies", {})

    lin_raw = identity.get("lineage")
    identity["lineage"] = rules_obj.canon_lineage(lin_raw)

    cls = identity.get("class")
    bg = identity.get("background")

    skills = prof.get("skills")
    if not isinstance(skills, list):
        skills = []
    skills = [s for s in skills if isinstance(s, str)]

    all_skills = set(rules_raw.get("skills_all", []))

    seen = set()
    cleaned: List[str] = []
    for s in skills:
        if s not in all_skills:
            continue
        if s in seen:
            continue
        seen.add(s)
        cleaned.append(s)

    if cls in rules_raw.get("classes", {}) and bg in rules_raw.get("backgrounds", {}):
        bg_fixed_list = rules_raw["backgrounds"][bg].get("skills_fixed", []) or []
        bg_fixed = [s for s in bg_fixed_list if s in all_skills]

        class_info = rules_raw["classes"][cls]
        class_count = int(class_info.get("skill_choice_count", 0))
        allowed_order = class_info.get("skill_choices_from", []) or []
        allowed = [s for s in allowed_order if s in all_skills]

        out: List[str] = []
        used = set()

        for s in bg_fixed:
            if s not in used:
                used.add(s)
                out.append(s)

        for s in cleaned:
            if s in used:
                continue
            if s not in allowed:
                continue
            used.add(s)
            out.append(s)
            if len(out) >= len(bg_fixed) + class_count:
                break

        for s in allowed:
            if len(out) >= len(bg_fixed) + class_count:
                break
            if s in used:
                continue
            used.add(s)
            out.append(s)

        target = len(bg_fixed) + class_count
        prof["skills"] = out[:target]
    else:
        prof["skills"] = cleaned
        print("[sanitize_character] skills_out", prof.get("skills"))

    if bg in rules_raw.get("backgrounds", {}):
        bg_info = rules_raw["backgrounds"][bg]

        fixed_tools = bg_info.get("tools_fixed", []) or []
        tools = prof.get("tools", [])
        if not isinstance(tools, list):
            tools = []
        for t in fixed_tools:
            if t not in tools:
                tools.append(t)
        prof["tools"] = tools

        lang_count = bg_info.get("languages_fixed_count")
        if isinstance(lang_count, int):
            langs = prof.get("languages", [])
            if not isinstance(langs, list):
                langs = []
            prof["languages"] = langs[:lang_count]

    lin = identity.get("lineage")
    if lin in rules_raw.get("lineages", {}):
        ch.setdefault("combat", {})
        ch["combat"]["speed"] = int(
            rules_raw["lineages"][lin].get("speed", ch["combat"].get("speed", 30))
        )

    return ch
