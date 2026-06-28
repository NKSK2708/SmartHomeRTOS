# DEMO: Running Scenarios

Example scenario: High Temperature

1. Edit `config/config.json` and set `temp_threshold` to 25 to more frequently trigger fan actions.
2. Run `python src/main.py` and observe the console/log output showing ControlTask decisions and ActuatorTask actions.

Important output lines:
- `[SensorTask]` shows sensor readings.
- `[ControlTask]` shows decisions (e.g., turning fan ON).
- `[ActuatorTask]` shows current actuator states.

Use the log file `smart_home.log` for reproducibility and sharing demo outputs.
