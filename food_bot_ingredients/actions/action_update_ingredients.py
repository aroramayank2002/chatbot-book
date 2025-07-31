from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher


class ActionUpdateIngredients(Action):
    def name(self) -> Text:
        return "action_update_ingredients"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> List[EventType]:
        """
        Extract ingredient entities and store them in 'ingredients_map' slot with quantity=None if missing.
        """
        # Get current ingredients_map or create if None
        ingredients_map = tracker.get_slot("ingredients_map") or {}

        # Find ingredient entities from the message
        extracted_ingredients = [
            ent["value"] for ent in tracker.latest_message.get("entities", [])
            if ent["entity"] == "ingredient"
        ]

        for ing in extracted_ingredients:
            if ing not in ingredients_map:
                ingredients_map[ing] = None  # quantity not provided yet

        return [SlotSet("ingredients_map", ingredients_map)]
