import sys
sys.path.append('..')

import requests
import random
from datetime import datetime, timedelta, UTC 
import pytz
import numpy as np

import config as cfg 

# Set random seed
random.seed(42)

def get_current_week():
    
    # Return current week 1..48 (4 weeks per month)
    return min(48, max(1, int(datetime.now().isocalendar()[1] / 52 * 48)))

def date_to_last_seen(date, time_format='24h'):
    # Convert date to '16 hrs ago' or '2 days ago'
    # below 1 hr use minutes
    # below 48 hrs use hours
    # above 48 hrs use days
    try:
        if time_format == '12h':
            date = datetime.strptime(date, '%m/%d/%Y - %I:%M %p')
        else:
            date = datetime.strptime(date, '%m/%d/%Y - %H:%M')
    except ValueError:
        # Try the other format if the first one fails
        try:
            date = datetime.strptime(date, '%m/%d/%Y - %H:%M')
        except ValueError:
            date = datetime.strptime(date, '%m/%d/%Y - %I:%M %p')
    
    delta = datetime.now() - date
    
    if delta.total_seconds() < 60:
        return '1 min ago'
    
    if delta.total_seconds() < 60 * 60:
        mins = int(delta.total_seconds() / 60)
        return f"{mins} min{'s' if mins > 1 else ''} ago"
    
    if delta.total_seconds() < 60 * 60 * 48:
        hrs = int(delta.total_seconds() / 3600)
        return f"{hrs} hr{'s' if hrs > 1 else ''} ago"
    
    days = int(delta.total_seconds() / 3600 / 24)
    return f"{days} day{'s' if days > 1 else ''} ago"

def to_local_time(utc_time, time_format='24h'):
    # Convert UTC time to local time
    try:
        utc_time = datetime.strptime(utc_time, '%m/%d/%Y - %I:%M %p')
    except ValueError:
        utc_time = datetime.strptime(utc_time, '%m/%d/%Y - %H:%M')
    
    timezone = pytz.timezone(cfg.TIMEZONE)
    local_time = utc_time.astimezone(timezone)
    
    if time_format == '12h':
        return local_time.strftime('%m/%d/%Y - %I:%M %p')
    else:
        return local_time.strftime('%m/%d/%Y - %H:%M')

def is_in_species_data(species_code):
    
    return species_code in cfg.SPECIES_DATA

def is_blacklisted(species_code):
    
    # Is in species data?
    if not is_in_species_data(species_code):
        return True
    
    return cfg.SPECIES_DATA[species_code]['blacklisted']

def get_confidence_score(species, confidence):
    
    week = get_current_week()
    try:
        species_freq = cfg.SPECIES_DATA[species]['frequencies'][week - 1]
    except:
        species_freq = 10
        
    # Blend confidence and frequency as weighted average
    confidence = int((confidence * 0.75) + (species_freq * 0.25))
    
    return min(100, max(1, confidence))

def get_battery_status(voltage):
    
    # Convert voltage to percentage
    # Everything above 12 is 100%, eveything below 9 is 10%, scale inbetween
    if not voltage is None:
        voltage = min(12, max(9, voltage))
    else:
        voltage = 9
    
    battery_level = max(10, int((voltage - 9) / (12 - 9) * 100) // 10 * 10)
    
    return str(battery_level) if battery_level > 10 else '< 10'

def get_recorder_state(recorder_id):
    
    url = 'https://api.ecopi.de/api/v0.1/recorderstates/'
    
    headers = {
        'Authorization': f'Token {cfg.API_TOKEN}'
    }
    params = {}
    
    # Project name
    params['project_name'] = cfg.PROJECT_NAME
    
    # Recorder ID
    params['recorder_field_id'] = recorder_id
    
    response = requests.get(url, headers=headers, params=params)
    response = response.json()
    
    last_status = response[0]
    
    time_since_last_status = datetime.now() - datetime.strptime(last_status['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S')            
    last_update = datetime.strptime(last_status['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y - %H:%M')
    
    is_ok = True if time_since_last_status.total_seconds() < 3600 * 24 else False
    
    current_status = 'Ok | Sleeping'
    status_color = '#69A0C2' # Blue
    if time_since_last_status.total_seconds() < 60 * 15 and not last_status['task'] == 'Finished':
        current_status = 'Ok | Listening'
        status_color = '#36824b' # Green
        
    if not is_ok:
        current_status = 'Error | Offline'
        status_color = '#DAD5BC' # Gray
    
    return {'current_status': current_status, 
            'status_color': status_color, 
            'last_update': date_to_last_seen(last_update),
            'battery': get_battery_status(last_status['voltage']),
            'cpu_temp': last_status['cpu_temp'], 
            'is_ok': is_ok}

def get_recorder_group():
    
    url = f"https://api.ecopi.de/api/v0.1/recordergroups/"
    
    headers = {
        'Authorization': f'Token {cfg.API_TOKEN}'
    }
    params = {}
    
    # Project name
    params['project_name'] = cfg.PROJECT_NAME
    
    response = requests.get(url, headers=headers, params=params)
    response = response.json()
    
    return response

def get_recorder_location(recorder_id):
    
    url = f"https://api.ecopi.de/api/v0.1/recorders/recordergroup/{cfg.RECORDER_GROUP}/"
    
    headers = {
        'Authorization': f'Token {cfg.API_TOKEN}'
    }
    params = {}
    
    # Recorder ID
    params['recorder_field_id'] = recorder_id
    
    response = requests.get(url, headers=headers, params=params)
    response = response.json()
    
    return [response[0]['lat'], response[0]['lon']]

def get_species_data(species):
    
    data = {}
    
    if not species in cfg.SPECIES_DATA:
        return data
    
    # This is example data, we'll parse this from the species data later
    if cfg.SITE_LOCALE.lower() in ['de', 'fr', 'cs'] and 'common_name_' + cfg.SITE_LOCALE.lower() in cfg.SPECIES_DATA[species]:
        data['common_name'] = cfg.SPECIES_DATA[species]['common_name_' + cfg.SITE_LOCALE.lower()]
    else:
        data['common_name'] = cfg.SPECIES_DATA[species]['common_name']
    data['scientific_name'] = cfg.SPECIES_DATA[species]['sci_name']
    #data['ebird_url'] = 'https://ebird.org/species/' + cfg.SPECIES_DATA[species]['new_ebird_code'] if not cfg.SPECIES_DATA[species]['new_ebird_code'].startswith('t-') else 'https://search.macaulaylibrary.org/catalog?taxonCode=' + cfg.SPECIES_DATA[species]['new_ebird_code']
    data['ebird_url'] = cfg.LEARN_MORE_BASE_URL + cfg.SPECIES_DATA[species]['new_ebird_code'] if not cfg.SPECIES_DATA[species]['new_ebird_code'].startswith('t-') else 'https://search.macaulaylibrary.org/catalog?taxonCode=' + cfg.SPECIES_DATA[species]['new_ebird_code']
    
    # Thumbnail image
    if cfg.SPECIES_DATA[species]['image']['src'].find('birds.cornell.edu') > 0:
        data['thumbnail_url'] = cfg.SPECIES_DATA[species]['image']['src'] + '/160'
    else:
        data['thumbnail_url'] = cfg.SITE_ROOT + cfg.SPECIES_DATA[species]['image']['src']
    
    # Low res species image
    if cfg.SPECIES_DATA[species]['image']['src'].find('birds.cornell.edu') > 0:
        data['image_url'] = cfg.SPECIES_DATA[species]['image']['src'] + '/320'
    else:
        data['image_url'] = cfg.SITE_ROOT + cfg.SPECIES_DATA[species]['image']['src']
    
    # High res species image
    if cfg.SPECIES_DATA[species]['image']['src'].find('birds.cornell.edu') > 0:
        data['image_url_highres'] = cfg.SPECIES_DATA[species]['image']['src'] + '/900'
    else:
        data['image_url_highres'] = cfg.SITE_ROOT + cfg.SPECIES_DATA[species]['image']['src']
    
    data['image_author'] = cfg.SPECIES_DATA[species]['image']['author']
    data['frequency'] = cfg.SPECIES_DATA[species]['frequencies'][get_current_week() - 1] / 100
    data['species_code'] = species 
    
    return data

def get_recorder_data(min_conf=0.5, species_list=[], days=1, min_count=5):
    
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
    
    # Count detections per recorder
    recorder_data = {}
    for item in response:
        if item['recorder_field_id'] not in recorder_data:
            recorder_data[item['recorder_field_id']] = {'detections': 0, 'species_counts': {}}
        recorder_data[item['recorder_field_id']]['detections'] += item['species_count']
        if item['species_code'] not in recorder_data[item['recorder_field_id']]['species_counts'] and (len(species_list) == 0 or item['species_code'] in species_list):
            recorder_data[item['recorder_field_id']]['species_counts'][item['species_code']] = 0
        recorder_data[item['recorder_field_id']]['species_counts'][item['species_code']] += item['species_count']
        
    # Only keep species with count >= min_count
    for recorder in recorder_data:
        recorder_data[recorder]['species_counts'] = {k: v for k, v in recorder_data[recorder]['species_counts'].items() if v >= min_count and not is_blacklisted(k)}
    
    # Add recorder metadata
    for recorder in recorder_data:
        if recorder not in cfg.RECORDERS:
            continue
        recorder_data[recorder]['lat'] = cfg.RECORDERS[recorder]['lat']
        recorder_data[recorder]['lon'] = cfg.RECORDERS[recorder]['lon']
        recorder_data[recorder]['id'] = recorder
        recorder_data[recorder]['species'] = len(recorder_data[recorder]['species_counts'])
    
    return recorder_data

def get_total_detections(min_conf=0.5, species_list=[], recorder_list=[], days=-1, min_count=5):
    
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
        if len(recorder_list) == 0 or item['recorder_field_id'] in recorder_list:
            if len(species_list) == 0 or item['species_code'] in species_list:
                if item['species_code'] not in detections:
                    detections[item['species_code']] = 0
                detections[item['species_code']] += item['species_count']
        
    # Sort by count
    detections = {k: v for k, v in sorted(detections.items(), key=lambda item: item[1], reverse=True)}
    
    # Only keep non-blacklisted species
    detections = {k: v for k, v in detections.items() if not is_blacklisted(k)}
    
    # Only keep species with count >= min_count
    detections = {k: v for k, v in detections.items() if v >= min_count}
    
    total_detections = {'total_detections': sum(detections.values()), 'species_counts': detections}

    return total_detections

def get_last_n_detections(n=8, min_conf=0.5, hours=24, limit=1000, min_count=5):
    url = cfg.API_BASE_URL + 'detections'
    
    headers = {
        'Authorization': f'Token ' + cfg.API_TOKEN
    }
    params = {}
    
    # Project name
    params['project_name'] = cfg.PROJECT_NAME
    
    # Minimum confidence
    params['confidence_gte'] = min_conf
    
    # Only detections with audio
    params['has_media'] = True
    
    # Only retrieve certain fields
    params['only'] = 'species_code, has_audio, datetime, url_media, confidence, recorder_field_id'
    
    # Pagination/limit
    params['limit'] = limit
    
    def fetch_detections(hours):
        if hours > 0:
            now = datetime.now()
            params['datetime_recording__gte'] = (now - timedelta(hours=hours)).isoformat()
            params['datetime_recording__lte'] = now.isoformat()
        else:
            params.pop('datetime_recording__gte', None)
            params.pop('datetime_recording__lte', None)
        
        # Send request
        response = requests.get(url, headers=headers, params=params)
        try:
            response = response.json()
        except:
            # Empty response
            return []
        
        return response
    
    # Initial fetch
    response = fetch_detections(hours)
    
    # Retry with hours set to -1 if the initial response is empty
    if not response:
        response = fetch_detections(-1)
    
    # Parse detections
    detections = {}
    for item in response:
        # Has audio?
        if not item['has_audio']:
            continue
        # Is species in species data?
        if not is_in_species_data(item['species_code']):
            continue
        # Is species blacklisted?
        if is_blacklisted(item['species_code']):
            continue
        if item['species_code'] not in detections:
            detections[item['species_code']] = []
        detections[item['species_code']].append(item)
        # format date
        item['datetime'] = datetime.strptime(item['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y - %H:%M')
        
        # convert to local time
        item['datetime'] = to_local_time(item['datetime'], cfg.TIME_FORMAT)
        
        # compute confidence as percentage
        item['confidence'] = get_confidence_score(item['species_code'], item['confidence'] * 100)
        
    # Remove species with less than min_count detections
    detections = {k: v for k, v in detections.items() if len(v) >= min_count}
        
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

def get_most_active_species(n=10, min_conf=0.5, hours=24, species_list=[], min_count=5):
    url = cfg.API_BASE_URL + 'detections'
    
    headers = {
        'Authorization': f'Token {cfg.API_TOKEN}'
    }
    params = {}
    
    # Project name
    params['project_name'] = cfg.PROJECT_NAME
    
    # Minimum confidence
    params['confidence_gte'] = min_conf
    
    # Only retrieve certain fields
    params['only'] = 'species_code, datetime, confidence'
    
    # set species code if species_list has len == 1
    if len(species_list) == 1:
        params['species_code'] = species_list[0]
    
    # Pagination/limit
    params['limit'] = 'None'
    
    def fetch_detections(hours):
        if hours > 0:
            now = datetime.now(UTC)
            params['datetime_recording__gte'] = (now - timedelta(hours=hours)).isoformat()
            params['datetime_recording__lte'] = now.isoformat()
        else:
            params.pop('datetime_recording__gte', None)
            params.pop('datetime_recording__lte', None)  
        
        # Send request
        response = requests.get(url, headers=headers, params=params)
        try:
            response = response.json()
        except:
            # Empty response
            return []
        
        return response
    
    # Initial fetch
    response = fetch_detections(hours)
    
    # Retry with hours set to -1 if the initial response is empty
    if not response:
        response = fetch_detections(-1)
    
    # Parse detections
    detections = {}
    for item in response:
        
        # Is species in species data?
        if not is_in_species_data(item['species_code']):
            continue
        
        # Is species blacklisted?
        if is_blacklisted(item['species_code']):
            continue
        
        # Is species in species_list?
        if len(species_list) > 0 and item['species_code'] not in species_list:
            continue
        
        if item['species_code'] not in detections:
            detections[item['species_code']] = {'detections': np.zeros(24, dtype=int)}
            
        # convert to local time
        item['datetime'] = datetime.strptime(item['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y - %H:%M')
        item['datetime'] = to_local_time(item['datetime'], time_format='24h')
        
        # format date
        hour = int(item['datetime'].split(' - ')[1].split(':')[0])
        detections[item['species_code']]['detections'][hour] += 1
        
    # Convert np array to list
    for species in detections:
        detections[species]['detections'] = detections[species]['detections'].tolist()
        
    # Remove species with less than min_count detections (but only if we have at least one species with more than min_count detections, if we don't, keep all species)
    if len([k for k, v in detections.items() if sum(v['detections']) >= min_count]) > 0:
        detections = {k: v for k, v in detections.items() if sum(v['detections']) >= min_count}
        
    # Sort by sum of detections
    detections = {k: v for k, v in sorted(detections.items(), key=lambda item: sum(item[1]['detections']), reverse=True)}
    
    # Remove species with no detections
    detections = {k: v for k, v in detections.items() if sum(v['detections']) > 0}
    
    # Limit to n species
    detections = {k: v for k, v in list(detections.items())[:n]}
    
    # Add species data
    for species in detections:
        species_data = get_species_data(species)
        for key, value in species_data.items():
            detections[species][key] = value
        detections[species]['total_detections'] = sum(detections[species]['detections'])
    
    return detections

def get_species_stats(species_code=None, recorder_id=None, min_conf=0.5, hours=168, limit=1000, max_results=50):
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
    
    # Only detections of species_code
    if species_code is not None:
        params['species_code'] = species_code
    
    # Recorder field ID
    if recorder_id is not None:
        params['recorder_field_id'] = recorder_id
        
    # Only retrieve certain fields
    params['only'] = 'species_code, has_audio, datetime, url_media, confidence, recorder_field_id'
    
    # Pagination/limit
    params['limit'] = limit
    
    def fetch_detections(hours):
        if hours > 0:
            now = datetime.now(UTC)
            params['datetime_recording__gte'] = (now - timedelta(hours=hours)).isoformat()
            params['datetime_recording__lte'] = now.isoformat()
        else:
            params.pop('datetime_recording__gte', None)
            params.pop('datetime_recording__lte', None)     
        
        # Send request
        response = requests.get(url, headers=headers, params=params)
        try:
            response = response.json()
        except:
            # Empty response
            return []
        
        return response
    
    # Initial fetch
    response = fetch_detections(hours)
    
    # Retry with hours set to -1 if the initial response is empty
    if not response:
        response = fetch_detections(-1)
    
    # For each detection, get the confidence score
    for item in response:
        # format date
        item['datetime'] = datetime.strptime(item['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y - %H:%M')
        
        # convert to local time
        item['datetime'] = to_local_time(item['datetime'], cfg.TIME_FORMAT)
        
        # compute confidence as percentage
        item['confidence'] = get_confidence_score(item['species_code'], item['confidence'] * 100) / 10.0
        
    # Remmove species not in species data
    response = [item for item in response if is_in_species_data(item['species_code'])]
    
    # Sort by confidence
    response = sorted(response, key=lambda x: x['datetime'], reverse=True)
    
    # Limit to max_results
    response = response[:max_results]
    
    return response
    
if __name__ == '__main__':    
    
    #print('Current week: ', get_current_week())
    
    #print('Number of detections in the last 24 hours:', get_total_detections(days=1)['total_detections'])
    #print('Number of detections with confidence >= 0.5:', get_total_detections(min_conf=0.5)['total_detections'])
    
    #print(get_last_n_detections())
    #print(get_most_active_species())
    
    #print(get_most_active_species(n=1, min_conf=0.5, hours=24*7, species_list=['whbnut']))
    
    #print(get_recorder_data(min_conf=0.5, days=2))
                                
    #print(get_species_stats('norcar', hours=24))
    
    #print(get_recorder_state(5))
    #print(get_recorder_group())
    for i in range(1, 13):
        print(f"#{i}: {get_recorder_location(i)}")
    
    #print(get_total_detections(min_conf=0.5, species_list=['norcar'], days=-1))
    #print(get_total_detections(min_conf=0.5, days=-1, recorder_list=[9]))
    
    