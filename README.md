# EEG Signal Visualizer – Hackathon Project

## 📌 Introduction
This project simulates a **real-time EEG monitoring system**.  
It loads previously recorded **40-channel bio-signals** (sampled at 50 Hz) from a CSV file and visualizes them in two ways:
1. **Heatmap** – Displays all 40 channels' intensities live in a 5×8 grid.
2. **Waveform Plot** – Shows the real-time signal of a selected channel.

It works like a simplified medical device monitor with interactive controls for play, pause, restart, seek, and waveform export.

---

## 🚀 Features
- **Live Heatmap View** – Updates 50 times/sec, with flicker effect for a realistic feel.
- **Interactive Channel Selection** – Click any heatmap cell to view its waveform.
- **Smooth Waveform Scrolling** – Displays last 4 seconds of data.
- **Playback Controls** – Play, Pause, Restart, and Seek.
- **Export Functionality** – Save any waveform snapshot as a PNG.
- **Timestamp & Status Display** – Shows time and device status (color-coded).

---

## 📂 Dataset Structure
CSV file format:
- **Timestamp** – Time of capture
- **Status** – Device state (e.g., "OK")
- **Ch1–Ch40** – Channel values (0 – 65,000)
- **Sampling Rate** – 50 Hz (one row every 0.02 s)

---

## 🛠 Tech Stack
- **Python**
- **Tkinter** – GUI
- **Matplotlib** – Waveform plotting
- **NumPy** – Data handling
- **CSV Module** – File reading
- **Random (NumPy)** – Flicker effect

---

## 📷 Demo
**Heatmap:**  
Shows all 40 channels in real time.  
**Waveform Plot:**  
Displays selected channel with smooth scrolling.

---

## 📜 Usage
1. Place your CSV dataset in the working directory.
2. Run the script:
   ```bash
   python eeg_visualizer.py
3. Use the GUI to:
   - Select a channel
   - Control playback
   - Export waveform images

---

## 🔮 Future Improvements
- Live streaming from real EEG hardware
- Additional color themes
- Multi-patient monitoring   

---

# Acknowledgments
Thanks to Apple and Berry Pvt for giving this task

---

## 📄 License
This project is for practical nd demonstration purposes only. Please credit the authors if reused or modified.

---

<img width="940" height="504" alt="image" src="https://github.com/user-attachments/assets/7405b011-e4d6-447e-8730-f2282281452a" />

<img width="621" height="328" alt="image" src="https://github.com/user-attachments/assets/4e124680-2320-403f-933c-3b4b061110ac" />

<img width="467" height="368" alt="image" src="https://github.com/user-attachments/assets/dd9770c9-9f56-4a77-abed-fb5ff042827b" />



