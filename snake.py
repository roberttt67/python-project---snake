#cel mai nou/ bun cod: culori sarpe + top 3 score
# imports of different modules
import pygame
import sys
import random
import time

'''
# Here first we will check if the pygame successfully Initialized
check_errors = pygame.init()

if check_errors[1] > 0:
    print("(!) had {0} initializing errors, exiting....".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(!) PyGame Initialized Successfully!!!")
'''

pygame.init()
# Play Surface
window_width = 720
window_length = 460
playSurface = pygame.display.set_mode((window_width, window_length)) # To set the console window where game will run, the set_mode expects a tupple having dimensions of the console
pygame.display.set_caption('!!! SNAKE GAME !!!') # To set the Upper heading of the game console window


#Colors
# The color method expects three parameters r,g,b combination to give the color
red = pygame.Color(255, 0 ,0) #red color-gameover
snake_color = pygame.Color(0, 255, 0) #green-snake
white = pygame.Color(255, 255, 255) #white-score
black = pygame.Color(0, 0, 0) #black-screen
dark_red = pygame.Color(128, 0, 0) #food color
brown = pygame.Color(165, 42, 42) #brown-food

# fps controller
fpsController = pygame.time.Clock()

# important varibles for the gameover
snakePos = [100, 50] #initial coordinate of the snake head
snakeBody = [[100, 50], [90, 50], [80, 50]] #snake snakeBody

    # Set a random start point.
#startx = random.randint(5, window_width - 6)
#starty = random.randint(5, window_length - 6)
#snakePos = [startx, starty]
#snakeBody =  [[startx, starty], [startx - 1, starty], [startx - 2, starty]]

foodPos = [random.randrange(1, (window_width//10)) * 10, 
           random.randrange(1,(window_length//10)) * 10] #random food positioning

foodSpawn = True
direction = 'RIGHT'
changeTo = direction
score = 0
snake_speed = 10
initscore = 0

# Game Over function
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72) #choose font name and size
    GOsurf = myFont.render(' GAME OVER !!!', True, red) # this is the surface where game over will display having 3 args : the message, antialiasing,and Color
    GOrect = GOsurf.get_rect() #to get rect coordinates of the game over text surface
    GOrect.midtop = (350, 15)
    playSurface.blit(GOsurf, GOrect) # bind the gameover text to the main surface
    showScore(0)
    pygame.display.flip() # to set the fps
    time.sleep(2)
    pygame.quit() # exit game window
    sys.exit() # exit cmd console

def showScore(choice=1):
    sFont = pygame.font.SysFont('monaco', 42) #choose font name and size
    Ssurf = sFont.render('SCORE : {0}'.format(score), True, white) # this is the surface where game over will display having 3 args : the message, antialiasing,and Color
    Srect = Ssurf.get_rect() #to get rect coordinates of the game over text surface
    if choice == 1:
        Srect.midtop = (80, 10)
    else:
        Srect.midtop = (360, 120)

    playSurface.blit(Ssurf, Srect) # bind the gameover text to the main surface
    pygame.display.flip() # to set the fps

#The "update_score" function appends the new score to the list, sorts it in descending order, keeps only the top 3 scores, and then writes them back to the file.
def update_score(nscore):
    scores = get_scores()
    # Add the new score to the list
    scores.append(nscore)
    # Sort the scores in descending order
    scores.sort(reverse=True)
    # Keep only the top 3 scores
    scores = scores[:3]

    with open('highest_score.txt', 'w') as f:
        for score in scores:
            f.write(str(score) + '\n')

#"get_scores" function reads all scores from the file and returns them as a list
def get_scores():
    with open('highest_score.txt', 'r') as f:
        lines = f.readlines()
        scores = [int(line.strip()) for line in lines]
    return scores

#The "display_scores" function prints the top 3 highest scores.
def display_scores():
    scores = get_scores()
    print("Top 3 Highest Scores:")
    for i, score in enumerate(scores[:3], 1):
        print(f"{i}. {score}")


# Main Logic Of The GAME
while True:
    for event in pygame.event.get(): # accepts the event
        if event.type == pygame.QUIT: # quit event
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN: # when keyboard key is pressed
            if event.key == pygame.K_RIGHT or event.key == ord('d'): # Right Move
                changeTo = 'RIGHT'
            if event.key == pygame.K_LEFT or event.key == ord('a'): # Left Move
                changeTo = 'LEFT'
            if event.key == pygame.K_UP or event.key == ord('w'): # Up Move
                changeTo = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'): # Down Move
                changeTo = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))  # post function first creates a event and inside it we emit a quit event

    # validation of direction
    if changeTo == 'LEFT' and not direction =='RIGHT':
        direction = 'LEFT'
    if changeTo == 'RIGHT' and not direction =='LEFT':
        direction = 'RIGHT'
    if changeTo == 'UP' and not direction =='DOWN':
        direction = 'UP'
    if changeTo == 'DOWN' and not direction =='UP':
        direction = 'DOWN'

    # Value change after direction change
    if direction == 'RIGHT':
        snakePos[0] += 10
    if direction == 'LEFT':
        snakePos[0] -= 10
    if direction == 'UP':
        snakePos[1] -= 10
    if direction == 'DOWN':
        snakePos[1] += 10

    # Snake Body Mechanism
    snakeBody.insert(0, list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 1
        foodSpawn = False

    #Change snake color to a random color when it picks up a point
        snake_color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    else:
        snakeBody.pop()
    # food spawn
    if foodSpawn == False:
        foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10]
    foodSpawn = True
    playSurface.fill(black)
    for pos in snakeBody:
        pygame.draw.rect(playSurface, snake_color, pygame.Rect(pos[0],pos[1],10,10))
    pygame.draw.rect(playSurface,dark_red,pygame.Rect(foodPos[0],foodPos[1],10,10))

    # Boundary Condition
    if snakePos[0] > 710 or snakePos[0] < 0:
        update_score(score)
        gameOver()
    if snakePos[1] > 450 or snakePos[1] < 0:
        update_score(score)
        gameOver()

    # Self Body Collision
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            update_score(score) 
            gameOver()

    showScore() # To show the score
    # FPS CONTROL
    pygame.display.update()
    #pygame.display.update()
    if score == initscore+3:
        snake_speed+=5
        initscore = score
    fpsController.tick(snake_speed)
