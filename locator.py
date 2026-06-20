import tkinter as tk

import geopy
import requests
import tkintermapview
from desktop_notifier import DesktopNotifier
from geopy.adapters import AdapterHTTPError
from geopy.exc import GeocoderUnavailable
from geopy.geocoders import ArcGIS, Nominatim


class Locator:
    def __init__(self):
        self.font = "Courier"
        self.bg_color = "#a7adb2"
        self.root = None
        self.map = None
        self.iss_marker = None
        self.user_marker = None
        self.location = None
        self.setup_root()
        self.setup_title()
        self.setup_location()
        self.setup_map()

    def setup_root(self) -> None:
        """
        Sets up the root window
        """
        self.root = tk.Tk()
        self.center_root()
        self.root.title("ISS Locator")
        self.root.config(bg=self.bg_color)

    def center_root(self) -> None:
        """
        Centers the root window using the screen size and window size
        """
        # Screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Window dimensions
        window_width = 510
        window_height = 700
        # (x,y) starts at top left of window (0, 0)
        # x increases moving right, decreases moving left
        # y increases moving down, decreases moving up
        x = screen_width / 2 - window_width / 2 # position top left corner's x at this x
        y = screen_height / 2 - window_height # position top left corner's y at a smaller y (otherwise window too low)
        self.root.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y)) # Adds x and y offsets to window dims
        self.root.resizable(width=False, height=False) # Prevent window from being resizable

    def setup_title(self) -> None:
        """
        Sets up the title label
        """
        title = tk.Label(self.root, justify="center", text="ISS Locator Map", font=(self.font, 20, "bold"), bg=self.bg_color)
        title.grid(row=0, column=0, columnspan=2)

    def setup_map(self) -> None:
        """
        Sets up the map widget
        """
        self.map = tkintermapview.TkinterMapView(self.root, width=510, height=500, corner_radius=0)
        self.map.grid(row=1, column=0, columnspan=2, pady=10)
        self.map.set_zoom(0)
        self.marker = self.map.set_position(0, 0, marker=True)
        self.marker.set_text("ISS")

    def setup_location(self) -> None:
        """
        Sets up the location display for the ISS
        """
        self.location_title = tk.Label(self.root, text="ISS Location:", font=(self.font, 10, "bold"), bg=self.bg_color)
        self.location_title.grid(row=3, column=0, columnspan=2)
        self.location = tk.Label(self.root, wraplength=self.root.winfo_width(), bg=self.bg_color)
        self.location.grid(row=4, column=0, columnspan=2)

    def update_iss_pos(self) -> None:
        """
        Updates the position of the ISS on the map
        """
        new_lat, new_long = get_iss_coords()
        if new_lat and new_long:
            self.marker.set_position(new_lat, new_long)
            self.location.config(text=get_location(new_lat, new_long), font=(self.font, 10))
        self.root.after(10000, self.update_iss_pos) # Update the position every 10 seconds

def get_iss_coords() -> tuple:
    """
    Gets the current coordinates of the International Space Station
    :return: a tuple representing the latitude longitude coordinates of the ISS
    """
    try:
        iss_json = requests.get("http://api.open-notify.org/iss-now.json").json()
    except (requests.exceptions.ConnectTimeout, 
            requests.exceptions.ConnectionError,
            TimeoutError):
        return None, None
    else:
        iss_position = iss_json["iss_position"]
        iss_lat = float(iss_position["latitude"])
        iss_long = float(iss_position["longitude"])
        return iss_lat, iss_long
    
def get_location(lat, long) -> str:
    """
    Converts latitude and longitude coordinates to a location
    :param lat: the latitude coordinate
    :param long: the longitude coordinate
    :return: a string representing the location of the given coordinates
    """
    # Try seeing if ISS is over land (specifically a country)
    try: 
        geolocator = Nominatim(user_agent="ISS-Locator")
        location = geolocator.reverse((lat, long), language="en")
    except (geopy.exc.GeocoderUnavailable, geopy.adapters.AdapterHTTPError):
        return None
    else:
        if not location: # If the location is not over land 
            # Find out what ocean/body of water it is currently over
            geolocator = ArcGIS()
            location = geolocator.reverse((lat, long)) # English is the default
        return location.address

if __name__ == "__main__":
    locator = Locator()
    locator.update_iss_pos()
    locator.root.mainloop()