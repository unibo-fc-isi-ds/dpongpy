# Description

The **PongTerminal** has been modified to priotitize availability over consistency.

Similarly to the `PongCoordinator` a `thread receiver` has been added to the `PongTerminal` so that the game doesn't block when messages don't reach the terminal, letting the user move their paddle.

The game status of the terminal gets overridden when the terminal receives a new message, containing the status, from the coordinator. Until then the game gets updated as if the local state is the correct one.

# How to test 

The game must be run in `centralised` mode, with one coordinator and as many terminal you want to test it with.
The commands to run both roles weren't changed.
