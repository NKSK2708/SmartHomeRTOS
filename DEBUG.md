# DEBUG — how to run and attach a debugger

This short guide explains how to debug the SmartHomeRTOS prototype locally and in VS Code. It covers quick `pdb` checks, attaching VS Code (debugpy), and running tests under the debugger.

Prerequisites

- Python 3.9+ (3.8 often works but CI tests are configured for 3.9+) 
- (Optional) A virtual environment for development
- `debugpy` installed in the same environment used by VS Code or your terminal:

```bash
pip install debugpy
```

Quick patterns

1. Terminal (fast, no IDE): use `pdb` or `breakpoint()`

```python
# insert into code where you want to pause
breakpoint()
```

Run program from terminal and interact in the REPL when it pauses.

2. Attach VS Code (recommended for threaded code)

- We include a `.vscode/launch.json` with a `Run src.main (module)` and `Attach to debugpy` configurations. Use the `Run` config if you want VS Code to start and debug the program for you.
- To attach to a process started outside VS Code, use the debugpy attach helper (optional) or run debugpy as a wrapper.

Option A — run debugpy wrapper (no code edits):

```bash
# from project root
python -m debugpy --listen 5678 --wait-for-client -m src.main
```

Then in VS Code choose the `Attach to debugpy (port 5678)` configuration and click Start.

Option B — env-guarded attach helper (edit code once)

Add this near the top of `src/main.py` (before threads are created):

```python
import os
if os.getenv("DEBUG_ATTACH") == "1":
    try:
        import debugpy
        debugpy.listen(("127.0.0.1", 5678))
        print("Waiting for debugger to attach on port 5678...")
        debugpy.wait_for_client()
        print("Debugger attached, continuing.")
    except Exception as e:
        print("debugpy attach helper failed:", e)
```

Start the program in a terminal and it will wait for VS Code to attach:

```bash
DEBUG_ATTACH=1 python -m src.main
```

Then attach from VS Code using the `Attach to debugpy (port 5678)` configuration.

3. Debugging tests

Run a single test under the debugger for fast iteration. Example (attach wrapper):

```bash
python -m debugpy --listen 5678 --wait-for-client -m pytest tests/test_simulation.py -q
```

Then attach from VS Code.

Tips for threaded programs

- Prefer attaching before threads start so you can set breakpoints in the main thread before workers spawn. The env-guarded snippet is useful for this.
- Use the Debug pane's Threads view to switch between threads and inspect each thread's call stack and local variables.
- Avoid `pdb.set_trace()` inside worker threads unless you know how to interact with that thread's REPL — use the IDE attach method instead.

Common issues & fixes

- "attempted relative import with no known parent package": run with module form:

```bash
python -m src.main
```

- Breakpoints not hit: ensure VS Code uses the same Python interpreter (Command Palette → "Python: Select Interpreter") as the one used to run the process and where `debugpy` is installed.
- Attach appears to hang: confirm the process is listening on port 5678:

```bash
lsof -iTCP -sTCP:LISTEN -n -P | grep 5678
```

Security & safety

- Bind debugpy to `127.0.0.1` and avoid `0.0.0.0` on public hosts.
- Don’t leave `DEBUG_ATTACH` enabled on production systems.

Further reading

- debugpy docs: https://aka.ms/debugpy
- VS Code Python debugging docs: https://code.visualstudio.com/docs/python/debugging

Example session — pause in control_task when temperature > threshold

This example shows a short session you can reproduce locally to (a) pause execution when the control logic detects a high temperature, and (b) inspect the actuator command that will be produced.

1) Set a conditional breakpoint in VS Code

- Open `src/tasks/control.py` and add a breakpoint on the line where the decision is made (the code that checks temperature against `temp_threshold`). Right-click the breakpoint and choose "Edit Breakpoint" → set condition:

    reading.get('temperature', 0) > config.get('temp_threshold', 30.0)

2) Start the program and attach the debugger

Option A (VS Code launch): select `Run src.main (module)` in the Run & Debug pane and start the debugger.

Option B (attach): from the project root run:

```bash
# wait for VS Code to attach
python -m debugpy --listen 5678 --wait-for-client -m src.main
```

Then attach using the `Attach to debugpy (port 5678)` launch configuration in VS Code.

3) Observe when the condition fires

- When a sensor reading with temperature > threshold is processed in `control_task`, VS Code will pause at the conditional breakpoint.
- In the Debug pane switch to the thread that hit the breakpoint. Inspect local variables: `sensor` (the reading), `config`, and any temporary `commands` that will be enqueued.

4) Sample commands & console output

Below is a short, realistic snippet you might see in the Debug Console and the log (`smart_home.log`) when the breakpoint fires and the control task produces a fan command:

```
[12:00:02] [SensorTask] Sensor: {'timestamp': 1676548802.12, 'temperature': 32.4, 'motion': True, 'door_open': False}
[12:00:02] [ControlTask] Decision: {'actor': 'fan', 'action': 'set', 'value': 80, 'reason': 'temp>30.0'}
[12:00:02] [ActuatorTask] Applied {'actor': 'fan', 'action': 'set', 'value': 80} -> {'fan': 80, 'light': 0, 'door_lock': 'locked'}
```

5) Quick checks while paused

- Evaluate `sensor.get('temperature')` in the Debug Console. It should be > threshold.
- Evaluate `commands` (or the variable holding new actuator commands) to see what will be sent to `actuator_queue`.
- Step over (F10) to let the control task enqueue the command and then inspect queues with expressions like `actuator_queue.qsize()`.

6) Clean up

- After confirming behavior, press Continue (F5) to let the simulation run. Remove or disable the conditional breakpoint when finished if you do not want frequent pauses.