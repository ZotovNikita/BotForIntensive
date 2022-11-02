from typing import Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionProblems(Action):

    def name(self) -> Text:
        return "action_problems"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Text]) -> List[Dict[Text, Text]]:
        dispatcher.utter_message(text="Модератор свяжется с вами в течение дня, ожидайте :)")
        print(tracker.slots)
        return []

class ActionWishes(Action):

    def name(self) -> Text:
        return "action_wishes"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: List[Text]) -> List[List[Text]]:
        dispatcher.utter_message(text="Спасибо за обратную связь :)")
        print(tracker.slots)
        return []