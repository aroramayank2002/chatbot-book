from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from rasa_sdk import FormValidationAction


class ValidateSimplePizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_pizza_form"

    async def validate_pizza_size(
            self,
            value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""
        valid_pizza_sizes = ["small", "medium", "large"]
        if value.lower() in valid_pizza_sizes:
            return {"pizza_size": value}
        else:
            dispatcher.utter_message(text=f"'{value}' is not a valid size. Please choose from small, medium, or large.")
            return {"pizza_size": None}

    async def validate_pizza_type(
            self,
            value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_type` value."""
        valid_pizza_types = ["pepperoni", "cheese", "vegetarian", "margherita"]
        if value.lower() in valid_pizza_types:
            return {"pizza_type": value}
        else:
            dispatcher.utter_message(
                text=f"'{value}' is not a valid type. Please choose from pepperoni, cheese, vegetarian, or margherita.")
            return {"pizza_type": None}