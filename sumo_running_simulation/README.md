# SmartTransportationRuppin

# SUMO Traffic Simulation Project 🚗🚦

## 📌 Overview
This project is a **SUMO (Simulation of Urban Mobility) traffic simulation** controlled via **Python (TraCI)**.  
It allows for **real-time traffic light management, vehicle speed/lane changes**, and logs detailed simulation data.

---

## 📂 Project Structure
![image](https://github.com/user-attachments/assets/67542c14-89c2-42fb-b611-2c72bbeba211)
```
sumo_running_simulation/
│── core/                  # Core simulation logic (Python classes)
│   ├── __init__.py        # Marks 'core' as a package
│   ├── logger.py          # Logger class (handles logging to console + file)
│   ├── simulation_runner.py      # SimulationRunner (controls SUMO execution)
│   ├── traffic_controller.py         # TrafficController (manages traffic lights)
│   ├── vehicle_controller.py         # VehicleController (manages vehicles)
│── main/                  # Main entry point for running the simulation
│   ├── __pycache__/       # (Auto-generated) Compiled Python files
│   ├── main.py            # Runs the SUMO simulation
│── sumo_config/           # SUMO configuration files
│   ├── StudyArea.sumocfg  # SUMO configuration file
│   ├── StudyAreaNetwork.net.xml  # SUMO road network definition
│   ├── Demand.rou.xml     # SUMO vehicle route file
│   ├── PublicTransport.xml # SUMO public transport data
│   ├── SUMO.log           # SUMO log file
│── test_examples/         # (Optional) For additional test cases
│── README.md              # Project documentation (this file)
```

---

## 🚀 How to Run the Simulation:
1. **Install SUMO** (if not installed):
   - Download from: [https://sumo.dlr.de/docs/Downloads.html](https://sumo.dlr.de/docs/Downloads.html)
   - Add SUMO to your system's `PATH` (for `sumo-gui` to work).

2. **Install Required Python Packages:**
   ```bash
   pip install termcolor
   ```

3. **Navigate to the project folder:**
   ```bash
   cd sumo_running_simulation
   ```

4. **Run the Simulation Using Python Module Mode:**
   ```bash
   python -m main.main
   ```
   ✅ This ensures Python recognizes `core/` as a package.

---

## 🎯 Features
✔ **Real-time control of traffic lights**  
✔ **Vehicle speed and lane management**  
✔ **Simulation logs written to `simulation_log.log`**  
✔ **SUMO-GUI integration for visual monitoring**  
✔ **Structured project for easy expansion**  

---

## 🛠️ Configuration Files (Inside `sumo_config/`)
- **`StudyArea.sumocfg`** → Main SUMO configuration file
- **`StudyAreaNetwork.net.xml`** → Defines the road network
- **`Demand.rou.xml`** → Defines vehicle flow & routes
- **`PublicTransport.xml`** → Defines public transport schedules

**📝 To modify simulation parameters, edit `StudyArea.sumocfg`.**  

---

## 📜 Example Log And Output
```
[2025-02-07 17:15:30] [INFO] ✅ Simulation started successfully with SUMO-GUI!
[2025-02-07 17:15:31] [INFO] 🔹 Step 1: 5 vehicles on the road
[2025-02-07 17:15:32] [INFO] 🚦 Traffic light 'gneJ1' changed to phase 2
[2025-02-07 17:15:35] [INFO] 🚗 Vehicle 'veh_42' speed set to 10 m/s
[2025-02-07 17:15:40] [INFO] 🔄 Vehicle 'veh_51' changed to lane 1
[2025-02-07 17:16:00] [INFO] 🔚 Simulation finished and closed successfully!
```
![image](https://github.com/user-attachments/assets/e8772671-b456-42bc-ad83-37ada5002161)

---
