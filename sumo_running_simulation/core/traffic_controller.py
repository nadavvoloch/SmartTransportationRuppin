import traci

class TrafficController:
    """ Controls traffic lights in the SUMO simulation. """
    def __init__(self, logger):
        self.logger = logger
        self.traffic_lights = traci.trafficlight.getIDList()
        self.logger.log(f"Detected Traffic Lights: {self.traffic_lights}", "INFO", "yellow")
        self.active_light = self.traffic_lights[0] if self.traffic_lights else None

    def update_traffic_light(self, step):
        """ Changes the traffic light phase every 20 steps. """
        if self.active_light and step % 20 == 0:
            try:
                current_phase = traci.trafficlight.getPhase(self.active_light)
                new_phase = (current_phase + 1) % 4
                traci.trafficlight.setPhase(self.active_light, new_phase)
                self.logger.log(f"🚦 Traffic light {self.active_light} changed to phase {new_phase}", "INFO", "cyan")
            except traci.TraCIException:
                self.logger.log("⚠️ Error: Unable to update traffic light phase!", "ERROR", "red")
