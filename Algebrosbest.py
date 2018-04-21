import pygame
from random import randint
import try2

def make_font(fonts, size):
    available = pygame.font.get_fonts()
    # get_fonts() returns a list of lowercase spaceless font names
    choices = map(lambda x:x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)

_cached_fonts = {}
def get_font(font_preferences, size):
    global _cached_fonts
    key = str(font_preferences) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font == None:
        font = make_font(font_preferences, size)
        _cached_fonts[key] = font
    return font

_cached_text = {}
def create_text(text, fonts, size, color):
    global _cached_text
    key = '|'.join(map(str, (fonts, size, color, text)))
    image = _cached_text.get(key, None)
    if image == None:
        font = get_font(fonts, size)
        image = font.render(text, True, color)
        _cached_text[key] = image
    return image

pygame.init()
FONT = pygame.font.Font(None, 32)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((640, 480))
done = False
is_blue = True
color = (0, 128, 255)
color2 = (255, 255, 255)
color3 = (0,0,0)
COLOR_INACTIVE = color3
COLOR_ACTIVE = color2
x = 200
y = 270
button = pygame.Rect(x, y, 200, 60)
backbutton = pygame.Rect(20, 520, 80, 60)
answerbox = pygame.Rect(200,300, 100, 60)
font_preferences = [
        "CASTELLAR"]
font_preferences1 = [
        "SHOWCARD GOTHIC"]

text = create_text("Start", font_preferences, 40, (0, 0, 0))
text1 = create_text("ALGEBROS", font_preferences1, 72, (255, 0, 0))
text2 = create_text("Easy", font_preferences1, 40, (255, 0, 0))
text3 = create_text("Medium", font_preferences1, 40, (255, 0, 0))
text4 = create_text("Hard", font_preferences1, 40, (255, 0, 0))
text5 = create_text("Difficulty", font_preferences1, 72, (255, 0, 0))
text6 = create_text("What is the solution?", font_preferences1, 50, (255, 255, 255))

# add = pygame.image.load("addtionsign.png")
# subtract = pygame.image.load("subtractsign.png")
# div = pygame.image.load("divisionsign.png")
# multi = pygame.image.load("multisign.png")
# back =  pygame.image.load("back.png")
# equal =  pygame.image.load("equal.png")

class InputBox():

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

class SceneBase:
    def __init__(self):
        self.next = self

    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)

def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()

        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
                # if event.key == pygame.K_SPACE:
                #     EasyScene()

            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)

        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(fps)

# The rest is code where you implement your game using the Scenes model

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        for event in events:

                if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = event.pos

                            if button.collidepoint(mouse_pos):
                                self.SwitchToScene(difficultyScene())

    def Update(self):
        pass

    def Render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((0, 128, 255))
        color = (0, 0, 0)
        pygame.draw.rect(screen, color, pygame.Rect(x+3, y+3, 200, 60))
        color = (0, 255, 255)
        pygame.draw.rect(screen, color, pygame.Rect(x, y, 200, 60))
        screen.blit(text,(239, 273))
        screen.blit(text1,(122, 35))
        # screen.blit(add,(x-100,y+90))
        # screen.blit(subtract,(x+250,y-100))
        # screen.blit(multi,(x-80,y-100))
        # screen.blit(div,(x+250,y+100))
        pygame.display.flip()
        clock.tick(60)

class difficultyScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        for event in events:

                if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = event.pos

                            if backbutton.collidepoint(mouse_pos):
                                self.SwitchToScene(TitleScene())
                            if button.collidepoint(mouse_pos):
                                self.SwitchToScene(EasyScene())

    def Update(self):
        pass

    def Render(self, screen):
        # The game scene is just a blank blue screen
        screen.fill((0, 128, 255))
        color = (0, 0, 0)
        pygame.draw.rect(screen, color, pygame.Rect(x+3, y+3, 200, 60))
        pygame.draw.rect(screen, color, pygame.Rect(x+3, y-97, 200, 60))
        pygame.draw.rect(screen, color, pygame.Rect(x+3, y+103, 200, 60))
        color = (0, 255, 255)
        pygame.draw.rect(screen, color, pygame.Rect(x, y, 200, 60))
        pygame.draw.rect(screen, color, pygame.Rect(x, y-100, 200, 60))
        pygame.draw.rect(screen, color, pygame.Rect(x, y+100, 200, 60))
        screen.blit(text2,(226, 178))
        screen.blit(text3,(226, 278))
        screen.blit(text4,(226, 378))
        screen.blit(text5,(122, 35))
        # screen.blit(back,(20,520))
        pygame.display.flip()
        clock.tick(60)


class EasyScene(SceneBase):

    def __init__(self):
        SceneBase.__init__(self)

    def ProcessInput(self, events, pressed_keys):
        
        for event in events:

                if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = event.pos

                            if backbutton.collidepoint(mouse_pos):
                                self.SwitchToScene(TitleScene())
                            if button.collidepoint(mouse_pos):
                                self.SwitchToScene(TitleScene())

    def Update(self):
        pass

    def Render(self, screen):

        clock = pygame.time.Clock()
        input_box1 = InputBox(100, 300, 140, 32)
        input_boxes = [input_box1]
        done = False
        num = (randint(0, 10))
        num1 = (randint(0, 10))

        while not done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                for box in input_boxes:
                    box.handle_event(event)

            for box in input_boxes:
                box.update()

            screen.fill((color))
            for box in input_boxes:
                box.draw(screen)
                pygame.draw.rect(screen, color2, pygame.Rect(100,200, 100, 60))
                pygame.draw.rect(screen, color2, pygame.Rect(300, 200, 100, 60))
                screen.blit(create_text("  " + str(num) + "     +   " + str(num1) + "     =", font_preferences, 50, (0, 0, 0)),(100, 200))


            pygame.display.flip()
            clock.tick(30)


    # def main():
    #     clock = pygame.time.Clock()
    #     input_box1 = InputBox(100, 300, 140, 32)
    #     input_boxes = [input_box1]
    #     done = False
    #     num = (randint(0, 10))
    #     num1 = (randint(0, 10))

    #     while not done:

    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 done = True
    #             for box in input_boxes:
    #                 box.handle_event(event)

    #         for box in input_boxes:
    #             box.update()

    #         screen.fill((color))
    #         for box in input_boxes:
    #             box.draw(screen)
    #             pygame.draw.rect(screen, color2, pygame.Rect(100,200, 100, 60))
    #             pygame.draw.rect(screen, color2, pygame.Rect(300, 200, 100, 60))
    #             screen.blit(create_text("  " + str(num) + "     +   " + str(num1) + "     =", font_preferences, 50, (0, 0, 0)),(100, 200))


    #         pygame.display.flip()
    #         clock.tick(30)


    # if __name__ == '__main__':
        # main()
        # pygame.quit()


        #guess = input()
        #if guess == answer:
        #pygame.draw.rect(screen, color, pygame.Rect(300, 500, 100, 60))
        #pygame.display.flip()
        #clock.tick(1)



run_game(400, 300, 60, TitleScene())
