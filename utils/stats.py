import csv
import os
from datetime import datetime

import config as cfg

def increment_site_views(site):

    # Get the current timestamp
    timestamp = datetime.now().isoformat()

    # Check if the CSV file exists
    file_exists = os.path.exists(cfg.SITE_VIEWS_LOG)

    # Write the new entry to the CSV file
    with open(cfg.SITE_VIEWS_LOG, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write the header if the file does not exist
            writer.writerow(["timestamp", "site"])
        writer.writerow([timestamp, site])

    return timestamp

def get_site_views(site):
    # Check if the CSV file exists
    if not os.path.exists(cfg.SITE_VIEWS_LOG):
        return []

    # Read the entries from the CSV file
    with open(cfg.SITE_VIEWS_LOG, "r") as file:
        reader = csv.DictReader(file)
        entries = list(reader)
        
    # Filter the entries by the site
    entries = [entry for entry in entries if entry["site"] == site]

    return len(entries)