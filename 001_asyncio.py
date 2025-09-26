import asyncio
import time


async def task(name, delay):
    print(f"{name} started at {time.strftime('%X')}")
    await asyncio.sleep(delay)
    print(f"{name} finished at {time.strftime('%X')}")



async def main():
    print("Hello from nonblocking-python!")
    await asyncio.gather(
        task("A", 3),
        task("B", 2),
    )
    print("""
    If you had use `time.sleep()` insted, they would run sequentially instead of concurent,
    taking aprox. 5sec (3+2).
          """)


if __name__ == "__main__":
    asyncio.run(main())
