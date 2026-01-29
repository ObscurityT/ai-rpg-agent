from typing import Dict,Any

REQUIRED_FIELDS = {
    "identity.lineage",
    "identity.class",
    "identity.background",
    "identity.alignment"
}

def is_breaf_complete(brief : Dict[str, Any]) -> bool:
    def get(path):
        cur = brief
        for p in path.split("."):
            if not isinstance(cur,dict)or p not in cur:
                return None
            cur = cur[p]
        return cur
    return all(get(field) is not None for field in REQUIRED_FIELDS)

def merge_brief(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    for k,v in update.items():
        if isinstance(v, dict):
            base[k] = merge_brief(base.get(k, {}), v)
        else:
            base[k] = v
    return base