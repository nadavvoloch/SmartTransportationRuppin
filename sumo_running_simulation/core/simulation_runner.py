import traci
import time
from .logger import Logger
from .traffic_controller import TrafficController
from .vehicle_controller import VehicleController

class SimulationRunner:
    def __init__(self):
        self.logger = Logger()

        if traci.isLoaded():
            self.logger.log("⚠️ Closing existing SUMO connection before starting a new one.", "WARNING", "yellow")
            traci.close()

        # ✅ Updated path to use sumo_config folder
        sumo_cmd = ["sumo-gui", "-c", "sumo_config/StudyArea.sumocfg", "--start"]
        traci.start(sumo_cmd)
        self.logger.log("✅ Simulation started successfully with SUMO-GUI!", "INFO", "green")

        self.traffic_controller = TrafficController(self.logger)
        self.vehicle_controller = VehicleController(self.logger)
        self.num_of_steps = 100
        self.most_veh = 0
        self.most_veh_step = 0

    def run_simulation(self):
        """ Runs the simulation loop while logging all events. """
        try:
            for step in range(self.num_of_steps):
                traci.simulationStep()
                time.sleep(0.05)  # ✅ Adds 50ms delay

                num_vehicles = traci.vehicle.getIDCount()
                self.logger.log(f"🔹 Step {step}: {num_vehicles} vehicles on the road", "INFO")

                if num_vehicles > self.most_veh:
                    self.most_veh = num_vehicles
                    self.most_veh_step = step

                self.traffic_controller.update_traffic_light(step)
                vehicle_id = self.vehicle_controller.get_active_vehicle()
                self.vehicle_controller.update_vehicle_speed(vehicle_id, step)
                self.vehicle_controller.change_vehicle_lane(vehicle_id, step)
                self.vehicle_controller.log_vehicle_info()

            self.logger.log(f"\n✅ Most vehicles on the road: {self.most_veh}, at step {self.most_veh_step}", "INFO", "green")

        except Exception as e:
            self.logger.log(f"❌ Critical simulation error: {e}", "ERROR", "red")

        finally:
            traci.close()
            self.logger.log("🔚 Simulation finished and closed successfully!", "INFO", "green")
            self.logger.close()
