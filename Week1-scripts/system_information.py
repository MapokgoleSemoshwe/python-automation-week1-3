import platform
import os
from datetime import datetime


def get_system_information():
    """Collect and display basic computer information."""

    print("=" * 40)
    print("       SYSTEM INFORMATION")
    print("=" * 40)

    print(f"Operating System : {platform.system()}")
    print(f"OS Version       : {platform.version()}")
    print(f"Machine          : {platform.machine()}")
    print(f"Processor        : {platform.processor()}")
    print(f"Computer Name    : {platform.node()}")
    print(f"Python Version   : {platform.python_version()}")
    print(f"Current User     : {os.getlogin()}")
    print(f"Date and Time    : {datetime.now()}")

    print("=" * 40)


try:
    get_system_information()
except Exception as error:
    print(f"Unable to retrieve system information: {error}")