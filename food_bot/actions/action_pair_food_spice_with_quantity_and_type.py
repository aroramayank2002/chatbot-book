from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import logging

# Initialize logger
logger = logging.getLogger(__name__)


def split_on_or(value: str) -> List[str]:
    """
    Splits a string on the literal substring ' or ' to handle multiple variations.
    Example: "Kashmiri chili powder or paprika" => ["Kashmiri chili powder", "paprika"]
    """
    if not value:
        return []
    # Note: this is a simple approach that only splits on ' or ' (lowercase with spaces).
    # If needed, consider more nuanced parsing or case-insensitive matching.
    parts = [v.strip() for v in value.split(" or ")]
    return parts if parts else []


class ActionPairFoodSpiceTypeWithQty(Action):
    def name(self) -> Text:
        return "action_pair_food_spice_type_with_qty"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        """
        This action pairs any 'food' or 'spice' entity with the nearest preceding 'qty' entity,
        and also attempts to match the nearest preceding 'type' entity. If any entity contains
        ' or ', we split it into multiple possible values, resulting in multiple distinct pairings.
        """

        entities = tracker.latest_message.get("entities", [])
        logger.info(f"Extracted entities: {entities}")
        print(f"Extracted entities: {entities}")  # For local debugging

        # Group entities by type
        food_entities = [e for e in entities if e.get("entity") == "food"]
        spice_entities = [e for e in entities if e.get("entity") == "spice"]
        qty_entities = [e for e in entities if e.get("entity") == "qty"]
        type_entities = [e for e in entities if e.get("entity") == "type"]

        logger.info(f"Food entities: {food_entities}")
        logger.info(f"Spice entities: {spice_entities}")
        logger.info(f"Qty entities: {qty_entities}")
        logger.info(f"Type entities: {type_entities}")

        def get_closest_preceding(entities_list: List[Dict], current_start: int) -> Dict[str, Any]:
            """
            Returns the entity in entities_list whose 'start' is closest to (but not greater than)
            current_start. If none is found, returns None.
            """
            candidate = None
            for ent in entities_list:
                if ent["start"] <= current_start:
                    if candidate is None or ent["start"] > candidate["start"]:
                        candidate = ent
            return candidate

        # Convert all relevant entities to a structured form, splitting on 'or' if present
        def build_item_list(ents: List[Dict], label: Text) -> List[Dict]:
            """
            For all given entities, returns a list of dicts:
            { "start": ..., "possible_values": [list_of_values_after_splitting], "type": label }
            """
            results = []
            for e in ents:
                raw_value = e.get("value", "")
                sub_values = split_on_or(raw_value)  # handle multiple "or" variants
                results.append({
                    "start": e.get("start", 0),
                    "possible_values": sub_values,
                    "type": label
                })
            return results

        foods = build_item_list(food_entities, label="food")
        spices = build_item_list(spice_entities, label="spice")

        # For quantities and types, we'll also store them in a similar structure
        quantities = []
        for e in qty_entities:
            raw_value = e.get("value", "")
            sub_values = split_on_or(raw_value)
            quantities.append({
                "start": e.get("start", 0),
                "possible_values": sub_values
            })

        typedescs = []
        for e in type_entities:
            raw_value = e.get("value", "")
            sub_values = split_on_or(raw_value)
            typedescs.append({
                "start": e.get("start", 0),
                "possible_values": sub_values
            })

        # We merge foods and spices into a single "items" list.
        items = sorted(foods + spices, key=lambda x: x["start"])
        quantities = sorted(quantities, key=lambda x: x["start"])
        typedescs = sorted(typedescs, key=lambda x: x["start"])

        # Build preliminary pairs: each item gets matched with the nearest preceding qty and type
        preliminary_pairs = []
        for item in items:
            q = get_closest_preceding(quantities, item["start"])
            t = get_closest_preceding(typedescs, item["start"])
            # We'll store the entire arrays of possible values to expand later
            pair_info = {
                "item_vals": item["possible_values"],
                "item_label": item["type"],  # "food" or "spice"
                "qty_vals": q["possible_values"] if q else [],
                "type_vals": t["possible_values"] if t else []
            }
            preliminary_pairs.append(pair_info)

        logger.info(f"Preliminary pairs (unexpanded): {preliminary_pairs}")
        print(f"Preliminary pairs (unexpanded): {preliminary_pairs}")

        # Now we expand each preliminary pair if it has multiple possible values for item, qty, type
        expanded_pairs = []
        for pair in preliminary_pairs:
            for i_val in pair["item_vals"]:
                # If there's no quantity or type, we keep them as empty or single
                # so we at least produce a single pairing with missing fields
                if pair["qty_vals"]:
                    qty_variants = pair["qty_vals"]
                else:
                    # If there's no quantity, just create a placeholder
                    qty_variants = [None]

                if pair["type_vals"]:
                    type_variants = pair["type_vals"]
                else:
                    type_variants = [None]

                for q_val in qty_variants:
                    for t_val in type_variants:
                        expanded_pairs.append({
                            "item": i_val,
                            "item_label": pair["item_label"],
                            "quantity": q_val,
                            "type_description": t_val
                        })

        logger.info(f"Computed expanded pairs: {expanded_pairs}")
        print(f"Computed expanded pairs: {expanded_pairs}")

        # Format response to user
        if expanded_pairs:
            response = "Here are all the possible pairings (including variations with 'or'):\n\n"
            for p in expanded_pairs:
                # If quantity or type is missing, note that
                qty_display = p["quantity"] if p["quantity"] else "no qty"
                type_display = p["type_description"] if p["type_description"] else "no type"
                response += (
                    f"- {p['item']} ({p['item_label']}): {qty_display}, type: {type_display}\n"
                )
        else:
            response = (
                "I couldn't find any valid pairings. "
                "Please include foods/spices, their quantities, and optional types."
            )

        dispatcher.utter_message(text=response)
        return []