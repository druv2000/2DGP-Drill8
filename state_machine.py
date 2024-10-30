# event ( 이벤트 종류, 실제 값 )
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a


def start(event):
    return event[0] == 'START'

def space_down(event):
    return (event[0] == 'INPUT' and
            event[1].type == SDL_KEYDOWN and
            event[1].key == SDLK_SPACE)

def time_out(event):
    return event[0] == 'TIME_OUT'

def right_down(event):
    return (event[0] == 'INPUT' and
            event[1].type == SDL_KEYDOWN and
            event[1].key == SDLK_RIGHT)

def right_up(event):
    return (event[0] == 'INPUT' and
            event[1].type == SDL_KEYUP and
            event[1].key == SDLK_RIGHT)

def left_down(event):
    return (event[0] == 'INPUT' and
            event[1].type == SDL_KEYDOWN and
            event[1].key == SDLK_LEFT)

def left_up(event):
    return (event[0] == 'INPUT' and
            event[1].type == SDL_KEYUP and
            event[1].key == SDLK_LEFT)

def a_down(event):
    return(event[0] == 'INPUT' and
           event[1].type == SDL_KEYDOWN and
           event[1].key == SDLK_a)

















# 상태 머신을 처리해주는 클래스
class StateMachine:
    def __init__(self, obj):
        self.obj = obj
        self.event_que = [] # 발생하는 이벤트(큐)
        pass

    def update(self):
        self.cur_state.do(self.obj)
        if self.event_que: # 리스트에 요소가 있으면
            event = self.event_que.pop(0) # 리스트의 첫 번째 요소를 꺼냄
            self.handle_event(event)


    def start(self, start_state):
        # 현재 상태를 시작 상태로 변경
        self.cur_state = start_state
        self.cur_state.enter(self.obj, ('START', 0))
        print(f'ENTER into {self.cur_state}')
        pass

    def draw(self):
        self.cur_state.draw(self.obj)
        pass

    def set_transitions(self, transitions):
        self.transitions = transitions
        pass

    def add_event(self, event):
        self.event_que.append(event) # 상태 머신용 이벤트 추가
        print(f'    DEBUG: new event {event} is added.')
        pass

    def handle_event(self, event):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(event):
                self.cur_state.exit(self.obj, event)
                print(f'EXIT from {self.cur_state}')
                self.cur_state = next_state
                self.cur_state.enter(self.obj, event)
                print(f'ENTER into {next_state}')
                return