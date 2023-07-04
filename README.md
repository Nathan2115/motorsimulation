# MotorSimulation
Foray into motor modeling, analysis, and control in a custom Python simulation environment. The 'notebooks' folder contains .ipynb documentation of some basic linear magnetic simulations that I used to prototype the main simulation suite, Big Brain Motor Modeling, Analysis and Control (BigMMAC). My progress on BigMMAC may be found within the titular folder, and will be updated as I figure out more stuff.

## Most recent commit progress:
- added `motorparams.py` to store motor parameter dicts
- added `commands.py` to bookmark reference generation and live capture capability, added `commands.Step()` for step cinput generation
- realized that given current architecture, controllers need to be implemented as classes to hang on to error.
- added current control examples to the example PMDC control scripts
## To Do:
- Add 3-phase surface mount permanent magnet simulation capability
- Figure out how to enable user specifcation of controller update frequency
  - Want to emulate hardware timers as they would be used on a microcontroller