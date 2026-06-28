# API (Module & Function Reference)

This file summarizes the prototype's modules, the main public functions, and how they interact. It's intended to help contributors quickly understand where to extend functionality.

## `src/main.py`

- `main(run_time=15)`
  - Entrypoint used for running the simulation.
  - Loads `config/config.json` if present.
  - Creates three queues: `sensor_queue`, `actuator_queue`, and an `EventQueue` instance.
  - Creates a `stop_event` threading.Event used to gracefully stop tasks.
  - Starts the following task threads: `SensorTask`, `ControlTask`, `ActuatorTask`, `CommTask`, and `UserInputTask`.

## `src/rtos/simulation.py`

- `class EventQueue`
  - Thin wrapper around `queue.Queue` used to publish structured event dictionaries (e.g. `{"task": "SensorTask", "msg": "..."}`).
  - Methods: `put(item)` and `get(timeout=None)`.

- `class TaskThread(threading.Thread)`
  - Helper to run a target function in a named thread. It catches and prints exceptions raised by the target.
  - Construct with `TaskThread(name, target, args)`.

## `src/tasks/sensor.py`

- `sensor_task(sensor_queue, event_queue, stop_event, config)`
  - Periodically generates a dictionary with keys: `timestamp`, `temperature`, `motion`, `door_open`.
  - Pushes sensor readings to `sensor_queue` and emits an event to `event_queue` for logging/visualization.
  - Configurable via `config` keys: `sensor_interval`, `random.temp`, `random.motion_chance`, `random.door_chance`.

## `src/tasks/control.py`

- `control_task(sensor_queue, actuator_queue, event_queue, stop_event, config)`
  - Pulls readings from `sensor_queue` and applies decision logic.
  - Example decisions: turn fan ON/OFF based on `temp_threshold`, turn lights ON when motion is detected, alert on door open.
  - Outputs actuator commands (simple dicts like `{"actor": "fan", "action": "set", "value": 80}`) into `actuator_queue`.

## `src/tasks/actuator.py`

- `class ActuatorState`
  - Holds an in-memory mapping of actuator states (e.g. `{"fan": 0, "light": 0, "door_lock": "locked"}`).
  - Method `apply(cmd)` updates the internal state according to a command dictionary.

- `actuator_task(actuator_queue, event_queue, stop_event, config)`
  - Reads commands from `actuator_queue`, applies them to `ActuatorState`, and emits a descriptive event to `event_queue`.

## `src/tasks/comm.py`

- `comm_task(event_queue, stop_event, config)`
  - Central logger. Dequeues event dicts from `event_queue`, prints a human-friendly line to stdout, and appends the same to a logfile (path from `config["logfile"]`).

## `src/tasks/user_input.py`

- `user_input_task(actuator_queue, event_queue, stop_event, config)`
  - Simulates remote user actions at an interval (`user_input_interval`).
  - Produces actuator commands (e.g., lock/unlock door) and puts them on `actuator_queue`.

## `config/config.json`

- JSON file controlling runtime parameters:
  - `sensor_interval` (seconds between sensor samples)
  - `temp_threshold` (Celsius threshold for fan control)
  - `user_input_interval` (seconds between simulated user commands)
  - `logfile` (path to the event log file)
  - `random` nested object controlling random ranges and chances for sensor simulation

## How to extend

- Add a new task: create a file in `src/tasks/` with a function that accepts the same basic arguments (queues and `stop_event`) and register it in `src/main.py` using `TaskThread`.
- Add new config parameters in `config/config.json` and read them from the `config` dict passed to tasks.

If you want, I can generate a machine-readable API reference (OpenAPI-style JSON or a Sphinx autodoc site) from these docfiles—tell me which format you prefer.
