from enum import Enum

WIDTH = 4
values = [2 ** i for i in range(1, 12)]  # [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]


# ==============================
#           Exceptions
# ==============================

class Exceptions:
    class UniqueBlockIdError(Exception):
        """Block id should be unique"""


# -----------------------------
#           Functions
# -----------------------------

def first(items: list, condition):
    for i in items:
        if condition(i):
            return i


# ==============================
#           Position
# ==============================

class Position:

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __eq__(self, other) -> bool:
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y


# ==============================
#           Block
# ==============================

class Block:

    def __init__(self,
                 block_id: int,
                 value: int):
        self.block_id = block_id
        self.value = value

    def __eq__(self, other) -> bool:
        if isinstance(other, Block):
            return self.block_id == other.block_id


# ==============================
#           Set
# ==============================

class Set:

    def __init__(self,
                 position: Position,
                 block: Block):
        self.position = position
        self.block = block


# ==============================
#           Board
# ==============================

class Board:

    def __init__(self):
        self.board = [[None for _ in range(WIDTH)] for _ in range(WIDTH)]

    def get_sets(self) -> list:  # returns a tuple of (block, position)
        pass

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
        if self.first(lambda x: x.block_id == s.block.block_id):
            raise Exceptions.UniqueBlockIdError
        self.board[s.position.x][s.position.y] = s.block

    def __str__(self) -> str:
        # TODO display as string for debugging
        pass


# ==============================
#           Direction
# ==============================

class Direction(Enum):
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"


# ==============================
#         Game View Model
# ==============================

# viewmodel layer
class GameViewModel:

    def __init__(self):
        self.board = Board()

    def move(self, direction: Direction):
        pass


# ==============================
#          Game View
# ==============================

# view layer
class GameView:

    def __init__(self, viewmodel: GameViewModel):
        self.viewmodel = viewmodel
        self.board = Board()

    def user_input(self, direction: Direction):
        self.viewmodel.move(direction)

    def increment_value(self, block: Block):
        self.board.increment_block(block)
        # TODO animate
        pass

    def new_block(self, s: Set):
        self.board.add_block(s)
        # TODO animate
        pass

    def update_positions(self):
        old_sets = self.board.get_sets()
        new_sets = self.viewmodel.board.get_sets()

        for new_set in new_sets:
            old_set = first(old_sets, lambda s: s.block == new_set.block)

            if not old_set:  # block is new
                self.new_block(new_set)
                continue

            old_sets.remove(old_set)

            if old_set.position == new_set.position:
                continue  # block is in same place

            else:  # block is moved
                self.animate_to(old_set.block, new_set.position)

            if old_set.block.value != new_set.block.value:
                self.increment_value(old_set.block)

    def animate_to(self, block: Block, new_position: Position):
        # TODO update the position of block to new position with animation
        pass
