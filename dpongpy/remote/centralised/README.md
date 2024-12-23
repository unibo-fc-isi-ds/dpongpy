# Exercise: Available Distributed Pong

The implementation has been modified to prioritize availability over consistency, in order to make the game more fluid for the user.

To achieve the goal, it has been implemented the speculative execution on the terminal-side. In particular, the terminal's game-loop should not block while waiting for updates from the coordinator, so the handling of receiving events is given to a separate thread.

The terminal updates his local game state according to the local input received, so it has to overwrite the local game state with the remote one only in case of an update provided by the coordinator.

## Testing

In order to test the implementation, it's necessary to execute a coordinator and at least two terminals:

- to execute the coordinator:
    ```
    python -m dpongpy --mode centralised --role coordinator
    ```

- to execute the terminals:
    ```
    python -m dpongpy --mode centralised --role terminal --side {left,up,right,down} --keys {wasd,arrows,ijkl,numpad}
    ```

It's also possible to specify the host and the port of the coordinator, so accordingly in the terminal execution's command.
