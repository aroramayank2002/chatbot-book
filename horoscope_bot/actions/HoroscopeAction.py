from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGetHoroscope(Action):
    def name(self) -> Text:
        return "action_get_horoscope"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        zodiac_sign = tracker.get_slot("zodiac_sign")  # Retrieve slot from user input

        # Hardcoded horoscope predictions (example)
        horoscopes = {
            "aries": "Your energy levels are high today. A good day to take on new challenges!",
            "taurus": "Patience is your best friend today. Avoid rushing important decisions.",
            "gemini": "You might find yourself juggling multiple tasks. Stay flexible.",
            "cancer": "An emotional day, but your instincts will guide you through any challenges.",
            "leo": "A perfect day for creativity! Take time to focus on your hobbies.",
            "virgo": "Organization and planning will be key to achieving your goals today.",
            "libra": "Balance is crucial. Spend time with someone who inspires or supports you.",
            "scorpio": "Your passion helps you excel, but avoid unnecessary conflict.",
            "sagittarius": "A day of exploration! Step outside your comfort zone and try something new.",
            "capricorn": "Hard work pays off. Stay focused and keep working toward your objectives.",
            "aquarius": "Your unique ideas will shine in group discussions. Share your thoughts!",
            "pisces": "Trust your intuition today, and let your creativity bloom."
        }

        # Fetch the horoscope for the specific zodiac sign
        if zodiac_sign in horoscopes:
            dispatcher.utter_message(
                text=f"Here is your horoscope for {zodiac_sign.capitalize()}: {horoscopes[zodiac_sign]}"
            )
        else:
            dispatcher.utter_message(
                text="I couldn't find a horoscope for that zodiac sign. Please try again."
            )

        return []  # No slots are modified