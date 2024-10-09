import time
from enum import Enum


class LightState(Enum):
    RED = "Красный"
    GREEN = "Зеленый"


class TrafficLight:
    def __init__(self):
        self.state = LightState.RED
        self.button_pressed = False
        self.green_duration = 30
        self.red_duration = 90
        self.time_left = self.red_duration

    def display_state(self):
        print(f"Текущий сигнал: {self.state.value.upper()}")
        if self.button_pressed and self.state == LightState.RED or self.state != LightState.RED:
            print(f"Оставшееся время: {self.time_left} сек.")
        if self.state == LightState.RED:
            print("Нажмите Enter, чтобы нажать кнопку. Нажмите 'q' и Enter для выхода.")
        if self.button_pressed:
            print("Кнопка нажата. Ожидайте зеленый сигнал.")

    def change_state(self):
        if self.state == LightState.RED:
            self.state = LightState.GREEN
            self.time_left = self.green_duration
        elif self.state == LightState.GREEN:
            self.state = LightState.RED
            self.time_left = self.red_duration
        self.button_pressed = False

    def press_button(self):
        if self.state == LightState.RED:
            self.button_pressed = True

    def run(self):
        while True:
            self.display_state()
            if self.state == LightState.RED:
                if self.time_left > 0:
                    user_input = input()
                    if user_input.lower() == 'q':
                        print("Выход из программы.")
                        return
                    elif user_input == "":
                        self.press_button()
                self.time_left -= 1
            else:
                time.sleep(1)
                self.time_left -= 1
            if self.time_left <= 0:
                self.change_state()


if __name__ == "__main__":
    traffic_light = TrafficLight()
    traffic_light.run()
