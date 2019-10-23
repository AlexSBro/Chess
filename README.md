# Chess

Simple Pygame Chess

This is a project im doing to refresh my memory of python syntax before I move into work with django.
The goal is to make a simple chess board that you can play against another human that only allows legal chess moves.

## Architecture
This is the architecture form top level to bottom level the class above has an instance of the class below it. All of these classes should only have one instance.

##### Game --top level
This is where all of the below classes are initialized and passed to each other. This is also where all of the user input is gathered and passed to the interested class. This is what holds the main game loop.

##### MoveManager
This is what checks for the possibility of moves based on information provided by the piece manager and board (for highlighting and presence of other pieces). It then logs moves that happen so that these moves can then be undone. 
- refers to piece manager
- Contains moves in a list

##### PieceManager
This class is responsible for checking if a tile is occupied and by what color of piece. This is used by the move manager to confirm that a move is possible.

- refers to board
- Contains living pieces in a list
- Contains dead pieces in a list

##### Board --bottom level
This class is mostly for rendering the board itself. It is what is responsible for highlighting and sending returning x,y indexes from mouse clicks. 
-- Contains tiles in a list