#!/usr/bin/env python3
"""
Control servos for waste-bin lids using GPIOZero on a Raspberry Pi.
Each class name in data/labels.txt is mapped to a GPIO pin.
"""
try:
    from gpiozero import Servo
    HAS_GPIOZERO = True
except ImportError:
    HAS_GPIOZERO = False
import time

# Map classification names to GPIO pins
PIN_MAP = {
    "trash":        17,
    "recycle":      27,
    "compost":      22,
    "electronics":  23
}

# Initialize servos if gpiozero is available
SERVOS = {}
if HAS_GPIOZERO:
    for cls, pin in PIN_MAP.items():
        # SG90 servo calibration
        SERVOS[cls] = Servo(pin, min_pulse_width=0.5/1000, max_pulse_width=2.4/1000)
else:
    print("[Warning] gpiozero not available, pick_bin will only log actions.")


def pick_bin(cls_name: str) -> None:
    """
    Open the lid for the given class by moving the servo, then close it.
    Falls back to logging if gpiozero is unavailable.
    """
    if not HAS_GPIOZERO:
        print(f"[Stub] Would open lid for: {cls_name}")
        return

    servo = SERVOS.get(cls_name)
    if not servo:
        print(f"[Error] No servo configured for class: {cls_name}")
        return

    # Open lid
    servo.max()
    time.sleep(1.0)
    # Close lid
    servo.min()
