import asyncio
from httpx import AsyncClient

async def run_update_test():
    async with AsyncClient(base_url="http://localhost:8000/api") as client:
        res = await client.get("/tournament/categories")
        print(res.json())

if __name__ == "__main__":
    asyncio.run(run_update_test())
