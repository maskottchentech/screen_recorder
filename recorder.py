import tkinter as tk
import pyautogui
import cv2
import keyboard
import numpy as np
from tkinter import filedialog

def record_screen(tk_root):
    # Hide the tkinter window during the recording
    tk_root.iconify()

    # Get screen size
    screen_width = tk_root.winfo_screenwidth()
    screen_height = tk_root.winfo_screenheight()

    # Prompt user to select output file path
    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if not output_file:
        # User canceled, stop recording
        return

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, 20.0, (screen_width, screen_height))

    try:
        while True:
            # Capture screenshot
            img = pyautogui.screenshot()

            # Convert the screenshot to a numpy array representation
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

            # Write the frame to the video file
            out.write(frame)

            # Update the tkinter window to handle events and prevent "Not Responding" message
            tk_root.update()

            # Break the loop when 'Esc' is pressed
            if keyboard.is_pressed('Esc'):
                break
    finally:
        # Release the VideoWriter and destroy the OpenCV windows
        out.release()
        cv2.destroyAllWindows()

        # Show the tkinter window again after recording
        tk_root.deiconify()

def create_gui():
    # Create the main tkinter window
    root = tk.Tk()
    root.title("Screen Recorder")
    
    # Set the background color
    root.configure(bg="#f2f2f2")
    
    # Calculate the window position to center it
    window_width = 500
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Create a label widget
    label = tk.Label(root, text="Screen Recorder", font=("Arial", 20), fg="blue", bg="#f2f2f2")
    label.pack(pady=20)
    
    # Create a button widget
    button = tk.Button(root, text="Start Recording", font=("Arial", 16), fg="white", bg="green")
    button.pack(pady=10)
    
    # Function to start or stop recording
    def toggle_recording():
        if button["text"] == "Start Recording":
            button["text"] = "Stop Recording"
            record_screen(root)
            button["text"] = "Start Recording"
    
    # Bind the toggle_recording function to the button click event
    button.config(command=toggle_recording)
    
    # Run the tkinter event loop
    root.mainloop()

# Create the GUI
create_gui()
