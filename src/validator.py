from typing import Any, Dict, List
from src.rules import Rules

class CharacterValidator:
    def __init__(self, rules: Rules):
        self.rules = rules
        self.raw = rules.raw

    def validate_identity(self, ch: Dict[str, Any]) -> List[str]:
        issues = []
        identity = ch.get("identity", {})

        cls = identity.get("class")
        bg = identity.get("background")
        
        lin_raw = identity.get("lineage")
        lin = self.rules.canon_lineage(lin_raw)
        identity["lineage"] = lin


        lvl = ch.get("meta", {}).get("level")

        if lvl is None or not(1 <= int(lvl) <= 3):
            issues.append("Level must be between 1 and 3")
        

        if cls not in self.raw["classes"]:
            issues.append(f"Class not in rules: {cls}")
        if bg not in self.raw["backgrounds"]:
            issues.append(f"Background not in rules: {bg}")
        if lin not in self.raw["lineages"]:
            issues.append(f"Lineage not in rules: {lin}")
        
        return issues

    def validate_skills(self,ch: Dict[str,Any]) -> List[str]:
        issues = []
        identity = ch.get("identity", {})
        cls = identity.get("class")
        bg = identity.get("background")

        skills = ch.get("proficiencies", {}).get("skills", [])

        if not isinstance(skills, list):
            return ["proficiencies.skills must be  list"]
        
        all_skills = set(self.raw["skills_all"])

        for s in skills:
            if s not in all_skills:
                issues.append(f"Invalid skill name: {s}")
        
        if len(skills) != len(set(skills)):
            issues.append("Duplicate skills found in proficiencies.skills")
        
        if cls in self.raw["classes"] and bg in self.raw["backgrounds"]:
            bg_fixed = set(self.raw["backgrounds"][bg].get("skills_fixed", []))
            class_skills_allowed = set(self.raw["classes"][cls]["skill_choices_from"])

            chosen_class_skills = set(skills) - bg_fixed
            
            for s in chosen_class_skills:
                if s not in class_skills_allowed:
                    issues.append(f"Skill not allowed for class {cls}: {s}")
            
            missing_bg = bg_fixed - set(skills)
            for s in missing_bg:
                issues.append(f"Missing background fixed skill: {s}")
            
            class_count = int(self.raw["classes"][cls]["skill_choice_count"])
            total_required = class_count + len(bg_fixed)

            if len(skills) != total_required:
                issues.append(f"Total skill count mismatch: got {len(skills)}, expected {total_required}")

        return issues

        
    def validate_character(self, ch: Dict[str, Any]) -> List[str]:
        issues = []
        issues += self.validate_identity(ch)

        abilities = ch.get("abilities", {})
        ok, _, pb_issues = self.rules.point_buy_cost(abilities)
        if not ok:
            issues += pb_issues
            
        issues += self.validate_skills(ch)
            
        return issues