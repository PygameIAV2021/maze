Mazewalker
====

## The Game

The game follows a simple principle. The goal is to move your Character to the exit (the small silver/golden Trapdoor) while evading the patrolling Skeletons. It is possible to pause the game at any time or to show the visited tiles. The player always begins in the upper left corner (quadrant II.) and the exit will be created in the lower right (quadrant IV.). All enemies will spawn on random tiles in every quadrant except the upper left quadrant, where the player spawns.

## Controls

The Movement is controlled with W, A, S, D.
When the SHIFT key is pressed, the player can move twice as fast.
The game can be paused with P and can be closed by pressing ESCAPE.
The creation of tilemarkers can be toggled with T and can be hidden by pressing M.
When R is pressed, the view will be centered on the player and by pressing Z the automatic scrolling can be deactivated.
When the automatic scrolling is deactivated the map can be moved with your mouse while pressing the left mouse button.

## Textures

All visible texts were created on [Textcraft.net](https://textcraft.net/).
All background textures for the map are customized and based loosely on the game [Minecraft](https://www.minecraft.net).
All character models were designed by Johannes Sjölund (Wulax) and published on [Open Game Art](https://opengameart.org/content/lpc-medieval-fantasy-character-sprites).

## Why did I choose to do that project?

I decided to do a randomly generated labyrinth in order to learn the underlying algorithms. The algorithm used here is a [loop-erased random walk](https://en.wikipedia.org/wiki/Loop-erased_random_walk), more precise Wilson’s algorithm. The created labyrinth get adjusted to the needs of the game. All important POI like player and enemy spawn are randomly chosen.

## Used libraries

The following libraries are used in the project:

* pygame 
   * the complete project is based on this library
* math
   * used for rounding numbers
* random 
  * shuffling lists
  * generating random numbers
* os 
  * adjusting path to folders
* enum 
  * enumerations for several values

## Configuration

The values for configuring can be found in [const.py](./const.py).  
The constants in the first lines of the file can be adjusted to change the following values:

- TILE_SIZE: Size of a tile in pixel
- ENEMY_SIZE = Size of an enemy in pixel (<= TILE_SIZE>)
- PLAYER_SIZE = Size of the player in pixel (<= TILE_SIZE>)
- PLAYER_SPEED = Movement speed of the player in tiles per seconds
- ENEMY_SPEED = Movement speed of the enemies in tiles per seconds
- ENEMY_RAND_SPEED = Added randomized movement speed of the enemies in tiles per seconds
- ENEMY_COUNT = Maximum count of enemies
- WINDOW_SIZE = Size of the window (Width, Height)
- MAZE_SIZE = Size of the maze in tiles (final size is 2*MAZE_SIZE+1 !!!)

## Internal structure

The project is object oriented.  
The following classed are used in the project:

* Main
   * shows the main menu
   * start the game after player input
* Game
   * creates the player
   * create the map class for generating and managing the map
   * react to inputs
   * move enemies
   * control the flow of the game
* Player
   * draw the player
* Models
   * load all sprites for the enemies
* Enemy
   * draw all enemies
* Map
   * create the map generator
   * draw the maze
* Generator
   * create the maze
   * choose the player spawn
   * choose the target tile
   * choose the enemy spawns

The following classes inheriting from enum.Intenum:

* game_state
   * Contains all possible values for the main game loops
* direction
   * Contains all possible directions
* field_v
   * Values used while generating the maze
* draw_v
   * Values describing the final look of the maze at the end of the generation process
* base_id
   * Values of the three tile types (Road, Wall, Exit)
* return_v
   * Values used while generating the maze
