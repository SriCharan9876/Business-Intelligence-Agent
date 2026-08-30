import httpx

from app.config import settings


MONDAY_API_URL = "https://api.monday.com/v2"


class MondayClient:

    def __init__(self):
        self.headers = {
            "Authorization": settings.MONDAY_API_TOKEN,
            "Content-Type": "application/json",
        }

    async def query(self, query: str, variables: dict = None):
        payload = {
            "query": query,
            "variables": variables or {}
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                MONDAY_API_URL,
                headers=self.headers,
                json=payload,
                timeout=30
            )

        response.raise_for_status()

        result = response.json()

        if "errors" in result:
            raise Exception(
                f"Monday API Error: {result['errors']}"
            )

        return result["data"]

    async def get_board_items(self, board_id: str):

        query = """
        query ($board_ids: [ID!]) {
          boards(ids: $board_ids) {
            id
            name

            columns {
              id
              title
              type
            }

            items_page(limit: 500) {
              items {
                id
                name

                column_values {
                  id
                  text
                  value
                  type
                }
              }
            }
          }
        }
        """

        data = await self.query(
            query,
            {
                "board_ids": [str(board_id)]
            }
        )

        return data["boards"][0]

    async def get_deals(self):
        return await self.get_board_items(
            settings.DEALS_BOARD_ID
        )

    async def get_work_orders(self):
        return await self.get_board_items(
            settings.WORK_ORDERS_BOARD_ID
        )


monday_client = MondayClient()