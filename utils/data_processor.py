import sys
sys.path.append('..')

import os
import hashlib
import json
import time
import threading
import requests
import random
from datetime import datetime, timedelta, UTC 
import pytz
import numpy as np
import csv

from utils.strings import Strings

import config as cfg 

# Set random seed
random.seed(42)

def get_local_time(time_format='24h'):
    return datetime.now(pytz.timezone(cfg.TIMEZONE)).strftime('%I:%M %p') if time_format == '12h' else datetime.now(pytz.timezone(cfg.TIMEZONE)).strftime('%H:%M')

def get_current_week(date=None):
    if date is None:
        date = datetime.now(pytz.timezone(cfg.TIMEZONE))
    else:
        date = date.astimezone(pytz.timezone(cfg.TIMEZONE))
    
    fraction = min(52, max(0, (date.isocalendar()[1])) / 52)
    week = round(fraction * 48)
    
    return min(48, max(1, week))

def get_week_from_date(date):
    return get_current_week(date)

def get_share_data(data, locale):
    
    strings = Strings(locale, project=cfg.PROJECT_ID)
    
    share_data = {
            "title": f"{strings.get('misc_share_title')}",
            "url": data['url_media'],
            "text": f"{strings.get('project_main_title')} \n\n {data['common_name']} ({data['scientific_name']}) \n\n📅 {data['datetime']} \n📍{data['recorder_field_id']} \n\n🎧 {strings.get('misc_share_listen')}: ",
            "files": [data['url_media']],
            "filename": f"{cfg.PROJECT_ACRONYM.lower()}_{data['common_name'].replace(' ', '_').lower()}_{data['datetime'].split(': ')[-1].replace(' - ', '_').replace(' ', '_').replace(':', '-').replace('.', '-').replace('/', '-').lower()}.mp3",
        }
    
    return share_data

def date_to_last_seen(date, time_format='24h', locale='en'):
    strings = Strings(locale)
    date_formats = [
        cfg.DATE_FORMAT + ' - %I:%M %p',
        cfg.DATE_FORMAT + ' - %H:%M',
        '%m/%d/%Y - %I:%M %p',
        '%m/%d/%Y - %H:%M'
    ]
    for fmt in date_formats:
        try:
            date = datetime.strptime(date, fmt)
            break
        except ValueError:
            continue
    else:
        raise ValueError(f"Date {date} does not match any expected format.")
    
    delta = datetime.now() - date
    
    if delta.total_seconds() < 60:
        return f"{strings.get('dp_time_delta_ago_prefix')} 1 {strings.get('dp_time_delta_min')} {strings.get('dp_time_delta_ago_postfix')}"
    
    if delta.total_seconds() < 60 * 60:
        mins = int(delta.total_seconds() / 60)
        return f"{strings.get('dp_time_delta_ago_prefix')} {mins} {strings.get('dp_time_delta_min')} {strings.get('dp_time_delta_ago_postfix')}"
    
    if delta.total_seconds() < 60 * 60 * 48:
        hrs = int(delta.total_seconds() / 3600)
        hr_str = strings.get('dp_time_delta_hr') if hrs == 1 else strings.get('dp_time_delta_hrs')
        return f"{strings.get('dp_time_delta_ago_prefix')} {hrs} {hr_str} {strings.get('dp_time_delta_ago_postfix')}"
    
    days = int(delta.total_seconds() / 3600 / 24)
    day_str = strings.get('dp_time_delta_day') if days == 1 else strings.get('dp_time_delta_days')
    return f"{strings.get('dp_time_delta_ago_prefix')} {days} {day_str} {strings.get('dp_time_delta_ago_postfix')}"

def to_local_time(utc_time, time_format='24h', date_format=cfg.DATE_FORMAT):
    # Convert UTC time to local time
    try:
        utc_time = datetime.strptime(utc_time, '%m/%d/%Y - %I:%M %p')
    except ValueError:
        try:
            utc_time = datetime.strptime(utc_time, '%m/%d/%Y - %H:%M')
        except ValueError:
            try:
                utc_time = datetime.strptime(utc_time, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                raise ValueError(f"Date {utc_time} does not match any expected format.")
    
    timezone = pytz.timezone(cfg.TIMEZONE)
    local_time = utc_time.astimezone(timezone)
    
    if time_format == '12h':
        return local_time.strftime(date_format + ' - %I:%M %p')
    elif time_format == 'precise':
        return local_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    else:
        return local_time.strftime(date_format + ' - %H:%M')

def is_in_species_data(species_code):
    
    return species_code in cfg.SPECIES_DATA

def is_blacklisted(species_code):
    
    # Is in species data?
    if not is_in_species_data(species_code):
        return True
    
    return cfg.SPECIES_DATA[species_code]['blacklisted']

def is_before_project_start(date):
    
    project_start_date = datetime.strptime(cfg.PROJECT_START_DATE, '%d-%m-%Y')
    date = datetime.strptime(date.split('.')[0], '%Y-%m-%d %H:%M:%S')
    
    return date < project_start_date

def get_species_frequency(species):
    
    week = get_current_week()
    try:
        species_freq = cfg.SPECIES_DATA[species]['frequencies'][week - 1]
    except:
        species_freq = 10
        
    return species_freq

def get_confidence_score(species, confidence):
    
    # Get eBird species frequency
    species_freq = get_species_frequency(species)
        
    # Blend confidence and frequency as weighted average
    if species_freq >= 10 or species.startswith('t-'):
        confidence = int(confidence)
    elif species_freq > 0 and species_freq < 10:
        confidence = int((confidence * 0.75) + (species_freq * 0.25))
    else:
        confidence = int((confidence * 0.5) + (species_freq * 0.5))
    
    return min(99, max(1, confidence))

def get_battery_status(voltage):
    
    # Convert voltage to percentage
    # Everything above 12 is 100%, eveything below 9 is 10%, scale inbetween
    if not voltage is None:
        voltage = min(12, max(9, voltage))
    else:
        voltage = 9
    
    battery_level = max(10, int((voltage - 9) / (12 - 9) * 100) // 10 * 10)
    
    return str(battery_level) if battery_level > 10 else '< 10'

def get_weather_data():
    
    url = "http://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "lat": cfg.DEPLOYMENT_LAT,
        "lon": cfg.DEPLOYMENT_LON,
        "appid": cfg.OWM_API_KEY,
        "units": "metric"
    }
    
    headers = {}
    
    response = make_request(url, headers, params, cache_timeout=1500, ignore_cache=False)
    
    try:
        weather_data = {
            "temperature": round(response["main"]["temp"], 1),
            "weather": response["weather"][0]["main"],
            "wind_speed": response["wind"]["speed"],
            "humidity": response["main"]["humidity"],
            "pressure": response["main"]["pressure"]
        }
    except:
        weather_data = {
            "temperature": "N/A",
            "weather": "N/A",
            "wind_speed": "N/A",
            "humidity": "N/A",
            "pressure": "N/A"
        }     
    
    return weather_data

def ping():
    
    url = cfg.API_BASE_URL + 'detections'
    
    headers = {
        'Authorization': f'Token ' + cfg.API_TOKEN
    }
    params = {}
    
    # Project name
    params['project_name'] = cfg.PROJECT_NAME
    
    # Only retrieve certain fields
    params['only'] = 'species_code, datetime'
    
    # Pagination/limit
    params['limit'] = 5
    
    response = make_request(url, headers, params, cache_timeout=300)
    
    if len(response) == 0:
        return False
    
    return True

def get_project_list():
    
    url = 'https://api.ecopi.de/api/v0.1/projects/'
    
    headers = {
        'Authorization': f'Token {cfg.API_TOKEN}'
    }
    
    # No limit
    params = {}
    
    params['limit'] = 'None'
    
    response = make_request(url, headers, params, cache_timeout=0)
    
    project_list = []
    for project in response:
        project_list.append(project['project_name'])
    
    return project_list

def run_cache_costly_requests():
    threading.Thread(target=cache_costy_requests).start()

def cache_costy_requests():
    
    result = {}
    
    #print(f"Running cache_costly_requests at {datetime.now()}")
    
    # Total detections
    if 'total_detections' in get_total_detections():
        result['total_detections'] = 'chached'
    else:
        result['total_detections'] = 'error'
    
    if 'total_detections' in get_total_detections(days=1):
        result['total_detections_day'] = 'chached'
    else:
        result['total_detections_day'] = 'error'
        
    if 'total_detections' in get_total_detections(days=90):
        result['total_detections_90'] = 'chached'
    else:
        result['total_detections_90'] = 'error'
    
    # Most active species
    if len(get_most_active_species(n=8, min_conf=0.5, hours=7*24, recorder_list=[], locale='en')) > 0:
        result['most_active_species'] = 'chached'
    else:
        result['most_active_species'] = 'error'
        
    # Recorder stats
    for recorder_id in cfg.RECORDERS:
        try:
            if 'current_status' in get_recorder_state(recorder_id, locale='en'):
                result['recorder_state_' + str(recorder_id)] = 'chached'
            else:
                result['recorder_state_' + str(recorder_id)] = 'error'
            recorder_stats = get_species_stats(recorder_id=recorder_id, max_results=15)
            if len(recorder_stats) > 0:
                result['recorder_stats_' + str(recorder_id)] = 'chached'
            else:
                result['recorder_stats_' + str(recorder_id)] = 'error'
            species_data = get_most_active_species(n=8, min_conf=0.5, hours=7*24, recorder_list=[recorder_id], locale='en')
            if len(species_data) > 0:
                result['recorder_most_active_species_' + str(recorder_id)] = 'chached'
            else:
                result['recorder_most_active_species_' + str(recorder_id)] = 'error'
        except:
            continue
        
    # Total Audio Duration
    if get_total_audio_duration() > 0:
        result['total_audio_duration'] = 'chached'
        
    # Last N detections
    last_n = get_last_n_detections(n=24, hours=72, locale='en')
    if len(last_n) > 0:
        result['last_n_detections'] = 'chached'
    else:
        result['last_n_detections'] = 'error'
    
    # For each species in last_n, get weekly detections
    for species in last_n:
        #print(f"Checking species data for {species}")
        try:
            weekly_detections = get_weekly_detections(min_conf=0.5, species_code=species, recorder_id=None, min_count=5, locale='en')
            weekly_detections = {'detections': []}
            if len(weekly_detections['detections']) > 0:
                result['weekly_detections_' + species] = 'chached'
            else:
                result['weekly_detections_' + species] = 'error'
            species_stats = get_species_stats(species, max_results=10)
            if len(species_stats) > 0:
                result['species_stats_' + species] = 'chached'
            else:
                result['species_stats_' + species] = 'error'
        except:
            continue
    
    return result

def clean_cache(cache_dir, max_age=60*60*24):
    
    now = time.time()
    
    # Check if we need to clean the cache or if we did it recently
    if hasattr(cfg, 'LAST_CACHE_CLEANUP'):
        if now - cfg.LAST_CACHE_CLEANUP < 60*60:
            return
    
    # Open each file in the cache directory and check if it's older than max_age
    for filename in os.listdir(cache_dir):
        file_path = os.path.join(cache_dir, filename)
        if os.path.isfile(file_path):
            try:
                file_age = now - os.path.getmtime(file_path)
                if file_age > max_age:
                    os.remove(file_path)
            except:
                pass
            
    # Set LAST_CACHE_CLEANUP to now
    cfg.LAST_CACHE_CLEANUP = now

def make_request(url, headers, params, cache_timeout=3600, ignore_cache=False):
    
    # Does the cache directory exist?
    cache_dir = cfg.make_cache_dir(cfg.CACHE_DIR)
        
    # Clean the cache
    clean_cache(cache_dir)
    
    # Create a unique cache key
    cache_key = hashlib.md5((url + json.dumps(headers) + json.dumps(params)).encode()).hexdigest()
    cache_file = os.path.join(cache_dir, cache_key)

    # Check if the cache file exists and is still valid
    if os.path.exists(cache_file) and not ignore_cache:
        try:
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
                timestamp = cached_data['timestamp']
                if time.time() - timestamp < cache_timeout:
                    #print(f"Using cached data for {url}")
                    return cached_data['response']
        except:
            pass

    # Send the request
    #print(f"Making request to {url}")    
    try:
        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()
    except:
        # Empty response or request error
        response_data = []

    # Cache the response if it's not empty
    if len(response_data) > 0 and not ignore_cache:
        try:
            with open(cache_file, 'w') as f:
                json.dump({'timestamp': time.time(), 'response': response_data}, f)
        except:
            pass

    return response_data

def get_recorder_state(recorder_id, locale):
    
    strings = Strings(locale)
    
    url = 'https://api.ecopi.de/api/v0.1/recorderstates/'
    
    headers = {
        'Authorization': f'Token {cfg.API_TOKEN}'
    }
    params = {}
    
    # Project name
    params['project_name'] = cfg.PROJECT_NAME
    
    # Recorder ID
    params['recorder_field_id'] = recorder_id
    
    response = make_request(url, headers, params, cache_timeout=600)
    
    if len(response) == 0:
        
        return {'current_status': f"{strings.get('dp_recorder_status_error')} | {strings.get('dp_recorder_status_offline')}", 
                'status_color': '#DAD5BC', 
                'last_update': 'N/A',
                'battery': 'N/A',
                'cpu_temp': 'N/A', 
                'is_ok': False}
    
    last_status = response[0]
    
    time_since_last_status = datetime.now() - datetime.strptime(last_status['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S')            
    last_update = datetime.strptime(last_status['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y - %H:%M')
    
    is_ok = True if time_since_last_status.total_seconds() < 3600 * 24 else False
    
    current_status = f"Ok | {strings.get('dp_recorder_status_sleeping')}"
    status_color = '#69A0C2' # Blue
    if time_since_last_status.total_seconds() < 60 * 15 and not last_status['task'] == 'Finished':
        current_status = f"Ok | {strings.get('dp_recorder_status_listening')}"
        status_color = '#36824b' # Green
        
    if not is_ok:
        current_status = f"{strings.get('dp_recorder_status_error')} | {strings.get('dp_recorder_status_offline')}"
        status_color = '#DAD5BC' # Gray
    
    return {'current_status': current_status, 
            'status_color': status_color, 
            'last_update': date_to_last_seen(last_update, locale=locale),
            'battery': get_battery_status(last_status['voltage']),
            'cpu_temp': last_status['cpu_temp'], 
            'is_ok': is_ok}

def get_recordings_list():
    
    url = 'https://api.ecopi.de/api/v0.1/recordings/'
    
    headers = {
        'Authorization': f'Token {cfg.API_TOKEN}'
    }
    params = {}
    
    # Project name
    params['project_name'] = cfg.PROJECT_NAME
    
    # Get all recordings
    params['limit'] = 'None'
    
    # Only retrieve certain fields
    params['only'] = 'creation_time, duration, file_name'
    
    response = make_request(url, headers, params, cache_timeout=1500, ignore_cache=False)
    
    # Remove recordings that were recorded before the project start date
    response = [recording for recording in response if not is_before_project_start(recording['creation_time'])]
    
    return response
    
def get_total_audio_duration():
    
    recordings_list = get_recordings_list()
    
    total_audio = sum(min(300, recording['duration']) for recording in recordings_list)
    
    return max(0, int(total_audio))

def get_recorder_group():
    
    url = f"https://api.ecopi.de/api/v0.1/recordergroups/"
    
    headers = {
        'Authorization': f'Token {cfg.API_TOKEN}'
    }
    params = {}
    
    # Project name
    params['project_name'] = cfg.PROJECT_NAME
    
    response = make_request(url, headers, params, cache_timeout=0)
    
    return response

def get_recorder_location(recorder_id):
    
    url = f"https://api.ecopi.de/api/v0.1/recorders/recordergroup/{cfg.RECORDER_GROUP}/"
    
    headers = {
        'Authorization': f'Token {cfg.API_TOKEN}'
    }
    params = {}
    
    # Recorder ID
    params['recorder_field_id'] = recorder_id
    
    response = make_request(url, headers, params, cache_timeout=0)
    
    if len(response) == 0:
        return [None, None]
    
    return [response[0]['lat'], response[0]['lon']]

def get_recorder_inventory_name(recorder_id):
    
    url = 'https://api.ecopi.de/api/v0.1/recorderstates/'
    
    headers = {
        'Authorization': f'Token {cfg.API_TOKEN}'
    }
    params = {}
    
    # Project name
    params['project_name'] = cfg.PROJECT_NAME
    
    # Recorder ID
    params['recorder_field_id'] = recorder_id
    
    response = make_request(url, headers, params, cache_timeout=600)
    
    return response[0]['recorder_inventory_name']

def get_species_data(species, locale):
    
    data = {}
    
    if not species in cfg.SPECIES_DATA:
        return data
    
    if locale.lower() in cfg.SUPPORTED_SITE_LOCALES.values() and 'common_name_' + locale.lower() in cfg.SPECIES_DATA[species]:
        data['common_name'] = cfg.SPECIES_DATA[species]['common_name_' + locale.lower()]
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
        data['image_url'] = f"{cfg.SITE_ROOT}/image?url={cfg.SPECIES_DATA[species]['image']['src']}/320"
    else:
        data['image_url'] = cfg.SITE_ROOT + cfg.SPECIES_DATA[species]['image']['src']
    
    # High res species image
    if cfg.SPECIES_DATA[species]['image']['src'].find('birds.cornell.edu') > 0:
        data['image_url_highres'] = f"{cfg.SITE_ROOT}/image?url={cfg.SPECIES_DATA[species]['image']['src']}/900"
    else:
        data['image_url_highres'] = cfg.SITE_ROOT + cfg.SPECIES_DATA[species]['image']['src']
    
    data['image_author'] = cfg.SPECIES_DATA[species]['image']['author']
    if 'ml_asset_id' in cfg.SPECIES_DATA[species]['image'] and len(cfg.SPECIES_DATA[species]['image']['ml_asset_id']) > 0:
        data['ml_asset_id'] = ' | Macaulay Library ML' + cfg.SPECIES_DATA[species]['image']['ml_asset_id']
    else:
        data['ml_asset_id'] = ''
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
    
    response = make_request(url, headers, params, cache_timeout=600)
    
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

def get_total_detections(min_conf=0.5, species_list=[], recorder_list=[], days=-1, min_count=3):
    url = cfg.API_BASE_URL + 'meta/project/' + cfg.PROJECT_NAME + '/detections/recorderspeciescounts/'
    
    headers = {
        'Authorization': f'Token {cfg.API_TOKEN}'
    }
    params = {}
    
    # Minimum confidence
    params['min_confidence'] = min_conf
    
    # Set start date
    if days < 0:
        project_start_date = datetime.strptime(cfg.PROJECT_START_DATE, '%d-%m-%Y')
        params['start_date'] = project_start_date.strftime('%Y-%m-%d')
    else:
        params['start_date'] = (datetime.now(UTC).replace(minute=0, second=0, microsecond=0) - timedelta(days=days)).strftime('%Y-%m-%d')
    
    response = make_request(url, headers, params, cache_timeout=3300)
    
    # Count entries
    detections = {}
    for item in response:
        recorder_id = item['recorder_field_id']
        species_code = item['species_code']
        species_count = item['species_count']
        
        if len(recorder_list) == 0 or recorder_id in recorder_list:
            if len(species_list) == 0 or species_code in species_list:
                if species_code not in detections:
                    detections[species_code] = {'total_count': 0, 'recorders': {}}
                
                detections[species_code]['total_count'] += species_count
                
                if recorder_id not in detections[species_code]['recorders']:
                    detections[species_code]['recorders'][recorder_id] = 0
                
                detections[species_code]['recorders'][recorder_id] += species_count
    
    # Sort by total count
    detections = {k: v for k, v in sorted(detections.items(), key=lambda item: item[1]['total_count'], reverse=True)}
    
    # Only keep non-blacklisted species
    detections = {k: v for k, v in detections.items() if not is_blacklisted(k)}
    
    # If day == 1, remove species with species_freq == 0
    if days == 1:
        detections = {k: v for k, v in detections.items() if get_species_frequency(k) > 0}
    
    # Only keep species with total count >= min_count
    detections = {k: v for k, v in detections.items() if v['total_count'] >= min_count}
    
    total_detections = {'total_detections': sum(v['total_count'] for v in detections.values()), 'species_counts': detections}

    return total_detections

def get_weekly_detections(min_conf=0.5, species_code=None, recorder_id=None, min_count=5, locale='en'):
    
    # Check if either species_code or recorder_id is set
    assert species_code or recorder_id, 'Either species_code or recorder_id must be set.'
    
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
    params['only'] = 'species_code, datetime, recorder_field_id'
    
    # set species code and/or recorder id
    if species_code:
        params['species_code'] = species_code
    if recorder_id:
        params['recorder_field_id'] = recorder_id
    
    # Pagination/limit
    params['limit'] = 'None'
    
    # past 12 months
    now = datetime.now(UTC)
    if now.hour < 12:
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        now = now.replace(hour=12, minute=0, second=0, microsecond=0)
    params['datetime_recording__gte'] = (now - timedelta(days=365)).isoformat()
    params['datetime_recording__lte'] = now.isoformat()
    
    response = make_request(url, headers, params, cache_timeout=60*60*12, ignore_cache=False)
    
    # Count detections per week
    weekly_detections = np.zeros(48, dtype=int)
    
    # Based on cfg.PROJECT_START_DATE, set weeks to -1 if no - 365 days is before start date
    project_start_date = datetime.strptime(cfg.PROJECT_START_DATE, '%d-%m-%Y')
    project_start_date = project_start_date.replace(tzinfo=UTC)  # Make project_start_date timezone-aware
    
    if project_start_date > (now - timedelta(days=365)) and project_start_date.year < now.year:
        start_week = get_week_from_date(project_start_date)
        current_week = get_current_week()
        weekly_detections[current_week:start_week - 1] = -1
    elif project_start_date.year == now.year:
        start_week = get_week_from_date(project_start_date)
        current_week = get_current_week()
        weekly_detections[:start_week] = -1
        weekly_detections[current_week:] = -1
    
    # Add detections to weekly_detections
    for detection in response:
        
        # Is detection before project start date?
        if is_before_project_start(detection['datetime']):
            continue
        
        week = get_week_from_date(datetime.strptime(detection['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S'))
        weekly_detections[week - 1] += 1
    
    # Get projected frequency from species data
    if species_code:
        species_freq = cfg.SPECIES_DATA[species_code]['frequencies']
        try:
            species_freq /= np.max(species_freq)
        except:
            species_freq = np.ones(48, dtype=int).tolist()
            species_freq = [x / 100 for x in species_freq]
    else:
        species_freq = np.ones(48, dtype=int).tolist()
        species_freq = [x / 100 for x in species_freq]
        
    
    
    return {'detections': weekly_detections.tolist(), 'frequencies': species_freq, 'current_week': get_current_week()}

def get_last_n_detections(n=8, min_conf=0.5, hours=24, limit=5000, min_count=5, locale='en'):
    url = cfg.API_BASE_URL + 'detections'
    
    headers = {
        'Authorization': f'Token ' + cfg.API_TOKEN
    }
    params = {}
    
    # Project name
    params['project_name'] = cfg.PROJECT_NAME
    
    # Minimum confidence
    params['confidence__gte'] = min_conf
    
    # Only detections with audio
    params['has_media'] = True
    
    # Only retrieve certain fields
    params['only'] = 'species_code, has_audio, datetime, url_media, confidence, recorder_field_id'
    
    # Pagination/limit
    params['limit'] = limit
    
    def fetch_detections(hours):
        if hours > 0:
            now = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)
            params['datetime_recording__gte'] = (now - timedelta(hours=hours)).isoformat()
            params['datetime_recording__lte'] = now.isoformat()
        else:
            params.pop('datetime_recording__gte', None)
            params.pop('datetime_recording__lte', None)
        
        # Send request
        response = make_request(url, headers, params, cache_timeout=3300, ignore_cache=False)
        
        return response
    
    # Initial fetch
    response = fetch_detections(hours)
    
    # Retry with hours set to -1 if the initial response is empty
    if not response:
        response = fetch_detections(-1)
    
    # Parse detections
    detections = {}
    for item in response:
        
        # Is before project start date?
        if is_before_project_start(item['datetime']):
            continue
        
        # Has audio?
        if not item['has_audio']:
            continue
        # Is species in species data?
        if not is_in_species_data(item['species_code']):
            continue
        # Is species blacklisted?
        if is_blacklisted(item['species_code']):
            continue
        
        # compute confidence as percentage
        item['confidence'] = get_confidence_score(item['species_code'], item['confidence'] * 100)
        
        if item['confidence'] < 10:
            continue
        
        # format date
        item['datetime'] = datetime.strptime(item['datetime'].split('.')[0], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y - %H:%M')
        
        # convert to local time
        item['datetime'] = to_local_time(item['datetime'], cfg.TIME_FORMAT)    
        
        if item['species_code'] not in detections:
            detections[item['species_code']] = []
        detections[item['species_code']].append(item)
        
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
        species_data = get_species_data(species, locale)
        for key, value in species_data.items():
            last_n[species][key] = value
    
    return last_n

def get_most_active_species(n=10, min_conf=0.5, hours=24, species_list=[], min_count=5, recorder_list=[], locale='en'):
    url = cfg.API_BASE_URL + 'detections'
    
    headers = {
        'Authorization': f'Token {cfg.API_TOKEN}'
    }
    params = {}
    
    # Project name
    params['project_name'] = cfg.PROJECT_NAME
    
    # Minimum confidence
    params['confidence__gte'] = min_conf
    
    # Only retrieve certain fields
    params['only'] = 'species_code, datetime, confidence, recorder_field_id'
    
    # set species code if species_list has len == 1
    if len(species_list) == 1:
        params['species_code'] = species_list[0]
    
    # Pagination/limit
    params['limit'] = 'None'
    
    def fetch_detections(hours):
        if hours > 0:
            now = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)
            params['datetime_recording__gte'] = (now - timedelta(hours=hours)).isoformat()
            params['datetime_recording__lte'] = now.isoformat()
        else:
            params.pop('datetime_recording__gte', None)
            params.pop('datetime_recording__lte', None)  
        
        # Send request
        response = make_request(url, headers, params, cache_timeout=3300)
        
        return response
    
    # Initial fetch
    response = fetch_detections(hours)
    
    # Retry with hours set to -1 if the initial response is empty
    if not response:
        response = fetch_detections(-1)
    
    # Parse detections
    detections = {}
    for item in response:
        
        # Is before project start date?
        if is_before_project_start(item['datetime']):
            continue
        
        # Is species in species data?
        if not is_in_species_data(item['species_code']):
            continue
        
        # Is species blacklisted?
        if is_blacklisted(item['species_code']):
            continue
        
        # Is species in species_list?
        if len(species_list) > 0 and item['species_code'] not in species_list:
            continue
        
        # Is recorder in recorder_list?
        if len(recorder_list) > 0 and item['recorder_field_id'] not in recorder_list:
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
        species_data = get_species_data(species, locale)
        for key, value in species_data.items():
            detections[species][key] = value
        detections[species]['total_detections'] = sum(detections[species]['detections'])
    
    return detections

def get_species_stats(species_code=None, recorder_id=None, min_conf=0.5, hours=168, limit=5000, max_results=50):
    url = cfg.API_BASE_URL + 'detections'
    
    headers = {
        'Authorization': f'Token {cfg.API_TOKEN}'
    }
    params = {}
    
    # Project name
    params['project_name'] = cfg.PROJECT_NAME
    
    # Minimum confidence
    params['confidence__gte'] = min_conf
    
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
            now = datetime.now(UTC).replace(minute=0, second=0, microsecond=0)
            params['datetime_recording__gte'] = (now - timedelta(hours=hours)).isoformat()
            params['datetime_recording__lte'] = now.isoformat()
        else:
            params.pop('datetime_recording__gte', None)
            params.pop('datetime_recording__lte', None)     
        
        # Send request
        response = make_request(url, headers, params, cache_timeout=3300)
        
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
        
    # Remove species not in species data
    response = [item for item in response if is_in_species_data(item['species_code'])]
    
    # Remove blacklisted species
    response = [item for item in response if not is_blacklisted(item['species_code'])]
    
    # Remove low confidence detections
    response = [item for item in response if item['confidence'] >= 2]
    
    # Limit to at most 3 detections per species or per recorder
    if recorder_id is not None:
        species_detections = {}
        for item in response:
            species = item['species_code']
            if species not in species_detections:
                species_detections[species] = []
            if len(species_detections[species]) < 3:
                species_detections[species].append(item)
        response = [item for sublist in species_detections.values() for item in sublist]
    elif species_code is not None:
        recorder_detections = {}
        for item in response:
            recorder = item['recorder_field_id']
            if recorder not in recorder_detections:
                recorder_detections[recorder] = []
            if len(recorder_detections[recorder]) < 5:
                recorder_detections[recorder].append(item)
        response = [item for sublist in recorder_detections.values() for item in sublist]
    
    # Limit to max_results
    response = response[:max_results]
    
    return response

def export_detections(species_codes, recorder_ids, filepath, min_conf=0.1, from_date=None, to_date=None, limit=None):     
    
    url = cfg.API_BASE_URL + 'detections'
    
    headers = {
        'Authorization': f'Token {
            cfg.API_TOKEN}'
    }
    
    params = {}
    
    # Project name
    params['project_name'] = cfg.PROJECT_NAME
    
    # Minimum confidence
    params['confidence__gte'] = min_conf
    
    # Only detections with audio
    params['has_media'] = True
    
    # Pagination/limit
    if limit is not None:
        params['limit'] = limit
    else:
        params['limit'] = 'None'
    
    # Set species codes
    if len(species_codes) > 0:
        params['species_code__in'] = ','.join(species_codes)
        
    # Set recorder IDs
    if len(recorder_ids) > 0:
        params['recorder_field_id__in'] = ','.join(recorder_ids)
        
    # Set date range
    if from_date is not None:
        params['datetime_recording__gte'] = from_date
    if to_date is not None:
        params['datetime_recording__lte'] = to_date
        
    response = make_request(url, headers, params, cache_timeout=3300, ignore_cache=True)
    
    # Convert to local time
    for item in response:
        item['datetime'] = to_local_time(item['datetime'], time_format='precise')
        item['datetime_recording'] = to_local_time(item['datetime_recording'], time_format='precise')
    
    # Make dirs
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save to file
    if filepath.endswith('.csv'):
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['uid', 'species_code', 'datetime_recording', 'recorder_field_id', 'confidence', 'start', 'end', 'url_media'])
            for item in response:
                writer.writerow([item['uid'], item['species_code'], item['datetime_recording'], item['recorder_field_id'], item['confidence'], item['start'], item['end'], item['url_media']])
    else:
        with open(filepath, 'w') as f:
            json.dump(response, f, indent=4)
        
    return response    

def download_audio(url, filepath):
    
    # audio is publicly accessible, so no need for headers
    headers = {}
    
    # Send request
    response = requests.get(url, headers=headers)
    
    # Make dirs
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save to file
    with open(filepath, 'wb') as f:
        f.write(response.content)
        
    return filepath
    
if __name__ == '__main__':   
    
    print('Current week: ', get_current_week())
    
    #print('Number of detections in the last 24 hours:', get_total_detections(days=1)['total_detections'])
    #print('Number of detections with confidence >= 0.5:', get_total_detections(min_conf=0.5)['total_detections'])
    
    #print(get_last_n_detections())
    #print(get_most_active_species())
    
    #print(get_most_active_species(n=1, min_conf=0.5, hours=24*7, species_list=['whbnut']))
    
    #print(get_recorder_data(min_conf=0.5, days=2))
                                
    #print(get_species_stats('norcar', hours=24))
    
    #print(get_recorder_state(4, locale='en'))
    #print(get_recorder_group())
    #for i in range(1, 11):
    #    print(f"#{i}: lat: {get_recorder_location(i)[0]}, lon: {get_recorder_location(i)[1]}")
    #    print(f"#{i}: {get_recorder_inventory_name(i)}")
    
    #print(get_total_detections(min_conf=0.5, species_list=['eurnut2'], days=-1))
    #print(get_total_detections(min_conf=0.5, days=-1, recorder_list=[9]))
    
    #print(get_weekly_detections(min_conf=0.5, species_code='eurnut2', recorder_id=None))
    
    #for p in get_project_list():
    #    print(p)
    
    print(get_weather_data())
    
    #print(get_total_audio_duration())  
    #print(get_recordings_list())
    
    """
    print(len(export_detections(species_codes=['amewoo'], 
                                recorder_ids=['1', '2', '3'], 
                                filepath='../export/amewoo_detections.csv', 
                                min_conf=0.1, 
                                from_date='2025-03-14', 
                                to_date='2025-03-15', 
                                limit=None)))
    """
    