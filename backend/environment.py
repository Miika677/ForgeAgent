import random

class ForgeEnvironment:
    
    def __init__(self):

        self.finish = False
        self.finish_msg = "unknown"

        self.progress = 0
        self.progress_goal = 120

        self.fail_count = 0
        self.fail_count_max = 5

        self.heat = 75
        self.heat_max = 150

        self.action_list = ["hammer", "grind", "polish", "hammer",] 
        random.shuffle(self.action_list)
        self.current_action = 0
        self.desired_action = self.action_list[self.current_action]

      
    def initial_state(self):
        return{
            "progressMax" : self.progress_goal,
            "failCountMax" : self.fail_count_max,
            "heatMax" : self.heat_max
        }

    #Get current game sessions stats
    def get_state(self):
        return{
            "progress" : self.progress,
            "heat" : self.heat,
            "failCount" : self.fail_count,
            "desiredAction" : self.desired_action
        }
    
    #Reset game to defaults
    def reset_state(self):
        self.progress = 0
        self.heat = 75
        self.fail_count = 0
        
        random.shuffle(self.action_list)
        self.check_desired_action()



    #Initial method: run the action method with a matching name, with which speed modifier and how many times
    def choose_action(self, action_name : str, speed_modifier : int, repeats : int):
        #Get method by its name
        chosen_action = getattr(self, action_name)
        #Run it with chosen speed and repeats
        chosen_action(speed_modifier, repeats)

        #Set desired action to the one that matches the amount of progress
        self.check_desired_action()

    #This is its own function so it can be checked during repeated actions
    #Change desired action every 30 progress
    def check_desired_action(self):
        self.current_action = min(self.progress // 30, len(self.action_list) - 1)
        self.desired_action = self.action_list[self.current_action]


    #Blade-working actions
    def hammer(self, speed_modifier : int, repeats : int):
        for i in range(repeats):
            if self.desired_action == "hammer" and 100 <= self.heat <= 140:
                self.successful__action(speed_modifier, -random.randint(1, 5))
            else:
                self.action_fail()

    def grind(self, speed_modifier : int, repeats : int):
        for i in range(repeats):
            if self.desired_action == "grind" and 50 <= self.heat <= 100:
                self.successful__action(speed_modifier, random.randint(1, 5))
            else:
                self.action_fail()

    def polish(self, speed_modifier : int, repeats : int):
        for i in range(repeats):
            if self.desired_action == "polish" and 10 <= self.heat <= 50:
                self.successful__action(speed_modifier, -random.randint(1, 5))
            else:
                self.action_fail()


    #Temperature regulating actions
    def quench(self, speed_modifier : int, repeats : int):
        for i in range(repeats):
            self.reduce_heat(5 * speed_modifier)

    def lava_dunk(self, speed_modifier : int, repeats : int):
        for i in range(repeats):
            self.add_heat(5 * speed_modifier)

            
    #Action results
    def successful__action(self, speed_modifier: int, heat_change: int):
        self.add_progress(speed_modifier)
        if heat_change > 0:
            self.add_heat(heat_change)
        else:
            self.reduce_heat(abs(heat_change))
        self.check_desired_action()

        if self.progress >= self.progress_goal:
            return self.end_game("victory")
        
    def end_game(self, result : str):
        self.finish = True
        self.finish_msg = result
        return result
    
    def add_progress(self, speed):
        self.progress += random.randint(3,5) * speed
        if self.progress >= 150:
            self.end_game("victory")

    def action_fail(self):
        self.fail_count += 1
        if self.fail_count >= self.fail_count_max:
            self.end_game("failure")

    def add_heat(self, amount : int):
        self.heat += amount
        if self.heat > 150:
            self.heat = 150

    def reduce_heat(self, amount : int):
        self.heat -= amount
        if self.heat < 0:
            self.heat = 0



