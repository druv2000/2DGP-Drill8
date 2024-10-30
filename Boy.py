from pico2d import load_image, get_time

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
        pass

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(boy):
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
        pass
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
