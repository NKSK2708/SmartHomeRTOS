"""Communication/log task: collects events and writes to console + file."""
import time

def comm_task(event_queue, stop_event, config):
    logfile = config.get("logfile", "smart_home.log")
    with open(logfile, "w") as f:
        while not stop_event.is_set():
            try:
                ev = event_queue.get(timeout=0.5)
            except Exception:
                continue
            line = f"[{time.strftime('%H:%M:%S')}] [{ev.get('task')}] {ev.get('msg')}\n"
            print(line, end="")
            f.write(line)
            f.flush()
