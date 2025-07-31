import logging
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

logger = logging.getLogger(__name__)


class ActionProcessIngredients(Action):
    def name(self) -> Text:
        return "action_process_ingredients"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Collect all 'ingredient' entities, convert them to a dictionary
        where each key is the ingredient text and each value is None.
        Then set this dictionary as the 'ingredients_map' slot.
        """

        # Get all recognized 'ingredient' entities in this user message
        ingredient_entities = tracker.get_latest_entity_values("ingredient")

        # Convert them into a dictionary: {ingredient_name: None}
        # Using a dict comprehension to assign None to each recognized ingredient
        ingredients_map = {}
        for ing in ingredient_entities:
            ingredient_lower = ing.lower().strip()
            if ingredient_lower not in ingredients_map:
                ingredients_map[ingredient_lower] = None

        # If no entities found, you might do something else such as prompt user again
        if not ingredients_map:
            logger.info("No 'ingredient' entities were recognized.")
            dispatcher.utter_message(
                text="I didn't catch any ingredients. Could you try again?"
            )
            return []

        logger.info(f"Created ingredients_map: {ingredients_map}")

        # Set the slot
        return [SlotSet("ingredients_map", ingredients_map)]