# Google IT Automation with Python: Weeks 1-3

Practical scripts from the CAPACITI Google IT Automation with Python programme.
The Week 4 capstone is in a separate repository (it-automation-toolkit).

## Week 1: Python Fundamentals
System-information script, password-strength checker, user-account validation, and an employee/device record manager.

## Week 2: Operating-System Automation and GitHub
- `file_organizer.py`: sorts files into folders by type, flags duplicates, logs every action
- `log_analyzer.py`: extracts errors, dates and IP addresses from log files using regex
- `system_health_checker.py`: command-line CPU, memory and disk check with a warning threshold

## Week 3: Troubleshooting, Configuration Management and Cloud
- `broken-script-practice.py` / `fixed-script-practice.py`: five deliberate bugs and their fixes
- `test-automation-scripts.py`: unit tests for the Week 2 scripts
- `performance-profiler.py`: timing and cProfile to find slow code
- `configurable-setup.py`: builds a project structure from a JSON config
- `cloud-readiness-check.py`: checks a project is portable to a cloud or virtual environment

## Setup
    pip install psutil

## Usage
    python Week2-scripts/file_organizer.py "<folder>" --dry-run
    python Week2-scripts/log_analyzer.py "<logfile>"
    python Week2-scripts/system_health_checker.py --threshold 80
    python Week3-scripts/cloud-readiness-check.py "<project folder>"
    python Week3-scripts/configurable-setup.py setup_config.json

Run the Week 3 tests from inside `Week3-scripts`, because they import the Week 2 scripts from the same folder.
