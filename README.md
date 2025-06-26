# smart-trashbin

Objective was to create a IoT trash bin for automatic sorting of waste.

<img width="486" alt="Screenshot 2025-06-25 at 11 51 14 PM" src="https://github.com/user-attachments/assets/81120d4b-ad84-40b8-a99c-b8a6b0e83424" />

<img width="632" alt="Screenshot 2025-06-25 at 11 51 32 PM" src="https://github.com/user-attachments/assets/c4e34ac2-c1e2-4c24-ac8b-8b79a1943bba" />

## Motivation

Every day, countless recyclable and compostable materials get dumped into the single closet trash bin someone can find. Unfortunately, existing systems make it confusing and inconvenient for someone to properly dispose of their trash. There is usually confusion about whether the material is recyclable, and if it is, where is the recycling bin for me to dispose of it? With everyone’s busy schedule, the most convenient decision is to toss it in the closet bin. This decision repeated thousands of times a day can lead to very serious environmental damage.
	Contamination in recycling streams is an even bigger issue. Approximately 25% of materials in recycling bins are contaminated, resulting in entire batches of recycled items being sent to landfills.[1] This mismanagement results in a loss of valuable resources and imposes substantial financial burdens on municipalities, where waste management consumes up to 20% of city budgets.[2] Moreover, organic waste such as food and yard clippings, when improperly disposed of in landfills, decomposes anaerobically and produces methane, a greenhouse gas 80 times more potent than carbon dioxide over 20 years. Food waste alone accounts for 58% of methane emissions from solid waste landfills.[3] 
	Our team plans to tackle these challenges with our IoT-based Smart Bin. It is built to automatically sort waste into four categories: recyclables, trash, compost, and electronics. Using a combination of sensors and machine learning, the system identifies and sorts each item to reduce human error. All the user needs to do is place their waste in the center of the bin, and the system takes care of the rest, automatically dropping it into the correct compartment. This solution saves time, removes the need for decision-making, and helps conserve valuable resources for the future.

 Sources:
 
[1]https://recyclops.com/understanding-recycling-contamination/#:~:text=The%20Impact%20of%20Recycling%20Contamination,contaminated%20and%20cannot%20be%20recycled.

[2]https://www.hlp.city/en-us/articles/how-us-cities-can-win-the-fight-against-trash

[3]https://news.climate.columbia.edu/2020/03/13/fix-recycling-america/

## Software

Image classifcation model can be found in smart-bin/models

Built a new library found in smart-bin-main. This library consists mainly of the smartbin.py file (adapted from the picarx.py file). This file configures the 4 PWM pins we used for the 4 servos to control the 4 flaps. Calibration values for the 4 servo motors are hard-coded to the library, such that when a servo angle is zero, the servo is turned to a degree where the flap is closed. 

driver.py loads the classifier model and sets up connections with the camera. Then, the bin sequentially does the following: checks bin fullness (if full, lights up LED and exits), captures a trash image, determines trash category, opens the corresponding bin, and closes the bin. 

## Hardware

3D printed Servo Hinges: https://www.thingiverse.com/thing:1323380

Hardware used included a raspberry pi, pi cammera, 4 servo, 4 servo hinges, ultrasonice sensor and LED
