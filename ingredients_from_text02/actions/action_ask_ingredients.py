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

    # In this one you have to type complete response '5 cups rice'
    # def run(self, dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    #     logger.info(f"action_collect_quantities")
    #
    #     ingredients = tracker.get_slot("ingredients")
    #     quantities = tracker.get_slot("quantities") or {}
    #
    #     logger.info(f"ingredients: {ingredients}")
    #     logger.info(f"quantities: {quantities}")
    #
    #     # Try to extract latest input (user just gave a quantity)
    #     latest_entities = tracker.latest_message.get("entities", [])
    #     latest_ingredient = None
    #     latest_quantity = None
    #
    #     for ent in latest_entities:
    #         if ent.get("entity") == "ingredient":
    #             latest_ingredient = ent.get("value")
    #         elif ent.get("entity") == "quantity":
    #             latest_quantity = ent.get("value")
    #
    #     # If user just gave a valid pair, store it
    #     if latest_ingredient and latest_quantity:
    #         quantities[latest_ingredient] = latest_quantity
    #
    #     # Find next ingredient that hasn't been filled yet
    #     for ingredient in ingredients:
    #         if ingredient not in quantities:
    #             # Ask user for quantity of the next ingredient
    #             dispatcher.utter_message(text=f"How much {ingredient} do you need?")
    #             return [SlotSet("quantities", quantities)]
    #
    #     # All ingredients collected → show summary
    #     return [SlotSet("quantities", quantities),
    #             FollowupAction("action_show_summary")]

    # In this one you can say only quantity '5 cups'
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:
        logger.info(f"action_collect_quantities")

        ingredients = tracker.get_slot("ingredients") or []
        quantities = tracker.get_slot("quantities") or {}
        current_ingredient = tracker.get_slot("current_ingredient")
        logger.info(f"ingredients: {ingredients}")
        logger.info(f"quantities: {quantities}")
        logger.info(f"current_ingredient: {current_ingredient}")

        latest_entities = tracker.latest_message.get("entities", [])
        latest_ingredient = None
        latest_quantity = None
        logger.info(f"latest_entities: {latest_entities}")

        for ent in latest_entities:
            if ent.get("entity") == "ingredient":
                latest_ingredient = ent.get("value")
            elif ent.get("entity") == "quantity":
                latest_quantity = ent.get("value")

        # CASE 1: User only gave quantity (e.g., "2 cups")
        if latest_quantity and not latest_ingredient and current_ingredient:
            quantities[current_ingredient] = latest_quantity

        # CASE 2: User gave both ingredient and quantity
        elif latest_ingredient and latest_quantity:
            quantities[latest_ingredient] = latest_quantity

        # # CASE 3: User gave incomplete or invalid input
        # elif latest_quantity is None:
        #     dispatcher.utter_message(text="Sorry, I didn't understand the quantity.")
        #     return []

        # Ask next ingredient
        for ingredient in ingredients:
            if ingredient not in quantities:
                dispatcher.utter_message(text=f"How much {ingredient} do you need?")
                return [
                    SlotSet("quantities", quantities),
                    SlotSet("current_ingredient", ingredient)
                ]

        dispatcher.utter_message(text="All ingredients received. Type 'summary' to see them.")
        # return [
        #     SlotSet("quantities", quantities),
        #     SlotSet("current_ingredient", None)
        # ]
        return [SlotSet("quantities", quantities),
            FollowupAction("action_show_summary")]


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
