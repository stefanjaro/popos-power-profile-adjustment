# Pop!_OS Automatic Battery Profile Management

# Purpose

This Python script (which could've been a Bash script had I known the language better) will switch between the battery profile options on Pop!_OS based on the battery status (charging, discharging, etc.) and capacity (power level) of your battery.

It was heavily inspired by an existing bash script which you can find here: https://github.com/kulkarnip150/linux-setup-script/blob/main/extras/switch_power_profile.sh.

The reason why I wrote this one instead of forking the above is because I wanted to use Python instead.

# Configuration Options

The global variables at the top of the script have been set to my liking and for my machine. You'll probably need to adjust these first, especially the locations of the battery status and battery capacity files.

* `SLEEP_TIMER` -- How long the script will sleep before it's run again.
* `DISCHARGING INDICATOR` -- What the battery status file says when you're NOT CHARGING your battery.
* `CHARGING INDICATOR` -- What the battery status file says when you ARE CHARGING your battery.
* `FULL_CHARGE_INDIACTOR` -- What the battery status file says when you're at FULL CHARGE (interestingly mine says unknown and that's probably because of the battery charge limit options I've set on my Windows instance).
* `CHARGING_THRESHOLD` -- If the battery is charging but is below this threshold, it'll be set to `balanced`. If not, it'll be set to `performance`.
* `BATTERY_STATUS_FILE_LOC` -- The location of the battery status file. It's `"/sys/class/power_supply/BAT1/status"` for me but might be BAT0 for you.
* `BATTERY_CAPACITY_FILE_LOC` -- The location of the battery capacity file. It's `"/sys/class/power_supply/BAT1/capacity"` for me but might be BAT0 for you.
* `LOG_FILE_PATH` -- Where the log file will be saved. By default, it'll be created and saved in the Documents folder.

# Log File

By default, the script stores all activity in a log file saved in the Documents folder. Every 60 seconds (the default sleep time is 60 seconds) a new line will be written to the file. Each line is structured as follows:

`Date and time` | `Profile status change` | `Battery status` | `Battery capacity`

You can check on the log file by either opening it in your favourite text editor or by running:

`cat Documents/battery_profile_changes.txt`

# Installation

## One Time Use

If you just want to check it out, download this repository, edit the environment variables (mentioned above) at the top of the script, navigate to the directory and run the script using:

```python
python3 power-profile-adjustment.py
```

Please note that at the time of writing the latest version of Pop!_OS comes with Python 3.9.5 pre-installed.

## Load on Startup

By far the easiest way to set it up is by using the Startup Applications tool that comes pre-installed on Pop!_OS.

1. Hit your super key (e.g. the windows key) and search for `Startup Applications`.
2. Click on `Add`.
3. In the `Command` field, type `python3 /path/to/folder/power_profile_adjustment.py &`. Replace `/path/to/folder` with where the script is saved.
4. Give it a name like "Power Profile Adjustment" and a comment if you'd like.
5. Click `Save`.

Now reboot, and the Python script will run on boot.

## Troubleshooting

* If you're having issues, try changing the script's permission setting using `chmod u+x /path/to/folder/power_profile_adjustment.py`.
* Check if the Python script is running using `ps -fA | grep python` and looking for the script.

# Additional Tips

If you're struggling with short battery life issues on Pop!_OS, make sure to check out [tlp](https://linrunner.de/tlp/) and [Powertop](https://wiki.archlinux.org/title/powertop).
