# DESIGN: SmartHomeRTOS Prototype

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           SmartHomeRTOS                                 │
│                    (RTOS Simulation Framework)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐             │
│  │   Sensor     │    │   Control    │    │   Actuator   │             │
│  │    Task      │───▶│    Task      │───▶│    Task      │             │
│  │              │    │              │    │              │             │
│  │  - Temp      │    │  - Decision │    │  - Fan       │             │
│  │  - Motion    │    │  - Logic    │    │  - Light     │             │
│  │  - Door      │    │              │    │  - Door Lock │             │
│  └──────────────┘    └──────────────┘    └──────────────┘             │
│         │                   │                   │                      │
│         ▼                   ▼                   ▼                      │
│  ┌─────────────────────────────────────────────────────────┐          │
│  │              Event Queue (Inter-task comm)             │          │
│  └─────────────────────────────────────────────────────────┘          │
│         │                   │                   │                      │
│         ▼                   ▼                   ▼                      │
│  ┌──────────────┐    ┌──────────────┐                              │
│  │     Comm     │    │  User Input  │                              │
│  │    Task      │    │    Task      │                              │
│  │              │    │              │                              │
│  │  - Logging   │    │  - Commands  │                              │
│  │  - Console   │    │  - Toggle    │                              │
│  │  - File      │    │              │                              │
│  └──────────────┘    └──────────────┘                              │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────┐          │
│  │              Configuration (config.json)                │          │
│  │  - Sensor intervals  - Thresholds  - Random ranges      │          │
│  └─────────────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Task Flow

1. **SensorTask** generates simulated data (temperature, motion, door status)
2. **ControlTask** consumes sensor data and makes decisions
3. **ActuatorTask** applies commands to simulated hardware
4. **CommTask** logs all events to console and file
5. **UserInputTask** simulates remote user commands

## Overview

- Tasks are implemented as independent threads to simulate RTOS tasks.
- Inter-task communication is via thread-safe queues.
- Event logging is centralized through a communication task which writes to console and a log file.

Tasks

- SensorTask: emits simulated temperature, motion, door status.
- ControlTask: consumes sensor data and produces actuator commands.
- ActuatorTask: applies commands to a simulated actuator state.
- CommTask: collects events and logs them.
- UserInputTask: simulates remote user commands.

Configuration

Change behavior in `config/config.json` (intervals, thresholds, random ranges).

Scheduling and priorities

This prototype uses OS threads — to demonstrate priorities and preemption you'd extend the scheduler to simulate priority-based dispatching or use a cooperative scheduling model.
