import json
import re

from google import genai

from app.config import settings


class LLMService:


    def __init__(self):

        self.client = genai.Client(

            api_key=
            settings.GEMINI_API_KEY
        )


        self.model = (
            "gemini-3.6-flash"
        )


    # =================================
    # QUERY UNDERSTANDING
    # =================================

    def _fallback_understand_question(self, question: str) -> dict:
        q_lower = question.lower()
        sector = None
        known_sectors = [
            "energy", "mining", "renewables", "powerline",
            "railways", "dsp", "tender", "construction",
            "security"
        ]
        for s in known_sectors:
            if s in q_lower:
                sector = s.capitalize()
                break

        import re
        time_period = None
        
        match = re.search(r'(last|past)\s+(\d+)?\s*(month|year)s?', q_lower)
        if match:
            num_str = match.group(2)
            num = int(num_str) if num_str else 1
            if "year" in match.group(3):
                num *= 12
            time_period = f"last_{num}_months"
        elif "quarter" in q_lower:
            time_period = "current_quarter"
        elif "month" in q_lower:
            time_period = "current_month"
        elif "year" in q_lower:
            time_period = "current_year"

        if any(k in q_lower for k in ["work order", "completion", "billed", "collected", "receivable", "execution"]):
            intent = "work_order_analysis"
            needs_deals = False
            needs_work_orders = True
        elif any(k in q_lower for k in ["opportunity", "created", "generated", "new deal"]):
            intent = "opportunity_generation"
            needs_deals = True
            needs_work_orders = False
        elif any(k in q_lower for k in ["compare", "overview", "leadership", "executive", "summary"]):
            intent = "business_overview"
            needs_deals = True
            needs_work_orders = True
        else:
            intent = "pipeline_analysis"
            needs_deals = True
            needs_work_orders = False

        return {
            "intent": intent,
            "sector": sector,
            "time_period": time_period,
            "needs_deals": needs_deals,
            "needs_work_orders": needs_work_orders
        }

    def understand_question(
        self,
        question: str
    ) -> dict:

        prompt = f"""
You are a query understanding component
for a business intelligence agent.

The company has two datasets:

1. DEAL FUNNEL
Columns:
- Deal Name
- Owner code
- Client Code
- Deal Status
- Close Date (A)
- Closure Probability
- Masked Deal value
- Tentative Close Date
- Deal Stage
- Product deal
- Sector/service
- Created Date

2. WORK ORDER TRACKER
Columns include:
- Deal name masked
- Customer Name Code
- Serial #
- Nature of Work
- Execution Status
- Data Delivery Date
- Date of PO/LOI
- Probable Start Date
- Probable End Date
- BD/KAM Personnel code
- Sector
- Type of Work
- Amount in Rupees
- Billed Value
- Collected Amount
- Amount to be billed
- Amount Receivable
- Invoice Status
- Collection status
- Billing Status

Classify the question.

Allowed intents:
1. pipeline_analysis
2. pipeline_by_sector
3. opportunity_generation
4. work_order_analysis
5. business_overview
6. leadership_update
7. sector_comparison

Also extract 'time_period' if the user mentions a timeframe.
Valid time_periods:
- "current_month"
- "current_quarter"
- "current_year"
- "last_N_months" (e.g., if user says "last 12 months", return "last_12_months", if "past 3 months", return "last_3_months")

Return ONLY valid JSON containing 'intent', 'time_period', and 'sector' (if applicable).

Question:
{question}
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            text = response.text.strip()
            text = re.sub(r"^```json", "", text, flags=re.MULTILINE)
            text = re.sub(r"^```", "", text, flags=re.MULTILINE).strip()

            parsed = json.loads(text)
            if not isinstance(parsed, dict):
                return self._fallback_understand_question(question)
            return parsed

        except Exception as e:
            print(f"[LLMService] Gemini API call failed ({e}), using fallback parser.")
            parsed = self._fallback_understand_question(question)
            parsed["fallback_error"] = str(e)
            return parsed


    # =================================
    # EXECUTIVE ANSWER
    # =================================

    def _fallback_generate_answer(
        self,
        question: str,
        analysis: dict,
        data_quality: list[str],
        error_msg: str = "Unknown error"
    ) -> str:
        
        # If understand_question failed earlier, include its error too
        parser_error = analysis.get("fallback_error")
        
        # Hide internal error details from the user, provide a generic explanation
        if parser_error and "429" in error_msg:
            error_str = "High demand/Rate limited (Parser & Generator)"
        elif "429" in error_msg:
            error_str = "High demand/Rate limited (Generator)"
        elif parser_error:
            error_str = "Query parsing failed, used strict keyword fallback"
        else:
            error_str = "Service unavailable"

        lines = [
            "### Executive Analysis Summary (Auto-Generated)",
            f"> **API Error Alert**: Due to an AI service error (`{error_str}`), this is an automated structured summary.",
            "",
            f"**Question**: {question}\n"
        ]

        # Extract the date filter note if present
        date_note = analysis.get("date_filter_note", "")
        if date_note:
            lines.append(f"> **Context Alert**: {date_note}\n")

        analysis_type = analysis.get("analysis_type", "Business Analysis")
        
        lines.append("### Key Metrics & Insights")
        for key, val in analysis.items():
            if key in ["analysis_type", "filters", "date_fallback_applied", "date_filter_note", "message"]:
                continue
            
            clean_key = key.replace('_', ' ').title()
            
            if isinstance(val, (int, float)):
                formatted_val = f"{val:,.2f}" if isinstance(val, float) else f"{val:,}"
                lines.append(f"* **{clean_key}**: {formatted_val}")
            
            elif isinstance(val, dict) and val:
                lines.append(f"\n#### {clean_key} Breakdown")
                for sub_k, sub_v in val.items():
                    if isinstance(sub_v, dict):
                        # Nested dict (like sector breakdown)
                        metrics_str = ", ".join(
                            f"{mk.replace('_', ' ').title()}: {mv:,.2f}" if isinstance(mv, (float, int)) and not isinstance(mv, bool) else f"{mk.replace('_', ' ').title()}: {mv}"
                            for mk, mv in sub_v.items()
                        )
                        lines.append(f"  - **{str(sub_k).title()}**: {metrics_str}")
                    else:
                        if isinstance(sub_v, (int, float)) and not isinstance(sub_v, bool):
                            formatted_sub = f"{sub_v:,.2f}" if isinstance(sub_v, float) else f"{sub_v:,}"
                        else:
                            formatted_sub = str(sub_v)
                        lines.append(f"  - **{str(sub_k).title()}**: {formatted_sub}")

        if data_quality:
            lines.append("\n### Risks & Data Quality Caveats")
            for note in data_quality:
                # Avoid duplicating the date note
                if note != date_note:
                    lines.append(f"* {note}")

        return "\n".join(lines)

    def generate_answer(
        self,
        question: str,
        analysis: dict,
        data_quality: list[str]
    ) -> str:

        prompt = f"""
You are a business intelligence
assistant for company founders
and executives.

Answer the user's question using
ONLY the calculated analysis provided.

Do NOT invent numbers.
Do NOT perform new calculations.
Do NOT claim causation unless
directly supported by the data.

Be concise but insightful.

Structure the response as:
1. Executive summary
2. Key metrics
3. Important insights
4. Risks or caveats

User Question:
{question}

Calculated Analysis:
{json.dumps(analysis, default=str, indent=2)}

Data Quality Notes:
{json.dumps(data_quality, indent=2)}
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"[LLMService] Gemini generate_answer failed ({e}), using fallback formatting.")
            return self._fallback_generate_answer(question, analysis, data_quality, str(e))


llm_service = LLMService()