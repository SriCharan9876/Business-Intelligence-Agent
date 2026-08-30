import re

import pandas as pd


class DataCleaner:


    # ============================
    # COMMON CLEANING
    # ============================

    def normalize_text(
        self,
        value
    ):

        if pd.isna(value):

            return pd.NA


        value = str(value).strip()


        if not value:

            return pd.NA


        return value


    def normalize_category(
        self,
        series: pd.Series
    ) -> pd.Series:

        return (
            series
            .astype("string")
            .str.strip()
            .str.replace(
                r"\s+",
                " ",
                regex=True
            )
        )


    def clean_numeric(
        self,
        series: pd.Series
    ) -> pd.Series:

        cleaned = (
            series
            .astype("string")
            .str.replace(
                ",",
                "",
                regex=False
            )
            .str.replace(
                "₹",
                "",
                regex=False
            )
            .str.replace(
                r"[^\d.\-]",
                "",
                regex=True
            )
        )


        return pd.to_numeric(

            cleaned,

            errors="coerce"
        )


    def clean_date(
        self,
        series: pd.Series
    ) -> pd.Series:

        return pd.to_datetime(

            series,

            errors="coerce"
        )


    # ============================
    # DEAL FUNNEL
    # ============================

    def clean_deals(
        self,
        rows: list[dict]
    ) -> pd.DataFrame:


        df = pd.DataFrame(rows)


        if df.empty:

            return df


        # Remove whitespace from
        # column names

        df.columns = [

            str(column).strip()

            for column in df.columns
        ]


        # --------------------------------
        # EXPECTED EXACT DATASET COLUMNS
        # --------------------------------

        text_columns = [

            "Deal Name",

            "Owner code",

            "Client Code",

            "Deal Status",

            "Closure Probability",

            "Deal Stage",

            "Product deal",

            "Sector/service"
        ]


        for column in text_columns:

            if column in df.columns:

                df[column] = (
                    self.normalize_category(
                        df[column]
                    )
                )


        # --------------------------------
        # NUMERIC COLUMN
        # --------------------------------

        if (
            "Masked Deal value"
            in df.columns
        ):

            df[
                "Masked Deal value"
            ] = self.clean_numeric(

                df[
                    "Masked Deal value"
                ]
            )


        # --------------------------------
        # DATE COLUMNS
        # --------------------------------

        date_columns = [

            "Close Date (A)",

            "Tentative Close Date",

            "Created Date"
        ]


        for column in date_columns:

            if column in df.columns:

                df[column] = (
                    self.clean_date(
                        df[column]
                    )
                )


        # --------------------------------
        # REMOVE BAD HEADER ROWS
        # --------------------------------

        if "Deal Status" in df.columns:

            df = df[
                df["Deal Status"]
                .astype("string")
                .str.lower()
                .ne("deal status")
            ]


        # --------------------------------
        # STANDARDIZE STATUS
        # --------------------------------

        if "Deal Status" in df.columns:

            df[
                "Deal Status Normalized"
            ] = (

                df["Deal Status"]

                .str.lower()

                .str.strip()
            )


        # --------------------------------
        # STANDARDIZE SECTOR
        # --------------------------------

        if "Sector/service" in df.columns:

            df[
                "Sector Normalized"
            ] = (

                df["Sector/service"]

                .str.lower()

                .str.strip()
            )


        # --------------------------------
        # STANDARDIZE PROBABILITY
        # --------------------------------

        if (
            "Closure Probability"
            in df.columns
        ):

            df[
                "Probability Normalized"
            ] = (

                df[
                    "Closure Probability"
                ]

                .str.lower()

                .str.strip()
            )


        return df.reset_index(
            drop=True
        )


    # ============================
    # WORK ORDERS
    # ============================

    def clean_work_orders(
        self,
        rows: list[dict]
    ) -> pd.DataFrame:


        df = pd.DataFrame(rows)


        if df.empty:

            return df


        df.columns = [

            str(column).strip()

            for column in df.columns
        ]


        # --------------------------------
        # TEXT COLUMNS
        # --------------------------------

        text_columns = [

            "Deal name masked",

            "Customer Name Code",

            "Serial #",

            "Nature of Work",

            "Last executed month of recurring project",

            "Execution Status",

            "Document Type",

            "BD/KAM Personnel code",

            "Sector",

            "Type of Work",

            "Is any Skylark software platform part of the client deliverables in this deal?",

            "latest invoice no.",

            "AR Priority account",

            "Invoice Status",

            "Expected Billing Month",

            "Actual Billing Month",

            "Actual Collection Month",

            "WO Status (billed)",

            "Collection status",

            "Billing Status"
        ]


        for column in text_columns:

            if column in df.columns:

                df[column] = (
                    self.normalize_category(
                        df[column]
                    )
                )


        # --------------------------------
        # NUMERIC COLUMNS
        # --------------------------------

        numeric_columns = [

            "Amount in Rupees (Excl of GST) (Masked)",

            "Amount in Rupees (Incl of GST) (Masked)",

            "Billed Value in Rupees (Excl of GST.) (Masked)",

            "Billed Value in Rupees (Incl of GST) (Masked)",

            "Billed Value in Rupees (Incl of GST.) (Masked)",

            "Collected Amount in Rupees (Incl. of GST) (Masked)",

            "Collected Amount in Rupees (Incl. of GST.) (Masked)",

            "Amount to be billed in Rs. (Exl. of GST) (Masked)",

            "Amount to be billed in Rs. (Incl. of GST) (Masked)",

            "Amount Receivable (Masked)",

            "Quantity by Ops",

            "Quantities as per PO",

            "Quantity billed (till date)",

            "Balance in quantity"
        ]


        for column in numeric_columns:

            if column in df.columns:

                df[column] = (
                    self.clean_numeric(
                        df[column]
                    )
                )


        # --------------------------------
        # DATE COLUMNS
        # --------------------------------

        date_columns = [

            "Data Delivery Date",

            "Date of PO/LOI",

            "Probable Start Date",

            "Probable End Date",

            "Last invoice date",

            "Collection Date"
        ]


        for column in date_columns:

            if column in df.columns:

                df[column] = (
                    self.clean_date(
                        df[column]
                    )
                )


        # --------------------------------
        # STANDARDIZED FIELDS
        # --------------------------------

        if "Sector" in df.columns:

            df[
                "Sector Normalized"
            ] = (

                df["Sector"]

                .str.lower()

                .str.strip()
            )


        if "Execution Status" in df.columns:

            df[
                "Execution Status Normalized"
            ] = (

                df[
                    "Execution Status"
                ]

                .str.lower()

                .str.strip()
            )


        return df.reset_index(
            drop=True
        )


data_cleaner = DataCleaner()