import pandas as pd


class DataCleaner:

    def board_to_dataframe(self, board: dict):

        column_mapping = {
            column["id"]: column["title"]
            for column in board["columns"]
        }

        rows = []

        for item in board["items_page"]["items"]:

            row = {
                "Item ID": item["id"],
                "Item Name": item["name"]
            }

            for column_value in item["column_values"]:

                column_id = column_value["id"]

                column_title = column_mapping.get(
                    column_id,
                    column_id
                )

                row[column_title] = (
                    column_value["text"]
                    if column_value["text"] is not None
                    else None
                )

            rows.append(row)

        return pd.DataFrame(rows)

    def normalize_text(self, value):

        if pd.isna(value):
            return None

        return str(value).strip()

    def normalize_sector(self, value):

        if pd.isna(value) or not value:
            return "Unknown"

        value = str(value).strip().lower()

        mappings = {
            "energy": "Energy",
            "energy sector": "Energy",

            "mining": "Mining",

            "powerline": "Powerline",
            "power line": "Powerline",

            "agriculture": "Agriculture",
        }

        return mappings.get(
            value,
            value.title()
        )

    def normalize_dates(self, df, columns):

        for column in columns:

            if column in df.columns:

                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce",
                    dayfirst=False
                )

        return df

    def normalize_numeric(self, df, columns):

        for column in columns:

            if column in df.columns:

                df[column] = (
                    df[column]
                    .astype(str)
                    .str.replace(",", "")
                    .str.replace("₹", "")
                )

                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

        return df


data_cleaner = DataCleaner()