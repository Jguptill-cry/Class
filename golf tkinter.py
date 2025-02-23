
import tkinter as tk
from tkinter import messagebox

class VirtualCaddy:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Caddy - Golf Club Selector")

        # Welcome Message
        tk.Label(root, text="Welcome to Virtual Caddy!", font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(root, text="Select the clubs in your bag and enter your distances:", font=("Arial", 12)).pack(pady=5)

        # List of possible clubs (now includes Gap Wedge)
        self.default_distances = {
            "Driver": 220,
            "3-Wood": 190,
            "5-Wood": 175,
            "3-Iron": 170,
            "4-Iron": 160,
            "5-Iron": 150,
            "6-Iron": 140,
            "7-Iron": 130,
            "8-Iron": 120,
            "9-Iron": 110,
            "Pitching Wedge": 90,
            "Gap Wedge": 80,
            "Sand Wedge": 60,
            "Putter": 10
        }

        # Dictionaries to store checkbox variables and distance entry fields
        self.selected_clubs = {}
        self.distance_entries = {}

        # Create checkboxes and distance entry fields for each club
        for club, default_yardage in self.default_distances.items():
            frame = tk.Frame(root)
            frame.pack(anchor="w")

            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame, text=club, variable=var)
            chk.pack(side="left")
            self.selected_clubs[club] = var

            entry = tk.Entry(frame, width=5)
            entry.insert(0, str(default_yardage))  # Set default distance
            entry.pack(side="right")
            self.distance_entries[club] = entry

        # Distance Input
        tk.Label(root, text="Enter distance to pin (yards):", font=("Arial", 12)).pack(pady=5)
        
        self.distance_entry = tk.Entry(root)
        self.distance_entry.pack(pady=5)

        # Buttons
        self.submit_button = tk.Button(root, text="Find Club", command=self.recommend_club)
        self.submit_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Reset to Defaults", command=self.reset_distances)
        self.reset_button.pack(pady=5)

    def recommend_club(self):
        """Determines the best club based on distance and available clubs."""
        try:
            distance = float(self.distance_entry.get())
            available_clubs = {}

            # Get user-defined distances
            for club, var in self.selected_clubs.items():
                if var.get():  # If club is selected
                    try:
                        yardage = float(self.distance_entries[club].get())
                        available_clubs[club] = yardage
                    except ValueError:
                        messagebox.showerror("Invalid Input", f"Please enter a valid number for {club} distance.")
                        return

            if not available_clubs:
                messagebox.showwarning("No Clubs Selected", "Please select at least one club!")
                return

            # Find the best club based on distance
            recommended_club = None
            for club, yardage in sorted(available_clubs.items(), key=lambda x: -x[1]):
                if distance >= yardage:
                    recommended_club = club
                    break

            # Display the recommendation
            if recommended_club:
                messagebox.showinfo("Recommended Club", f"Virtual Caddy suggests using your {recommended_club}!")
            else:
                messagebox.showinfo("Recommended Club", "Use your highest lofted club for a short shot!")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for distance.")

    def reset_distances(self):
        """Resets the distances to their default values."""
        for club, default_yardage in self.default_distances.items():
            self.distance_entries[club].delete(0, tk.END)
            self.distance_entries[club].insert(0, str(default_yardage))

# Run the GUI
root = tk.Tk()
app = VirtualCaddy(root)
root.mainloop()
