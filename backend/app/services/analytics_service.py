import pandas as pd

from app.services.data_cleaner import data_cleaner
from app.utils.dates import filter_current_quarter


class AnalyticsService:

    def prepare_deals(self, board):

        df = data_cleaner.board_to_dataframe(board)

        if "Sector/service" in df.columns:
            df["Sector/service"] = (
                df["Sector/service"]
                .apply(data_cleaner.normalize_sector)
            )

        df = data_cleaner.normalize_dates(
            df,
            [
                "Close Date (A)",
                "Tentative Close Date",
                "Created Date"
            ]
        )

        df = data_cleaner.normalize_numeric(
            df,
            [
                "Masked Deal value"
            ]
        )

        return df

    def prepare_work_orders(self, board):

        df = data_cleaner.board_to_dataframe(board)

        if "Sector" in df.columns:

            df["Sector"] = (
                df["Sector"]
                .apply(data_cleaner.normalize_sector)
            )

        df = data_cleaner.normalize_dates(
            df,
            [
                "Data Delivery Date",
                "Date of PO/LOI",
                "Probable Start Date",
                "Probable End Date",
                "Collection Date"
            ]
        )

        numeric_columns = [

            "Amount in Rupees (Excl of GST) (Masked)",

            "Billed Value in Rupees (Excl of GST.) (Masked)",

            "Collected Amount in Rupees (Incl of GST.) (Masked)",

            "Amount Receivable (Masked)"
        ]

        df = data_cleaner.normalize_numeric(
            df,
            numeric_columns
        )

        return df

    def pipeline_analysis(
        self,
        deals_df,
        sector=None,
        current_quarter=False
    ):

        df = deals_df.copy()

        if "Deal Status" in df.columns:

            df = df[
                df["Deal Status"]
                .astype(str)
                .str.lower()
                .eq("open")
            ]

        if sector and "Sector/service" in df.columns:

            df = df[
                df["Sector/service"]
                .str.lower()
                .eq(sector.lower())
            ]

        if (
            current_quarter
            and "Tentative Close Date" in df.columns
        ):

            df = filter_current_quarter(
                df,
                "Tentative Close Date"
            )

        value_column = "Masked Deal value"

        valid_values = df[
            value_column
        ].dropna()

        total_pipeline = valid_values.sum()

        average_deal = (
            valid_values.mean()
            if len(valid_values) > 0
            else 0
        )

        stage_breakdown = {}

        if "Deal Stage" in df.columns:

            stage_breakdown = (
                df.groupby("Deal Stage")[value_column]
                .sum()
                .sort_values(ascending=False)
                .to_dict()
            )

        missing_value_count = int(
            df[value_column].isna().sum()
        )

        return {
            "total_pipeline": float(total_pipeline),

            "deal_count": int(len(df)),

            "average_deal_value": float(
                average_deal
            ),

            "stage_breakdown": stage_breakdown,

            "missing_value_count":
                missing_value_count
        }

    def work_order_analysis(
        self,
        work_orders_df,
        sector=None
    ):

        df = work_orders_df.copy()

        if sector and "Sector" in df.columns:

            df = df[
                df["Sector"]
                .str.lower()
                .eq(sector.lower())
            ]

        total = len(df)

        completed = 0

        if "Execution Status" in df.columns:

            completed = int(
                df["Execution Status"]
                .astype(str)
                .str.lower()
                .eq("completed")
                .sum()
            )

        completion_rate = (
            completed / total * 100
            if total > 0
            else 0
        )

        value_column = (
            "Amount in Rupees "
            "(Excl of GST) (Masked)"
        )

        total_value = 0

        if value_column in df.columns:

            total_value = float(
                df[value_column]
                .dropna()
                .sum()
            )

        return {
            "work_order_count": total,

            "completed_count": completed,

            "completion_rate":
                round(completion_rate, 2),

            "total_work_order_value":
                total_value
        }

    def sector_comparison(
        self,
        deals_df,
        work_orders_df
    ):

        deal_summary = (
            deals_df.groupby(
                "Sector/service"
            )["Masked Deal value"]
            .sum()
            .reset_index()
        )

        deal_summary.columns = [
            "Sector",
            "Pipeline Value"
        ]

        work_column = (
            "Amount in Rupees "
            "(Excl of GST) (Masked)"
        )

        work_summary = (
            work_orders_df.groupby(
                "Sector"
            )[work_column]
            .sum()
            .reset_index()
        )

        work_summary.columns = [
            "Sector",
            "Work Order Value"
        ]

        merged = pd.merge(
            deal_summary,
            work_summary,
            on="Sector",
            how="outer"
        ).fillna(0)

        return merged.to_dict(
            orient="records"
        )


analytics_service = AnalyticsService()