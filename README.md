# 📊 System Monitor

A sleek, lightweight, and standalone desktop application built with Python to monitor your system's hardware resources in real-time. 

![System Monitor Screenshot](https://github.com/user-attachments/assets/8fa979bc-3a3f-4d04-bc6c-1fb3719412ec)

## 🚀 Features
* **Real-Time Tracking:** Live monitoring of CPU and RAM usage percentages.
* **Hardware Specs:** Automatically detects and displays total CPU cores and physical RAM capacity.
* **Modern UI/UX:** Built with `customtkinter` for a native dark-mode experience and smooth progress bars.
* **Standalone Operation:** Requires no third-party background services or WMI workarounds. Pure Python efficiency.

## 🛠️ Technologies Used
* **Python 3.x** - Core logic
* **psutil** - For cross-platform system monitoring and hardware data extraction
* **CustomTkinter** - For the modern, hardware-accelerated graphical user interface

## ⚙️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zalialgl/system-monitor.git

2. **Install the required dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt

3. **Run the Application**
   ```bash
   python main.py
