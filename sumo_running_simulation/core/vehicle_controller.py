import traci

class VehicleController:
    """ Controls vehicles in the SUMO simulation. """
    def __init__(self, logger):
        self.logger = logger

    def get_active_vehicle(self):
        """ Retrieves the first active vehicle in the simulation. """
        vehicles = traci.vehicle.getIDList()
        return vehicles[0] if vehicles else None

    def update_vehicle_speed(self, vehicle_id, step):
        """ Changes vehicle speed after 30 steps. """
        if vehicle_id and step == 30:
            try:
                traci.vehicle.setSpeed(vehicle_id, 10)
                self.logger.log(f"🚗 Vehicle {vehicle_id} speed set to 10 m/s", "INFO", "blue")
            except traci.TraCIException:
                self.logger.log("⚠️ Error: Unable to update vehicle speed!", "ERROR", "red")

    def change_vehicle_lane(self, vehicle_id, step):
        """ Moves vehicle to another lane after 50 steps. """
        if vehicle_id and step == 50:
            try:
                traci.vehicle.changeLane(vehicle_id, 1, 5)
                self.logger.log(f"🔄 Vehicle {vehicle_id} changed to lane 1", "INFO", "magenta")
            except traci.TraCIException:
                self.logger.log("⚠️ Error: Unable to change lane!", "ERROR", "red")

    def log_vehicle_info(self):
        """ Logs detailed vehicle info. """
        vehicles = traci.vehicle.getIDList()
        if vehicles:
            for v_id in vehicles:
                position = traci.vehicle.getPosition(v_id)
                speed = traci.vehicle.getSpeed(v_id)
                lane = traci.vehicle.getLaneIndex(v_id)
                self.logger.log(f"🚙 Vehicle {v_id}: Position ({position[0]:.3f}, {position[1]:.3f}), Speed {speed:.3f} m/s, Lane {lane}", "INFO")
        else:
            self.logger.log("⚠️ No vehicles detected in the simulation!", "WARNING", "red")
