import logging
from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.forms import FormValidationAction

logger = logging.getLogger(__name__)


class ValidateMultiIngredientsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_multi_ingredients_form"

    async def required_slots(
            self,
            domain_slots: List[Text],
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Text]:
        """
        We want 'ingredients_map' first, then 'ingredient_quantity' repeatedly
        until all dictionary values are filled.
        """
        return ["ingredients_map", "ingredient_quantity"]

    def validate_ingredients_map(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """
        We'll assume slot_value is a dictionary mapping each ingredient to None initially.
        If your NLU extracts multiple ingredients, you'll need a custom action/logic
        to build this dict before the form, or do it right here.
        """
        # Example structure we want: {"carrots": None, "celery": None, "onions": None}
        if isinstance(slot_value, dict) and len(slot_value) > 0:
            logger.info(f"Captured ingredients_map: {slot_value}")
            return {"ingredients_map": slot_value}
        else:
            dispatcher.utter_message(text="I didn't detect any ingredients. Can you rephrase?")
            return {"ingredients_map": None}

    def validate_ingredient_quantity(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """
        Once the user gives a quantity for the current 'ingredient_in_question',
        store it in the dictionary, then proceed to the next ingredient if any remain.
        """
        ingredients_map = tracker.get_slot("ingredients_map") or {}
        current_ingredient = tracker.get_slot("ingredient_in_question")

        logger.info(f"Current ingredient: {current_ingredient}, user provided: {slot_value}")

        # Store the just-provided quantity in the dictionary
        if current_ingredient in ingredients_map:
            ingredients_map[current_ingredient] = slot_value

        return {
            "ingredient_quantity": slot_value,
            # Updated dictionary
            "ingredients_map": ingredients_map
        }

    def request_next_slot(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> Any:
        """
        1) If 'ingredients_map' is empty or None, ask for it.
        2) Otherwise, iterate over ingredients_map to find the first ingredient with None quantity.
        3) Ask for it, storing that as 'ingredient_in_question'.
        4) If all ingredients have values, return None to end the form.
        """
        ingredients_map = tracker.get_slot("ingredients_map")

        # 1) If no dict yet, ask for it
        if not ingredients_map:
            dispatcher.utter_message(response="utter_ask_ingredients_map")
            return "ingredients_map"
        else:
            logger.info(f"ingredients_map: {ingredients_map}")

        # 2) Otherwise, find the first ingredient that is None
        for ingredient, quantity in ingredients_map.items():
            logger.info(f"Found ingredient {ingredient} with None quantity.")
            if quantity is None:
                # Found an ingredient needing a quantity
                dispatcher.utter_message(response="utter_ask_ingredient_quantity")
                return [SlotSet("ingredient_in_question", ingredient), "ingredient_quantity"]
            else:
                logger.info(f"Ingredient {ingredient} already has a quantity.")

        # 3) If we get here, there is no ingredient with None
        return None  # form is done


class ActionSubmitMultiIngredientsForm(Action):
    def name(self) -> Text:
        return "action_submit_multi_ingredients_form"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[EventType]:
        ingredients_map = tracker.get_slot("ingredients_map") or {}
        logger.info(f"Final ingredients_map: {ingredients_map}")

        # You might want to do a summary here
        dispatcher.utter_message(response="utter_completed_form")
        return []