import os
from google import genai
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini Client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

class ParsedTransaction(BaseModel):
    intent: str = Field(description="One of: expense, income, lent, borrowed, settle_received, settle_paid")
    amount: float = Field(description="The numeric amount of the transaction")
    category: str = Field(description="Category (Food, Travel, Bills, Shopping, Health, Entertainment, Other)")
    person: Optional[str] = Field(None, description="Person involved if it is an udhaar/settlement transaction")
    note: Optional[str] = Field(None, description="Short description of the transaction")
    needs_clarification: bool = Field(False, description="True if vital info is missing")
    question: Optional[str] = Field(None, description="Question to ask if clarification is needed")

def parse_expense_text(text: str) -> ParsedTransaction:
    """
    Pass the user's text to Gemini and return a structured ParsedTransaction.
    """
    # TODO: Implement google-genai call with few-shot examples and structured output.
    pass
