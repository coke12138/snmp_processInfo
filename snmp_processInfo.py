# This script formats the process information in the SNMP enumeration result file.
# 
# 1.
# snmpbulkwalk -c <COMMUNITY> -v2c <IP> . | tee allInfo_snmpbulk
# 2.
# python3 snmp_processInfo.py allInfo_snmpbulk

import sys
import re
from collections import defaultdict


if len(sys.argv) >= 2:
    filename = sys.argv[1]
else:
    filename = input("Input File: ").strip()

data = defaultdict(dict)

try:
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.search(r'hrSWRun(Path|Parameters)\.(\d+)\s*=\s*STRING:\s*"(.+)"', line)
            if match:
                field_type = match.group(1)
                pid = match.group(2)
                value = match.group(3)
                data[pid][field_type] = value

    for pid in sorted(data.keys(), key=int):
        path = data[pid].get('Path', '')
        params = data[pid].get('Parameters', '')
        print(f"{pid} {path} {params}")

except FileNotFoundError:
    print(f"Error: file '{filename}' does not exist")
    sys.exit(1)
