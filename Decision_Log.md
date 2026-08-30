# Decision Log

## 1. Key Assumptions Made
* **Data Refresh Rate**: It is assumed that the data in Monday.com is not updated every single second, allowing the application to cache the data per session or at a reasonable interval if performance became a bottleneck, although currently, the agent dynamically fetches the data upon each query for maximum accuracy.
* **API Constraints**: It is assumed that the Gemini API is the primary model for inference but given rate limit exhaustion errors (429 RESOURCE_EXHAUSTED), a robust fallback parsing and generating mechanism using RegEx/rule-based analytics is required to keep the application functional at all times.
* **Date Context**: The "current month" and "current year" are strictly bound to the data's timeline. Given the provided dataset (e.g. deals recorded up to January 2026), the system assumes that queries regarding "last 6 months" should intelligently adapt to the maximum available date in the dataset if no data exists in the absolute present calendar month.

## 2. Trade-offs Chosen and Why
* **Deterministic Analytics vs. LLM Code Execution**: I chose to restrict the LLM purely to intent-parsing and final explanation-generation, pushing all mathematical aggregation, filtering, and counting to a deterministic Python Pandas analytics engine (`analytics_service.py`).
  * *Why*: LLMs frequently hallucinate numbers and miscount records. By separating the routing logic from the math logic, the system guarantees 100% accuracy on financial totals and record counts while preserving the conversational flexibility of AI.
* **Semantic Token Time Filtering vs. Dynamic Range Parsing**: I opted for a hybrid time-filtering approach where the LLM or Fallback Regex maps user phrases to standard semantic tokens (e.g. `last_6_months`, `current_quarter`).
  * *Why*: Attempting to let the LLM generate arbitrary date ranges (e.g., `2025-01-01 to 2025-06-30`) requires extremely strict prompt engineering and validation. Semantic tokens delegate the date math safely to Python's `dateutils`/`pandas`, avoiding hallucinated dates.
* **Read-only Monday.com Architecture**: The agent strictly limits its API requests to read operations.
  * *Why*: Allowing an LLM agent to mutate or write operational project data poses a massive security/integrity risk without human-in-the-loop approvals.
* **Generic Fallback Error Display**: Instead of exposing raw API exceptions and stack traces directly in the UI, I map API errors to generic user-friendly strings (e.g. "High demand/Rate limited").
  * *Why*: Protects backend execution context and prevents overwhelming the user with internal JSON error blocks, maintaining an executive-level experience.

## 3. What You'd Do Differently With More Time
* **Agentic Multi-Step Reasoning (ReAct)**: Instead of a single intent-routing pass, I would implement a fully agentic ReAct loop where the agent could iteratively query the analytics engine, analyze the intermediate results, and decide to run follow-up analytical functions before finally answering the user.
* **Monday.com Webhook Subscriptions**: I would implement Webhooks to sync Monday.com updates to a local SQLite/PostgreSQL caching layer in real-time. This would eliminate the latency of hitting the Monday.com GraphQL API on every user query.
* **Visualization Engine**: Integrate a charting library (like `recharts` or `chart.js`) in the frontend, and allow the backend analytics service to return JSON configurations for rendering dynamic bar charts or pie charts based on sector breakdowns.

## 4. How You Interpreted "Leadership Updates"
I interpreted "Leadership Updates" as a **high-level, cross-functional executive briefing** that abstracts away minor details to focus strictly on overall business health and major operational bottlenecks. 

Specifically, when the user asks for a leadership update, the agent:
1. **Aggregates Multi-Board Data**: It automatically triggers analysis across *both* the Deals Pipeline (Sales) and Work Orders (Operations) datasets without needing the user to specify.
2. **Focuses on Key KPIs**: It isolates macro-metrics: Total Pipeline Value, Total Billed Value, Total Collected Amount, and Total Outstanding Receivables.
3. **Highlights Data Quality/Risks**: Instead of just reporting numbers, a true leadership update must point out blind spots. The agent automatically calculates and reports data risks (e.g., "176 deal records have missing or invalid deal values"), which is crucial for a founder assessing the trustworthiness of their projections.
