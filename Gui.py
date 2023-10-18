import serial
import tkinter as tk

# Open the serial port (replace '/dev/ttyACM0' with the correct port)
se = serial.Serial('/dev/ttyACM0', 9600, timeout=1.0)

print("Serial port opened.")

root = tk.Tk()
root.title("Data Log")

# Set the dimensions of the GUI window
root.geometry("800x400")  # Width x Height

# Create a Text widget to display the log
log_text = tk.Text(root, wrap=tk.WORD)
log_text.pack(fill=tk.BOTH, expand=True)

# Variables to keep track of log entries and the current set
log_entries = []
current_set = []

# Function to add a new log entry
def add_log_entry(data):
    log_entries.append(data)

# Function to add an empty line
def add_empty_line():
    log_entries.append("")

# Function to clear and auto-scroll the log
def update_log():
    arduino_data = se.readline().decode('utf-8').strip()
    if arduino_data:
        print("Data from Arduino:", arduino_data)

        # Check if it's the end of the set (i.e., "PF")
        if "PF" in arduino_data:
            # Add the current set entries to the log
            add_log_entry("Data from Arduino: " + "\n".join(current_set))
            add_empty_line()

            # Clear the current set
            current_set.clear()
        
        # Add the data to the current set
        current_set.append(arduino_data)

        # Check if the log text exceeds the visible window area
        if float(log_text.index(tk.END)) - float(log_text.index('1.0')) > log_text.winfo_height():
            log_text.delete('1.0', '2.0')  # Remove the first line to create an auto-scroll effect

        log_text.see(tk.END)  # Auto-scroll to the end
    root.after(1, update_log)  # Update as frequently as possible

# Start updating the log
update_log()

root.mainloop()
