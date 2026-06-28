"""User input task: simulates remote user commands periodically."""
import time

def user_input_task(actuator_queue, event_queue, stop_event, config):
    interval = config.get("user_input_interval", 10.0)
    toggle = True
    while not stop_event.is_set():
        # simulate a user toggling the door lock state
        cmd = {"actor": "door_lock", "action": "set", "value": "locked" if toggle else "unlocked", "reason": "user_toggle"}
        actuator_queue.put(cmd)
        event_queue.put({"task": "UserInputTask", "msg": f"User command: {cmd}"})
        toggle = not toggle
        time.sleep(interval)
