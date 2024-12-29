from enum import Enum
from random import randint

WIDTH = 4
values = [2 ** i for i in range(1, 12)]  # [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]


class Exceptions:
    class UniqueBlockIdError(Exception):
        pass

    class OccupiedBlockPosition(Exception):
        pass

    class BoardIsFull(Exception):
        pass


def first(items: list, condition):
    for i in items:
        if condition(i):
            return i


class Position:

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y


class Block:

    def __init__(self, block_id: int, value: int):
        self.block_id = block_id
        self.value = value

    def __eq__(self, other) -> bool:
        if isinstance(other, Block):
            return self.block_id == other.block_id

    def __str__(self):
        return str(values[self.value])


class Set:

    def __init__(self, position: Position, block: Block):
        self.position = position
        self.block = block


class Board:
    index = -1

    def __init__(self):
        self.board = [[None for _ in range(WIDTH)] for _ in range(WIDTH)]

    def new_block(self, position, v: int):
        if self.board[position.x][position.y]:
            raise Exceptions.OccupiedBlockPosition

        self.index += 1
        self.board[position.x][position.y] = Block(self.index, v)

        return self.index

    def get_sets(self) -> list:
        result = []
        for x in range(0, WIDTH):
            for y in range(0, WIDTH):
                if self.board[x][y]:
                    result.append(Set(Position(x, y), self.board[x][y]))
        return result

    def first(self, condition) -> Set:
        for s in self.get_sets():
            if condition(s):
                return s

    def find_if(self, condition) -> Position:
        for x in range(0, WIDTH):
            for y in range(0, WIDTH):
                if condition(self.board[x][y]):
                    return Position(x, y)

    def increment_block(self, block):
        pos = self.find_if(lambda b: b == block)
        self.board[pos.x][pos.y].value += 1

    def update_position(self, block: Block, new_position: Position):
        pos = self.find_if(lambda b: b == block)
        self.board[pos.x][pos.y] = None
        self.board[new_position.x][new_position.y] = block

    def add_block(self, s: Set):
        if self.first(lambda x: x.block.block_id == s.block.block_id):
            raise Exceptions.UniqueBlockIdError
        self.board[s.position.x][s.position.y] = s.block

    def move_block(self, block: Block, new_position: Position):
        if self.board[new_position.x][new_position.y]:
            raise Exceptions.OccupiedBlockPosition

        old_position = self.find_if(lambda b: b.block_id == block.block_id)
        self.board[old_position.x][old_position.y] = None
        self.board[new_position.x][new_position.y] = block

    def get_blanks(self) -> list:
        result = []
        for x in range(0, WIDTH):
            for y in range(0, WIDTH):
                if not self.board[x][y]:
                    result.append(Position(x, y))
        return result

    def __str__(self) -> str:
        result = ""
        for x in range(0, WIDTH):
            for y in range(0, WIDTH):
                result += f"{0 if not self.board[x][y] else self.board[x][y]}\t"
            result += "\n"
        return result


class Direction(Enum):
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"


class GameViewModel:

    def __init__(self):
        self.board = Board()

    def move(self, direction: Direction):
        if direction == Direction.UP:
            for x in range(WIDTH):
                for y in range(1, WIDTH):
                    if self.board.board[y][x]:
                        for k in range(y, 0, -1):
                            if not self.board.board[k - 1][x]:
                                self.board.board[k - 1][x] = self.board.board[k][x]
                                self.board.board[k][x] = None
                            elif self.board.board[k - 1][x].value == self.board.board[k][x].value:
                                self.board.board[k - 1][x].value += 1
                                self.board.board[k][x] = None
                                break
        elif direction == Direction.DOWN:
            for x in range(WIDTH):
                for y in range(WIDTH - 2, -1, -1):
                    if self.board.board[y][x]:
                        for k in range(y, WIDTH - 1):
                            if not self.board.board[k + 1][x]:
                                self.board.board[k + 1][x] = self.board.board[k][x]
                                self.board.board[k][x] = None
                            elif self.board.board[k + 1][x].value == self.board.board[k][x].value:
                                self.board.board[k + 1][x].value += 1
                                self.board.board[k][x] = None
                                break
        elif direction == Direction.LEFT:
            for y in range(WIDTH):
                for x in range(1, WIDTH):
                    if self.board.board[y][x]:
                        for k in range(x, 0, -1):
                            if not self.board.board[y][k - 1]:
                                self.board.board[y][k - 1] = self.board.board[y][k]
                                self.board.board[y][k] = None
                            elif self.board.board[y][k - 1].value == self.board.board[y][k].value:
                                self.board.board[y][k - 1].value += 1
                                self.board.board[y][k] = None
                                break
        elif direction == Direction.RIGHT:
            for y in range(WIDTH):
                for x in range(WIDTH - 2, -1, -1):
                    if self.board.board[y][x]:
                        for k in range(x, WIDTH - 1):
                            if not self.board.board[y][k + 1]:
                                self.board.board[y][k + 1] = self.board.board[y][k]
                                self.board.board[y][k] = None
                            elif self.board.board[y][k + 1].value == self.board.board[y][k].value:
                                self.board.board[y][k + 1].value += 1
                                self.board.board[y][k] = None
                                break

    def add_block(self):
        blanks = self.board.get_blanks()
        if not blanks:
            raise Exceptions.BoardIsFull

        pos = blanks[randint(0, len(blanks) - 1)]
        value = 0 if randint(0, 4) < 4 else 1
        self.board.new_block(pos, value)


class GameView:

    def __init__(self, viewmodel: GameViewModel):
        self.viewmodel = viewmodel

    def user_input(self, direction: Direction):
        self.viewmodel.move(direction)
        self.viewmodel.add_block()

    def display(self):
        print(self.viewmodel.board)


if __name__ == "__main__":
    viewmodel = GameViewModel()
    game = GameView(viewmodel)

    for _ in range(2):
        viewmodel.add_block()

    while True:
        game.display()
        move = input("Enter move (W/A/S/D): ").strip().upper()
        if move == "W":
            game.user_input(Direction.UP)
        elif move == "S":
            game.user_input(Direction.DOWN)
        elif move == "A":
            game.user_input(Direction.LEFT)
        elif move == "D":
            game.user_input(Direction.RIGHT)
        else:
            print("Invalid input!")
