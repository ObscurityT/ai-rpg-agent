from src.llm import LLMClient
from src.rules import Rules
from src.pipeline import run_pipeline,run_advisor
from pprint import pprint

def main():
    llm = LLMClient()
    rules = Rules.load("rules/phb_min_rules.json")

    character = None
    
    user_request = input("\nDescribe the character you want: ")
    if user_request.lower() in {"exit", "quit"}:
        print("Goodbye!")
        return
    
    result = run_pipeline(user_request, rules, llm)


    character = result["character"]

    print("\n===== GENERATED CHARACTER =====")
    pprint(character, sort_dicts=False)

    print("\n===== LOCAL VALIDATION =====")
    pprint(result["review_local"], sort_dicts=False)

    print("\nYou can now ask questions about this character.")
    print("Type 'exit' to finish.\n")

    while True:
        msg = input("You: ")
        if msg.lower() in {"exit", "quit"}:
            break

        normalized = msg.lower()
        
        reset_phrases = ["new character", "create a new character", "start a new character", "new one", "discard", "discard the character", "delete character","reset", "regenerate"]

        if any(p in normalized for p in reset_phrases):
            print("\n--- Starting a new character ---\n")
            character = None
            continue
        
        if character is None:
            result = run_pipeline(msg, rules, llm)
            character = result["character"]


            print("\n=====GENERATED CHARACTER=====")
            pprint(character, sort_dicts=False)

            print("\n=====LOCAL VALIDATION=====")
            pprint(result["review_local"], sort_dicts= False)
            continue

        reply = run_advisor(msg,rules,character,llm)
        print("\nAgent:", reply, "\n")


if __name__ == "__main__":
    main()