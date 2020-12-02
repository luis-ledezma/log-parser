# ---------------------------------------------------------------------------------------------------------------------
# RETRIEVES DATA FROM LOCAL LOG FILE AND PARSE IT
# This library will retrieve text from a locally provided log file and parse its contents, obtaining valuable data like
# the number of error occurrences.
# Usage:
# python3 FILE
# FILE: The local file that contains the logs to be read.
# ---------------------------------------------------------------------------------------------------------------------

import argparse
import re
from collections import Counter

# Regex used to parse the log contents, specific to a defined logging format: %DATE% [service-name instance-id]: log-trace
REGEX = "^[TZ\d\.\-\:]+\s+\[([\w-]*)\s([\w\d]*)\].*(\[error\])"

def main():
  args = get_args()
  lines = read_file(args.file)
  errors = parse_errors(lines)
  count = count_errors(errors)
  report = max_errors(count)
  print(report)

def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('file', type=str, help="The local file that contains the logs to be read.")
  return parser.parse_args()

def read_file(file_path):
  log_file = open(file_path, 'r')
  lines = log_file.readlines()
  return lines

# Returns an object with all the services and the instances with errors
def parse_errors(data):
    errors = {}
    for line in data:
        matches = re.search(REGEX, line)
        if matches is not None:
            if matches.group(1) in errors:
                errors[matches.group(1)].append(matches.group(2))
            else:
                errors[matches.group(1)] = [matches.group(2)]
    return errors

# Returns the data from parse_errors with the total of errors and the instance with most occurrences
def count_errors(errors):
    services_count = {}
    for service in errors:
        temp = Counter(errors[service]).most_common(1)
        services_count[service] = {"instance" : temp[0][0], "count" : temp[0][1], "total" : len(errors[service])}
    return services_count

# Returns the object with max service errors
def max_errors(errors):
    if errors:
        index = max(errors, key=lambda item: errors[item]["total"])
        report = (
            f"[{index}]: {errors[index]['total']} errors\n"
            f"[{errors[index]['instance']}]: {errors[index]['count']}/{errors[index]['total']} errors")
        return report
    else:
        return "No errors to report."

if __name__ == "__main__":
    main()