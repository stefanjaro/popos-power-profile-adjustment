#!/usr/bin/env python

# A script to automate switching between performance, balanced, and battery power profiles on Pop!_OS
# The script was inspired by: https://github.com/kulkarnip150/linux-setup-script/blob/main/extras/switch_power_profile.sh

# import libraries
import os
import time
import subprocess

# =================
# GLOBAL VARIABLES
# =================

# global variables (the only things you'll need to change)
SLEEP_TIMER = 60 # how long until the script runs again 
DISCHARGING_INDICATOR = "Discharging" # indicates if the battery is discharging
CHARGING_INDICATOR = "Charging" # indicates if the battery is charging
FULL_CHARGE_INDICATOR = "Unknown" # oddly my computer doesn't say charged, it says unknown
CHARGING_THRESHOLD = 50 # battery charge level threshold between balanced and performance when charging
BATTERY_STATUS_FILE_LOC = "/sys/class/power_supply/BAT1/status" # the location of the battery status file
BATTERY_CAPACITY_FILE_LOC = "/sys/class/power_supply/BAT1/capacity" # the location of the battery capacity file
LOG_FILE_PATH = "/Documents/battery_profile_changes.txt" # where the log file should be saved

# ====================
# ESSENTIAL FUNCTIONS
# ====================

def get_battery_status():
    """
    Opens the system file that contains the charging/discharging 
    status of the battery
    """
    with open(BATTERY_STATUS_FILE_LOC, "r") as file:
        battery_status = file.read().strip()
    return battery_status

def get_battery_capacity():
    """
    Opens the system file that contains the battery's current charge level
    """
    with open(BATTERY_CAPACITY_FILE_LOC, "r") as file:
        battery_capacity = file.read().strip()
    return float(battery_capacity)

def log_profile_changes(change_status, battery_status, battery_capacity):
    """
    Log changes made to the battery profile

    Keyword arguments:
        change_status -- the battery profile change to be logged
        battery_status -- whether the battery is charging or not
        battery_capacity -- the battery's current charge level
    """
    # get current time
    current_time = time.asctime(time.localtime())

    # form full log file path
    full_log_file_path = os.path.expanduser("~") + LOG_FILE_PATH

    with open(full_log_file_path, "a") as file:
        file.write(f"{current_time} | {battery_status} | {battery_capacity} | {change_status}\n")
    return None

def optimize_power_profile(battery_status, battery_capacity):
    """
    Optimizes the battery power profile based on the battery_status and capacity
    but does nothing if we're already on our ideal profile

    Keyword arguments:
        battery_status -- whether the battery is charging or not
        battery_capacity -- the battery's current charge level
    """
    # determine the ideal battery profile based on existing battery information
    if battery_status == DISCHARGING_INDICATOR:
        ideal_profile = "battery"
    elif battery_status == FULL_CHARGE_INDICATOR:
        ideal_profile = "performance"
    elif battery_status == CHARGING_INDICATOR:
        if battery_capacity < CHARGING_THRESHOLD:
            ideal_profile = "balanced"
        else:
            ideal_profile = "performance"
    else:
        log_profile_changes("Unknown battery_status value", battery_status, battery_capacity)
        return None

    # get current profile (parsing the string for the value we need)
    profile_cmd_output = subprocess.getoutput("system76-power profile")
    current_profile = profile_cmd_output.split("\n")[0].split(":")[-1].strip().lower()

    # optimize if it's not the same
    if ideal_profile != current_profile:
        os.system(f"system76-power profile {ideal_profile}")
        log_profile_changes(f"Changing to {ideal_profile}", battery_status, battery_capacity)
    else:
        log_profile_changes("No change in profile", battery_status, battery_capacity)

    return None

# =================
# SCRIPT EXECUTION
# =================

if __name__ == "__main__":
    while True:
        # get battery details
        battery_status = get_battery_status()
        battery_capacity = get_battery_capacity()

        # optimize power profile
        optimize_power_profile(battery_status, battery_capacity)
        
        # sleep for a specified number of seconds
        time.sleep(SLEEP_TIMER)