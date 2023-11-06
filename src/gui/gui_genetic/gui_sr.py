##
#%%  



import pygame
import os
import sys

from gui.gui_genetic.utils.constants import WINDOW_HEIGHT, WINDOW_WIDTH, WHITE, BLACK, BLUE, RED, GREEN
from environment.utils.constants import X_SCALE, Y_SCALE
from maps.basic_map_1 import MAP

FRAMES_PER_SECOND = 1

fx = lambda x : int(WINDOW_WIDTH * x / X_SCALE)
fy = lambda y : WINDOW_HEIGHT - int(WINDOW_HEIGHT * y / Y_SCALE)


image_directory_path = "/home/smaug/Documents/CodingGames/MarsLander/image/"




class EnvRender:
    def __init__(self, map_=MAP, ):
        lands, initial_state = map_
        super().__init__(lands, initial_state)
        self.env_id = 0
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.Font(None, 36)
        

    def screen_reset(self):
        self.display.fill(BLACK)
        self.draw_surface()
        
    def reset(self):
        super().reset()
        self.trajectory = []

    def display_text(self, text, position):
        id_text = self.font.render(text, True, (255, 255, 255))
        self.display.blit(id_text, position)

    def render_reset(self, population_size = None, chromosome_size = None):        
        self.env_id +=1
        self.screen_reset()
        self.display_text(
            "Evolution number : " + str(self.env_id),
            (100, 100)
        )
    


    def draw_surface(self):
        for line in self.surface.lines():
            if not line.point_a in border_left and not line.point_b in border_right:
                pygame.draw.line(
                    self.display, 
                    RED, 
                    [fx(line.point_a.x), fy(line.point_a.y)],
                    [fx(line.point_b.x), fy(line.point_b.y)]
                )

    def step(self, action):
        done = super().step(action)
        self.trajectory.append([self.lander.x, self.lander.y])
        #pygame.transform.rotate(self.lander_image,self.rotate)
        
        if done :
            if self.successful_landing():
                self.env_id -=1
                self.render_reset()
                color = GREEN
                width_ = 5

            else:
                color = BLUE
                width_ = 1
            x_, y_ = self.trajectory[0]
            for x,y in self.trajectory[1:]:
                pygame.draw.line(
                    self.display, 
                    color, 
                    [fx(x_), fy(y_)],
                    [fx(x), fy(y)],
                    width=width_
                )
                x_, y_ = x, y

        return done
      

    
def print_console(comments):
    print(comments, file=sys.stderr)

def no_random_initial_chromosome(chromosome_size):
    falling_chromosome = Chromosome([Action(0,0)]*chromosome_size)

def power_repartition(chromosome):
    data = str(chromosome).split("|")
    powers = [int(action.split(" ")[1]) for action in data]
    graded_minus = powers.count(-1)/len(powers)
    graded_zeros = powers.count(0)/len(powers)
    graded_ones = powers.count(1)/len(powers)
    print_console(f"-1 : {graded_minus} | 0 : {graded_zeros} | 1 : {graded_ones}")

## START 
def start(
        lands,
        initial_state,
        population_size = 200,
        chromosome_size = 200,
        chromosome_type = Chromosome
        ):
    env = EnvRender(lands, initial_state)
    env.reset()
    env.render_reset(population_size, chromosome_size)

    population = Population(population_size, chromosome_size, chromosome_type)
    return env,population


## PLAY POPULATION


def play_population(
        verbose=True,
        **middlemen,
        ):
    
    def print_ending(chromosome : Chromosome):
        print_console("------SUCCESS------")
        print_console(f"Population {population.evolution_number}")
        print_console(env)
        power_repartition(chromosome)

    def print_avancement(chromosome):
        print_console(f"--------Score : {round(chromosome.score)} -----------")
        print_console(f"Speed : {round(env.lander.v_speed)} | {round(env.lander.h_speed)} ")
        print_console(f"Rotation {env.lander.rotate}")

    global env
    global population

    for number, chromosome in enumerate(population):
        env.reset()
        if chromosome.use(env):
            print_ending(chromosome)
            if middlemen["activate"]:
                population.final_chromosome.extend(
                    chromosome.actions
                )
                env.reset()
                population.final_chromosome.use(env)
            return True

    best_chromosome = population.evolution()
    
    if middlemen["activate"]:
    
        if population.evolution_number % middlemen["step"] == 0 and\
              (not population.evolution_number == 0):
            print_console(f"Choosing the best one")
            population.final_chromosome.extend(
                best_chromosome.actions[middlemen["offset"]:]
                )
            env.reset()
            best_chromosome.use(env, step = middlemen["offset"])
            env.initial_state = env.lander.get_state()
            population.right_shift(middlemen["offset"])
            
    if verbose: print_avancement(best_chromosome)

    return False
    
## PLAY PYGAME    
def play_pygame_turn(**kwargs):

    global new_population_by_refresh
    global success
    pygame.display.flip()
    pygame.event.wait()

    while True:
        event = pygame.event.wait()
        if success:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
               success = False
               break
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                new_population_by_refresh = int(input())
                break
            if event.key == pygame.K_RIGHT:
                break
                
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    env.render_reset()
    env.display_text(
        "Parameters : ",
        (400, 100)
    )
    env.display_text(
        f"Population size : {population.population_size}",
        (400, 130) 
    )
    env.display_text(
        f"chromosome size : " + str(population.chromosome_size),
        (400, 160)
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()


### MAIN ####

def main():
    global env
    global population
    global new_population_by_refresh
    global success
    env, population = start(
        *test_grotte_inv,
        population_size = 200,
        chromosome_size = 300,
        chromosome_type = ChromosomeAction
    )
    new_population_by_refresh = 1
    success = False
    middlemen_activate = False
    if middlemen_activate:
        population.final_chromosome = Chromosome()
            
    while True:
        for _ in range(new_population_by_refresh):
            if play_population(
                activate = middlemen_activate,
                step = 5,
                offset = 3
            ):
                success = True
                break
        play_pygame_turn()
        if success:
            return 

if __name__ == "__main__":
    main()


#%% 
    







# %%
