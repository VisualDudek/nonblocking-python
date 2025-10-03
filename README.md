# nonblocking-python

## pytania/wątpliwości

- how `asyncio.sleep()` diff from `time.sleep()` and what makes it nonblocking?
- how both above fn. are implemented? chekc source code.
- usage of `asyncio.sleep(0)` and implementation that alows negative _delay_ arg.
- why `async/await` style concurrency is oftern considered more popular in Python than `threading`?
- `asyncio.sleep(delay, result=None)` what are usecases for _result_ arg. ?
- `@types.coroutine` what it is?
- "Preemptive Multitasking (Threads/Processes)" vs. "Cooperative Multitasking (Async Python)"
- czy `asyncio.Lock()` powoduje że corutyny są wykonywane sekwencyjnie?
- jakie są prymitywy biblioteki `asyncio`?
- Producer-Consumer za pomocą Eventów? chyba jednak dedykowane jest `.Condition()`
- Jaka jest różnica pomiędzy `.Event()` vs. `.Condition()` -> Condition combines the functionality of an Event with a Lock.
- Po co `await` `queue.put()` ???
- pamiętaj też o kolejkach typu `PriorityQueue` oraz `LifoQueue`
- `Semaphore` jako Rate Limiting/Resource Allocation, używaj jako context manager
- Co to jest `asyncio.Protocol`? UUUU ale fajny docstring jest do tego, dziwny sposób deklaracji interface-u.
- Higher-Level approach to network communication -> StreamReader, StreamWriter
- co to jest `struct`?
- `asyncio.TaskGroup()`
- `asyncio` + `websockets`
- `pytest-asyncio` package extends `pytest` framework to handle asyncio coroutines.


## src
- https://www.alexisalulema.com/2023/09/18/advanced-asyncio-topics-beyond-the-basics/
- ??? Book "Python Concurrency with asyncio" by Matthew Fowler


## takeaway
- cpython implementation, `timemodule.c`
```c
static PyObject *
time_sleep(PyObject *self, PyObject *timeout_obj)
{
    if (PySys_Audit("time.sleep", "O", timeout_obj) < 0) {
        return NULL;
    }

    PyTime_t timeout;
    if (_PyTime_FromSecondsObject(&timeout, timeout_obj, _PyTime_ROUND_TIMEOUT))
        return NULL;
    if (timeout < 0) {
        PyErr_SetString(PyExc_ValueError,
                        "sleep length must be non-negative");
        return NULL;
    }
    if (pysleep(timeout) != 0) {
        return NULL;
    }
    Py_RETURN_NONE;
}
```
- ^^^ ciekaw jest implementacja w C fn `pysleep()` uuuu jedno wielkie makro:
```c
// time.sleep() implementation.
// On error, raise an exception and return -1.
// On success, return 0.
static int
pysleep(PyTime_t timeout)
{
    assert(timeout >= 0);

#ifndef MS_WINDOWS
#ifdef HAVE_CLOCK_NANOSLEEP
    struct timespec timeout_abs;
#elif defined(HAVE_NANOSLEEP)
    struct timespec timeout_ts;
#else
    struct timeval timeout_tv;
#endif
    PyTime_t deadline, monotonic;
    int err = 0;
...
```
- intro, what is `asyncio`, **001**
- usecase for _result_ arg in `sleep()`, **002**
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
- best usecase for _delay_ in `asyncio.sleep()` I can find is Testing and Mocking, e.g. mocking I/O bound db query, **002**
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
- `math.isnan(x)` Return `True` if x is a NaN (not a number), and `False` otherwise.
- `__sleep0()` code heredoc, usecase avoid hogging the loop in a long-running coroutine, **003**
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
- `asyncio.Lock()` wymusza sekwencyjność **004**, użycie `.Lock()` w formie kontext menagera
- producer-consumer design, użycie `.Ecent()` **005**
- w przykładzie **007** nie potrafie wyłuskać wartości dodanej w "Acquires the lock"
- będąc w scopie `async with condtition:` jest subtelna różnica pomiędzy `await condition.wait()` a `await asyncio.sleep(1)` pierwsze uwalnia internal lock a to drugie nie, ALE musze to sprawdzić.



## Comprehensive Learning Path

### Project Overview
This educational Python project focuses on **asynchronous programming with asyncio**. It serves as a learning laboratory for understanding non-blocking operations in Python, specifically exploring the differences between `asyncio.sleep()` and `time.sleep()`.

### Architecture and Structure

**Project Structure:**
```
/home/m/workspace/labs/nonblocking-python/
├── 001_asyncio.py          # Basic concurrency introduction
├── 002_asyncio.py          # Advanced workflow with state management
├── 003_asyncio_sleep_zero.py # Event loop yielding demonstration
├── README.md               # Learning notes and takeaways
├── pyproject.toml          # Modern Python project configuration
└── .python-version         # Python 3.13 specification
```

### Technologies and Patterns

**Core Technologies:**
- **Python 3.13** (latest stable version)
- **asyncio** (core asynchronous programming library)
- **dataclasses** (modern Python data structures)
- **enum** (type-safe enumeration)
- **uv** (modern Python package manager)

**Design Patterns:**
1. **Async/Await Pattern** - Basic concurrent execution
2. **State Machine Pattern** - Workflow state management
3. **Workflow Orchestration Pattern** - Sequential steps with concurrent workflows
4. **Cooperative Multitasking** - Event loop yielding with `asyncio.sleep(0)`

### Learning Path by Phase

#### Phase 1: Foundational Level (Weeks 1-2)
**Focus: Core Async Concepts**
- Study `001_asyncio.py` example
- **Key Topics:**
  - Event loops and how they work
  - Difference between `asyncio.sleep()` and `time.sleep()`
  - async/await syntax and semantics
  - `asyncio.gather()` for concurrent execution

**Practical Exercise:**
Create timing comparison scripts demonstrating performance differences between synchronous and asynchronous sleep operations.

#### Phase 2: Intermediate Level (Weeks 3-4)
**Focus: Advanced Asyncio Patterns**
- Analyze `002_asyncio.py` thoroughly
- **Key Topics:**
  - Dataclasses for structured data (`@dataclass`)
  - Enums for type-safe state management
  - Error handling in async contexts
  - Using asyncio.sleep's result parameter for data passing

**Practical Exercise:**
Extend the workflow example with:
- Retry mechanism for failed steps
- Timeout handling
- Progress reporting with async callbacks

#### Phase 3: Advanced Level (Weeks 5-6)
**Focus: Event Loop Optimization**
- Study `003_asyncio_sleep_zero.py`
- **Key Topics:**
  - Event loop internals and `__sleep0()` implementation
  - Cooperative multitasking principles
  - When and why to use `asyncio.sleep(0)`
  - Performance implications of blocking the event loop

**Practical Exercise:**
Create CPU-intensive tasks that properly yield control to other coroutines without blocking the event loop.

#### Phase 4: Expert Level (Weeks 7+)
**Focus: Production-Ready Applications**
- **Key Topics:**
  - asyncio with databases (aiopg, motor, etc.)
  - Web frameworks (FastAPI, aiohttp)
  - Testing async code (pytest-asyncio)
  - Debugging async applications
  - Memory management in long-running async applications

### Immediate Next Steps

1. **Experiment with existing code:**
   - Run each example and time execution
   - Modify delays and observe behavior changes
   - Add more concurrent tasks to see scaling effects

2. **Code improvements to implement:**
   - Add comprehensive type hints
   - Replace print statements with proper logging
   - Create unit tests with pytest-asyncio
   - Add error handling and retry mechanisms

3. **Real-world examples to build:**
   - HTTP client making concurrent API calls
   - File I/O operations
   - Database connectivity patterns

### Technologies to Master Next

Based on this foundation:
1. **FastAPI** - For building async web APIs
2. **aiohttp** - For async HTTP client/server operations
3. **SQLAlchemy 2.0** - For async database operations
4. **pytest-asyncio** - For testing async code
5. **asyncio debugging tools** - For production troubleshooting

### Key Takeaways for Learning

- Start with basic concurrency concepts and gradually progress to advanced patterns
- Focus on understanding event loop mechanics before building complex applications
- Practice with the provided examples to solidify understanding
- The progression from `001_asyncio.py` → `002_asyncio.py` → `003_asyncio_sleep_zero.py` represents an ideal learning sequence
- This codebase provides an excellent foundation for mastering Python's asyncio ecosystem