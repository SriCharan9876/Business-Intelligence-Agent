from datetime import datetime

import pandas as pd


class AnalyticsService:


    # =================================
    # HELPER METHODS
    # =================================

    def safe_sum(
        self,
        series
    ):

        if series is None:

            return 0.0


        value = series.sum(
            skipna=True
        )


        if pd.isna(value):

            return 0.0


        return float(value)


    def safe_mean(
        self,
        series
    ):

        if series is None:

            return None


        value = series.mean(
            skipna=True
        )


        if pd.isna(value):

            return None


        return float(value)


    def percentage(
        self,
        numerator,
        denominator
    ):

        if not denominator:

            return None


        return round(

            (
                numerator
                /
                denominator
            )
            * 100,

            2
        )


    # =================================
    # FILTER HELPERS
    # =================================

    def filter_by_sector(
        self,
        df,
        sector,
        sector_column
    ):

        if (
            not sector
            or df is None
            or df.empty
            or sector_column not in df.columns
        ):
            return df

        sector_normalized = (
            sector
            .lower()
            .strip()
        )

        if sector_normalized in ["energy", "energy sector"]:
            target_sectors = ["energy", "renewables", "powerline"]
            return df[
                df[sector_column]
                .astype("string")
                .str.lower()
                .str.strip()
                .isin(target_sectors)
            ]

        return df[
            df[sector_column]
            .astype("string")
            .str.lower()
            .str.strip()
            == sector_normalized
        ]


    def filter_current_quarter(
        self,
        df,
        date_column
    ):

        if (

            df.empty

            or date_column
            not in df.columns

        ):

            return df


        today = pd.Timestamp.today()


        quarter = today.quarter

        year = today.year


        dates = df[
            date_column
        ]


        return df[

            (dates.dt.year == year)

            &

            (dates.dt.quarter == quarter)
        ]


    def filter_time_period(
        self,
        df,
        time_period,
        date_column
    ):

        if not time_period:
            return df

        if (
            df is None
            or df.empty
            or date_column not in df.columns
        ):
            return df

        today = pd.Timestamp.today()

        if time_period == "current_month":
            return df[
                (
                    df[date_column].dt.year
                    == today.year
                )
                & (
                    df[date_column].dt.month
                    == today.month
                )
            ]

        if time_period == "current_quarter":
            return df[
                (
                    df[date_column].dt.year
                    == today.year
                )
                & (
                    df[date_column].dt.quarter
                    == today.quarter
                )
            ]

        if time_period == "current_year":
            return df[
                df[date_column].dt.year
                == today.year
            ]

        return df


    # =================================
    # DEAL PIPELINE ANALYSIS
    # =================================

    def analyze_pipeline(
        self,
        df,
        sector=None,
        time_period=None
    ):


        if df.empty:

            return {

                "record_count": 0,

                "message":
                    "No deal records found."
            }


        working_df = df.copy()


        # Only active pipeline

        if (
            "Deal Status Normalized"
            in working_df.columns
        ):

            working_df = (

                working_df[

                    working_df[
                        "Deal Status Normalized"
                    ]

                    ==
                    "open"

                ]
            )


        # Sector filter
        sector_df = (
            self.filter_by_sector(
                working_df,
                sector,
                "Sector Normalized"
            )
        )

        # Time filter
        working_df = (
            self.filter_time_period(
                sector_df,
                time_period,
                "Tentative Close Date"
            )
        )

        date_fallback_applied = False
        fallback_note = None

        if working_df.empty and not sector_df.empty and time_period:
            working_df = sector_df
            date_fallback_applied = True
            fallback_note = (
                f"Note: No open deals in the '{sector.title() if sector else 'selected'}' sector have tentative close dates "
                f"in the current calendar quarter ({time_period}). Showing all {len(sector_df)} open deals available in the dataset for this sector."
            )


        value_column = (
            "Masked Deal value"
        )


        total_pipeline = (

            self.safe_sum(

                working_df[
                    value_column
                ]

                if value_column
                in working_df.columns
                else None

            )
        )


        average_deal_value = (

            self.safe_mean(

                working_df[
                    value_column
                ]

                if value_column
                in working_df.columns
                else None

            )
        )


        probability_summary = {}


        if (

            "Probability Normalized"
            in working_df.columns

            and

            value_column
            in working_df.columns

        ):

            grouped = (

                working_df

                .groupby(
                    "Probability Normalized",
                    dropna=False
                )

                [value_column]

                .sum()
            )


            probability_summary = {

                str(key):
                float(value)

                for key, value
                in grouped.items()

                if pd.notna(key)

            }


        stage_summary = {}


        if (

            "Deal Stage"
            in working_df.columns

            and

            value_column
            in working_df.columns

        ):

            grouped = (

                working_df

                .groupby(
                    "Deal Stage",
                    dropna=False
                )

                [value_column]

                .sum()

                .sort_values(
                    ascending=False
                )
            )


            stage_summary = {

                str(key):
                float(value)

                for key, value
                in grouped.items()

                if pd.notna(key)

            }


        return {

            "analysis_type":
                "pipeline",

            "filters": {

                "sector":
                    sector,

                "time_period":
                    time_period

            },

            "record_count":
                int(len(working_df)),

            "total_pipeline_value":
                total_pipeline,

            "average_deal_value":
                average_deal_value,

            "pipeline_by_probability":
                probability_summary,

            "pipeline_by_stage":
                stage_summary,

            "date_fallback_applied":
                date_fallback_applied,

            "date_filter_note":
                fallback_note
        }


    # =================================
    # SECTOR PIPELINE COMPARISON
    # =================================

    def analyze_pipeline_by_sector(
        self,
        df
    ):


        if df.empty:

            return {}


        working_df = df.copy()


        if (
            "Deal Status Normalized"
            in working_df.columns
        ):

            working_df = (

                working_df[

                    working_df[
                        "Deal Status Normalized"
                    ]

                    ==
                    "open"

                ]
            )


        grouped = (

            working_df

            .groupby(
                "Sector/service",
                dropna=False
            )

            ["Masked Deal value"]

            .agg(
                ["sum", "count"]
            )

            .reset_index()
        )


        results = []


        for _, row in grouped.iterrows():

            results.append({

                "sector":
                    str(
                        row[
                            "Sector/service"
                        ]
                    ),

                "pipeline_value":
                    float(
                        row["sum"]
                    ),

                "deal_count":
                    int(
                        row["count"]
                    )
            })


        return sorted(

            results,

            key=lambda x:
            x["pipeline_value"],

            reverse=True
        )


    # =================================
    # WORK ORDER PERFORMANCE
    # =================================

    def analyze_work_orders(
        self,
        df,
        sector=None
    ):


        if df.empty:

            return {

                "record_count": 0,

                "message":
                    "No work order records found."
            }


        working_df = df.copy()


        working_df = (

            self.filter_by_sector(

                working_df,

                sector,

                "Sector Normalized"
            )
        )


        # Find actual available column name

        billed_column = (
            "Billed Value in Rupees "
            "(Incl of GST) (Masked)"
        )


        if (
            billed_column
            not in working_df.columns
        ):

            billed_column = (
                "Billed Value in Rupees "
                "(Incl of GST.) (Masked)"
            )


        work_order_value = (
            "Amount in Rupees "
            "(Incl of GST) (Masked)"
        )


        collected_column = (
            "Collected Amount in Rupees "
            "(Incl. of GST) (Masked)"
        )


        receivable_column = (
            "Amount Receivable "
            "(Masked)"
        )


        to_bill_column = (
            "Amount to be billed in Rs. "
            "(Incl. of GST) (Masked)"
        )


        total_work_order_value = (

            self.safe_sum(

                working_df[
                    work_order_value
                ]

                if work_order_value
                in working_df.columns
                else None
            )
        )


        total_billed = (

            self.safe_sum(

                working_df[
                    billed_column
                ]

                if billed_column
                in working_df.columns
                else None
            )
        )


        total_collected = (

            self.safe_sum(

                working_df[
                    collected_column
                ]

                if collected_column
                in working_df.columns
                else None
            )
        )


        total_receivable = (

            self.safe_sum(

                working_df[
                    receivable_column
                ]

                if receivable_column
                in working_df.columns
                else None
            )
        )


        total_to_bill = (

            self.safe_sum(

                working_df[
                    to_bill_column
                ]

                if to_bill_column
                in working_df.columns
                else None
            )
        )


        execution_summary = {}


        if (
            "Execution Status"
            in working_df.columns
        ):

            execution_counts = (

                working_df[
                    "Execution Status"
                ]

                .value_counts(
                    dropna=False
                )
            )


            execution_summary = {

                str(key):
                int(value)

                for key, value
                in execution_counts.items()

                if pd.notna(key)

            }


        total_orders = (
            len(working_df)
        )


        completed_orders = 0


        if (
            "Execution Status Normalized"
            in working_df.columns
        ):

            completed_orders = int(

                (
                    working_df[
                        "Execution Status Normalized"
                    ]

                    ==

                    "completed"

                ).sum()
            )


        return {

            "analysis_type":
                "work_order_performance",

            "filters": {

                "sector":
                    sector
            },

            "record_count":
                int(total_orders),

            "total_work_order_value":
                total_work_order_value,

            "total_billed_value":
                total_billed,

            "total_collected":
                total_collected,

            "total_receivable":
                total_receivable,

            "total_amount_to_bill":
                total_to_bill,

            "collection_rate_percent":

                self.percentage(

                    total_collected,

                    total_billed
                ),

            "billing_progress_percent":

                self.percentage(

                    total_billed,

                    total_work_order_value
                ),

            "completion_rate_percent":

                self.percentage(

                    completed_orders,

                    total_orders
                ),

            "execution_status_summary":
                execution_summary
        }


    # =================================
    # CROSS BOARD ANALYSIS
    # =================================

    def analyze_business_overview(
        self,
        deals_df,
        work_orders_df,
        sector=None
    ):


        pipeline = (

            self.analyze_pipeline(

                deals_df,

                sector=sector
            )
        )


        work_orders = (

            self.analyze_work_orders(

                work_orders_df,

                sector=sector
            )
        )


        return {

            "analysis_type":
                "business_overview",

            "sector":
                sector,

            "sales_pipeline":
                pipeline,

            "operations_and_finance":
                work_orders
        }

    def filter_current_month(
        self,
        df,
        date_column
    ):

        if (
            df.empty
            or date_column not in df.columns
        ):
            return df


        today = pd.Timestamp.today()


        return df[

            (
                df[date_column].dt.year
                ==
                today.year
            )

            &

            (
                df[date_column].dt.month
                ==
                today.month
            )
        ]
    def analyze_opportunity_generation(
        self,
        df,
        sector=None,
        time_period=None
    ):

        if df.empty:

            return {

                "analysis_type":
                    "opportunity_generation",

                "record_count":
                    0,

                "message":
                    "No deal records found."
            }


        working_df = df.copy()


        # -------------------------
        # FILTER BY SECTOR
        # -------------------------

        working_df = (

            self.filter_by_sector(

                working_df,

                sector,

                "Sector Normalized"
            )
        )


        # -------------------------
        # FILTER BY CREATED DATE
        # -------------------------

        working_df = (

            self.filter_time_period(

                working_df,

                time_period,

                "Created Date"
            )
        )


        # -------------------------
        # COUNT NEW OPPORTUNITIES
        # -------------------------

        new_opportunity_count = (
            len(working_df)
        )


        # -------------------------
        # TOTAL VALUE GENERATED
        # -------------------------

        total_value = 0.0


        if (
            "Masked Deal value"
            in working_df.columns
        ):

            total_value = (

                self.safe_sum(

                    working_df[
                        "Masked Deal value"
                    ]
                )
            )


        # -------------------------
        # SECTOR BREAKDOWN
        # -------------------------

        sector_breakdown = {}


        if (

            "Sector/service"
            in working_df.columns

            and

            "Masked Deal value"
            in working_df.columns
        ):

            grouped = (

                working_df

                .groupby(
                    "Sector/service",
                    dropna=False
                )

                .agg({

                    "Masked Deal value":
                        ["sum", "count"]

                })
            )


            for sector_name, row in grouped.iterrows():

                sector_breakdown[
                    str(sector_name)
                ] = {

                    "opportunity_count":

                        int(

                            row[
                                (
                                    "Masked Deal value",
                                    "count"
                                )
                            ]
                        ),

                    "total_value":

                        float(

                            row[
                                (
                                    "Masked Deal value",
                                    "sum"
                                )
                            ]
                        )
                }


        return {

            "analysis_type":
                "opportunity_generation",

            "filters": {

                "sector":
                    sector,

                "time_period":
                    time_period,

                "date_column":
                    "Created Date"
            },

            "new_opportunity_count":
                int(
                    new_opportunity_count
                ),

            "total_new_pipeline_value":
                total_value,

            "sector_breakdown":
                sector_breakdown
        }


analytics_service = (
    AnalyticsService()
)