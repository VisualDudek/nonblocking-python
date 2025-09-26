import asyncio


async def crunch():
    for i in range(100_000):
        if i % 1_000 == 0:
            await asyncio.sleep(0) # let other task run
        

async def main():
    await crunch()

if __name__ == "__main__":
    asyncio.run(main())
