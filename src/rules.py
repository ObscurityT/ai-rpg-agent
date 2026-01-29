import json
from dataclasses import dataclass
from typing import Any, Dict,List,Tuple

LINEAGE_ALIASES = {
    "Variant Human": "Human (Variant)",
    "Human Variant": "Human (Variant)",
    "High Elf": "Elf (High)",
    "Elf High": "Elf (High)"
}

@dataclass
class Rules:
    raw: Dict[str, Any]

    @staticmethod
    def load(path: str) -> "Rules": 
        with open(path, "r", encoding="utf-8") as f:
            return Rules(raw = json.load(f))
        
    def canon_lineage(self, value: str | None)-> str | None:
        if  value is None:
            return None
        return LINEAGE_ALIASES.get(value, value)
    
    def point_buy_cost(self, abilities: Dict[str, int])-> Tuple[bool,int,List[str]]:
        pb = self.raw["ability_methods"]["point_buy"] 
        costs = pb["costs"] 
        min_s, max_s = pb["min_score"], pb["max_score"] 
        issues: List[str] = [] 
        total = 0 

        for key in ["str", "dex", "con", "int", "wis", "cha"]: 
            if key not in abilities: 
                issues.append(f"Missing ability: {key}") 
                continue 
            v = abilities[key] 
            if v < min_s or v > max_s: 
                issues.append(f"{key} out of range for point buy: {v} (must be {min_s}-{max_s})") 
                continue 
            total += costs[str(v)] 
        if total > pb["total_points"]: issues.append(f"Point buy cost is too high: {total} > {pb['total_points']}") 
        
        return len(issues) == 0, total, issues
    
