*Read this in other languages: [Português-BR](readme_pt-BR.md)


# About this project
This is a **pygame** implementation of the classic game Nine Men´s Morris, also called Mill, Mills and even Cowboy Checkers.


## Table of Contents
  - [Nine Men´s Morris](#nine-mens-morris)
  	- [Phase One - Placement](#phase-one)
  	- [Phase Two - Movement](#phase-two)
  	- [Phase Three - Movement](#phase-three)
  - [The Implementation](#the-implementation)
  	- [The Game](#the-game)
  	- [The AI](#the-ai)
	- [Minimax and Negamax](#minimax-and-negamax)
  	- [The UI](#the-ui)
	- [Pygame](#minimax-and-negamax)
	- [Widgets](#widgets)


## Nine Men´s Morris

The game is played on this [Board](#the-board)

There are 3 phases in the game:
- [Phase One - Placement](#phase-one)
- [Phase Two - Movement](#phase-two)
- [Phase Three - Flying](#phase-three)

Obviously, the game starts in phase one, and similarly to other two player games, the starting player is always the white one. In all phases the players can form mills and remove the opponent´s pieces. The winning condition is if a player has no legal move, or if a player is left with two pieces, however the game cannot end in phase one!


### Phase One

In this phase of the game, the players alternate in placing their pieces on the board. Whenever three pieces of the same player line up, horizontally or vertically, it is said that the player has made a mill with those pieces, and can instantly remove a piece from the opponent.

After each player has placed nine pieces, begins phase two of the game.

### Phase Two

It is in phase two that the players now move the pieces they have previouly placed. A piece´s legal move is one to an empty adjacent tile.

Again, if a mill is formed, the player can remove a piece from the opponent.

### Phase Three

If a player is left with only three pieces in phase two, it is said that the player is flying, and begins phase three, where the losing player can now move pieces to any empty tile, and not just adjacent ones. This gives this player an advantage, so as to not make the end game boring.

### Mills

A mill a set of three pieces in a row or collumn. Whenever a mill is formed the player who made it can remove a piece from the opponent, making progress towards victory.

Pieces from the opponent´s mills cannot be removed, unless the opponent only has three pieces, that happen to be in a mill.

If a move forms **n** new mills, the player can remove **n** pieces from the opponent.


### The Board
The game is played on the following board. which consists of 24 locations where the players can place and move pieces.

![Empty Board](https://png.vector.me/files/images/1/2/124490/nine_mens_morris_game_board_clip_art.jpg "Empty Board")

### Aditional Info
You can read more about the game at:

[Wikipedia](https://en.wikipedia.org/wiki/Nine_men%27s_morris "Wikipedia")

[Old Game](https://web.archive.org/web/20041121040028/http://mc2.vicnet.net.au/home/aura/shared_files/Berger1.pdf)

[Perfect Game Solution](http://library.msri.org/books/Book29/files/gasser.pdf)

[Another Perfect Game Solution](https://althofer.de/stahlhacke-lasker-morris-2003.pdf)

## The Implementation

All implementation was built in Python 3.7 and the libraries used so far are:
- Numpy: used for some calculations.
- Pygame: used to create the game display and handle input events.
- OS: used to get easy acess to files.

The project started with the base game with no interface whatsoever, and that's where I'll start explaning it.

### The Game

The first thing I did was create a Nine Morris game Class to store the board, active player and the mills, and have functions to act on the board and read information from it.

##### The players

The white player will be considered as being equal to 1 and the black player as -1. This will be stored in a player class. The numbers were choosen because it´s easy to chang the active player with ``active_player = -active_player``.

```python
class Player:
	WHITE = 1
	BLACK = -1
```

#### The board

The 24 positions of the board will be stored in a **np.array** of size 24, and will be labeled as follows.

![Labeled Board](https://imgur.com/nXBDbyN.png)

Doing this means will have to know all possible mill configurations. This I have already done, and wrote in the file [Possible Mills](Assets/possible_mills.py).


#### The moves

There are three types of possible moves, either you place a piece, move a piece or remove a piece. With this in mind, we´ll make the class `MoveType` 

```python
class MoveType:
	PLACE_PIECE = 1
	MOVE_PIECE = 2
	REMOVE_PIECE = 3
```

We´ll also have a class for the move itself, storing the position where the move will act upon, the type of move and, if it´s a piece movement, the final position of the piece.

```python
class Move:
    def __init__(self, position, move_type, final_position=None):
        self.move_type = move_type
        self.position = position
        self.final_position = final_position
```

This class will also have a method to verify if the move is valid, a method to pretty print the move, and a method to hash it (more about this later).


### The AI

#### Minimax and Negamax

### The UI

#### Pygame


#### Widgets

## To Do
- Add in game time.
- Add minimal (plus random number) time for AI to play.
- Ability to go back to the main menu once the game has starded.
