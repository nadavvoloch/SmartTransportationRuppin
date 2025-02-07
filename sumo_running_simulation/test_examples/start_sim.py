import traci

# הפעלת SUMO
sumo_cmd = ["sumo", "-c", "StudyArea.sumocfg"]
traci.start(sumo_cmd)
num_of_steps = 100
most_veh = 0
most_veh_step = 0

# הרצת הסימולציה במשך 100 צעדים
for step in range(num_of_steps):
    traci.simulationStep()
    print(f"Step {step}: Vehicles on the road - {traci.vehicle.getIDCount()}")
    if traci.vehicle.getIDCount() > most_veh:
        most_veh = traci.vehicle.getIDCount()
        most_veh_step = step
print(f"\nMost vehicles on the road: {most_veh}, at step {most_veh_step}")
# סגירת החיבור לסימולציה
traci.close()
