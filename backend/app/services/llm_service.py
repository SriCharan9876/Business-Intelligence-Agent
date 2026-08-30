import json
from typing import Optional, Literal
from pydantic import BaseModel

from google import genai
from google.genai import types

from app.config import settings


class QuerySchema(BaseModel):
    intent: Literal[
        "pipeline_analysis",
        "work_order_analysis",
        "sector_comparison",
        "leadership_update"
    ]
    sector: Optional[str] = None
    time_period: Optional[str] = None


class LLMService:

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = "gemini-2.5-flash"


    def understand_question(
        self,
        question: str
    ):

        prompt = f"""
You are a Business Intelligence
query understanding system.

You work with two monday.com boards.

DEALS BOARD:

- Deal Name
- Deal Status
- Close Date
- Closure Probability
- Deal Value
- Tentative Close Date
- Deal Stage
- Product
- Sector
- Created Date

WORK ORDERS BOARD:

- Customer
- Nature of Work
- Execution Status
- Delivery Date
- Start Date
- End Date
- Sector
- Work Order Value
- Billed Value
- Collected Amount
- Receivable Amount
- Billing Status
- Collection Status

Classify the user's business question.

Use:

pipeline_analysis
for sales, deals, pipeline and
opportunities.

Use:

work_order_analysis
for operations, execution,
billing, collection and
work orders.

Use:

sector_comparison
when comparing sectors or
combining sales and operations.

Use:

leadership_update
when requesting an executive,
leadership or founder update.

Time period values:

current_quarter
current_month
this_year
all_time
or null.

User question:

{question}
"""

        response = (
            self.client.models.generate_content(

                model=self.model,

                contents=prompt,

                config=
                    types.GenerateContentConfig(

                        response_mime_type=
                            "application/json",

                        response_schema=
                            QuerySchema,

                        temperature=0
                    )
            )
        )

        return json.loads(
            response.text
        )


    def generate_answer(
        self,
        question: str,
        analysis: dict
    ):

        analysis_json = json.dumps(
            analysis,
            default=str,
            indent=2
        )

        prompt = f"""
You are an executive Business
Intelligence Agent for Skylark Drones.

Answer using ONLY the provided
analysis.

Never invent metrics or numbers.

The audience is a founder.

Your response should contain:

DIRECT ANSWER

KEY INSIGHTS

RISKS OR CAVEATS

DATA QUALITY NOTES
only if relevant.

Be concise and business-focused.

Question:

{question}

Analysis:

{analysis_json}
"""

        response = (
            self.client.models.generate_content(

                model=self.model,

                contents=prompt,

                config=
                    types.GenerateContentConfig(

                        temperature=0.2
                    )
            )
        )

        return response.text


llm_service = LLMService()