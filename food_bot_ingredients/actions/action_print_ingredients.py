from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher


class ActionPrintIngredients(Action):
    def name(self) -> Text:
        return "action_print_ingredients"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> List[EventType]:
        """
        At conversation end (or whenever appropriate), print all ingredients with final quantities.
        """
        ingredients_map = tracker.get_slot("ingredients_map") or {}

        if not ingredients_map:
            dispatcher.utter_message(text="No ingredients found.")
            return []

        # Format the output
        message = "Here are your ingredients with quantities:\n"
        for ing, qty in ingredients_map.items():
            # If quantity wasn't provided yet, just say None
            message += f"- {ing}: {qty or 'No quantity specified'}\n"

        dispatcher.utter_message(text=message)
        return []