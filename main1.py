import tkinter as tk
from tkinter import StringVar, Entry, Button, Text
import threading
import time

class AssistantApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Virtual Assistant")
        self.geometry("500x600")
        self.configure(bg="#0d1117")

        # Heading
        tk.Label(
            self, text="Virtual Assistant Simulator",
            font=("Inter", 24, "bold"), fg="#818cf8", bg="#0d1117"
        ).pack(pady=(20, 10))

        # Central animated circle
        self.canvas = tk.Canvas(self, width=120, height=120, bg="#0d1117", highlightthickness=0)
        self.canvas.pack(pady=15)
        self.circle = self.canvas.create_oval(15, 15, 105, 105, fill="#6366f1", outline="")
        self.pulse_running = False

        # Status & Output
        self.status_var = StringVar(value="Ready. Click the icon or ask a question!")
        tk.Label(self, textvariable=self.status_var, font=("Inter", 15, "bold"),
                 fg="#c7d2fe", bg="#1e293b", width=38, anchor="center"
        ).pack(pady=(16,3))
        self.output_text = Text(self, height=4, width=55, bg="#1e293b", fg="#a1a1aa",
                                font=("Inter", 12), bd=0)
        self.output_text.pack(pady=(0, 15))
        self.output_text.config(state='disabled')

        # Input & Button
        self.input_var = StringVar()
        frame = tk.Frame(self, bg="#0d1117")
        frame.pack(pady=8)
        self.input_entry = Entry(
            frame, textvariable=self.input_var, font=("Inter", 12),
            width=30, bg="#27272a", fg="white", bd=2, relief='groove'
        )
        self.input_entry.grid(row=0, column=0, ipady=7)
        self.input_entry.bind("<Return>", lambda e: self.start_processing())
        self.send_btn = Button(
            frame, text="Send", font=("Inter", 12, "bold"),
            command=self.start_processing, bg="#6366f1", fg="white", relief="raised", width=10
        )
        self.send_btn.grid(row=0, column=1, padx=4, ipadx=6, ipady=5)

        # Enable clickable circle
        self.canvas.bind("<Button-1>", lambda e: self.start_processing())

    def animate_pulse(self, grow=True, step=0):
        if not self.pulse_running:
            return
        # Pulsing effect by resizing circle
        scale = 0.7 + 0.3 * abs((step % 40) / 20 - 1) # scale 0.7 to 1.0
        color = "#6366f1" if step % 60 < 30 else "#fb923c" if step % 90 < 60 else "#22c55e"
        self.canvas.coords(self.circle, 60-45*scale, 60-45*scale, 60+45*scale, 60+45*scale)
        self.canvas.itemconfig(self.circle, fill=color)
        self.after(50, lambda: self.animate_pulse(grow=True, step=step+1))

    def start_processing(self):
        if getattr(self, "is_processing", False):
            return
        self.is_processing = True
        self.status_var.set(f'Receiving: "{self.input_var.get().strip() or "Find a fun fact about space."}"')
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')
        self.input_entry.config(state='disabled')
        self.send_btn.config(state='disabled')
        self.send_btn.config(text="Wait...")
        self.pulse_running = True
        self.animate_pulse()
        threading.Thread(target=self.process_request, daemon=True).start()

    def process_request(self):
        query = self.input_var.get().strip() or "Find a fun fact about space."
        time.sleep(1.5)
        self.status_var.set("Processing request and querying database...")
        time.sleep(2.5)
        self.status_var.set("Compiling and formulating response...")
        time.sleep(2)
        response = self.simulated_response(query)
        self.status_var.set("Response Generated.")
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, f"Assistant: {response}")
        self.output_text.config(state='disabled')
        time.sleep(1)
        # Reset UI
        self.pulse_running = False
        self.canvas.itemconfig(self.circle, fill="#6366f1")
        self.canvas.coords(self.circle, 15, 15, 105, 105)
        self.status_var.set("Ready. Click the icon or send a new request.")
        self.input_entry.config(state='normal')
        self.send_btn.config(state='normal')
        self.send_btn.config(text="Send")
        self.is_processing = False

    def simulated_response(self, query):
        lower = query.lower()
        if "capital of india" in lower:
            return "The capital of india is Delhi."
        elif "time" in lower:
            return f"The current time is {time.strftime('%H:%M:%S')}."
        elif "fun fact" in lower or "space" in lower:
            return ("A fun fact about space is that a day on Venus is longer than its year. "
                    "It takes 243 Earth days for Venus to complete one rotation, but only 225 "
                    "Earth days to orbit the Sun.")
        elif "your name" in lower:
            return "I am a Virtual Assistant Simulator created to demonstrate real-time processing and animation."
        else:
            return ("I have completed the task. Please provide a more detailed query "
                    "for a richer response, such as a math problem or a definition.")

if __name__ == "__main__":
    AssistantApp().mainloop()
