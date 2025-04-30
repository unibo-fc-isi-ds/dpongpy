# Available Distributed Pong
Goal: prioritize availability over consistency, in order to make the game fluid, even in presence of network issues

## Changes to the PongTerminal class:
A separate thread now handles the coordinator's message reception. This ensures that the terminal's game loop can continue updating and displaying the game without waiting for message reception, improving responsiveness and reducing the impact of network delays.

## Changes to the Controller class used in PongTerminal:
* The ```on_paddle_move()``` method inherited by the ```EventHandler``` class has been implemented.
* The ```on_time_elapsed()``` method has been modified to handle the game loop updates within the terminal, ensuring the game logic progresses even without new updates from the coordinator.
* The ```handle_inputs()``` method handles now the time elapsed. This way an ```ControlEvent.TIME_ELAPSED``` event is added to the pygame event queue, triggering updates to the terminal's game state.

Any update received from the coordinator ovverrides the internal game state of the terminal. 

## Test
In order to simulate network issues, set the UDP_DROP_RATE environment variable to a number $p\in [0,1]$ (say 0.2) before launching the coordinator to affect the probability of a package being dropped.  