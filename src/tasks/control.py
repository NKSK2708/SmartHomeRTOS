"""Control task: consumes sensor readings, makes decisions, and issues actuator commands."""
import time

def control_task(sensor_queue, actuator_queue, event_queue, stop_event, config):
    temp_threshold = config.get("temp_threshold", 30.0)
    while not stop_event.is_set():
        try:
            sensor = sensor_queue.get(timeout=0.5)
        except Exception:
            continue

        # Simple control logic
        commands = []
        t = sensor.get("temperature")
        if t is not None:
            if t > temp_threshold:
                commands.append({"actor": "fan", "action": "set", "value": 80, "reason": f"temp>{temp_threshold}"})
            else:
                commands.append({"actor": "fan", "action": "set", "value": 0, "reason": f"temp<= {temp_threshold}"})

        if sensor.get("motion"):
            commands.append({"actor": "light", "action": "set", "value": 100, "reason": "motion detected"})

        if sensor.get("door_open"):
            commands.append({"actor": "door_lock", "action": "alert", "value": None, "reason": "door opened"})

        for cmd in commands:
            actuator_queue.put(cmd)
            event_queue.put({"task": "ControlTask", "msg": f"Decision: {cmd}"})
        time.sleep(0.01)
