# MotorSimulation
Foray into motor modeling, analysis, and control in a custom Python simulation environment. The 'notebooks' folder contains .ipynb documentation of some basic linear magnetic simulations that I used to prototype the main simulation suite, Big Brain Motor Modeling, Analysis and Control (BigMMAC). My progress on BigMMAC may be found within the titular folder, and will be updated as I figure out more stuff.

## Most recent commit progress:
- added `params2igains` method in `motormath.py` to compute current control gains
## To Do:
- Develop "ideal" controller script psuedocode as would be implemented on a microcontroller
  - Use this script to drive how BigMMAC's truth side of simulation should interface with its controller side
- Reference must be read and updated every time controller is updated
  - Reference should be specified controller side, and capability for realtime vs predefined reference specification should be bookmarked
  - Need to bake in an auto interpolation for predefined complex time varying references to allow changing of `dt` without having to re-generate the reference table
- Figure out a better way of defining controller()
  - Explore controller(armature current, speed, theta, reference), specify current=, speed=, theta= in the backend. Essentially configure the truth side to always pass the controller ALL motor states correctly regardless of order of argument definition on the controller side. 
- Figure out how to enable user specifcation of controller update frequency
  - Want to emulate hardware timers as they would be used on a microcontroller