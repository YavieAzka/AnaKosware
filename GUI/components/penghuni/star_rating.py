# components/star_rating.py
import tkinter as tk

class StarRating(tk.Frame):
    """Component for star rating"""

    def __init__(self, master, rating_variable, max_stars=5):
        super().__init__(master, bg='white')
        
        self.rating_variable = rating_variable
        self.max_stars = max_stars
        self.star_buttons = []

        self.create_stars()

    def create_stars(self):
        """Create the star buttons for rating"""
        for i in range(1, self.max_stars + 1):
            button = tk.Button(
                self, 
                text="★", 
                font=('Arial', 18), 
                fg="systemButtonFace",  # Use systemButtonFace to simulate transparency
                bg='white', 
                activebackground='white', 
                relief="flat", 
                command=lambda i=i: self.set_rating(i)
            )
            button.grid(row=0, column=i-1, padx=5)
            self.star_buttons.append(button)

    def set_rating(self, rating_value):
        """Set the rating when a star is clicked"""
        self.rating_variable.set(rating_value)

        # Update the color of the stars based on the rating
        for i, button in enumerate(self.star_buttons):
            if i < rating_value:
                button.config(fg="#F7D116")  # Yellow color for selected stars
            else:
                button.config(fg="systemButtonFace")  # Reset to default color (transparent-like effect)
