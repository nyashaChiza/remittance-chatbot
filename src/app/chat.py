from fastapi import HTTPException
from loguru import logger
from src.app.intent_actions import INTENT_ACTIONS
from src.app.state import get_state_instance
import re

class Chat:
    def __init__(self, state=None):
        self.state = state or get_state_instance()
        self.intent_actions = INTENT_ACTIONS

    @staticmethod
    def get_intent(prompt: str) -> str:
        """
        Determines the appropriate intent based on the prompt using pattern matching.
        """
        prompt = prompt.lower().strip()

        patterns = {
            "greeting": r"\b(hello|hi|hie|hey|good morning|good afternoon|good evening|greetings|howdy)\b",
            "good_bye": r"\b(thank you|thanks|bye|goodbye|i'm good|i'm all set|got it)\b",
        }

        for intent, pattern in patterns.items():
            if re.search(pattern, prompt):
                return intent

        return "unknown"
    

    def process_prompt(self,data: dict) -> dict:
        try:
            platform = data.get("Platform", "whatsapp")
            message = data.get("Body", "").strip().lower()
            sender = data.get("From")

            if not message or not sender:
                raise HTTPException(status_code=422, detail="Missing required fields: 'message' or 'sender'")

            return {
                "platform": platform,
                "message": message,
                "sender": sender
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Input processing error: {str(e)}")


_chat_instance = None  # Private variable to hold the single instance of Chat

def get_chatbot_instance() -> Chat:
    """
    Factory function to return a singleton instance of the Chat class.
    If an instance already exists, it returns that instance.
    Otherwise, it creates a new one.
    """
    global _chat_instance
    if _chat_instance is None:
        state = get_state_instance()
        _chat_instance = Chat(state=state)
    return _chat_instance

