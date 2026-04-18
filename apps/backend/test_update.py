import asyncio
from httpx import AsyncClient

async def test():
    async with AsyncClient(base_url="http://localhost:8000/api") as client:
        res = await client.get("/tournament/categories")
        print(res.json())

asyncio.run(test())
