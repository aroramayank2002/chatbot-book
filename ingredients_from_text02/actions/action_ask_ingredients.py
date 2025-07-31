from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import logging
logger = logging.getLogger(__name__)

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

# Sample ingredients for demo purposes
RECIPE_INGREDIENTS = ["rice", "eggs", "olive oil"]

class ActionAskIngredients(Action):
    def name(self) -> Text:
        return "action_ask_ingredients"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info(f"action_ask_ingredients")

        # return [SlotSet("ingredients", RECIPE_INGREDIENTS), SlotSet("quantities", {})]
        # return [SlotSet("ingredients", RECIPE_INGREDIENTS), SlotSet("quantities", {})]
        # return []
        recipe_ingredients = ["rice", "eggs", "olive oil"]

        dispatcher.utter_message(text=f"Setting ingredients: {recipe_ingredients}")
        dispatcher.utter_message(text="Initializing quantities to empty dict")

        # Set ingredients list and initialize empty quantity dictionary
        return [SlotSet("ingredients", recipe_ingredients), SlotSet("quantities", {})]


class ActionCollectQuantities(Action):
    def name(self) -> Text:
        return "action_collect_quantities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info(f"action_collect_quantities")

        ingredients = tracker.get_slot("ingredients")
        quantities = tracker.get_slot("quantities") or {}

        logger.info(f"ingredients: {ingredients}")
        logger.info(f"quantities: {quantities}")

        # Try to extract latest input (user just gave a quantity)
        latest_entities = tracker.latest_message.get("entities", [])
        latest_ingredient = None
        latest_quantity = None

        for ent in latest_entities:
            if ent.get("entity") == "ingredient":
                latest_ingredient = ent.get("value")
            elif ent.get("entity") == "quantity":
                latest_quantity = ent.get("value")

        # If user just gave a valid pair, store it
        if latest_ingredient and latest_quantity:
            quantities[latest_ingredient] = latest_quantity

        # Find next ingredient that hasn't been filled yet
        for ingredient in ingredients:
            if ingredient not in quantities:
                # Ask user for quantity of the next ingredient
                dispatcher.utter_message(text=f"How much {ingredient} do you need?")
                return [SlotSet("quantities", quantities)]

        # All ingredients collected → show summary
        return [SlotSet("quantities", quantities),
                FollowupAction("action_show_summary")]
        # dispatcher.utter_message(text="All ingredients received. Type 'summary' to see them.")
        # return [SlotSet("quantities", quantities)]


class ActionShowSummary(Action):
    def name(self) -> Text:
        return "action_show_summary"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info(f"action_show_summary")

        quantities = tracker.get_slot("quantities")
        if not quantities:
            dispatcher.utter_message(text="No ingredients received.")
            return []

        summary = "Here's your ingredient list:\n"
        for ingredient, qty in quantities.items():
            summary += f"- {ingredient}: {qty}\n"

        dispatcher.utter_message(text=summary)
        return []
