import tkinter as tk
import os

def run_user_script():
    os.system("python user.py")

def run_auto_script():
    os.system("python auto.py")

root = tk.Tk()
root.title("2048 Game")
root.configure(bg='#ffffcc')  # Set background color to a light shade of yellow

# Increase window size and set position
root.geometry("400x150+100+100")

# Create a frame to hold the buttons and place it in the root window
frame = tk.Frame(root, bg='#ffffcc')
frame.pack()

# Add heading
heading_label = tk.Label(frame, text="2048 Game", bg='#ffffcc', fg='orange', font=("Arial", 14, "bold"))
heading_label.pack(side=tk.TOP, pady=10)  # Pack the heading label to the top with padding

user_button = tk.Button(frame, text="User", command=run_user_script, bg='orange', fg='white', font=("Arial", 12, "bold"))  # Set button color to orange with white text
user_button.pack(side=tk.LEFT, padx=20, pady=(0, 10))  # Pack the button to the left with padding and a specific vertical padding

auto_button = tk.Button(frame, text="Auto", command=run_auto_script, bg='orange', fg='white', font=("Arial", 12, "bold"))  # Set button color to orange with white text
auto_button.pack(side=tk.LEFT, padx=20, pady=(0, 10))  # Pack the button to the left with padding and a specific vertical padding

# Adjust bottom padding to move the buttons closer to the bottom border
frame.pack_configure(pady=10)

root.mainloop()
