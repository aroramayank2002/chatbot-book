from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import logging
logger = logging.getLogger(__name__)


class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        logger.info("Action 'action_hello_world' started.")


        extracted_food_items = tracker.get_latest_entity_values("food_item")

        # Convert the generator to a list
        food_items_list = list(extracted_food_items)

        # Log the items to console (for debugging/monitoring)
        print(f"Extracted food items: {food_items_list}")
        dispatcher.utter_message(text=f"Here are the items I recognized: {food_items_list}")
        return []
