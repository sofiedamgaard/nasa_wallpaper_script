NASA APOD Wallpaper Automation (macOS)

This project is a macOS automation script written in Python that automatically fetches NASA’s Astronomy Picture of the Day (APOD) and sets it as the desktop wallpaper.

The script is scheduled using launchd and integrates directly with macOS via AppleScript to ensure reliable wallpaper updates across desktops.

Features
- Fetches daily data from NASA’s APOD API
- Automatically downloads and caches images locally
- Sets desktop wallpaper using AppleScript and System Events
- Handles network failures and API timeouts using fallback images
- Displays the APOD explanation in a macOS note
- Designed to run unattended as a daily background job

Technologies
- Python
- NASA APOD API
- AppleScript (System Events)
- macOS launchd
- macOS UI automation (AppleScript / System Events)
