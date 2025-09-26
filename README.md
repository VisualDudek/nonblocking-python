# nonblocking-python

- how `asyncio.sleep()` diff from `time.sleep()` and what makes it nonblocking?
- how both above fn. are implemented? chekc source code.
- usage of `asyncio.sleep(0)` and implementation that alows negative _delay_ arg.
- why `async/await` style concurrency is oftern considered more popular in Python than `threading`?
- `asyncio.sleep(delay, result=None)` what are usecases for _result_ arg. ?
- `@types.coroutine` what it is?



## takeaway
- intro, what is `asyncio`, `001`
- usecase for _result_ arg in `sleep()`, `002`
- awaited fn. in same sope run SEQUENTIALLY, steps in diff scopes run CONCURRENT, diff. scopes are added into event loop by `asyncio.gather()` 
```python
# Same scope = like standing in a line
async def same_scope():
    await step1()  # Wait in line for step1
    await step2()  # Then wait in line for step2  
    await step3()  # Then wait in line for step3

# Different scopes = like having multiple people
async def different_scopes():
    await asyncio.gather(
        person1_does_step1(),  # Person 1 does their thing
        person2_does_step2(),  # Person 2 does their thing  
        person3_does_step3()   # Person 3 does their thing
    )
```
- best usecase for _delay_ in `asyncio.sleep()` I can find is Testing and Mocking, e.g. mocking I/O bound db query, `002`
- `asyncio.sleep()` code heredoc, interesting `delay <= 0` branch usecase see below
```python
async def sleep(delay, result=None):
    """Coroutine that completes after a given time (in seconds)."""
    if delay <= 0:
        await __sleep0()
        return result

    if math.isnan(delay):
        raise ValueError("Invalid delay: NaN (not a number)")

    loop = events.get_running_loop()
    future = loop.create_future()
    h = loop.call_later(delay,
                        futures._set_result_unless_cancelled,
                        future, result)
    try:
        return await future
    finally:
        h.cancel()
```
- `__sleep0()` code heredoc,
```python
@types.coroutine
def __sleep0():
    """Skip one event loop run cycle.

    This is a private helper for 'asyncio.sleep()', used
    when the 'delay' is set to 0.  It uses a bare 'yield'
    expression (which Task.__step knows how to handle)
    instead of creating a Future object.
    """
    yield
```