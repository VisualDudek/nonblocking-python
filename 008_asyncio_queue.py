import asyncio
 
async def producer(queue):
    for i in range(5):
        print(f"Producing item {i}")
        await queue.put(i) # do I need to await here?
        await asyncio.sleep(0)
 
async def consumer(queue):
    while True:
        item = await queue.get()
        print(f"Consuming item {item}")
        await asyncio.sleep(1)
        queue.task_done()
 
async def main():
    queue = asyncio.Queue()
    await asyncio.gather(producer(queue), consumer(queue))
 
if __name__ == "__main__":
    asyncio.run(main())