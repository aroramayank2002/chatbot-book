from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import logging

logger = logging.getLogger(__name__)


class ActionPairFoodSpiceTypeWithQty(Action):
    def name(self) -> Text:
        return "action_group_foods_spices"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        # 1) Extract entities from the tracker
        entities = tracker.latest_message.get("entities", [])
        logger.info(f"Extracted entities: {entities}")

        food_entities = [e for e in entities if e.get("entity") == "food"]
        spice_entities = [e for e in entities if e.get("entity") == "spice"]
        qty_entities = [e for e in entities if e.get("entity") == "qty"]
        type_entities = [e for e in entities if e.get("entity") == "type"]

        # 2) Convert to internal structures (tagging which category they belong to)
        foods = [
            {"item_type": "food", "item": e.get("value"), "start": e.get("start")}
            for e in food_entities
        ]
        spices = [
            {"item_type": "spice", "item": e.get("value"), "start": e.get("start")}
            for e in spice_entities
        ]
        quantities = [
            {"qty": e.get("value"), "start": e.get("start")}
            for e in qty_entities
        ]
        types = [
            {"type_label": e.get("value"), "start": e.get("start")}
            for e in type_entities
        ]

        # 3) Sort
        all_items = sorted(foods + spices, key=lambda x: x["start"])
        quantities = sorted(quantities, key=lambda x: x["start"])
        types = sorted(types, key=lambda x: x["start"])

        # 4) Create pairs
        #    Note: In a real scenario, you might have more logic to match
        #    item->quantity->type instead of a simple zip/index-based approach.
        food_pairs = []
        spice_pairs = []
        for i, item in enumerate(all_items):
            qty_val = quantities[i]["qty"] if i < len(quantities) else None
            type_val = types[i]["type_label"] if i < len(types) else None
            pair = {
                "item": item["item"],
                "quantity": qty_val if qty_val else "No quantity",
                "type": type_val if type_val else "No type"
            }
            # Add to appropriate category
            if item["item_type"] == "food":
                food_pairs.append(pair)
            else:
                spice_pairs.append(pair)

        logger.info(f"Food Pairs: {food_pairs}")
        logger.info(f"Spice Pairs: {spice_pairs}")

        # 5) Create response grouped by foods and spices
        if not food_pairs and not spice_pairs:
            response = (
                "I couldn't find any valid items. "
                "Make sure you have foods/spices, their quantities, and optionally a type."
            )
        else:
            response = "Here are the ingredient pairings grouped by category:\n\n"

            # Foods
            if food_pairs:
                response += "Foods:\n"
                for pair in food_pairs:
                    response += (
                        f"- {pair['item']}: {pair['quantity']} (type: {pair['type']})\n"
                    )

            # Spices
            if spice_pairs:
                response += "\nSpices:\n"
                for pair in spice_pairs:
                    response += (
                        f"- {pair['item']}: {pair['quantity']} (type: {pair['type']})\n"
                    )

        dispatcher.utter_message(text=response)
        return []