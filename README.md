# ISS LOCATOR 🛰️

Python program to locate the International Space Station with an interactive map.  
Inspired by Angela Yu's ISS Overhead Project.

![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![Version](https://img.shields.io/badge/Version-2.1-blue)

--- 

## FEATURES 🌟
- Locates the International Space Station using coordinates converted to a physical address
- Interactivate map of the world with zoom features and markers for the ISS
- Desktop notifications for when the ISS is near you (COMING SOON)

## INSTALLATION ⚙️
Clone the repository while in your desired directory:
```bash
git clone https://github.com/Program-Arcana/iss-locator.git
```
Navigate to the repository directory to begin using it.

Create and activate a virtual environment:
MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```
Windows:
```bash
python -m venv venv
venv\Scripts\activate.bat
```

Use package manager pip to install the following:
```bash
pip install requests
pip install geopy
pip install desktop-notifier
```

## USAGE 🔧
Run the following command to start the locator program:
```bash
python3 locator.py
```

On the map you will see a red marker labeled "ISS". That is the current position of the International Space Station.  

When you are done using the program, you can deactivate the virtual environment with this command:
```bash
deactivate
```

## ATTRIBUTION ©️
- ISS Current Location API: http://open-notify.org/Open-Notify-API/ISS-Location-Now/
- Geopy API: https://github.com/geopy/geopy
- Desktop Notifier: https://github.com/samschott/desktop-notifier
- Tkinter Map Viewer: https://github.com/TomSchimansky/TkinterMapView
- Requests: https://requests.readthedocs.io/en/latest/
