from core.simulation_runner import SimulationRunner

if __name__ == "__main__":
    simulation = SimulationRunner("flow_444.0") # Initialize the simulation with tracking specific vehicle
    delay = 0.01 # Add delay to slow down the simulation speed for better visualization
    simulation.run_simulation(delay=0)
