# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import logging
logger = logging.getLogger(__name__)


class ActionFetchRecipe(Action):
    def name(self) -> Text:
        return "action_fetch_recipe"

    def get_recipe_file(self, recipe_name: Text) -> Text:
        # Map recipe names to their corresponding files
        recipe_files = {
            "aloo gobi": "aalu-gobi.txt",
            "aalu gobi": "aalu-gobi.txt",
            # "butter chicken": "butter-chicken.txt",
            # "dal makhani": "dal-makhani.txt",
        }

        # Return the corresponding file name for the recipe, if it exists
        return recipe_files.get(recipe_name.lower(), None)

    def read_file_content(self, file_name: Text) -> Text:
        file_path = os.path.join("documents/recipes", file_name)  # Modify path as needed
        # file_path = os.path.join("/Users/mayankarora/dib/poc/chatbot-book/food_bot/documents/recipes", file_name)  # Modify path as needed

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return file.read()
        return "Sorry, I couldn't find the recipe for that dish in file: " + file_name


    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Extract the recipe name from the user's input
        recipe_name = next(tracker.get_latest_entity_values("recipe_name"), None)
        logger.info(f"Received recipe_name: {recipe_name}")

        if recipe_name:
            # Get the corresponding file name for the recipe
            file_name = self.get_recipe_file(recipe_name)
            logger.info(f"Received file_name: {file_name}")

            if file_name:
                # Read the recipe content from the file
                recipe_content = self.read_file_content(file_name)

                if recipe_content:
                    # Respond with the recipe content
                    dispatcher.utter_message(text=recipe_content)
                else:
                    dispatcher.utter_message(
                        text=f"I found the recipe file for '{recipe_name}', but it seems empty or unreadable.")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find the recipe file for '{recipe_name}'.")
        else:
            dispatcher.utter_message(text="Could you please tell me the name of the recipe?")

        return []
