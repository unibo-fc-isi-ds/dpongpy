# Exercise: Available Distributed Pong

The dpongpy implementation has been modified to prioritize availability over consistency, in order to make the game run smoothly, even in the presence of network issues.

In particular, the reception of events in the terminal has been inserted into a thread, in order to avoid the terminal executing blocking instructions during the execution of the main thread.

The terminal processes the local game state with the update method.

The local state is modified if it receives a new game state from the coordinator.

To execute pong coordinator:

``` python -m dpongpy --mode centralised --role coordinator ```

To execute pong terminal:

``` python -m dpongpy --mode centralised --role terminal --side left --keys wasd --host IP_COORDINATOR --port PORT_COORDINATOR ```

Specifying paddle side, coordinator ip address and coordinator port
