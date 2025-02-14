from core.simulation_runner import SimulationRunner

if __name__ == "__main__":
    simulation = SimulationRunner("flow_10.0")
    delay = 0.01 # Add delay to slow down the simulation speed for better visualization
    simulation.run_simulation(delay=0)
