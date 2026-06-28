# 🏠 SmartHomeRTOS – RTOS Smart Home Controller Simulation

A Python-based simulation of a **Real-Time Operating System (RTOS)** for a smart home controller. I built this project to better understand RTOS concepts such as task scheduling, inter-task communication, synchronization, and concurrent execution before implementing them on embedded hardware.

---

## 📌 Project Overview

This project simulates how an RTOS manages multiple tasks in a smart home environment. Independent tasks communicate through queues while sharing resources safely using synchronization mechanisms, closely resembling the architecture used in embedded firmware.

The simulation includes:

* Sensor monitoring
* Smart control logic
* Actuator control
* Communication and event logging
* User interaction

The objective was to gain hands-on experience with RTOS design principles that are commonly used in embedded systems.

---

## 🚀 Features

* RTOS-inspired multitasking using Python threads
* Inter-task communication with message queues
* Event-driven architecture
* Configurable runtime parameters
* Thread-safe resource sharing
* Centralized event logging
* Modular and scalable software architecture

---

## 🛠 Technologies Used

* Python 3
* Threading
* Queue
* JSON Configuration
* Logging
* Pytest

---

## 🏗 System Architecture

The controller is divided into independent tasks:

```
Sensor Task
      │
      ▼
Control Task
      │
      ▼
Actuator Task
      │
      ▼
Communication Task
```

Each task executes independently and exchanges information through queues, similar to tasks running under an RTOS scheduler.

---

## 📂 Project Structure

```
SmartHomeRTOS/
│
├── src/
│   ├── main.py
│   ├── tasks/
│   └── rtos/
│
├── config/
│   └── config.json
│
├── docs/
│   ├── API.md
│   ├── DESIGN.md
│   ├── DEMO.md
│   └── DEBUG.md
│
├── tests/
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Getting Started

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/SmartHomeRTOS.git
cd SmartHomeRTOS
```

### Create a virtual environment (optional)

```bash
python -m venv .venv
```

Activate it:

**Linux/macOS**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
pip install pytest
```

### Run the simulation

```bash
python -m src.main
```

or

```bash
python src/main.py
```

---

## 📝 Sample Output

```
[SensorTask] Temperature = 31.2°C
[ControlTask] Fan turned ON
[ActuatorTask] Fan speed = 80%
[CommTask] Event logged
```

---

## 🧪 Testing

Run all tests using:

```bash
python -m pytest
```

---

## 📚 What I Learned

Through this project, I gained practical experience with:

* RTOS concepts and task scheduling
* Multithreading
* Producer–Consumer architecture
* Queue-based communication
* Synchronization techniques
* Modular software design
* Event-driven programming
* Logging and debugging concurrent systems

---

## 🔮 Future Improvements

* Replace Python threads with FreeRTOS running on an ESP32
* Add MQTT communication
* Integrate Wi-Fi and IoT devices
* Build a web dashboard for real-time monitoring
* Simulate task priorities and priority inversion
* Add sensor fault detection and recovery

---

## 🎯 Why I Built This Project

As someone interested in embedded systems and firmware development, I wanted to better understand how RTOS-based applications are structured before implementing similar designs on embedded hardware. This project helped me explore concurrent programming, task communication, and scalable software architecture in a simplified environment.

---

## 👨‍💻 Author

**Krishna Sai Kaushik Nivarthi**

Graduate Student | Embedded Systems | Firmware Development | Machine Learning

If you found this project interesting, feel free to ⭐ the repository or connect with me on LinkedIn!
