# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "list_ingredients"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Get entities from the latest user message
        entities = tracker.latest_message.get("entities", [])

        if entities:
            # Build a list of entity-value pairs
            entity_list = [f"- {entity['entity']}: {entity['value']}" for entity in entities]
            response_text = "I found the following entities:\n" + "\n".join(entity_list)
        else:
            response_text = "I didn’t find any entities in your message."

        dispatcher.utter_message(response_text)
        return []

