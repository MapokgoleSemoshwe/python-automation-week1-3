import time
import cProfile
import pstats
import functools
import io
 
 
def timed(func):
    """Decorator that prints how long a function took to run."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMED] {func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper
 
 
# --- Example operations to demonstrate the profiler on ---
 
@timed
def slow_way_to_sum(n):
    # Deliberately inefficient: string concatenation in a loop,
    # a common source of unnecessary slowness.
    total = 0
    for i in range(n):
        total += i
    return total
 
 
@timed
def fast_way_to_sum(n):
    # Uses the built-in sum() with a generator — much faster because
    # it's implemented in C rather than a Python-level loop.
    return sum(range(n))
 
 
def run_detailed_profile(func, *args):
    """
    Runs cProfile against a function and prints the top 10 slowest
    internal calls — this is how you'd find the actual bottleneck
    inside a bigger script like your capstone toolkit.
    """
    profiler = cProfile.Profile()
    profiler.enable()
    func(*args)
    profiler.disable()
 
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream).sort_stats("cumulative")
    stats.print_stats(10)
    print(stream.getvalue())
 
 
if __name__ == "__main__":
    n = 1_000_000
 
    print("--- Quick timing comparison ---")
    slow_way_to_sum(n)
    fast_way_to_sum(n)
 
    print("\n--- Detailed cProfile breakdown of the slow version ---")
    run_detailed_profile(slow_way_to_sum, n)