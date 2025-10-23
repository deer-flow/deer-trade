import asyncio

from src.workflow import graph


async def main():
    res = await graph.ainvoke(input={"stock_code": "BABA"})
    print(res)
    return res


if __name__ == "__main__":
    asyncio.run(main())
