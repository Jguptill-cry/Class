import tkinter as tk
from tkinter import messagebox

class VirtualCaddy:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Caddy - Golf Club Selector")

        # Set the background color of the root window to green
        self.root.configure(bg='green')

        # Default distances
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

        # Initialize distances (default to the default values)
        self.club_distances = self.default_distances.copy()

        # Show the initial distance setup window
        self.show_setup_window()

    def show_setup_window(self):
        """Creates the setup window where user can enter distances for each club."""
        self.setup_window = tk.Toplevel(self.root)
        self.setup_window.title("Set Club Distances")

        # Set the background color of the setup window to green
        self.setup_window.configure(bg='green')

        # Instructions and Entry Fields
        tk.Label(self.setup_window, text="Enter the distances for each club (yards):", font=("Arial", 12), bg='green', fg='white').pack(pady=5)

        # Create entry fields for each club
        self.distance_entries = {}
        for club, default_yardage in self.default_distances.items():
            frame = tk.Frame(self.setup_window, bg='green')
            frame.pack(anchor="w")

            tk.Label(frame, text=club, width=15, anchor="w", bg='green', fg='white').pack(side="left")

            entry = tk.Entry(frame, width=5)
            entry.insert(0, str(default_yardage))  # Set default distance
            entry.pack(side="right")
            self.distance_entries[club] = entry

        # Add buttons to increase or decrease all distances by 10 yards
        self.inc_button = tk.Button(self.setup_window, text="Increase All Distances by 10", command=self.increase_all_distances, bg='darkgreen', fg='white')
        self.inc_button.pack(pady=5)

        self.dec_button = tk.Button(self.setup_window, text="Decrease All Distances by 10", command=self.decrease_all_distances, bg='darkgreen', fg='white')
        self.dec_button.pack(pady=5)

        # Button to save distances and proceed to the next window
        self.submit_button = tk.Button(self.setup_window, text="Submit", command=self.submit_distances, bg='darkgreen', fg='white')
        self.submit_button.pack(pady=10)

    def increase_all_distances(self):
        """Increases all club distances by 10 yards."""
        for club in self.distance_entries:
            # Get the current value in the entry field and add 10 to it
            try:
                current_value = float(self.distance_entries[club].get())
                new_value = current_value + 10
                self.distance_entries[club].delete(0, tk.END)
                self.distance_entries[club].insert(0, str(new_value))
            except ValueError:
                # If the value is not a valid number, ignore
                pass

    def decrease_all_distances(self):
        """Decreases all club distances by 10 yards."""
        for club in self.distance_entries:
            # Get the current value in the entry field and subtract 10 from it
            try:
                current_value = float(self.distance_entries[club].get())
                new_value = current_value - 10
                self.distance_entries[club].delete(0, tk.END)
                self.distance_entries[club].insert(0, str(new_value))
            except ValueError:
                # If the value is not a valid number, ignore
                pass

    def submit_distances(self):
        """Save the distances entered by the user and proceed to the next screen."""
        try:
            # Save the distances entered by the user
            for club, entry in self.distance_entries.items():
                distance = float(entry.get())
                if distance <= 0:
                    raise ValueError(f"Invalid distance for {club}.")
                self.club_distances[club] = distance

            # Close the setup window
            self.setup_window.destroy()

            # Show the main recommendation window
            self.show_main_window()

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def show_main_window(self):
        """Create the main window where the user can input the target distance and get recommendations."""
        self.main_window = tk.Toplevel(self.root)
        self.main_window.title("Virtual Caddy - Club Recommendation")

        # Set the background color of the main window to green
        self.main_window.configure(bg='green')

        # Instructions for the target distance input
        tk.Label(self.main_window, text="Enter distance to target (yards):", font=("Arial", 12), bg='green', fg='white').pack(pady=5)

        # Distance to target input
        self.target_distance_entry = tk.Entry(self.main_window)
        self.target_distance_entry.pack(pady=5)

        # Button to get recommended club
        self.submit_button = tk.Button(self.main_window, text="Find Club", command=self.recommend_club, bg='darkgreen', fg='white')
        self.submit_button.pack(pady=5)

        # Button to reset the distances
        self.reset_button = tk.Button(self.main_window, text="Reset to Defaults", command=self.reset_distances, bg='darkgreen', fg='white')
        self.reset_button.pack(pady=5)

    def recommend_club(self):
        """Determines the best club based on the target distance and available clubs."""
        try:
            distance = float(self.target_distance_entry.get())
            available_clubs = {club: dist for club, dist in self.club_distances.items()}

            if not available_clubs:
                messagebox.showwarning("No Clubs Available", "Please set the distances for clubs first!")
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
            messagebox.showerror("Invalid Input", "Please enter a valid number for the distance to target.")

    def reset_distances(self):
        """Resets the distances to their default values."""
        self.club_distances = self.default_distances.copy()
        messagebox.showinfo("Reset", "Club distances have been reset to default values.")

# Run the GUI
root = tk.Tk()
app = VirtualCaddy(root)
root.mainloop()

