import random
import numpy as np

# INPUT DATA
#####################################################################
facilitators = [
    "Lock", "Glen", "Banks", "Richards", "Shaw", "Singer", "Uther", "Tyler", "Numen", "Zeldin"
]

facilitator_preferences = {
    "SLA100A": {
        "expected_enrollment": 50,
        "preferred_facilitators": ["Glen", "Lock", "Banks", "Zeldin"],
        "other_facilitators": ["Numen", "Richards"]
    },
    "SLA100B": {
        "expected_enrollment": 50,
        "preferred_facilitators": ["Glen", "Lock", "Banks", "Zeldin"],
        "other_facilitators": ["Numen", "Richards"]
    },
    "SLA191A": {
        "expected_enrollment": 50,
        "preferred_facilitators": ["Glen", "Lock", "Banks", "Zeldin"],
        "other_facilitators": ["Numen", "Richards"]
    },
    "SLA191B": {
        "expected_enrollment": 50,
        "preferred_facilitators": ["Glen", "Lock", "Banks", "Zeldin"],
        "other_facilitators": ["Numen", "Richards"]
    },
    "SLA201": {
        "expected_enrollment": 50,
        "preferred_facilitators": ["Glen", "Banks", "Zeldin", "Shaw"],
        "other_facilitators": ["Numen", "Richards", "Singer"]
    },
    "SLA291": {
        "expected_enrollment": 50,
        "preferred_facilitators": ["Lock", "Banks", "Zeldin", "Singer"],
        "other_facilitators": ["Numen", "Richards", "Shaw", "Tyler"]
    },
    "SLA303": {
        "expected_enrollment": 60,
        "preferred_facilitators": ["Glen", "Zeldin", "Banks"],
        "other_facilitators": ["Numen", "Singer", "Shaw"]
    },
    "SLA304": {
        "expected_enrollment": 25,
        "preferred_facilitators": ["Glen", "Banks", "Tyler"],
        "other_facilitators": ["Numen", "Singer", "Shaw", "Richards", "Uther", "Zeldin"]
    },
    "SLA394": {
        "expected_enrollment": 20,
        "preferred_facilitators": ["Tyler", "Singer"],
        "other_facilitators": ["Richards", "Zeldin"]
    },
    "SLA449": {
        "expected_enrollment": 60,
        "preferred_facilitators": ["Tyler", "Singer", "Shaw"],
        "other_facilitators": ["Zeldin", "Uther"]
    },
    "SLA451": {
        "expected_enrollment": 100,
        "preferred_facilitators": ["Tyler", "Singer", "Shaw"],
        "other_facilitators": ["Zeldin", "Uther", "Richards", "Banks"]
    }
}

room_capacities = {
    "Slater 003": 45,
    "Roman 216": 30,
    "Loft 206": 75,
    "Roman 201": 50,
    "Loft 310": 108,
    "Beach 201": 60,
    "Beach 301": 75,
    "Logos 325": 450,
    "Frank 119": 60
}

time_slots = [
    10, 11, 12, 13, 14, 15
]

#####################################################################

#Generate a random schedule based on above input data
def generate_random_schedule():
    schedule = {}
    activities = list(facilitator_preferences.keys())

    for activity in activities:
        available_rooms = list(room_capacities.keys())
        random.shuffle(available_rooms)
        
        # Randomly assign a room to the activity
        room = available_rooms[0]
        
        # Randomly assign a time slot to the activity
        time_slot = random.choice(time_slots)
        
        # Randomly assign a facilitator to the activity
        preferred_facilitators = facilitator_preferences[activity]["preferred_facilitators"]
        other_facilitators = facilitator_preferences[activity]["other_facilitators"]
        
        all_facilitators = preferred_facilitators + other_facilitators
        random.shuffle(all_facilitators)
        
        facilitator = all_facilitators[0]

        schedule[activity] = {
            "room": room,
            "time_slot": time_slot,
            "facilitator": facilitator
        }

    return schedule

def calculate_fitness(schedule):
    schedule_by_time = {time_slot: [] for time_slot in time_slots}
    schedule_by_facil = {facilitator: [] for facilitator in facilitators}
    facilitator_load = {facilitator: {time_slot: [] for time_slot in time_slots} for facilitator in facilitators}

    activities_fitness = {name: 0 for name in schedule}

    #build different schedule types to make comparison easier
    for class_name in schedule:
        class_details = schedule[class_name]
        time_slot = class_details['time_slot']
        facilitator = class_details['facilitator']
        schedule_by_time[time_slot].append(class_name)
        schedule_by_facil[facilitator].append(class_name)
        facilitator_load[facilitator][time_slot].append(class_name)

    for class_name in schedule:
        class_details = schedule[class_name]
        class_size = facilitator_preferences[class_name]['expected_enrollment']
        room = class_details['room']
        room_size = room_capacities[room]
        time_slot = class_details['time_slot']
        facilitator = class_details['facilitator']
        preferred_facilitators = facilitator_preferences[class_name]['preferred_facilitators']
        other_facilitators = facilitator_preferences[class_name]['other_facilitators']

        #Class and room size checks
        class_size_flag = True
        if class_size > room_size:
            activities_fitness[class_name] = activities_fitness[class_name] - .5
            class_size_flag = False     

        if (class_size * 3) < room_size:
            activities_fitness[class_name] = activities_fitness[class_name] - .2
            class_size_flag = False

        if (class_size * 6) < room_size:
            activities_fitness[class_name] = activities_fitness[class_name] - .4
            class_size_flag = False
        
        if class_size_flag:
            activities_fitness[class_name] = activities_fitness[class_name] + .3

        #Facilitator checks for preferred/other
        facilitator_flag = True
        if facilitator in preferred_facilitators:
            activities_fitness[class_name] = activities_fitness[class_name] + .5
            facilitator_flag = False

        if facilitator in other_facilitators:
            activities_fitness[class_name] = activities_fitness[class_name] + .2
            facilitator_flag = False

        if facilitator_flag:
            activities_fitness[class_name] = activities_fitness[class_name] -.1

        #Facilitator total classes taught
        if len(facilitator_load[facilitator][time_slot]) == 1:
            activities_fitness[class_name] = activities_fitness[class_name] +.2

        if len(facilitator_load[facilitator][time_slot]) > 1:
            activities_fitness[class_name] = activities_fitness[class_name] -.2


        for time in facilitator_load[facilitator]:
            penalty_flag = True
            if facilitator == 'Tyler':
                if len(schedule_by_facil[facilitator]) < 2:
                    penalty_flag = False

            if penalty_flag:
                if len(facilitator_load[facilitator][time]) in [2,3]:
                    activities_fitness[class_name] = activities_fitness[class_name] -.2

                if len(facilitator_load[facilitator][time]) > 4:
                    activities_fitness[class_name] = activities_fitness[class_name] -.5


        #Check if SLA 100 is first in the consecutive time slots
        for time_slot in range(10, 15):  
            for activity_100 in ['SLA100A', 'SLA100B']:
                if activity_100 in schedule_by_time[time_slot]:
                    for activity_191 in ['SLA191A', 'SLA191B']:
                        if activity_191 in schedule_by_time[time_slot + 1]:
                            building_100 = schedule[activity_100]['room'].split()[0]
                            building_191 = schedule[activity_191]['room'].split()[0]
                            activities_fitness[class_name] = activities_fitness[class_name] + .5
                            if  not (building_191 in ['Roman', 'Beach']) and (building_100 in ['Roman', 'Beach']):
                                activities_fitness[class_name] = activities_fitness[class_name] - .4

        #Check if SLA 191 is first in the consecutive time slots    
        for time_slot in range(10, 15):  
            for activity_191 in ['SLA191A', 'SLA191B']:
                if activity_191 in schedule_by_time[time_slot]:
                    for activity_100 in ['SLA100A', 'SLA100B']:
                        if activity_100 in schedule_by_time[time_slot + 1]:
                            building_191 = schedule[activity_191]['room'].split()[0]
                            building_100 = schedule[activity_100]['room'].split()[0]
                            activities_fitness[class_name] = activities_fitness[class_name] + .5
                            if  not (building_191 in ['Roman', 'Beach']) and (building_100 in ['Roman', 'Beach']):
                                activities_fitness[class_name] = activities_fitness[class_name] - .4
                                
        #Check for SLA100 before SLA191 seperated by an hour
        for time_slot in range(10, 14):  
            for activity_100 in ['SLA100A', 'SLA100B']:
                if activity_100 in schedule_by_time[time_slot]:
                    for activity_191 in ['SLA191A', 'SLA191B']:
                        if activity_191 in schedule_by_time[time_slot + 2]:  
                            activities_fitness[class_name] = activities_fitness[class_name] + 0.25
                        elif activity_191 in schedule_by_time[time_slot]:  
                            activities_fitness[class_name] = activities_fitness[class_name] - 0.25

        #Check for SLA191 before SLA100 seperated by an hour
        for time_slot in range(10, 14):  
            for activity_191 in ['SLA191A', 'SLA191B']:
                if activity_191 in schedule_by_time[time_slot]:
                    for activity_100 in ['SLA100A', 'SLA100B']:
                        if activity_100 in schedule_by_time[time_slot + 2]:  
                            activities_fitness[class_name] = activities_fitness[class_name] + 0.25
                        elif activity_100 in schedule_by_time[time_slot]: 
                            activities_fitness[class_name] = activities_fitness[class_name] - 0.25
        

        for compare_class_name in schedule:
            if class_name == compare_class_name:
                continue 

            compare_class_details = schedule[compare_class_name]
            compare_room = compare_class_details['room']
            compare_time_slot = compare_class_details['time_slot']
            compare_facilitator = class_details['facilitator']

            if time_slot == compare_time_slot:
                activities_fitness[class_name] = activities_fitness[class_name] - .5

    return activities_fitness    

#Select / Order the best resulting population
def selection(population):
    ranked_schedules = []
    for schedule in population:
        fitness_dict = calculate_fitness(schedule)
        scores = fitness_dict.values()
        ranked_schedules.append([sum(scores), schedule])
        
    ranked_schedules = sorted(ranked_schedules, key=lambda x: x[0], reverse=True)
    
    best_solutions = (ranked_schedules[:len(population)])

    return best_solutions

def crossover(parents):
    #Create offspring by combining genes of parents
    new_gen = []
    for i in range(0, len(parents)-1,2):
        parent1 = parents[i][1]
        parent2 = parents[i+1][1]
        
        crossover_point = random.choice(list(parent1.keys()))
        
        offspring = {}

        #Copy information from parent 1 before the crossover point
        crossed_flag = False
        for key in parent1:
            if key == crossover_point:
                break
            offspring[key] = parent1[key]

        #Copy information from parent 2 after the crossover point
        for key in parent2:
            if key == crossover_point:
                crossed_flag = True
                offspring[key] = parent2[key]
            if crossed_flag:
                offspring[key] = parent2[key]
        
        new_gen.append(offspring)

    for i in range(len(parents) - len(new_gen)):
        new_gen.append(parents[i][1])

    return new_gen


#Randomly mutate a schedule based on mutation_rate
def mutation(offspring,mutation_rate):
    results = []
    for schedule in offspring:
        if random.random() < mutation_rate:
            mutated_schedule = generate_random_schedule()
            results.append(mutated_schedule)
        else:
            results.append(schedule)

    return results

def genetic_algorithm(population_size, generations, mutation_rate):
    population = [generate_random_schedule() for _ in range(population_size)]

    for generation in range(generations):
        #Selection based on fitness scores
        selected_parents = selection(population)

        #Crossover to create offspring
        offspring = crossover(selected_parents)
        
        #Apply mutation to the offspring
        mutated_offspring = mutation(offspring,mutation_rate)
        
        #Replace the old population with the new offspring
        population = mutated_offspring

    #Get the best schedule from the final resulting population
    ranked_schedules = []
    for schedule in population:
        fitness_dict = calculate_fitness(schedule)
        scores = fitness_dict.values()
        ranked_schedules.append([sum(scores), schedule])

    ranked_schedules = sorted(ranked_schedules, key=lambda x: x[0], reverse=True)

    best_result = ranked_schedules[0]
    

    return best_result

#Change these to tweak simulation and genetic settings
population_size = 500
mutation_rate = 0.01
generations = 100
num_simulations = 5

results = []
for i in range(num_simulations):
    simulation = genetic_algorithm(population_size,generations,mutation_rate)
    results.append(simulation)

ranked_results = sorted(results, key=lambda x: x[0], reverse=True)
print('Genetic algorithm ran ' + str(num_simulations) + ' times, here are the results ordered')
for pair in ranked_results:
    print(pair[0])
print('')

best_overall_result = ranked_results[0]
#Uncomment this to print best schedule to console
#print('The best overall schedule with a score of ' + str(best_overall_result[0]))
#print(best_overall_result)

file_name = 'results.txt'
with open(file_name, 'w') as file:
    for item in best_overall_result:
        file.write(str(item) + '\n')  
print("Best schedule has been written to", file_name)
