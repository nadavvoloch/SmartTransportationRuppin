import traci
import time
import random
from .logger import Logger
from .traffic_controller import TrafficController
from .vehicle_controller import VehicleController
from .eta_logger import ETAFileLogger
from .eta_vehicle_tracker import ETAVehicleTracker

class SimulationRunner:
    """ Main class to run the SUMO simulation with plugins and dynamic vehicle behavior. """

    def __init__(self, tracked_vehicle_id_=None):
        self.logger = Logger()
        
        try:
            self.eta_logger = ETAFileLogger()
            self.logger.log("📝 ETA tracking logger initialized.", "INFO", "cyan",
                        class_name="SimulationRunner", function_name="__init__")
        except Exception as e:  
            self.logger.log(f"❌ Error initializing ETA tracking logger: {e}", "ERROR", "red",
                        class_name="SimulationRunner", function_name="__init__")

        # Close existing SUMO connection if it's already active
        if traci.isLoaded():
            self.logger.log("⚠️ Closing existing SUMO connection before starting a new one.", "WARNING", "yellow",
                            class_name="SimulationRunner", function_name="__init__")
            traci.close()

        # Start SUMO-GUI with the simulation configuration
        sumo_cmd = ["sumo-gui", "-c", "sumo_config/StudyArea.sumocfg", "--start"]
        traci.start(sumo_cmd)
        self.logger.log("✅ Simulation started successfully with SUMO-GUI!", "INFO", "green",
                        class_name="SimulationRunner", function_name="__init__")

        self.tracked_vehicle_id = tracked_vehicle_id_
        self.vehicle_tracker = ETAVehicleTracker(self.tracked_vehicle_id, self.eta_logger) if tracked_vehicle_id_ else None
        self.logger.log(f"🚦 Initializing SUMO simulation with vehicle tracking: {tracked_vehicle_id_}", "INFO", "green",
                        class_name="SimulationRunner", function_name="__init__")
        
        # Initialize controllers
        self.traffic_controller = TrafficController(self.logger)
        self.vehicle_controller = VehicleController(self.logger)

        # Simulation parameters
        self.num_of_steps = 100
        self.most_veh = 0
        self.most_veh_step = 0
        self.traffic_phase_duration = 10

        # Initialize vehicle tracking if requested
        if self.vehicle_tracker:
            self.vehicle_tracker.initialize_tracking()

    def run_simulation(self, delay=0.01):
        """ Runs the simulation loop while logging all events. """
        try:
            for step in range(self.num_of_steps):
                traci.simulationStep()
                time.sleep(delay)

                # Log current step and vehicle count
                num_vehicles = traci.vehicle.getIDCount()
                self.logger.log(f"🔹 Step {step}: {num_vehicles} vehicles on the road", "INFO",
                                class_name="SimulationRunner", function_name="run_simulation")

                # Track the maximum vehicle count
                if num_vehicles > self.most_veh:
                    self.most_veh = num_vehicles
                    self.most_veh_step = step

                # Adjust the speed of one random vehicle every 10 steps
                if step % 10 == 0:
                    self.adjust_vehicle_speeds_randomly()

                # Update traffic lights
                self.traffic_controller.update_traffic_light(step, self.traffic_phase_duration)

                # Log all vehicle information
                self.vehicle_controller.log_vehicle_info()

                # Track the fastest vehicle each step
                self.vehicle_controller.track_fastest_vehicle(step)

                # Track ETA for the selected vehicle
                if self.vehicle_tracker:
                    self.vehicle_tracker.track_vehicle(step)

            # Log the summary of the fastest vehicle
            fastest_vehicle, fastest_speed, fastest_step = self.vehicle_controller.get_fastest_vehicle_summary()
            self.logger.log(f"\n✅ Most vehicles on the road: {self.most_veh}, at step {self.most_veh_step}", "INFO", "green",
                            class_name="SimulationRunner", function_name="run_simulation")
            self.logger.log(f"🚀 Fastest vehicle: {fastest_vehicle} with speed {fastest_speed:.2f} m/s at step {fastest_step}", "INFO", "green",
                            class_name="SimulationRunner", function_name="run_simulation")

            # Log the ETA summary if tracking a specific vehicle
            if self.vehicle_tracker:
                self.eta_logger.log(self.vehicle_tracker.get_summary(), "INFO", "green",
                                    class_name="SimulationRunner", function_name="run_simulation")

        except Exception as e:
            self.logger.log(f"❌ Critical simulation error: {e}", "ERROR", "red",
                            class_name="SimulationRunner", function_name="run_simulation")

        finally:
            traci.close()
            self.logger.log("🔚 Simulation finished and closed successfully!", "INFO", "green",
                            class_name="SimulationRunner", function_name="run_simulation")
            self.logger.close()
            self.eta_logger.close()

    def adjust_vehicle_speeds_randomly(self):
        """ Randomly adjust the speed of one random active vehicle. """
        vehicles = self.vehicle_controller.get_active_vehicles()
        if vehicles:
            selected_vehicle = random.choice(vehicles)
            random_speed = random.uniform(5, 25)  # Speed between 5 and 25 m/s
            self.vehicle_controller.update_vehicle_speed(selected_vehicle, random_speed)
            self.logger.log(f"🔀 Randomly adjusted speed of vehicle {selected_vehicle} to {random_speed:.2f} m/s",
                            "INFO", "blue", class_name="SimulationRunner", function_name="adjust_vehicle_speeds_randomly")
