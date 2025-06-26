# Smart Trash Bin

Smart Bin Python library for Raspberry Pi, adopted from SunFounder PicarX Python library.

## Installation

 > **Note**
  You also need to install robot_hat, vilib, sunfounder_controller and other dependent libraries.\
  <https://docs.sunfounder.com/projects/picar-x-v20/en/latest/python/python_start/install_all_modules.html>

```bash
git clone -b v2.0 https://github.com/pbad2/smart-trashbin.git
cd smart-bin
sudo python3 setup.py install

```
----------------------------------------------

<img width="478" alt="Screenshot 2025-06-26 at 12 19 05 AM" src="https://github.com/user-attachments/assets/3585d9e4-a29b-4a8e-825b-d3207cc09b16" />

<img width="578" alt="Screenshot 2025-06-26 at 12 19 47 AM" src="https://github.com/user-attachments/assets/c4515bdc-2209-42ce-bbc8-b1c896793e05" />


## Motivation

Every day, countless recyclable and compostable materials get dumped into the single closet trash bin someone can find. Unfortunately, existing systems make it confusing and inconvenient for someone to properly dispose of their trash. There is usually confusion about whether the material is recyclable, and if it is, where is the recycling bin for me to dispose of it? With everyone’s busy schedule, the most convenient decision is to toss it in the closet bin. This decision repeated thousands of times a day can lead to very serious environmental damage.
 
Contamination in recycling streams is an even bigger issue. Approximately 25% of materials in recycling bins are contaminated, resulting in entire batches of recycled items being sent to landfills.[1] This mismanagement results in a loss of valuable resources and imposes substantial financial burdens on municipalities, where waste management consumes up to 20% of city budgets.[2] Moreover, organic waste such as food and yard clippings, when improperly disposed of in landfills, decomposes anaerobically and produces methane, a greenhouse gas 80 times more potent than carbon dioxide over 20 years. Food waste alone accounts for 58% of methane emissions from solid waste landfills.[3] 

Our team plans to tackle these challenges with our IoT-based Smart Bin. It is built to automatically sort waste into four categories: recyclables, trash, compost, and electronics. Using a combination of sensors and machine learning, the system identifies and sorts each item to reduce human error. All the user needs to do is place their waste in the center of the bin, and the system takes care of the rest, automatically dropping it into the correct compartment. This solution saves time, removes the need for decision-making, and helps conserve valuable resources for the future.

Sources:

[1]https://recyclops.com/understanding-recycling-contamination/#:~:text=The%20Impact%20of%20Recycling%20Contamination,contaminated%20and%20cannot%20be%20recycled.

[2]https://www.hlp.city/en-us/articles/how-us-cities-can-win-the-fight-against-trash

[3]https://news.climate.columbia.edu/2020/03/13/fix-recycling-america/

## Software

Trained model can be found in smart-bin/models

Created a fork of PiCarX and build smart-bin. This library consists mainly of the smartbin.py file (adapted from the picarx.py file). This file configures the 4 PWM pins we used for the 4 servos to control the 4 flaps. Calibration values for the 4 servo motors are hard-coded to the library, such that when a servo angle is zero, the servo is turned to a degree where the flap is closed. 

Driver file acts as the main loop, The driver first loads the classifier model and sets up connections with the camera. Then, the bin sequentially does the following: checks bin fullness (if full, lights up LED and exits), captures a trash image, determines trash category, opens the corresponding bin, and closes the bin. 

## Hardware

3D printed servo hinges: https://www.thingiverse.com/thing:1323380

Other hardware used: raspberry pi, pi camera, 4 servos, 4 servo hinges, ultrasonic sensor, led

____________________________________________________________________________________

## License

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied wa rranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

{Repository Name} comes with ABSOLUTELY NO WARRANTY; for details run ./show w. This is free software, and you are welcome to redistribute it under certain conditions; run ./show c for details.

SunFounder, Inc., hereby disclaims all copyright interest in the program '{Repository Name}' (which makes passes at compilers).

Mike Huang, 21 August 2015

Mike Huang, Chief Executive Officer

Email: service@sunfounder.com, support@sunfounder.com

----------------------------------------------
