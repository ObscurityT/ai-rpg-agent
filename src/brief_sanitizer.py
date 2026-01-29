from typing import Any,Dict,List

def sanitize_brief(brief: Dict[str,Any], rules_raw: Dict[str, Any])-> Dict[str,Any]:
    allowed_classes = set(rules_raw.get("classes", {}).keys())
    allowed_lineages = set(rules_raw.get("lineages", {}).keys())
    allowed_backgrounds = set(rules_raw.get("backgrounds", {}).keys())

    def keep_allowed(values: List[str], allowed: set) -> List[str]:
        if not isinstance(values, list):
            return[]
        return [v for v in values if v in allowed]
    
    brief["preferred_classes"] = keep_allowed(brief.get("preferred_classes", []), allowed_classes)
    brief["preferred_lineages"] = keep_allowed(brief.get("preferred_lineages", []), allowed_lineages)
    brief["preferred_backgrounds"] = keep_allowed(brief.get("preferred_backgrounds", []), allowed_backgrounds)

    def first_sorted(s: set[str]) -> str:
        return sorted(s)[0]

    if not brief["preferred_classes"] and allowed_classes:
        brief["preferred_classes"] = [first_sorted(allowed_classes)]
    if not brief["preferred_lineages"] and allowed_lineages:
        brief["preferred_lineages"] = [first_sorted(allowed_lineages)]
    if not brief["preferred_backgrounds"] and allowed_backgrounds:
        brief["preferred_backgrounds"] = [first_sorted(allowed_backgrounds)]
    
    return brief