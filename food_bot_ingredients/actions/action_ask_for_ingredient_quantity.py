from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType

class ActionAskForIngredientQuantity(Action):
    def name(self) -> Text:
        return "action_ask_for_ingredient_quantity"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> List[EventType]:
        
        # Suppose we have a slot named 'ingredients_map' that stores a dictionary
        # like {"carrots": None, "celery": None, "onions": "2"}.
        ingredients_map = tracker.get_slot("ingredients_map") or {}

        for ingredient, quantity in ingredients_map.items():
            # If the quantity is missing (None), ask the user for it.
            if quantity is None:
                dispatcher.utter_message(
                    text=f"How many {ingredient} do you need?"
                )
                # Optionally, you might set a slot to track which ingredient you're asking about
                return [SlotSet("ingredient_in_question", ingredient)]
        
        # If everything has a quantity, no further questions are needed
        dispatcher.utter_message(text="All ingredient quantities are set.")
        return []