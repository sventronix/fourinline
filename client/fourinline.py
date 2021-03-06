import pyglet
from pyglet.window import key
from pyglet.window import mouse

import game_logic
import constants as const
from board import Board

from visuals.coin import Coin
from visuals.pointer import Pointer
from visuals.turn_indicator import TurnIndicator
from visuals.new_game_button import NewGameButton

# Init

window = pyglet.window.Window(const.WINDOW_WIDTH, const.WINDOW_HEIGHT, caption='Connect Four')

front = pyglet.graphics.OrderedGroup(2)
foreground = pyglet.graphics.OrderedGroup(1)
background = pyglet.graphics.OrderedGroup(0)

batch = pyglet.graphics.Batch()
board_sprite = pyglet.sprite.Sprite(img=pyglet.resource.image('assets/board.png'),
                                    x=0, y=40, group=foreground, batch=batch)
coins = []


board = Board()
pointer = Pointer(board.next_player())
turn_indicator = TurnIndicator(board.next_player())

new_game_button = NewGameButton()


@window.event
def on_draw():
    window.clear()
    board_sprite.draw()
    batch.draw()

    pointer.draw()
    turn_indicator.draw()
    new_game_button.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.LEFT:
        pointer.move_left()
    elif symbol == key.RIGHT:
        pointer.move_right()

    if symbol == key.ENTER or symbol == key.SPACE:
        current_player = board.next_player()
        place_coin(board.move(pointer.column), pointer.column, current_player)

        game = game_logic.check_game_over(board.get_board())
        if game:
            print(game)
            victory_marker(game)


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        if new_game_button.is_clicked(x, y):
            restart_game()


def place_coin(row, column, player):
    c = Coin(const.COIN_X_START + (column * const.COIN_OFFSET),
             const.COIN_Y_START + ((const.GAME_ROWS-row-1) * const.COIN_OFFSET),
             batch, player, background, (row, column))

    coins.append(c)
    pointer.set_color(board.next_player())
    turn_indicator.change_image(board.next_player())


def victory_marker(points):
    print('Points', points)
    c = [list(filter(lambda coin: coin.get_position() == p, coins))[0] for p in points[0]]
    for i in c:
        i.group = front
        i.set_victory()


def restart_game():
    coins.clear()
    pointer.reset_pointer()
    board.clear_board()


if __name__ == '__main__':
    pyglet.app.run()
