import random

# Available study days and number of one-hour slots per day
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
SLOTS_PER_DAY = 4  # 20 study slots per week

# Sample tasks for weekly study schedule optimization
# hours: Number of one-hour slots required to complete the task
# priority: 3 = High, 2 = Medium, 1 = Low
# deadline: 0 = Monday, 1 = Tuesday, ..., 4 = Friday
#           Each task must be completed by the end of its deadline day

TASKS = {
    "A": {"name": "Assignment", "hours": 4,
          "priority": 1, "deadline": 2},
    "B": {"name": "Project", "hours": 5,
          "priority": 3, "deadline": 3},
    "C": {"name": "Essay", "hours": 3,
          "priority": 2, "deadline": 3},
    "D": {"name": "Exam Review", "hours": 3,
          "priority": 3, "deadline": 4}
}

# Total required study time: 15 hours
# Remaining available time: 5 free slots


def create_chromosome():
    chromosome = []

    # Add the required hours for each task
    for task_id, task in TASKS.items():
        chromosome.extend([task_id] * task["hours"])

    # Fill the remaining slots with free time
    total_slots = len(DAYS) * SLOTS_PER_DAY
    free_slots = total_slots - len(chromosome)
    if free_slots < 0:
        raise ValueError("Tasks exceed available study time.")

    chromosome.extend(["Free"] * free_slots)

    # Randomize the study schedule
    random.shuffle(chromosome)

    return chromosome


def display_schedule(chromosome):
    for i, day in enumerate(DAYS):
        start = i * SLOTS_PER_DAY
        end = start + SLOTS_PER_DAY

        print(day, ":", chromosome[start:end])
        

def create_population(size):
    # Generate multiple random chromosomes
    population = []

    for _ in range(size):
        population.append(create_chromosome())

    return population


if __name__ == "__main__":
    chromosome = create_chromosome()
    display_schedule(chromosome)
    
    population = create_population(100)
    print("Initial population size:", len(population))