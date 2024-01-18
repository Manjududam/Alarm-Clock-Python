import tkinter as tk
from tkinter import messagebox
import time
from threading import Thread

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")
        self.root.geometry("400x350")

        self.current_time_label = tk.Label(root, text="")
        self.current_time_label.pack(pady=10)

        self.label = tk.Label(root, text="Set Alarm Time (HH:MM:SS):")
        self.label.pack(pady=5)

        self.entry = tk.Entry(root)
        self.entry.pack(pady=5)

        self.set_alarm_button = tk.Button(root, text="Set Alarm", command=self.set_alarm)
        self.set_alarm_button.pack(pady=10)

        self.delete_alarm_button = tk.Button(root, text="Delete Alarm", command=self.delete_alarm)
        self.delete_alarm_button.pack(pady=5)

        self.stop_alarm_button = tk.Button(root, text="Stop Alarm", command=self.stop_alarm, state=tk.DISABLED)
        self.stop_alarm_button.pack(pady=5)

        self.alarm_thread = None
        self.alarms = []

        self.update_time()
        self.root.after(1000, self.update_time)

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.current_time_label.config(text=f"Current Time: {current_time}")
        self.root.after(1000, self.update_time)

    def set_alarm(self):
        alarm_time = self.entry.get()

        try:
            time.strptime(alarm_time, "%H:%M:%S")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM:SS.")
            return

        if alarm_time in self.alarms:
            messagebox.showinfo("Info", "Alarm already set for this time.")
        else:
            self.alarms.append(alarm_time)
            messagebox.showinfo("Info", f"Alarm set for {alarm_time}.")
            self.update_buttons_state()

    def delete_alarm(self):
        alarm_time = self.entry.get()

        if alarm_time in self.alarms:
            self.alarms.remove(alarm_time)
            messagebox.showinfo("Info", f"Alarm deleted for {alarm_time}.")
            self.update_buttons_state()
        else:
            messagebox.showinfo("Info", "No alarm set for this time.")

    def stop_alarm(self):
        if self.alarm_thread and self.alarm_thread.is_alive():
            self.alarm_thread = None
            messagebox.showinfo("Info", "Alarm stopped.")
            self.update_buttons_state()

    def play_alarm(self):
        messagebox.showinfo("Alarm", "Time to wake up!")

    def wait_for_alarm(self, alarm_time):
        current_time = time.strftime("%H:%M:%S")

        while current_time != alarm_time:
            time.sleep(1)
            current_time = time.strftime("%H:%M:%S")

        if self.alarm_thread and self.alarm_thread.is_alive():
            self.play_alarm()
            self.alarm_thread = None
            self.update_buttons_state()

    def update_buttons_state(self):
        if self.alarms and not self.alarm_thread:
            self.stop_alarm_button.config(state=tk.NORMAL)
        else:
            self.stop_alarm_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()
