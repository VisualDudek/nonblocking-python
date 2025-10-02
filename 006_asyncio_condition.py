import asyncio
 
condition = asyncio.Condition()
 
async def consumer():
    async with condition:
        print("Consumer waiting")
        await condition.wait()
        print("Consumer triggered")
        # Do something
 
async def producer():
    await asyncio.sleep(1)
    async with condition:
        print("Producer ready")
        condition.notify_all()
 
async def main():
    await asyncio.gather(consumer(), producer())
 
if __name__ == "__main__":
    asyncio.run(main())