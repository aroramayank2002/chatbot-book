from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionListEntities(Action):
    def name(self) -> Text:
        return "action_list_entities"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract entities from the user's message
        # food_entities = [e["value"] for e in tracker.latest_message["entities"] if e["entity"] == "food"]
        # spice_entities = [e["value"] for e in tracker.latest_message["entities"] if e["entity"] == "spice"]
        # qty_entities = [e["value"] for e in tracker.latest_message["entities"] if e["entity"] == "qty"]

        # Avoid duplicate in logs unlike the above lines
        food_entities = list(set([e["value"] for e in tracker.latest_message["entities"] if e["entity"] == "food"]))
        spice_entities = list(set([e["value"] for e in tracker.latest_message["entities"] if e["entity"] == "spice"]))
        qty_entities = list(set([e["value"] for e in tracker.latest_message["entities"] if e["entity"] == "qty"]))
        medium_entities = list(set([e["value"] for e in tracker.latest_message["entities"] if e["entity"] == "medium"]))
        type_entities = list(set([e["value"] for e in tracker.latest_message["entities"] if e["entity"] == "type"]))

        # Compile the response message
        response = "Here are the details I extracted:\n"

        if qty_entities:
            response += f"- Quantities: {', '.join(qty_entities)}\n"
        if food_entities:
            response += f"- Foods: {', '.join(food_entities)}\n"
        if spice_entities:
            response += f"- Spices: {', '.join(spice_entities)}\n"
        if medium_entities:
            response += f"- Medium: {', '.join(medium_entities)}\n"
        if type_entities:
            response += f"- Type: {', '.join(type_entities)}\n"

        if not qty_entities and not food_entities and not spice_entities:
            response += "I couldn't find any information related to food, spices, quantities or medium."

        # Send the response back to the user
        dispatcher.utter_message(text=response)
        return []