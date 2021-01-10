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

Obviously, the game starts in phase one, and similarly to other two player games, the starting player is always the white one.In all phases the players can form mills and remove the opponent´s pieces. The winning condition is if a player has no legal move, or if a player is left with two pieces, however the game cannot end in phase one!


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

### The Game


### The AI

#### Minimax and Negamax

### The UI

#### Pygame

#### Widgets
