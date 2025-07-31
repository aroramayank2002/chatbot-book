from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import logging  # Import logging module

# Initialize logger
logger = logging.getLogger(__name__)

class ActionAskForNextIngredient(Action):
    def name(self) -> Text:
        return "action_ask_for_next_ingredient"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # List of ingredients we want from the domain slot
        needed_ingredients = tracker.get_slot("needed_ingredients") or []
        # Current dictionary of {ingredient_name: quantity}
        ingredients_map = tracker.get_slot("ingredients_map") or {}

        # Find the first ingredient that is still missing
        for ing in needed_ingredients:
            if ing not in ingredients_map:
                # Ask for that ingredient
                dispatcher.utter_message(
                    response="utter_ask_ingredient",
                    ingredient=ing
                )
                return [SlotSet("requested_ingredient", ing)]

        # If nothing is missing, let the user know everything is filled
        dispatcher.utter_message(response="utter_already_filled")
        return [SlotSet("requested_ingredient", None)]
# ```
#
# Key points:
# • You do not hardcode “carrots” or “tomatoes” here; you simply iterate over the domain’s “needed_ingredients” list.
# • If an ingredient from that list isn’t in “ingredients_map,” prompt the user for it by calling “utter_ask_ingredient,” passing the name of the ingredient to the template.
#
# ---
#
# ## 3) Action To Store The Provided Quantity
#
# Next, whenever the user sends a quantity (e.g., “I want five”), we capture the “quantity” entity and update the “ingredients_map” accordingly.
#
# ```python
# ```python
class ActionStoreQuantity(Action):
    def name(self) -> Text:
        return "action_store_quantity"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        ingredients_map = tracker.get_slot("ingredients_map") or {}
        logger.info(f"action_store_quantity ingredients_map: {ingredients_map}")
        # We store which ingredient we’re currently asking about
        requested_ingredient = tracker.get_slot("requested_ingredient")
        if not requested_ingredient:
            # If there's no requested ingredient, we can't store a quantity yet
            dispatcher.utter_message(response="utter_missed_quantity")
            return []

        # Grab the quantity entity from the user's latest message
        quantity_value = None
        for ent in tracker.latest_message.get("entities", []):
            if ent.get("entity") == "quantity":
                quantity_value = ent.get("value")
                break

        if quantity_value is None:
            # Could not parse the required quantity
            dispatcher.utter_message(response="utter_missed_quantity")
            return []

        # Update the "ingredients_map" slot
        ingredients_map = tracker.get_slot("ingredients_map") or {}
        ingredients_map[requested_ingredient] = str(quantity_value)

        # Confirm to user using the domain-based template
        dispatcher.utter_message(
            response="utter_confirm_ingredient",
            ingredient=requested_ingredient,
            quantity=quantity_value
        )

        return [
            SlotSet("ingredients_map", ingredients_map),
            SlotSet("requested_ingredient", None)
        ]
# ```
#
# Key points:
# • The user’s input is matched against the “quantity” entity defined in your domain.
# • We store that quantity in “ingredients_map” under the key “requested_ingredient.”
# • We utter a templated response, “utter_confirm_ingredient,” passing the ingredient name and the quantity, so there’s no hardcoded text in code.
#
# ---
#
# ## 4) Example Stories or Rules
#
# Below is a simplified way to use these actions in your stories or rules:
#
# ```yaml
# rules:
#   - rule: Ask for next ingredient
#     steps:
#       - intent: request_food
#       - action: action_ask_for_next_ingredient
#
#   - rule: Provide quantity
#     steps:
#       - intent: provide_quantity
#       - action: action_store_quantity
#       - action: action_ask_for_next_ingredient
# ```
#
# Flow:
# 1. User triggers “request_food,” so Rasa calls “action_ask_for_next_ingredient.”
# 2. That checks if “carrots” or “tomatoes” (or both) are missing in the “ingredients_map.” It picks the first missing ingredient from the domain’s “needed_ingredients” list, prompting the user.
# 3. User responds with quantity → Rasa recognizes “provide_quantity” → calls “action_store_quantity,” which sets the correct quantity in “ingredients_map.”
# 4. After storing, we again call “action_ask_for_next_ingredient” to see if there are more ingredients left.
#
# This way:
# • “carrots” and “tomatoes” live only in your domain slot “needed_ingredients.”
# • The custom actions simply loop over that slot’s values and pass them to the domain-based responses as parameters.
# • No more hardcoding carrots or tomatoes in your code.