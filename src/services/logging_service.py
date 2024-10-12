import datetime
from supabase import Client

class LoggingService:
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client

    def log_interaction(self, user_question: str | None, bot_response: str)-> str | None:
        data = {
            "user_question": user_question,
            "bot_response": bot_response,
        }   

        try:
            response = self.supabase.schema("public").table("conversations_logs").insert(data).execute()
            return response.data[0].get("id")
        except Exception as e:
            print(e)
            return None

    def log_feedback(self, run_id: str, feedback: dict):
        data = {
            "liked":  True if feedback["score"] == "👍" else False,
            "reason": feedback["text"],
        }

        try:
            self.supabase.schema("public").table("conversations_logs").update(data).eq('id', run_id).execute()
        except Exception as e:
            print(e)