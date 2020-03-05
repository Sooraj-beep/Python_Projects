import pygame, time
from pygame.locals import *
pygame.init()

lp_color = 'blue'
ball_color = 'white'
bg_color = 'black'
rp_color = 'red'


def main():
    screen = pygame.display.set_mode((750,750))
    pygame.display.set_caption("Ping-Pong")
    pygame.display.toggle_fullscreen
    clock = pygame.time.Clock()
    clock.tick(60)
    game = Game(screen)
    game.play()
    pygame.quit()


class Game:
    def __init__(self, screen):
        pygame.key.set_repeat(20,20)
        height = screen.get_height()//6
        width =  screen.get_height()//30
        radius = screen.get_height()//60
        self.screen = screen
        self.bg_color = pygame.Color(bg_color)
        self.pause_time = 0.03  # smaller values equates to a faster game
        self.close_clicked = False
        self.continue_game = True
        self.ball = Ball(ball_color, radius, [screen.get_width()//2, screen.get_height()//2], [-15,5], pygame.display.get_surface())
        self.left_paddle = Paddle(pygame.display.get_surface(),lp_color,[self.screen.get_width()//9,(self.screen.get_height()//2)-self.screen.get_width()//9],[width, height])
        self.right_paddle = Paddle(pygame.display.get_surface(),rp_color,[self.screen.get_width()-((self.screen.get_width()//9)+width),(self.screen.get_height()//2)-self.screen.get_width()//9],[width, height]) 


    def play(self):

        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.
    
        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_event()
            self.draw()   
            if self.continue_game:
                self.update()
                self.decide_continue()
            time.sleep(self.pause_time)

            
            
    def handle_event(self):
        # Handle each user event by changing the game state
        # appropriately.
        # - self is the Game whose events will be handled
            
        event = pygame.event.poll()
        key_list = []
        key_list = pygame.key.get_pressed()
        if event.type == QUIT:
            self.close_clicked = True
        if key_list[K_q] and self.continue_game:
            self.left_paddle.paddle_up()
        elif key_list[K_a] and self.continue_game:
            self.left_paddle.paddle_down()
        if key_list[K_p] and self.continue_game:
            self.right_paddle.paddle_up()
        elif key_list[K_l] and self.continue_game:
            self.right_paddle.paddle_down()        
        
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
                  
        self.screen.fill((0,0,0))        
        self.left_paddle.draw()
        self.right_paddle.draw()       
        self.ball.draw()
        pygame.display.flip()
   
            
    def update(self):
        # Update the game objects.
        # - self is the Game to update
        self.ball.move(self.left_paddle,self.right_paddle)

        #self.left_paddle.update_paddle()
        #self.right_paddle.update_paddle()
    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        pass
class Ball:
    # An object in this class represents a colored circle.
    def __init__(self, color, radius, center, velocity, surface):
        # Initialize a Cirlcle.
        # - self is the Circle to initialize
        # - center is a list containing the x and y int
        # coords of the center of the Circle
        # - radius is the int pixel radius of the Circle
        # - color is the pygame.Color of the Circle
        # - screen is the uagame screen object

        self.center = center
        self.radius = radius
        self.color = pygame.Color(color)
        self.surface = surface
        self.velocity = velocity
        
    def draw(self):
        # Draw the Circle.
        # - self is the Circle to draw            
        pygame.draw.circle(self.surface, self.color, self.center, self.radius)
   
    def move(self, left_paddle, right_paddle):
        # Change the location and the velocity of the Ball so it
        # remains on the surface by bouncing from its edges.
        # - self is the Ball
        size = self.surface.get_size()
        for coordinate in range(0, 2):
            self.center[coordinate] = (self.center[coordinate] + self.velocity[coordinate]) 
            if  self.center[coordinate]  <= self.radius or self.center[coordinate] + self.radius >= size[coordinate]:
                self.velocity[coordinate] = - self.velocity[coordinate]  
            if coordinate == 0:
                if left_paddle.collision_check_left_paddle(self.center, self.velocity, self.radius):
                    self.velocity[coordinate] = - self.velocity[coordinate]
                if right_paddle.collision_check_right_paddle(self.center, self.velocity, self.radius):
                    self.velocity[coordinate] = - self.velocity[coordinate]


class Ball:

    # An object in this class represents a colored circle.
    def __init__(self, color, radius, center, velocity, surface):
        # Initialize a Cirlcle.
        # - self is the Circle to initialize
        # - center is a list containing the x and y int
        # coords of the center of the Circle
        # - radius is the int pixel radius of the Circle
        # - color is the pygame.Color of the Circle
        # - screen is the uagame screen object

        self.center = center
        self.radius = radius
        self.color = pygame.Color(color)
        self.surface = surface
        self.velocity = velocity
        
    def draw(self):
        # Draw the Circle.
        # - self is the Circle to draw            
        pygame.draw.circle(self.surface, self.color, self.center, self.radius)
   
    def move(self, left_paddle, right_paddle):
        # Change the location and the velocity of the Ball so it
        # remains on the surface by bouncing from its edges.
        # - self is the Ball
        size = self.surface.get_size()
        for coordinate in range(0, 2):
            self.center[coordinate] = (self.center[coordinate] + self.velocity[coordinate]) 
            if  self.center[coordinate]  <= self.radius or self.center[coordinate] + self.radius >= size[coordinate]:
                self.velocity[coordinate] = - self.velocity[coordinate]  
            if coordinate == 0:
                if left_paddle.collision_check_left_paddle(self.center, self.velocity, self.radius):
                    self.velocity[coordinate] = - self.velocity[coordinate]
                if right_paddle.collision_check_right_paddle(self.center, self.velocity, self.radius):
                    self.velocity[coordinate] = - self.velocity[coordinate]

    
class Paddle:
    def __init__(self, surface, color, coordinates, dimensions):
       
        self.surface = surface
        self.color = pygame.Color(color)
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.width = dimensions[0]
        self.height = dimensions[1]

    def draw(self):
        #draws a rectangle with the current coordinates and dimensions
        pygame.draw.rect(self.surface,self.color,pygame.Rect((self.x, self.y), (self.width, self.height)))
    
    def collision_check_left_paddle(self, center, velocity, radius):
        # Checks collision for front of left paddle
        edge = center[0] - radius       
        if pygame.Rect((self.x, self.y), (self.width, self.height)).collidepoint(edge,center[1]) and velocity[0]<0:
            return True
    def collision_check_right_paddle(self, center, velocity, radius):
        edge = center[0] + radius 
        # Checks collision for front of left paddle
        if pygame.Rect((self.x, self.y), (self.width, self.height)).collidepoint(edge,center[1]) and velocity[0]>0:
            return True 
    def paddle_up(self):
        if self.y > 0:
            self.y -= 25
    def paddle_down(self):
        if self.y < self.surface.get_height() - self.height:
            self.y += 25    

main()
    

