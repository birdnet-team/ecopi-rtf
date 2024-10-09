import requests
import random
from datetime import datetime, timedelta

import config as cfg 

def get_current_week():
    
    # Return current week 1..48 (4 weeks per month)
    return datetime.now().isocalendar()[1]

def is_in_species_data(species_code):
    
    return True

def get_species_data(species):
    
    data = {}
    
    # This is example data, we'll parse this from the species data later
    data['common_name'] = cfg.SPECIES_DATA[species]['common_name']
    data['scientific_name'] = cfg.SPECIES_DATA[species]['sci_name']
    data['ebird_url'] = 'https://ebird.org/species/' + cfg.SPECIES_DATA[species]['new_ebird_code']
    data['image_url'] = cfg.SPECIES_DATA[species]['image']['src'] + '/320'
    data['image_author'] = cfg.SPECIES_DATA[species]['image']['author']
    data['frequency'] = cfg.SPECIES_DATA[species]['frequencies'][get_current_week()] / 100
    
    return data

def get_total_detections(min_conf=0.5, species_list=[], days=-1, min_count=10):
    
    url = cfg.API_BASE_URL + 'meta/project/' + cfg.PROJECT_NAME + '/detections/recorderspeciescounts/'
    
    headers = {
        'Authorization': f'Token {cfg.API_TOKEN}'
    }
    params = {}
    
    # Minimum confidence
    params['min_confidence'] = min_conf
    
    # Set start date
    if days < 0:
        params['start_date'] = datetime(2023, 1, 1).strftime('%Y-%m-%d')
    else:
        params['start_date'] = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    response = requests.get(url, headers=headers, params=params)
    response = response.json()
    
    # Count entries
    detections = {}
    for item in response:
        if item['species_code'] not in detections and (len(species_list) == 0 or item['species_code'] in species_list):
            detections[item['species_code']] = 0
        detections[item['species_code']] += item['species_count']
        
    # Sort by count
    detections = {k: v for k, v in sorted(detections.items(), key=lambda item: item[1], reverse=True)}
    
    # Only keep species with count >= min_count
    detections = {k: v for k, v in detections.items() if v >= min_count}
    
    total_detections = {'total_detections': sum(detections.values()), 'species_counts': detections}

    return total_detections

def get_last_n_detections(n=6, min_conf=0.85, hours=24, limit=1000):
    
    url = cfg.API_BASE_URL + 'detections'
    
    headers = {
        'Authorization': f'Token {cfg.API_TOKEN}'
    }
    params = {}
    
    # Project name
    params['project_name'] = cfg.PROJECT_NAME
    
    # Minimum confidence
    params['confidence_gte'] = min_conf
    
    # Only detections with audio
    params['has_media'] = True
    
    # We only want detections from the last x hours
    # so we have to set datetime_gte and datetime_lte
    now = datetime.now()
    params['datetime_gte'] = (now - timedelta(hours=hours)).isoformat()
    params['datetime_lte'] = now.isoformat()  
    
    # Only retrieve certain fields
    params['only'] = 'species_code, has_audio, datetime, url_media, confidence, recorder_field_id'
    
    # Pagination/limit
    params['limit'] = limit
    
    # Send request
    response = requests.get(url, headers=headers, params=params)
    response = response.json()
    
    # Parse detections
    detections = {}
    for item in response:
        # Has audio?
        if not item['has_audio']:
            continue
        # Is species in species data?
        if not is_in_species_data(item['species_code']):
            continue
        if item['species_code'] not in detections:
            detections[item['species_code']] = []
        detections[item['species_code']].append(item)
        # format datetime to exclude milliseconds
        item['datetime'] = item['datetime'].split('.')[0]
        
    # For each species, sort by confidence and then randomly select 1 detection from the top 10
    last_n = {}
    for species in detections:
        detections[species] = sorted(detections[species], key=lambda x: x['confidence'], reverse=True)[:10]
        last_n[species] = random.choice(detections[species])
        
    # Sort last_n by confidence
    last_n = {k: v for k, v in sorted(last_n.items(), key=lambda item: item[1]['confidence'], reverse=True)}
    
    # Limit to n species
    last_n = {k: v for k, v in list(last_n.items())[:n]}
    
    # Add species data
    for species in last_n:
        species_data = get_species_data(species)
        for key, value in species_data.items():
            last_n[species][key] = value
    
    return last_n
    
if __name__ == '__main__':
    
    #print('Number of detections in the last 24 hours:', get_total_detections(days=1)['total_detections'])
    #print('Number of detections with confidence >= 0.5:', get_total_detections(min_conf=0.5)['total_detections'])
    
    print(get_last_n_detections())
    
    