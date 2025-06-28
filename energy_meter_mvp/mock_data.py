from datetime import datetime, timedelta
from typing import List, Dict
import random

def get_mock_smart_meter_data(smart_meter_id: str, start: datetime, end: datetime) -> List[Dict]:
    # For MVP, only allow smart_meter_id '123'
    if smart_meter_id != '123':
        return []
    data = []
    current = start
    while current <= end:
        data.append({
            'timestamp': current.isoformat() + 'Z',
            'smart_meter_id': smart_meter_id,
            'energy_kwh': round(random.uniform(0.5, 1.5), 2),
            'power_kw': round(random.uniform(2.0, 3.0), 2),
            'voltage_v': round(random.uniform(229.0, 231.0), 1),
            'current_a': round(random.uniform(8.5, 10.0), 1),
        })
        current += timedelta(minutes=1)
    return data 