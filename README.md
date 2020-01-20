# Chess-game
Two player chess game implemented in python for further AI experimentation

## Initial idea
 
 The main idea behind this project was to implement a fun project in python. 
 I have chosen a game concept, as it is one of the easier tasks at hand, which 
 are easily verified, if they work as intended. 
 
 Another aim of this project was to present basic programming concepts and paradigms
 to a begginner to be student. In this case an game would be fun and challenging 
 task to take up from start to finish.
 
## Implementation design

 As chess is a two player game, we will be using a server-client framework implementation
 in python programming language implemented via sockets. Also an OOP design patterns will
 be used further into the project. 
 
Server part of the implementation will keep an information about the board and provide
all possible moves to the client side of application. It will be considered as the 
processing core of this implementation. Client side applications will mostly be handling
olny representation of the board and pieces themselves. As well as recording the user
inputs for the game.

## Further plans

The goal is to implement a simple environment suitable for experimentation with different
AI methods. Also as a playground for implementing AI players who will be able to compete
with their AI or human oponents.
 