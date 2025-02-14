import traci
from .vehicle_tracker_plugin import VehicleTrackerPlugin

class ETAVehicleTracker(VehicleTrackerPlugin):
    """ Tracks a specific vehicle's estimated time of arrival (ETA). """

    def __init__(self, vehicle_id, eta_logger):
        self.vehicle_id = vehicle_id
        self.logger = eta_logger
        self.initial_position = None
        self.destination = None
        self.max_speed = 0
        self.fastest_step = 0
        self.logger.log(f"Tracking vehicle {self.vehicle_id} for ETA calculation.", "INFO", "cyan", 
                        class_name="ETAVehicleTracker", function_name="__init__")

    def initialize_tracking(self):
        """ Retrieves initial vehicle info and destination if available. """
        try:
            self.initial_position = traci.vehicle.getPosition(self.vehicle_id)
            self.max_speed = traci.vehicle.getMaxSpeed(self.vehicle_id)
            self.destination = traci.vehicle.getRoute(self.vehicle_id)[-1]  # Last waypoint
            self.logger.log(f"Tracking vehicle {self.vehicle_id}: Start Position: {self.initial_position}, Destination: {self.destination}",
                            "INFO", "cyan", class_name="ETAVehicleTracker", function_name="initialize_tracking")
        except traci.TraCIException:
            self.logger.log(f"Vehicle {self.vehicle_id} not found in simulation.", "ERROR", "red", class_name="ETAVehicleTracker", function_name="initialize_tracking")

    def track_vehicle(self, step):
        """ Tracks vehicle movement and calculates estimated arrival time. """
        try:
            position = traci.vehicle.getPosition(self.vehicle_id)
            speed = traci.vehicle.getSpeed(self.vehicle_id)

            if self.destination:
                distance_remaining = traci.simulation.getDistanceRoad(self.vehicle_id, self.destination)
                eta = distance_remaining / speed if speed > 0 else float("inf")

                self.logger.log(f"Step {step} | Vehicle {self.vehicle_id} | Position: {position} | Speed: {speed:.2f} m/s | ETA: {eta:.2f} s",
                                "INFO", "yellow", class_name="ETAVehicleTracker", function_name="track_vehicle")
        except traci.TraCIException:
            self.logger.log(f"Error tracking vehicle {self.vehicle_id} at step {step}.", "ERROR", "red", class_name="ETAVehicleTracker", function_name="track_vehicle")

    def get_summary(self):
        """ Returns the summary of the tracked vehicle's journey. """
        return f"Vehicle {self.vehicle_id} started at {self.initial_position} with destination {self.destination} and max speed {self.max_speed} m/s."
