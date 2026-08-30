import httpx

from app.config import settings


class MondayClient:

    API_URL = (
        "https://api.monday.com/v2"
    )


    def __init__(self):

        self.headers = {

            "Authorization":
                settings.MONDAY_API_TOKEN,

            "Content-Type":
                "application/json",

            "API-Version":
                "2024-10"
        }


    async def get_board_items(
        self,
        board_id: str
    ) -> list[dict]:

        query = """
        query ($board_id: ID!) {

            boards(
                ids: [$board_id]
            ) {

                id

                name

                columns {
                    id
                    title
                    type
                }

                items_page(
                    limit: 500
                ) {

                    items {

                        id

                        name

                        column_values {

                            id

                            text

                            value
                        }
                    }
                }
            }
        }
        """


        variables = {
            "board_id": board_id
        }


        async with httpx.AsyncClient(
            timeout=30.0
        ) as client:

            response = await client.post(

                self.API_URL,

                headers=self.headers,

                json={
                    "query": query,
                    "variables": variables
                }
            )


        response.raise_for_status()

        response_data = response.json()


        if "errors" in response_data:

            raise Exception(
                f"Monday API error: "
                f"{response_data['errors']}"
            )


        boards = (
            response_data
            .get("data", {})
            .get("boards", [])
        )


        if not boards:

            return []


        board = boards[0]


        column_map = {

            column["id"]:
            column["title"]

            for column in
            board.get("columns", [])
        }


        items = (
            board
            .get("items_page", {})
            .get("items", [])
        )


        rows = []


        for item in items:

            row = {

                "monday_item_id":
                item["id"],

                "item_name":
                item["name"]
            }


            for column_value in (
                item.get(
                    "column_values",
                    []
                )
            ):

                column_id = (
                    column_value["id"]
                )


                column_title = (
                    column_map.get(
                        column_id,
                        column_id
                    )
                )


                row[column_title] = (
                    column_value.get("text")
                )


            rows.append(row)

        
        return rows


    async def get_deals_data(
        self
    ) -> list[dict]:

        return await (
            self.get_board_items(
                settings.DEALS_BOARD_ID
            )
        )


    async def get_work_orders_data(
        self
    ) -> list[dict]:

        return await (
            self.get_board_items(
                settings.WORK_ORDERS_BOARD_ID
            )
        )


monday_client = MondayClient()