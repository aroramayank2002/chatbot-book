# actions.py

from typing import Any, Dict, List, Text
from rasa_sdk import FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import logging
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk import Action, Tracker

logger = logging.getLogger(__name__)


class ValidateRecipeForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_recipe_form"

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> List[Text]:
        """
        Dynamically determine which slots the form should fill next.
        We want to ask for 'ingredient_in_question' and 'ingredient_quantity'
        in sequence until all ingredients have been processed.
        """
        ingredients_list = tracker.get_slot("ingredients_list") or []
        ingredient_in_question = tracker.get_slot("ingredient_in_question")
        ingredients_map = tracker.get_slot("ingredients_map") or {}

        # Check whether we just finished with an ingredient, or haven't started yet
        if not ingredient_in_question or ingredient_in_question in ingredients_map:
            # Find next unfilled ingredient
            next_ingredient = None
            for ing in ingredients_list:
                if ing not in ingredients_map:
                    next_ingredient = ing
                    break

            if next_ingredient:
                # We'll collect 'ingredient_in_question' and then 'ingredient_quantity'
                return ["ingredient_in_question", "ingredient_quantity"]
            else:
                # All ingredients handled; end the form
                return []
        else:
            # Still need the quantity for the current ingredient
            return ["ingredient_in_question", "ingredient_quantity"]

    async def validate(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> List[Dict]:
        """
        Called after the form attempts to fill the slots in a single iteration.
        Here, once both 'ingredient_in_question' and 'ingredient_quantity' are filled,
        we update 'ingredients_map' and reset 'ingredient_quantity' for the next iteration.
        """
        slot_updates = []
        ingredient_in_question = tracker.get_slot("ingredient_in_question")
        ingredient_quantity = tracker.get_slot("ingredient_quantity")
        ingredients_map = tracker.get_slot("ingredients_map") or {}

        if ingredient_in_question and ingredient_quantity:
            # Store the quantity for this ingredient
            ingredients_map[ingredient_in_question] = ingredient_quantity
            slot_updates.append({"ingredients_map": ingredients_map})
            # Clear 'ingredient_quantity' so the form can prompt for the next one
            slot_updates.append({"ingredient_quantity": None})

        return slot_updates

    async def validate_ingredient_in_question(
            self,
            value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> Dict[Text, Any]:
        """
        Validate or transform the incoming value for 'ingredient_in_question'.
        Often, you can just trust the form logic here, but you can add checks if needed.
        """
        logger.info(f"User set ingredient_in_question to '{value}'")
        # By default, just accept as-is
        if value:
            # In a real scenario, you might check if the ingredient is recognized
            return {"ingredient_in_question": value}
        else:
            dispatcher.utter_message(text="I didn't quite catch the ingredient. Please try again.")
            return {"ingredient_in_question": None}


    async def validate_ingredient_quantity(
            self,
            value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> Dict[Text, Any]:
        """
        Validate or transform the incoming value for 'ingredient_quantity'.
        Here, we ensure the user input is numeric.
        """
        logger.info(f"User set ingredient_quantity to '{value}'")

        try:
            quantity_val = float(value)
            return {"ingredient_quantity": quantity_val}
        except ValueError:
            dispatcher.utter_message(text="Please provide a valid quantity.")
            return {"ingredient_quantity": None}

class ActionSubmitRecipeForm(Action):
    """
    Called when the form finishes. Logs the final slot values
    and summarizes them for the user.
    """

    def name(self) -> Text:
        return "action_submit_recipe_form"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[EventType]:
        ingredient = tracker.get_slot("ingredient_in_question")
        quantity = tracker.get_slot("ingredient_quantity")

        logger.info(f"Form completed with ingredient: {ingredient}, quantity: {quantity}")

        dispatcher.utter_message(response="utter_slots_summary")
        return []
