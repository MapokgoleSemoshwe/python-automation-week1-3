import argparse
import shutil
 
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
 
 
def check_cpu(threshold: float) -> tuple:
    if not PSUTIL_AVAILABLE:
        return ("CPU", None, "psutil not installed — cannot check CPU")
    try:
        usage = psutil.cpu_percent(interval=1)
        status = "WARNING" if usage >= threshold else "OK"
        return ("CPU", usage, status)
    except Exception as e:
        return ("CPU", None, f"Could not read CPU usage: {e}")
 
 
def check_memory(threshold: float) -> tuple:
    if not PSUTIL_AVAILABLE:
        return ("Memory", None, "psutil not installed — cannot check memory")
    try:
        mem = psutil.virtual_memory()
        status = "WARNING" if mem.percent >= threshold else "OK"
        return ("Memory", mem.percent, status)
    except Exception as e:
        return ("Memory", None, f"Could not read memory usage: {e}")
 
 
def check_disk(threshold: float, path: str = "/") -> tuple:
    # Uses the built-in shutil module as a fallback that works even
    # without psutil, since disk usage is a core Python feature.
    try:
        total, used, free = shutil.disk_usage(path)
        percent_used = (used / total) * 100
        status = "WARNING" if percent_used >= threshold else "OK"
        return ("Disk", round(percent_used, 1), status)
    except Exception as e:
        return ("Disk", None, f"Could not read disk usage: {e}")
 
 
def print_report(results: list, threshold: float) -> None:
    print("=" * 50)
    print(f"SYSTEM HEALTH CHECK (warning threshold: {threshold}%)")
    print("=" * 50)
    for name, value, status in results:
        if value is None:
            print(f"  {name:<10}: N/A — {status}")
        else:
            print(f"  {name:<10}: {value}%  [{status}]")
    print("=" * 50)
 
 
def main():
    parser = argparse.ArgumentParser(description="Check basic system health (CPU, memory, disk).")
    parser.add_argument("--threshold", type=float, default=80.0, help="Warning threshold percentage (default: 80)")
    args = parser.parse_args()
 
    results = [
        check_cpu(args.threshold),
        check_memory(args.threshold),
        check_disk(args.threshold),
    ]
    print_report(results, args.threshold)
 
 
if __name__ == "__main__":
    main()