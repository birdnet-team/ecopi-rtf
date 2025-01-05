import csv
import os
import hashlib
from datetime import datetime

import config as cfg

def headers_to_fingerprint(headers):
    
    # Extract data from request headers
    user_agent = headers.get('User-Agent', 'Unknown')
    client_hints = headers.get('Sec-CH-UA', 'Unknown')
    platform = headers.get('Sec-CH-UA-Platform', 'Unknown')
    platform_version = headers.get('Sec-CH-UA-Platform-Version', 'Unknown')
    is_mobile = headers.get('Sec-CH-UA-Mobile', 'Unknown')
    accept_language = headers.get('Accept-Language', 'Unknown')
    fingerprint_raw = f"{user_agent}-{client_hints}-{platform}-{platform_version}-{is_mobile}-{accept_language}"
    
    # Create a hash of the fingerprint_raw string
    hash_object = hashlib.sha256(fingerprint_raw.encode())
    fingerprint_hash = int(hash_object.hexdigest(), 16)
    
    # Truncate the hash to 6 digits
    fingerprint = fingerprint_hash % 1000000
    
    return fingerprint

def increment_site_views(site, headers):

    # Get the current timestamp
    timestamp = datetime.now().isoformat()

    # Check if the CSV file exists
    file_exists = os.path.exists(cfg.SITE_VIEWS_LOG)

    # Write the new entry to the CSV file
    with open(cfg.SITE_VIEWS_LOG, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write the header if the file does not exist
            writer.writerow(["timestamp", "project", "site", "user"])
        writer.writerow([timestamp, cfg.PROJECT_ACRONYM, site, headers_to_fingerprint(headers)])

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