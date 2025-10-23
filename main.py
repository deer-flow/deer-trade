import asyncio
import json

from src.workflow import graph


async def main():
    res = await graph.ainvoke(
        input={
            "stock_code": "300308.SH",
            "start_date": "20251020",
            "end_date": "20251023",
        }
    )
    print(json.dumps(res, indent=4, ensure_ascii=False))
    return res


if __name__ == "__main__":
    asyncio.run(main())
