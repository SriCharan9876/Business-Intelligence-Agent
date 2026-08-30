from app.services.llm_service import (
    llm_service
)

from app.services.monday_client import (
    monday_client
)

from app.services.data_cleaner import (
    data_cleaner
)

from app.services.analytics_service import (
    analytics_service
)


class BIAgent:


    async def answer_question(
        self,
        question: str
    ) -> dict:


        # ==========================
        # STEP 1
        # UNDERSTAND QUESTION
        # ==========================

        query_info = (

            llm_service
            .understand_question(
                question
            )
        )


        intent = (

            query_info.get(
                "intent",
                "unknown"
            )
        )


        sector = (
            query_info.get(
                "sector"
            )
        )


        time_period = (
            query_info.get(
                "time_period"
            )
        )


        needs_deals = (
            query_info.get("needs_deals")
        )
        if needs_deals is None or not needs_deals:
            needs_deals = intent in [
                "pipeline_analysis",
                "pipeline_by_sector",
                "opportunity_generation",
                "business_overview",
                "leadership_update",
                "sector_comparison",
                "unknown"
            ]

        needs_work_orders = (
            query_info.get("needs_work_orders")
        )
        if needs_work_orders is None or not needs_work_orders:
            needs_work_orders = intent in [
                "work_order_analysis",
                "business_overview",
                "leadership_update",
                "sector_comparison",
                "unknown"
            ]


        # ==========================
        # STEP 2
        # FETCH DATA
        # ==========================

        deals_df = None

        work_orders_df = None


        if needs_deals:

            raw_deals = (

                await monday_client
                .get_deals_data()
            )


            deals_df = (

                data_cleaner
                .clean_deals(
                    raw_deals
                )
            )


        if needs_work_orders:

            raw_work_orders = (

                await monday_client
                .get_work_orders_data()
            )


            work_orders_df = (

                data_cleaner
                .clean_work_orders(
                    raw_work_orders
                )
            )


        # ==========================
        # STEP 3
        # DATA QUALITY
        # ==========================

        data_quality = (

            self.get_data_quality_notes(

                deals_df,

                work_orders_df
            )
        )


        # ==========================
        # STEP 4
        # ANALYSIS ROUTING
        # ==========================

        analysis = (

            self.run_analysis(

                intent=intent,

                sector=sector,

                time_period=time_period,

                deals_df=deals_df,

                work_orders_df=
                    work_orders_df
            )
        )

        if isinstance(analysis, dict) and analysis.get("date_filter_note"):
            data_quality.insert(0, analysis["date_filter_note"])


        # ==========================
        # STEP 5
        # EXECUTIVE RESPONSE
        # ==========================

        answer = (

            llm_service
            .generate_answer(

                question=question,

                analysis=analysis,

                data_quality=
                    data_quality
            )
        )


        # ==========================
        # STEP 6
        # FINAL RESPONSE
        # ==========================

        return {

            "answer":
                answer,

            "intent":
                intent,

            "analysis":
                analysis,

            "data_quality":
                data_quality
        }


    # =================================
    # ANALYSIS ROUTER
    # =================================

    def run_analysis(

        self,

        intent,

        sector,

        time_period,

        deals_df,

        work_orders_df
    ):

        # -----------------------------
        # OPPORTUNITY GENERATION
        # -----------------------------

        if intent == (
            "opportunity_generation"
        ):

            return (

                analytics_service
                .analyze_opportunity_generation(

                    deals_df,

                    sector=sector,

                    time_period=time_period
                )
            )
        # -----------------------------
        # PIPELINE
        # -----------------------------

        if intent == (
            "pipeline_analysis"
        ):

            return (

                analytics_service
                .analyze_pipeline(

                    deals_df,

                    sector=sector,

                    time_period=
                        time_period
                )
            )


        # -----------------------------
        # PIPELINE BY SECTOR
        # -----------------------------

        if intent == (
            "pipeline_by_sector"
        ):

            return {

                "analysis_type":
                    "pipeline_by_sector",

                "results":

                    analytics_service
                    .analyze_pipeline_by_sector(

                        deals_df
                    )
            }


        # -----------------------------
        # WORK ORDERS
        # -----------------------------

        if intent == (
            "work_order_analysis"
        ):

            return (

                analytics_service
                .analyze_work_orders(

                    work_orders_df,

                    sector=sector
                )
            )


        # -----------------------------
        # BUSINESS OVERVIEW / LEADERSHIP / SECTOR COMPARISON
        # -----------------------------

        if intent in [
            "business_overview",
            "leadership_update",
            "sector_comparison"
        ]:

            return (

                analytics_service
                .analyze_business_overview(

                    deals_df,

                    work_orders_df,

                    sector=sector
                )
            )


        # -----------------------------
        # FALLBACK (DEFAULT TO BUSINESS OVERVIEW IF DATA PRESENT)
        # -----------------------------

        if deals_df is not None or work_orders_df is not None:
            return (
                analytics_service
                .analyze_business_overview(
                    deals_df,
                    work_orders_df,
                    sector=sector
                )
            )

        return {

            "analysis_type":
                "unknown",

            "message":

                "The question could not "
                "be mapped to a supported "
                "business analysis."
        }


    # =================================
    # DATA QUALITY CHECKS
    # =================================

    def get_data_quality_notes(

        self,

        deals_df,

        work_orders_df
    ) -> list[str]:


        notes = []


        # ==========================
        # DEALS QUALITY
        # ==========================

        if (

            deals_df is not None

            and

            not deals_df.empty
        ):


            if (

                "Masked Deal value"

                in deals_df.columns
            ):

                missing_values = int(

                    deals_df[
                        "Masked Deal value"
                    ]

                    .isna()

                    .sum()
                )


                if missing_values > 0:

                    notes.append(

                        f"{missing_values} deal "
                        "records have missing or "
                        "invalid deal values."
                    )


            if (

                "Sector/service"

                in deals_df.columns
            ):

                missing_sector = int(

                    deals_df[
                        "Sector/service"
                    ]

                    .isna()

                    .sum()
                )


                if missing_sector > 0:

                    notes.append(

                        f"{missing_sector} deal "
                        "records have missing "
                        "sector information."
                    )


            if (

                "Tentative Close Date"

                in deals_df.columns
            ):

                missing_date = int(

                    deals_df[
                        "Tentative Close Date"
                    ]

                    .isna()

                    .sum()
                )


                if missing_date > 0:

                    notes.append(

                        f"{missing_date} deal "
                        "records have missing or "
                        "invalid tentative close "
                        "dates."
                    )


        # ==========================
        # WORK ORDER QUALITY
        # ==========================

        if (

            work_orders_df is not None

            and

            not work_orders_df.empty
        ):


            if (

                "Amount Receivable (Masked)"

                in work_orders_df.columns
            ):

                missing_receivable = int(

                    work_orders_df[
                        "Amount Receivable (Masked)"
                    ]

                    .isna()

                    .sum()
                )


                if missing_receivable > 0:

                    notes.append(

                        f"{missing_receivable} work "
                        "order records have missing "
                        "receivable values."
                    )


            if (

                "Execution Status"

                in work_orders_df.columns
            ):

                missing_status = int(

                    work_orders_df[
                        "Execution Status"
                    ]

                    .isna()

                    .sum()
                )


                if missing_status > 0:

                    notes.append(

                        f"{missing_status} work "
                        "orders have missing "
                        "execution status."
                    )


        if not notes:

            notes.append(

                "No major missing-data issues "
                "were detected in the fields "
                "used for this analysis."
            )


        return notes


bi_agent = BIAgent()