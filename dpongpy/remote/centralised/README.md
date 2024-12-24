# General description
The exercise has been modified to prioritize availability over consistency, in order to make the game fluid, even in presence of network issues.

This change only applies to the game set in remote mode, not in local mode.

This has been achived by having a new thread that recives messages from the controller while the gui updates indipendently.

To start the game all of the original commands and options are unchanged.
