from pico2d import load_image, get_time
from sdl2 import SDL_SetTextureColorMod

from state_machine import *

class Idle:
   @staticmethod
   def enter(boy, event):
       if start(event):
           boy.action = 3
           boy.dir = 1
       elif right_down(event) or left_up(event):
           boy.action = 2
           boy.dir = -1
       elif left_down(event) or right_up(event):
           boy.action = 3
           boy.dir = 1
       elif time_out(event):
           if boy.dir == 1:
               boy.action = 3
           elif boy.dir == -1:
               boy.action = 2

       boy.start_time = get_time()
       pass

   @staticmethod
   def exit(boy, event):
       pass

   @staticmethod
   def do(boy):
       boy.frame = (boy.frame + 1) % 8

       # sleep 상태 비활성화 해둠
       # if get_time() - boy.start_time > 1:
       #     boy.state_machine.add_event(('TIME_OUT', 0))
       pass

   @staticmethod
   def draw(boy):
       boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
       pass



class Sleep:
   @staticmethod
   def enter(boy, event):
       boy.start_time = get_time()
       pass

   @staticmethod
   def exit(boy, event):
       pass

   @staticmethod
   def do(boy):
       boy.frame = (boy.frame + 1) % 8
       pass

   @staticmethod
   def draw(boy):
       if boy.dir == 1:
           boy.image.clip_composite_draw(
               boy.frame * 100, boy.action * 100, 100, 100,
               3.141592 / 2,
               '',
               boy.x, boy.y - 30, 100, 100
           )
       elif boy.dir == -1:
           boy.image.clip_composite_draw(
               boy.frame * 100, boy.action * 100, 100, 100,
               -3.141592 / 2,
               '',
               boy.x, boy.y - 30, 100, 100
           )

class AutoRun:
    @staticmethod
    def enter(boy, event):
        boy.start_time = get_time()
        if boy.dir == 1: boy.action = 1
        elif boy.dir == -1: boy.action = 0
        pass

    @staticmethod
    def exit(boy, event):
        boy.image.opacify(1.0)
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 10
        if boy.x < 0 or boy.x > 800:
            boy.dir *= -1
            boy.x = max(0, min(boy.x, 800))

            if boy.dir == 1:
                boy.action = 1
            else:
                boy.action = 0

        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(boy):
        boy.image.opacify(boy.frame / 10)
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass

class Run:
    @staticmethod
    def enter(boy, event):
        if right_down(event) or left_up(event): # 오른쪽으로 RUN
            boy.dir, boy.action = 1, 1
        elif left_down(event) or right_up(event): # 왼쪽으로 RUN
            boy.dir, boy.action = -1, 0
    @staticmethod
    def exit(boy, event):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5
        if boy.x < 0 or boy.x > 800:
            boy.x = max(0, min(boy.x, 800))
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)





class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Sleep:  {space_down: Idle, right_down: Run, left_down: Run, right_up: Run, left_up: Run},
                Idle:   {time_out: Sleep, right_down: Run, left_down: Run, right_up: Run, left_up: Run,
                         a_down: AutoRun},
                Run:    {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                AutoRun: {right_down: Run, left_down: Run, right_up: Run, left_up: Run,
                          time_out: Idle}

            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT', event)
        )
        pass

    def draw(self):
        self.state_machine.draw()
