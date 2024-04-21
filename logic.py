import json

from pyswip.prolog import Prolog
from pyswip.easy import Functor, Variable, registerForeign, call, Atom

def run_expert_system(shared_data):
    prolog = Prolog()  # Global handle to the interpreter
    retractall = Functor("retractall")
    known = Functor("known", 2)  # Functor representing the 'known' predicate used in Prolog

    # Load 'askables' data from a JSON file
    with open("askables.json") as f:
        askables = json.load(f)["askables"]

    # Function that interfaces with Prolog to handle user inputs
    def read_input(A, V, Y):
        if isinstance(Y, Variable):
            askable = str(A)
            # Retrieve the question data from the 'askables'
            ask_dict = askables.get(askable, {})
            shared_data["curr_question"] = {
                "id": askable,
                "text": ask_dict.get("text"),
                "type": ask_dict.get("type"),
                "options": ask_dict.get("options", []),
                "default": ask_dict.get("default"),
            }
            # Wait for response
            while f"{askable}_response" not in shared_data:
                pass
            # Retrieve the response
            response = shared_data[f"{askable}_response"]  # a list
            if ask_dict["type"] == "multi_choice":
                # For list-based responses, we need to convert each item to a Prolog atom and unify
                Y.unify(list(map(Atom, response)))
            elif ask_dict["type"] == "number" or ask_dict["type"] == "date":
                # For numeric or date responses, unify directly with the response value
                Y.unify(float(response[0]) if ask_dict["type"] == "number" else Atom(response[0]))
            else:
                # For single-choice responses
                Y.unify(Atom(response[0]))
            return True
        else:
            return False

    read_input.arity = 3
    registerForeign(read_input)

    # Load the Prolog knowledge base
    prolog.consult("expert.pl")

    # Reset the 'known' predicate in the KB to delete any prior user responses
    call(retractall(known))

    # Execute Prolog queries to get daily reminders and conclusions
    shared_data["reminders"] = []
    shared_data["conclusions"] = []
    for reminder in prolog.query("daily_reminder(R)"):
        shared_data["reminders"].append(reminder["R"])
    for conclusion in prolog.query("conclusion(C)"):
        shared_data["conclusions"].append(conclusion["C"])

    shared_data["done"] = True

