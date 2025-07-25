from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import logging  # Import logging module

# Initialize logger
logger = logging.getLogger(__name__)


class ActionPairFoodSpiceTypeWithQty(Action):
    def name(self) -> Text:
        return "action_pair_food_spice_type_with_qty"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
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
        type_entities = [e for e in entities if e.get("entity") == "type"]

        # Log specific entity groups
        logger.info(f"Food entities: {food_entities}")
        logger.info(f"Spice entities: {spice_entities}")
        logger.info(f"Quantity entities: {qty_entities}")
        logger.info(f"Type entities: {type_entities}")

        # Convert entities into internal structures
        foods = [{"item": e.get("value"), "start": e.get("start")} for e in food_entities]
        spices = [{"item": e.get("value"), "start": e.get("start")} for e in spice_entities]
        quantities = [{"qty": e.get("value"), "start": e.get("start")} for e in qty_entities]
        types = [{"type_label": e.get("value"), "start": e.get("start")} for e in type_entities]

        # Sort entities by their position in the input
        all_items = sorted(foods + spices, key=lambda x: x["start"])
        quantities = sorted(quantities, key=lambda x: x["start"])
        types = sorted(types, key=lambda x: x["start"])

        # Pair items with their quantities and types
        pairs = []
        for item, qty, t in zip(all_items, quantities, types):
            pairs.append({
                "item": item["item"],
                "quantity": qty["qty"],
                "type": t["type_label"]
            })

        # Log the computed pairs
        logger.info(f"Computed pairs: {pairs}")
        print(f"Computed pairs: {pairs}")  # For development and debugging

        # Create response with the pairs included
        if pairs:
            response = "Here are the ingredient pairings with type I found:\n\n"
            for pair in pairs:
                response += (
                    f"- {pair['item']}: {pair['quantity']} "
                    f"(type: {pair['type']})\n"
                )
        else:
            response = (
                "I couldn't find any valid pairings. "
                "Please make sure to include foods/spices, their quantities, and types."
            )

        # Send the response back to the user
        dispatcher.utter_message(text=response)

        return []