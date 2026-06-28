"""Sensor task: produces simulated sensor readings and pushes to a queue."""
import time
import random

def sensor_task(sensor_queue, event_queue, stop_event, config):
    interval = config.get("sensor_interval", 1.0)
    rng = config.get("random", {})
    temp_range = rng.get("temp", [18, 35])
    motion_chance = rng.get("motion_chance", 0.1)
    door_chance = rng.get("door_chance", 0.02)

    while not stop_event.is_set():
        reading = {
            "timestamp": time.time(),
            "temperature": round(random.uniform(*temp_range), 1),
            "motion": random.random() < motion_chance,
            "door_open": random.random() < door_chance,
        }
        sensor_queue.put(reading)
        event_queue.put({"task": "SensorTask", "msg": f"Sensor: {reading}"})
        time.sleep(interval)
