from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import logging  # Import logging module

# Initialize logger
logger = logging.getLogger(__name__)


class ActionPairFoodSpiceWithQty(Action):
    def name(self) -> Text:
        return "action_pair_food_spice_with_qty"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        # Retrieve all entities from the tracker
        entities = tracker.latest_message.get("entities", [])

        # Log the entities (to console or action server logs)
        logger.info(f"Extracted entities: {entities}")
        print(f"Extracted entities: {entities}")  # For local debugging

        # Group entities by type
        food_entities = [e for e in entities if e.get("entity") == "food"]
        spice_entities = [e for e in entities if e.get("entity") == "spice"]
        qty_entities = [e for e in entities if e.get("entity") == "qty"]
        medium_entities = [e for e in entities if e.get("entity") == "medium"]

        # Optionally log specific entity groups
        logger.info(f"Food entities: {food_entities}")
        logger.info(f"Spice entities: {spice_entities}")
        logger.info(f"Quantity entities: {qty_entities}")
        logger.info(f"Medium entities: {medium_entities}")

        # Convert entities into readable pairs
        foods = [{"item": e.get("value"), "start": e.get("start")} for e in food_entities]
        spices = [{"item": e.get("value"), "start": e.get("start")} for e in spice_entities]
        quantities = [{"qty": e.get("value"), "start": e.get("start")} for e in qty_entities]
        mediums = [{"medium": e.get("value"), "start": e.get("start")} for e in medium_entities]

        # Sort entities by their position in the input to pair correctly
        all_items = sorted(foods + spices, key=lambda x: x["start"])
        quantities = sorted(quantities, key=lambda x: x["start"])

        # Pair items (food or spice) with their quantities
        pairs = []
        for item, qty in zip(all_items, quantities):
            pairs.append({"item": item["item"], "quantity": qty["qty"]})

        # Log the computed pairs
        logger.info(f"Computed pairs: {pairs}")
        print(f"Computed pairs: {pairs}")  # For development and debugging

        # Create response with the pairs included
        if pairs:
            response = "Here are the food and spice pairings I found:\n\n"
            for pair in pairs:
                response += f"- {pair['item']}: {pair['quantity']}\n"
        else:
            response = "I couldn't find any valid food+qty pairings. Please make sure to include foods, spices, and their quantities."

        # Send the response back to the user
        dispatcher.utter_message(text=response)

        return []