import asyncio
 
event = asyncio.Event()
 
async def waiter():
    print("Waiting for the event to be set")
    await event.wait()
    print("The event was set, proceeding")
 
async def setter():
    await asyncio.sleep(1)
    print("Setting the event")
    event.set()
 
async def main():
    await asyncio.gather(waiter(), setter())
 
if __name__ == "__main__":
    asyncio.run(main())