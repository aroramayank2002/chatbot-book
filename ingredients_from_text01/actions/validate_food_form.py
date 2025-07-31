from typing import Text, Any, Dict, List
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
import logging  # Import logging module

# Initialize logger
logger = logging.getLogger(__name__)
class ValidateFoodForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_food_form"

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> List[Text]:
        """
        We dynamically determine how many quantities we need to fill
        based on newly recognized 'food' entities.
        """
        # logger.info(f"required_slots")

        entities = tracker.latest_message.get("entities", [])
        # logger.info(f"required_slots entities: {entities}")

        # 1. Grab the existing dictionary from the slot
        ingredients_map = tracker.get_slot("ingredients_map") or {}
        # logger.info(f"required_slots ingredients_map: {ingredients_map}")

        # 2. Capture new foods from the latest user message
        food_entities = [e["value"] for e in tracker.latest_message.get("entities", [])
                         if e["entity"] == "food"]
        # logger.info(f"required_slots food_entities: {food_entities}")

        # 3. Add new foods with quantity None (if they are not already in the map)
        for food_item in food_entities:
            if food_item not in ingredients_map:
                ingredients_map[food_item] = None
        logger.info(f"required_slots ingredients_map: {ingredients_map}")

        # 4. Save the current "ingredients_map"
        # return_slots = ["ingredients_map"]
        # return return_slots
        # return {"ingredients_map": ingredients_map}
        # return [SlotSet("ingredients_map", ingredients_map)]
        return ["ingredients_map"]


    def validate_ingredients_map(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        logger.info(f"validate_ingredients_map")

        """
        Each time the form requests 'ingredients_map', we:
        1. Check if there's any food whose quantity is None.
        2. If yes, ask the user: "How many <food> do you need?"
        3. Once user answers, fill that food's quantity in the dictionary.
        4. If all are filled, we consider the slot validated.
        """
        ingredients_map = tracker.get_slot("ingredients_map") or {}
        logger.info(f"validate_ingredients_map ingredients_map: {ingredients_map}")

        # 1. Find an item still missing a quantity (None)
        item_still_needed = next((item for item, qty in ingredients_map.items() if qty is None), None)
        logger.info(f"validate_ingredients_map item_still_needed: {item_still_needed}")

        # 2. If we find an item with no quantity, ask the user now
        if item_still_needed:
            # We'll store that item in a helper slot so we can fill it next turn
            dispatcher.utter_message(response="utter_ask_ingredients_map", item_in_focus=item_still_needed)
            # We MUST keep the form active until we get the quantity.
            # Return the same dictionary, but we haven't validated the slot yet.
            return {"ingredients_map": ingredients_map}
        else:
            # All items have a quantity -> fully validated
            return {"ingredients_map": ingredients_map}

# ```
#
# ### Explanation of Key Steps
#
# 1. required_slots():
# • We get the existing dictionary.
# • Then we check the latest message for any new “food” entities and add them to the dictionary with a None quantity.
# • Finally, we return just ["ingredients_map"] so that the form knows to keep requesting that slot until it’s “done.”
#
# 2. validate_ingredients_map():
# • We look for any item in the dictionary with None quantity.
# • If found, we ask the user “How many <item> do you need?” by uttering “utter_ask_ingredients_map.”
# • The form is still active, expecting the user to input a quantity.
#
# In a real scenario, you’d also define a custom action to actually parse the user’s numeric response and update the dictionary. For example, you might have an intent recognized as “provide_quantity” with an entity “number.” You’d handle that in a separate step (or slot validation method) that sets ingredients_map[item_still_needed] = user_input.
#
# ---

### 5. Putting It All Together
#
# • User says: “I want carrots and tomatoes.”
# → Rasa picks up two food entities: (“carrots,” “tomatoes”).
# → The form’s logic populates ingredients_map = { "carrots": None, "tomatoes": None }.
#
# • The form sees that carrots has None value, so it asks “How many carrots do you need?”
# • User says: “3.”
# → You capture that quantity in a subsequent step or slot validation, updating ingredients_map = { "carrots": 3, "tomatoes": None }.
#
# • Next turn, the form asks “How many tomatoes do you need?”
# • User says: “2.”
# → Now ingredients_map = { "carrots": 3, "tomatoes": 2 }.
# • No more missing quantities → the form completes.
#
# Finally, the conversation can end with a summary, e.g., “You need 3 carrots and 2 tomatoes!”
#
# This setup demonstrates:
# • A single dictionary slot (ingredients_map).
# • Dynamically adding recognized entities with quantity None.
# • Prompting for each quantity in a custom form flow.
# • Storing the result in the same dictionary.
#
# You can adapt this pattern to any use case where you need a “map slot” for entities and their respective details.