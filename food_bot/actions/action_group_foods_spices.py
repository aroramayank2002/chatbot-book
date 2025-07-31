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
        # 1) Extract entities
        entities = tracker.latest_message.get("entities", [])
        logger.info(f"Extracted entities: {entities}")

        # Separate out relevant entities
        food_entities = [e for e in entities if e.get("entity") == "food"]
        spice_entities = [e for e in entities if e.get("entity") == "spice"]
        qty_entities = [e for e in entities if e.get("entity") == "qty"]
        type_entities = [e for e in entities if e.get("entity") == "type"]

        # 2) Convert them into convenient structures
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

        # 4) Create pairs and separate into two groups
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
            if item["item_type"] == "food":
                food_pairs.append(pair)
            else:
                spice_pairs.append(pair)

        logger.info(f"Food Pairs: {food_pairs}")
        logger.info(f"Spice Pairs: {spice_pairs}")

        # 5) Build the aligned/column-based response
        if not food_pairs and not spice_pairs:
            response = (
                "I couldn't find any valid items. "
                "Make sure you have foods/spices, their quantities, and optionally a type."
            )
        else:
            # For best alignment in a monospace environment, you can:
            # • Use formatted string widths (e.g., {:20s}).
            # • Include tabs if you prefer (e.g., \t).
            # Below, we align each column with a width of 20 chars for item,
            # 10 chars for quantity, and then the type at the end.

            response = "Here are the ingredient pairings grouped by category:\n\n"

            # Display foods
            if food_pairs:
                response += "Foods:\n"
                response += f"{'Item':20s}{'Quantity':12s}{'Type'}\n"
                response += "-" * 45 + "\n"
                for pair in food_pairs:
                    response += (
                        f"{pair['item']:20s}"
                        f"{pair['quantity']:12s}"
                        f"{pair['type']}\n"
                    )

            # Spices
            if spice_pairs:
                response += "\nSpices:\n"
                response += f"{'Item':20s}{'Quantity':12s}{'Type'}\n"
                response += "-" * 45 + "\n"
                for pair in spice_pairs:
                    response += (
                        f"{pair['item']:20s}"
                        f"{pair['quantity']:12s}"
                        f"{pair['type']}\n"
                    )

        dispatcher.utter_message(text=response)
        return []