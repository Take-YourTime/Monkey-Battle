import pygame

from core.engine import GameEngine
from states.loading_page import LoadingState
from states.menu_page import MenuState
from states.game_page import GameState
from states.end_page import EndState

def main():
    # Waiting for the system getting ready.
    pygame.time.delay(500)

    # 實例化遊戲引擎
    engine = GameEngine()

    # 註冊所有狀態
    engine.state_machine.add_state("LOADING", LoadingState(engine))
    engine.state_machine.add_state("MENU", MenuState(engine))
    engine.state_machine.add_state("GAME", GameState(engine))
    engine.state_machine.add_state("END", EndState(engine))

    # 設定初始狀態
    engine.state_machine.change_state("LOADING")

    # 啟動主迴圈
    engine.run()

if __name__ == '__main__':    
    main()