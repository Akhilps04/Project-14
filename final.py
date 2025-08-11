import tkinter as tk
import csv
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# ---------------- Load and clean the data ----------------
timestamps = []
statuses = []
data = []

with open("C:/Users/HP/Desktop/Hackathon/Raw_Data_20250711_193117-hack.csv", newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        try:
            timestamps.append(row[0])       # First column (timestamp)
            statuses.append(row[1])         # Second column (status)
            values = [int(v) for v in row[2:]]  # 40 channels
            if len(values) == 40:
                data.append(values)
        except ValueError:
            continue

data = np.array(data)
frame_count = len(data)
window_size = 200

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("EEG Signal Visualizer")
root.configure(bg="white")

# Application heading
top_frame = tk.Frame(root, bg="white")
top_frame.pack(side=tk.TOP, pady=10)

app_heading = tk.Label(
    top_frame,
    text="EEG Signal Visualizer - Hackathon Project",
    font=("Segoe UI", 16, "bold"),
    fg="blue",
    bg="white"
)
app_heading.pack()

left_frame = tk.Frame(root, bg="white")
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

right_frame = tk.Frame(root, bg="white")
right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

bottom_frame = tk.Frame(root, bg="white")
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

# ---------------- Variables ----------------
selected_channel = tk.IntVar(value=-1)
current_frame = 0
is_playing = False
user_dragging = False

# ---------------- Heatmap ----------------
cells = []
for i in range(5):
    row = []
    for j in range(8):
        index = i * 8 + j
        label = tk.Label(left_frame, text=f"Ch {index+1}", width=8, height=3,
                         relief="solid", bg="#f0f0f0", fg="black", font=("Segoe UI", 9, "bold"))
        label.grid(row=i, column=j, padx=2, pady=2)

        def on_click(event, idx=index):
            selected_channel.set(idx)
            channel_label.config(text=f"Selected Channel: {idx+1}")

        label.bind("<Button-1>", on_click)
        row.append(label)
    cells.append(row)

# ---------------- Matplotlib Plot ----------------
fig = Figure(figsize=(6, 4), dpi=100, facecolor="white")
ax = fig.add_subplot(111)
ax.set_title("Selected Channel Signal", color="black")
ax.set_xlabel("Time (frames)", color="black")
ax.set_ylabel("Value", color="black")
ax.tick_params(colors='black')
fig.subplots_adjust(left=0.15, bottom=0.15)
line, = ax.plot([], [], color='blue')

canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.draw()
canvas.get_tk_widget().pack()

channel_label = tk.Label(right_frame, text="Selected Channel: None", font=("Segoe UI", 12), fg="black", bg="white")
channel_label.pack(pady=5)

# --- NEW: Label for timestamp & status ---
frame_info_label = tk.Label(right_frame, text="", font=("Segoe UI", 10), fg="darkgreen", bg="white", anchor="w")
frame_info_label.pack(pady=2, fill=tk.X)

# ---------------- Functions ----------------
def update_display():
    if current_frame >= frame_count:
        return

    # --- Heatmap ---
    frame_data = data[current_frame]
    max_val, min_val = 65000, 0
    for i in range(5):
        for j in range(8):
            val = frame_data[i * 8 + j] + np.random.randint(-500, 500)  # Add small random change

            if max_val != min_val:
                scaled = (val - min_val) / (max_val - min_val)
                scaled = max(0, min(1, scaled))
                adjusted = scaled ** 0.5  # gamma dark
                norm = int(255 * (1 - adjusted))
            else:
                norm = 128

            norm = max(0, min(255, norm))
            color = f'#{norm:02x}{norm:02x}{norm:02x}'
            cells[i][j].config(bg=color)

    # --- Plot waveform ---
    if selected_channel.get() >= 0:
        ch = selected_channel.get()
        start = max(0, current_frame - window_size)
        y_vals = data[start:current_frame, ch]
        x_vals = np.arange(len(y_vals))
        line.set_data(x_vals, y_vals)
        ax.set_xlim(0, window_size)
        if len(y_vals) > 0:
            ax.set_ylim(np.min(data[:, ch]), np.max(data[:, ch]))
    canvas.draw_idle()

    # --- Update timestamp + status ---
    timestamp_label.config(text=f"{current_frame / 50:.2f}s / {frame_count / 50:.2f}s")
    if 0 <= current_frame < len(timestamps):
        status = statuses[current_frame]
        color = "green" if status.lower() == "ok" else "red"
        frame_info_label.config(
            text=f"Timestamp: {timestamps[current_frame]}   |   Status: {status}",
            fg=color
        )

def playback_loop():
    global current_frame
    if is_playing and not user_dragging:
        update_display()
        current_frame += 1
        if current_frame >= frame_count:
            pause()
            return
        seek_bar.set(current_frame)
    root.after(20, playback_loop)

def play():
    global is_playing
    if selected_channel.get() >= 0:
        is_playing = True

def pause():
    global is_playing
    is_playing = False

def restart():
    global current_frame, is_playing
    is_playing = False
    current_frame = 0
    seek_bar.set(0)
    update_display()

def on_seek(val):
    global current_frame
    if user_dragging:
        current_frame = int(float(val))
        update_display()

def start_drag(event):
    global user_dragging
    user_dragging = True

def stop_drag(event):
    global user_dragging, current_frame
    user_dragging = False
    current_frame = int(seek_bar.get())
    update_display()

def export_waveform():
    if selected_channel.get() < 0:
        return
    ch = selected_channel.get()
    start = max(0, current_frame - window_size)
    y_vals = data[start:current_frame, ch]
    x_vals = np.arange(len(y_vals))
    plt.figure()
    plt.plot(x_vals, y_vals)
    plt.title(f"Channel {ch+1} Waveform")
    plt.xlabel("Time (frames)")
    plt.ylabel("Value")
    filename = f"Channel_{ch+1}_waveform.png"
    plt.savefig(filename)
    plt.close()
    print(f"Exported waveform to {filename}")

# ---------------- Buttons & Seekbar ----------------
button_frame = tk.Frame(bottom_frame, bg="white")
button_frame.pack(side=tk.TOP, pady=5)

btn_style = {"font": ("Segoe UI", 10, "bold"), "padx": 10, "pady": 2}
tk.Button(button_frame, text="Play", bg="lightgreen", command=play, **btn_style).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Pause", bg="khaki", command=pause, **btn_style).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Restart", bg="salmon", command=restart, **btn_style).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Export Waveform", bg="skyblue", command=export_waveform, **btn_style).pack(side=tk.LEFT, padx=5)

seek_frame = tk.Frame(bottom_frame, bg="white")
seek_frame.pack(side=tk.TOP, pady=5, fill=tk.X)

tk.Label(seek_frame, text="Seek:", fg="black", bg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(10, 5))
seek_bar = tk.Scale(seek_frame, from_=0, to=frame_count-1, orient=tk.HORIZONTAL, length=400, command=on_seek)
seek_bar.pack(side=tk.LEFT, padx=10)

seek_bar.bind("<Button-1>", start_drag)
seek_bar.bind("<ButtonRelease-1>", stop_drag)

timestamp_label = tk.Label(seek_frame, text="0.00s / 0.00s", fg="black", bg="white", font=("Segoe UI", 10))
timestamp_label.pack(side=tk.LEFT)

# ---------------- Start ----------------
update_display()
playback_loop()
root.mainloop()
