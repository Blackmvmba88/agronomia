"""
Generate sample sensor data for testing and demonstration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def generate_sample_sensor_data(days=7, device_id="ESP32-001"):
    """Generate realistic sensor data for hydroponic tomato growing"""
    
    # Time range
    start_time = datetime.now() - timedelta(days=days)
    timestamps = [start_time + timedelta(minutes=i*5) for i in range(days * 288)]  # Every 5 minutes
    
    data = []
    
    for i, ts in enumerate(timestamps):
        hour = ts.hour
        
        # Simulate day/night cycle
        is_day = 6 <= hour <= 20
        
        # Light follows day/night cycle
        if is_day:
            lux = np.random.normal(25000, 3000)
        else:
            lux = np.random.normal(0, 50)
        
        # Temperature varies with light
        if is_day:
            air_temp = np.random.normal(24, 1.5)
            water_temp = np.random.normal(22, 1)
        else:
            air_temp = np.random.normal(20, 1)
            water_temp = np.random.normal(21, 0.5)
        
        # Humidity inversely related to temperature
        humidity = 70 - (air_temp - 22) * 2 + np.random.normal(0, 3)
        
        # pH drifts slightly over time
        ph_base = 6.0 + 0.2 * np.sin(i / 100)
        ph = ph_base + np.random.normal(0, 0.1)
        
        # EC slowly decreases as plants consume nutrients
        ec_base = 2200 - (i / len(timestamps)) * 300
        ec = ec_base + np.random.normal(0, 100)
        
        record = {
            'timestamp': ts.isoformat(),
            'device_id': device_id,
            'ph': round(np.clip(ph, 5.5, 7.0), 2),
            'water_temp': round(water_temp, 1),
            'air_temp': round(air_temp, 1),
            'humidity': round(np.clip(humidity, 50, 80), 1),
            'ec': int(np.clip(ec, 1500, 2500)),
            'tds': int(np.clip(ec * 0.5, 750, 1250)),
            'lux': int(max(0, lux)),
            'full_spectrum': int(max(0, lux * 1.2)),
            'infrared': int(max(0, lux * 0.2)),
            'visible': int(max(0, lux)),
            'plant_type': 'tomato',
            'growth_stage': 'fruiting' if i > len(timestamps) * 0.7 else 
                           'flowering' if i > len(timestamps) * 0.5 else 
                           'vegetative'
        }
        
        data.append(record)
    
    return pd.DataFrame(data)

def generate_growth_records(days=7, device_id="ESP32-001"):
    """Generate daily growth measurements"""
    
    start_time = datetime.now() - timedelta(days=days)
    dates = [start_time + timedelta(days=i) for i in range(days)]
    
    data = []
    base_height = 60
    base_leaves = 12
    
    for i, date in enumerate(dates):
        record = {
            'date': date.strftime('%Y-%m-%d'),
            'device_id': device_id,
            'plant_type': 'tomato',
            'days_since_transplant': 45 + i,
            'plant_height': round(base_height + i * 1.2 + np.random.normal(0, 0.5), 1),
            'leaf_count': int(base_leaves + i * 0.3),
            'stem_diameter': round(8 + i * 0.1 + np.random.normal(0, 0.2), 1),
            'notes': 'Healthy growth' if i % 2 == 0 else ''
        }
        data.append(record)
    
    return pd.DataFrame(data)

def generate_harvest_records(num_harvests=5):
    """Generate historical harvest data"""
    
    plant_configs = {
        'lettuce': {'days': 45, 'yield': 250},
        'tomato': {'days': 75, 'yield': 2000},
        'cucumber': {'days': 60, 'yield': 1500},
        'pepper': {'days': 80, 'yield': 800},
        'herbs': {'days': 30, 'yield': 100}
    }
    
    data = []
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(num_harvests):
        plant_type = np.random.choice(list(plant_configs.keys()))
        config = plant_configs[plant_type]
        
        harvest_date = start_date + timedelta(days=i*50)
        
        record = {
            'harvest_date': harvest_date.strftime('%Y-%m-%d'),
            'device_id': f'ESP32-00{i%3 + 1}',
            'plant_type': plant_type,
            'days_to_harvest': int(config['days'] + np.random.normal(0, 3)),
            'yield_g': int(config['yield'] * (1 + np.random.normal(0, 0.15))),
            'quality_rating': np.random.randint(3, 6),
            'brix_level': round(np.random.normal(4.5, 0.5), 1) if plant_type == 'tomato' else None,
            'notes': 'Good harvest' if np.random.random() > 0.3 else ''
        }
        data.append(record)
    
    return pd.DataFrame(data)

def main():
    """Generate all sample datasets"""
    
    print("Generating sample sensor data...")
    sensor_data = generate_sample_sensor_data(days=7)
    sensor_data.to_csv('sensor_data_sample.csv', index=False)
    print(f"Created sensor_data_sample.csv with {len(sensor_data)} records")
    
    print("\nGenerating growth records...")
    growth_data = generate_growth_records(days=7)
    growth_data.to_csv('growth_records_sample.csv', index=False)
    print(f"Created growth_records_sample.csv with {len(growth_data)} records")
    
    print("\nGenerating harvest records...")
    harvest_data = generate_harvest_records(num_harvests=10)
    harvest_data.to_csv('harvest_records_sample.csv', index=False)
    print(f"Created harvest_records_sample.csv with {len(harvest_data)} records")
    
    # Display sample data
    print("\n" + "="*60)
    print("Sample Sensor Data (last 5 records):")
    print("="*60)
    print(sensor_data.tail(5).to_string())
    
    print("\n" + "="*60)
    print("Sample Growth Records:")
    print("="*60)
    print(growth_data.to_string())
    
    print("\n" + "="*60)
    print("Sample Harvest Records:")
    print("="*60)
    print(harvest_data.to_string())
    
    # Generate summary statistics
    print("\n" + "="*60)
    print("Sensor Data Statistics:")
    print("="*60)
    print(sensor_data[['ph', 'water_temp', 'air_temp', 'humidity', 'ec', 'lux']].describe())

if __name__ == "__main__":
    main()
