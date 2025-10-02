import asyncio
import time

# --- 1. Illustrating asyncio.Event (The Global Signal) ---
async def consumer_event(event: asyncio.Event, name: str):
    """Waits for the Event to be set, then proceeds."""
    print(f"[{name}] Waiting for Event signal...")
    
    # 🌟 KEY POINT 1: No lock required. Tasks wait passively.
    await event.wait()
    
    # All tasks are released instantly and run concurrently
    start_time = time.time()
    print(f"[{name}] Event SET! Starting work...")
    await asyncio.sleep(0.1) # Simulate a small amount of work
    print(f"[{name}] Finished work after {time.time() - start_time:.2f}s.")

async def producer_event(event: asyncio.Event):
    """Sets the Event flag after a delay."""
    print("\n[PRODUCER] Event example starting. Will set Event in 1 second...")
    await asyncio.sleep(1)
    
    # 🌟 KEY POINT 2: set() releases ALL waiting tasks simultaneously.
    event.set()
    print("[PRODUCER] Event SET complete. All waiting tasks released.")


# --- 2. Illustrating asyncio.Condition (The Lock and Conditional Signal) ---
async def consumer_condition(condition: asyncio.Condition, name: str):
    """Acquires the lock, waits for the condition, and then re-acquires the lock."""
    print(f"[{name}] Waiting for Condition lock and signal...")
    
    # 🌟 KEY POINT 3: Must acquire the lock to wait or notify.
    async with condition:
        print(f"[{name}] Acquired lock, releasing and WAITING for notify()...")
        
        # .wait() releases the lock, suspends the task, and waits for a notify() call.
        # When notified, it will RE-ACQUIRE the lock before proceeding.
        await condition.wait()
        
        # 🌟 KEY POINT 4: Only ONE task is released (due to notify(1) below)
        # and it holds the lock, blocking others.
        start_time = time.time()
        print(f"[{name}] Notified! **Re-acquired lock**. Starting work...")
        await asyncio.sleep(0.5) # Simulate work while holding the lock
        print(f"[{name}] Finished work after {time.time() - start_time:.2f}s. Releasing lock.")
        # Lock is automatically released upon exiting the 'async with' block.


async def producer_condition(condition: asyncio.Condition):
    """Notifies one waiting task after a delay."""
    print("\n[PRODUCER] Condition example starting. Will notify(1) in 1 second...")
    await asyncio.sleep(1)
    
    # 🌟 KEY POINT 5: Must acquire the lock to call notify().
    async with condition:
        # .notify(1) wakes up ONE waiting task. That task will then try to re-acquire the lock.
        condition.notify(1)
        print("[PRODUCER] Sent notify(1). One task is trying to re-acquire the lock now.")
        
        # Wait a moment to let the notified task finish its work
        await asyncio.sleep(1.0)
        
        # Notify the next one
        condition.notify(1)
        print("[PRODUCER] Sent a second notify(1). One more task released.")


async def main():
    # --- Event Example Run ---
    event = asyncio.Event()
    tasks_e = [
        producer_event(event),
        consumer_event(event, "Consumer A (E)"),
        consumer_event(event, "Consumer B (E)"),
        consumer_event(event, "Consumer C (E)"),
    ]
    await asyncio.gather(*tasks_e)
    
    print("\n" + "="*50)
    
    # --- Condition Example Run ---
    condition = asyncio.Condition()
    tasks_c = [
        producer_condition(condition),
        consumer_condition(condition, "Consumer X (C)"),
        consumer_condition(condition, "Consumer Y (C)"),
        consumer_condition(condition, "Consumer Z (C)"),
    ]
    await asyncio.gather(*tasks_c)
    
if __name__ == "__main__":
    asyncio.run(main())