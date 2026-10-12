import re
import argparse
from collections import Counter
 
# Regex patterns — each one targets a specific piece of information.
DATE_PATTERN = re.compile(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{2}/\d{2}/\d{4}\b")
IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
SEVERITY_PATTERN = re.compile(r"\b(ERROR|WARNING|CRITICAL|FAILURE)\b", re.IGNORECASE)
 
 
def analyze_log(filepath: str) -> dict:
    dates_found = []
    ips_found = []
    severity_counter = Counter()
    error_lines = []
 
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line_number, line in enumerate(f, start=1):
            dates_found += DATE_PATTERN.findall(line)
            ips_found += IP_PATTERN.findall(line)
 
            severity_match = SEVERITY_PATTERN.search(line)
            if severity_match:
                level = severity_match.group(1).upper()
                severity_counter[level] += 1
                error_lines.append((line_number, level, line.strip()))
 
    return {
        "total_dates": len(dates_found),
        "unique_dates": sorted(set(dates_found)),
        "unique_ips": sorted(set(ips_found)),
        "severity_counts": severity_counter,
        "flagged_lines": error_lines,
    }
 
 
def print_report(results: dict) -> None:
    print("=" * 50)
    print("LOG ANALYSIS SUMMARY")
    print("=" * 50)
 
    print(f"\nDates found ({results['total_dates']} total):")
    for d in results["unique_dates"]:
        print(f"  - {d}")
 
    print(f"\nUnique IP addresses found ({len(results['unique_ips'])}):")
    for ip in results["unique_ips"]:
        print(f"  - {ip}")
 
    print("\nSeverity breakdown:")
    for level, count in results["severity_counts"].most_common():
        print(f"  - {level}: {count}")
 
    print(f"\nFlagged lines ({len(results['flagged_lines'])}):")
    for line_number, level, content in results["flagged_lines"][:10]:  # show first 10
        print(f"  Line {line_number} [{level}]: {content}")
 
    if len(results["flagged_lines"]) > 10:
        print(f"  ... and {len(results['flagged_lines']) - 10} more.")
 
 
def main():
    parser = argparse.ArgumentParser(description="Analyse a log file for errors, dates and IPs.")
    parser.add_argument("logfile", help="Path to the log file to analyse")
    args = parser.parse_args()
 
    try:
        results = analyze_log(args.logfile)
        print_report(results)
    except FileNotFoundError:
        print(f"Error: could not find file '{args.logfile}'")
    except Exception as e:
        print(f"Unexpected error: {e}")
 
 
if __name__ == "__main__":
    main()