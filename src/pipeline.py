import json
from typing import Any, Dict
from .rules import Rules
from .llm import LLMClient
from .brief_sanitizer import sanitize_brief
from .character_sanitizer import sanitize_character
from .validator import CharacterValidator
from .schemas import BRIEF_SCHEMA, CHARACTER_SCHEMA, REVIEW_SCHEMA


def load_text(path: str) -> str:
    with open(path, "r", encoding= "utf-8") as f:
        return f.read()
    
def load_json(path: str) -> Any:
    with open(path, "r", encoding= "utf-8") as f:
        return json.load(f)
    
def run_pipeline(user_request: str, rules: Rules, llm: LLMClient) -> Dict[str, Any]:
    brief_prompt = load_text("prompts/character_brief_prompt.txt")
    gen_prompt = load_text("prompts/character_generator_prompt.txt")
    rev_prompt = load_text("prompts/character_reviewer_prompt.txt")

    brief = llm.json_call(prompt= brief_prompt, payload= {"user_request": user_request, "rules": rules.raw}, schema_name= "character_brief",schema= BRIEF_SCHEMA)
    brief = sanitize_brief(brief, rules.raw)

    character_template = load_json("character_schema.json")

    character = llm.json_call(prompt= gen_prompt, payload={"brief": brief, "rules": rules.raw, "character_schema": character_template}, schema_name= "character", schema= CHARACTER_SCHEMA)
    character =  sanitize_character(character, rules, rules.raw)

    review_llm = llm.json_call(prompt= rev_prompt, payload={"rules": rules.raw, "character": character}, schema_name= "review", schema= REVIEW_SCHEMA)

    validator = CharacterValidator(rules)
    local_issues = validator.validate_character(character)

    return {
        "brief":brief,
        "character":character,
        "review_llm": review_llm,
        "review_local": {
            "valid": len(local_issues) == 0,
            "issues": local_issues
        },
    }

def run_advisor(user_message: str, rules: Rules, character: Dict[str, Any], llm: LLMClient) -> str:
    advisor_prompt = load_text("prompts/character_advisor_prompt.txt")

    messages = [{
        "role": "system", "content": advisor_prompt},
        {"role": "user","content": json.dumps({"rules": rules.raw, "character": character, "user_message": user_message}, ensure_ascii=False)
    }]

    resp = llm.client.responses.create(model =llm.model, input = messages,max_output_tokens= 300)

    return resp.output_text.strip()


if __name__ == "__main__":
    run_pipeline()