import asyncio
 
lock = asyncio.Lock()
 
async def my_coroutine_with_lock(id):
    async with lock:
        print(f"Coroutine {id} has acquired the lock")
        await asyncio.sleep(1)
        print(f"Coroutine {id} has released the lock")


async def my_coroutine(id):
        print(f"Coroutine {id} starts without the lock")
        await asyncio.sleep(1)
        print(f"Coroutine {id} ends without the lock")


async def main():
    print("Starting coroutines with lock:")
    tasks = [my_coroutine_with_lock(i) for i in range(3)]
    await asyncio.gather(*tasks)

    print("\nStarting coroutines without lock:")
    tasks = [my_coroutine(i) for i in range(3)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())