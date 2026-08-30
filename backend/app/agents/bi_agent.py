from app.services.monday_client import (
    monday_client
)

from app.services.analytics_service import (
    analytics_service
)

from app.services.llm_service import (
    llm_service
)


class BIAgent:

    async def answer_question(
        self,
        question: str
    ):

        intent_data = (
            llm_service
            .understand_question(question)
        )

        intent = (
            intent_data
            .get("intent")
        )

        sector = (
            intent_data
            .get("sector")
        )

        time_period = (
            intent_data
            .get("time_period")
        )

        if intent == "pipeline_analysis":

            deals_board = (
                await monday_client.get_deals()
            )

            deals_df = (
                analytics_service
                .prepare_deals(
                    deals_board
                )
            )

            analysis = (
                analytics_service
                .pipeline_analysis(
                    deals_df,
                    sector=sector,
                    current_quarter=(
                        time_period
                        == "current_quarter"
                    )
                )
            )

        elif intent == "work_order_analysis":

            work_board = (
                await monday_client
                .get_work_orders()
            )

            work_df = (
                analytics_service
                .prepare_work_orders(
                    work_board
                )
            )

            analysis = (
                analytics_service
                .work_order_analysis(
                    work_df,
                    sector=sector
                )
            )

        elif intent == "sector_comparison":

            deals_board = (
                await monday_client.get_deals()
            )

            work_board = (
                await monday_client
                .get_work_orders()
            )

            deals_df = (
                analytics_service
                .prepare_deals(
                    deals_board
                )
            )

            work_df = (
                analytics_service
                .prepare_work_orders(
                    work_board
                )
            )

            analysis = {
                "sector_comparison":
                    analytics_service
                    .sector_comparison(
                        deals_df,
                        work_df
                    )
            }

        else:
            analysis = {
                "error":
                    "Unable to classify the business question.",
                "supported_queries": [
                    "pipeline analysis",
                    "work order analysis",
                    "sector comparison",
                    "leadership update"
                ]
            }

        answer = (
            llm_service.generate_answer(
                question,
                analysis
            )
        )

        return {
            "answer": answer,
            "intent": intent,
            "data_quality": {
                "analysis_based_on":
                    "Live monday.com board data"
            }
        }


bi_agent = BIAgent()