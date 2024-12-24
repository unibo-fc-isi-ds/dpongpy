Description
The PongTerminal has been updated to prioritize availability over consistency.
A new thread, similar to the one in PongCoordinator, has been added to the PongTerminal, so this ensures the game remains responsive and allows the user to move their paddle even there is a lag of receiving packets from coordinator, and will not be blocked while waiting coordinator's answer.
The terminal's game status is overridden whenever a new status message is received from the coordinator, obviously. Until then, the game continues to update based on the local state.

How to Test
Run the game in centralized mode, using one coordinator and as two terminals for testing. 

python -m dpongpy --mode centralised --role coordinator  
python -m dpongpy --mode centralised --role terminal --side left --keys wasd --host IP_COORDINATOR  
python -m dpongpy --mode centralised --role terminal --side right --keys arrows --host IP_COORDINATOR
