import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Newtonian Gravity Simulator")

#describing the global constants

Planet_Mass = 100
Obj_Mass = 1
G = 6
Planet_radi = 7.5 * 2.5
Obj_radi = 7.5
Vel_scale = 100

FPS = 60

Bg =pygame.transform.scale(pygame.image.load("img/background.jpg"),(WIDTH, HEIGHT))
Planet_img = pygame.transform.scale(pygame.image.load("img/jupiter.png"),(Planet_radi*2, Planet_radi*2))

button = pygame.image.load("buttons/button.png").convert_alpha()

White = (255,255,255)
Red = (255,0,0)
Blue = (0,0,255)
Green = (0,255,0)

class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        


    def draw(self):
        win.blit(self.image,self.rect.topleft)
        

    def if_clicked(self, pos):
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
        if not self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = False

        return self.clicked

    



class spacecraft:
    def __init__(self,x_pos,y_pos,x_vel,y_vel,Obj_Mass):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.mass = Obj_Mass

        self.path = []

    
    def draw(self):
        pygame.draw.circle(win, Red, (int(self.x_pos),int(self.y_pos)), Obj_radi)
        self.path.append((self.x_pos,self.y_pos))

        for i in range(len(self.path) - 1):
            pygame.draw.line(win, Blue, self.path[i], self.path[i + 1], 1)

    def move(self,planet=None,other_objects=None):

        distance = math.sqrt((self.x_pos - planet.x)**2 + (self.y_pos - planet.y)**2)
        force = (G* self.mass * planet.mass)/distance**2
        acceleration = force/self.mass
        angle = math.atan2((planet.y - self.y_pos),(planet.x - self.x_pos))

        x_acc = acceleration*math.cos(angle)
        y_acc = acceleration*math.sin(angle)

        self.x_vel += x_acc
        self.y_vel += y_acc

        for other_obj in other_objects:
            if other_obj != self:
                distance_obj = math.sqrt((self.x_pos - other_obj.x_pos) ** 2 + (self.y_pos - other_obj.y_pos) ** 2)
                force_obj = (G * self.mass * other_obj.mass) / distance_obj ** 2
                acceleration_obj = force_obj / self.mass
                angle_obj = math.atan2((other_obj.y_pos - self.y_pos), (other_obj.x_pos - self.x_pos))
                x_acc_obj = acceleration_obj * math.cos(angle_obj)
                y_acc_obj = acceleration_obj * math.sin(angle_obj)

                # Update velocities
                self.x_vel += x_acc + x_acc_obj
                self.y_vel += y_acc + y_acc_obj



        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

class PLANET:
    def __init__(self,x,y,x_vel,y_vel, mass):
        self.x = x
        self.y = y 
        self.mass = mass
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.path = []
    
    def move(self,other_objects=None):
        for other_obj in other_objects:
            if other_obj != self:
                distance_obj = math.sqrt((self.x - other_obj.x_pos) ** 2 + (self.y - other_obj.y_pos) ** 2)
                force_obj = (G * self.mass * other_obj.mass) / distance_obj ** 2
                acceleration_obj = force_obj / self.mass
                angle_obj = math.atan2((other_obj.y_pos - self.y), (other_obj.x_pos - self.x))
                x_acc_obj = acceleration_obj * math.cos(angle_obj)
                y_acc_obj = acceleration_obj * math.sin(angle_obj)

                # Update velocities
                self.x_vel +=  x_acc_obj
                self.y_vel +=  y_acc_obj

        self.x += self.x_vel
        self.y += self.y_vel


    def draw(self):
        #win.blit(Planet_img,(self.x - Planet_radi, self.y - Planet_radi))
        pygame.draw.circle(win, Green, (int(self.x - Planet_radi),int(self.y - Planet_radi)), Planet_radi)
        self.path.append((self.x,self.y))
        for i in range(len(self.path) - 1):
            pygame.draw.line(win, Blue, self.path[i], self.path[i + 1], 1)

def space_ship(location, mouse):
    x_loc, y_loc = location
    x_mos, y_mos = mouse

    x_vel = (x_mos - x_loc) / Vel_scale
    y_vel = (y_mos - y_loc) / Vel_scale

    obj = spacecraft(x_loc,y_loc,x_vel,y_vel,Obj_Mass)
    return obj

text_font = pygame.font.SysFont("Arial",30)

def render_text(text, font, col, x,y):
    img = font.render(text, True, col)
    win.blit(img,(x,y))





def main():
    text = "Press 'Space_Bar' to reset and Press 'ESC' to exit"
    running = True
    clock = pygame.time.Clock()
    objects = []
    temp_mos_pos = None
    planet = PLANET(WIDTH//2,HEIGHT//2,0,0,Planet_Mass)

    info_button = Button(10,20,button, 0.125)

    while running:
        clock.tick(FPS)

        

        #get the current mouse positions while running
        #returns a touple
        mos_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                # Reset everything here (e.g., clear objects, reset positions, etc.)
                    objects = []  # Clear the list of objects
                    planet = PLANET(WIDTH // 2, HEIGHT // 2, 0, 0, Planet_Mass)

            
            
            if event.type == pygame.MOUSEBUTTONDOWN and info_button.if_clicked(mos_pos) == False:
                

                #check if any mouse position has been already recorded
                if temp_mos_pos:
                    obj = space_ship(temp_mos_pos,mos_pos)
                    objects.append(obj)
                    temp_mos_pos = None

                #if not recorded already, record mouse position 
                else:
                    temp_mos_pos = mos_pos

            

        win.blit(Bg, (0,0))
        info_button.draw()
        if info_button.if_clicked(mos_pos) == True:
            render_text(text, text_font, Green, 70, 400)


        if temp_mos_pos:
            pygame.draw.line(win, White, temp_mos_pos, mos_pos, 2)
            pygame.draw.circle(win, Red, temp_mos_pos, Obj_radi)
            
        for objs in objects[:]:
            objs.draw()
            objs.move(planet,objects)
            planet.move(objects)
            off_screen = objs.x_pos < -500 or objs.x_pos > WIDTH + 500 or objs.y_pos < -800 or objs.y_pos > HEIGHT +800
            colided = math.sqrt((objs.x_pos - planet.x)**2 + (objs.y_pos - planet.y)**2) <= Planet_radi
            if off_screen or colided:
                objects.remove(objs)

        planet.draw()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
