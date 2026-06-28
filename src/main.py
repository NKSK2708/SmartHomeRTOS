"""Main runner for the SmartHomeRTOS prototype."""
import threading
import queue
import time
import json
import os

# Prefer package-relative imports when the module is run as part of the `src` package
try:
    from .rtos.simulation import TaskThread, EventQueue
    from .tasks import sensor, control, actuator, comm, user_input
except Exception:
    # Fall back to a script-friendly import path so `python src/main.py` also works.
    # This inserts the `src` directory on sys.path and imports the subpackages as top-level
    # modules (rtos, tasks). Prefer running as a module (python -m src.main) for package
    # semantics, but this fallback improves ergonomics for quick runs.
    import sys

    src_dir = os.path.dirname(os.path.abspath(__file__))
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    from rtos.simulation import TaskThread, EventQueue
    from tasks import sensor, control, actuator, comm, user_input

ROOT = os.path.dirname(os.path.abspath(__file__))


def load_config():
    cfg_path = os.path.join(os.path.dirname(ROOT), "config", "config.json")
    if os.path.exists(cfg_path):
        with open(cfg_path, "r") as f:
            return json.load(f)
    return {}


def main(run_time=15):
    config = load_config()
    sensor_queue = queue.Queue()
    actuator_queue = queue.Queue()
    event_queue = EventQueue()
    stop_event = threading.Event()

    # Create task threads
    threads = []
    threads.append(TaskThread("SensorTask", sensor.sensor_task, (sensor_queue, event_queue, stop_event, config)))
    threads.append(TaskThread("ControlTask", control.control_task, (sensor_queue, actuator_queue, event_queue, stop_event, config)))
    threads.append(TaskThread("ActuatorTask", actuator.actuator_task, (actuator_queue, event_queue, stop_event, config)))
    threads.append(TaskThread("CommTask", comm.comm_task, (event_queue, stop_event, config)))
    threads.append(TaskThread("UserInputTask", user_input.user_input_task, (actuator_queue, event_queue, stop_event, config)))

    for t in threads:
        t.start()

    try:
        time.sleep(run_time)
    except KeyboardInterrupt:
        pass

    print("Shutting down...")
    stop_event.set()
    for t in threads:
        t.join(timeout=1.0)
    print("Stopped.")


if __name__ == '__main__':
    main()
