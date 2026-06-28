"""Actuator task: receives commands and simulates hardware state changes."""
import time

class ActuatorState:
    def __init__(self):
        self.states = {"fan": 0, "light": 0, "door_lock": "locked"}

    def apply(self, cmd):
        actor = cmd.get("actor")
        action = cmd.get("action")
        value = cmd.get("value")
        if actor == "fan" and action == "set":
            self.states["fan"] = value
        if actor == "light" and action == "set":
            self.states["light"] = value
        if actor == "door_lock" and action == "alert":
            # for prototype, we just record alert
            self.states["door_lock"] = "alert"

    def __repr__(self):
        return str(self.states)


def actuator_task(actuator_queue, event_queue, stop_event, config):
    state = ActuatorState()
    while not stop_event.is_set():
        try:
            cmd = actuator_queue.get(timeout=0.5)
        except Exception:
            continue
        state.apply(cmd)
        event_queue.put({"task": "ActuatorTask", "msg": f"Applied {cmd} -> {state}"})
        time.sleep(0.01)
