import customtkinter as ctk
import psutil
import pynvml # NVIDIA GPU kütüphanesi

# --- 1. Arayüz ve Tema Ayarları (UI & Theme Setup) ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("450x650") # GPU barları için boyutu biraz artırdık
app.title("System Monitor Pro - Ultimate Edition")

# --- 2. GPU Başlatma Kontrolü (NVIDIA Initialization) ---
gpu_available = False
try:
    pynvml.nvmlInit()
    gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0) # İlk ekran kartını seç
    gpu_name = pynvml.nvmlDeviceGetName(gpu_handle)
    gpu_available = True
except Exception:
    gpu_available = False

# --- 3. Sabit Donanım Bilgileri (Static Hardware Info) ---
cpu_cores = psutil.cpu_count(logical=True)
total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)

# --- 4. ARAYÜZ ELEMANLARI (GUI Elements) ---

# Donanım Özet Yazısı
info_text = f"CPU Cores: {cpu_cores} | RAM: {total_ram_gb:.1f} GB"
if gpu_available:
    info_text += f" | GPU: {gpu_name}"

hardware_info_label = ctk.CTkLabel(app, text=info_text, font=("Arial", 11), text_color="gray")
hardware_info_label.pack(pady=15)

# CPU Bölümü
cpu_usage_label = ctk.CTkLabel(app, text="CPU Usage: 0%", font=("Arial", 15, "bold"))
cpu_usage_label.pack(pady=(10, 5))
cpu_progress_bar = ctk.CTkProgressBar(app, width=350)
cpu_progress_bar.pack(pady=5)
cpu_progress_bar.set(0)

# RAM Bölümü
ram_usage_label = ctk.CTkLabel(app, text="RAM Usage: 0%", font=("Arial", 15, "bold"))
ram_usage_label.pack(pady=(20, 5))
ram_progress_bar = ctk.CTkProgressBar(app, width=350)
ram_progress_bar.pack(pady=5)
ram_progress_bar.set(0)
ram_details_label = ctk.CTkLabel(app, text="Used RAM: 0 GB", font=("Arial", 11))
ram_details_label.pack(pady=5)

# --- GPU Bölümü (NVIDIA Specific) ---
# Eğer GPU varsa barları oluştur, yoksa uyarı yazısı göster
if gpu_available:
    # GPU Usage
    gpu_usage_label = ctk.CTkLabel(app, text="GPU Usage: 0%", font=("Arial", 15, "bold"), text_color="#10eb43") # NVIDIA Yeşili
    gpu_usage_label.pack(pady=(30, 5))
    gpu_progress_bar = ctk.CTkProgressBar(app, width=350, progress_color="#10eb43")
    gpu_progress_bar.pack(pady=5)
    gpu_progress_bar.set(0)

    # VRAM Usage
    vram_usage_label = ctk.CTkLabel(app, text="VRAM Usage: 0 GB", font=("Arial", 11))
    vram_usage_label.pack(pady=5)
else:
    # GPU Yoksa Uyarı Yazısı
    no_gpu_label = ctk.CTkLabel(app, text="GPU Monitoring: Only works with NVIDIA GPUs", 
                                font=("Arial", 13, "italic"), text_color="orange")
    no_gpu_label.pack(pady=50)

# --- 5. Ana Güncelleme Döngüsü (Main Update Loop) ---
def update_system_stats():
    # CPU & RAM Update
    current_cpu = psutil.cpu_percent()
    current_ram_pct = psutil.virtual_memory().percent
    used_ram_gb = psutil.virtual_memory().used / (1024 ** 3)
    
    cpu_progress_bar.set(current_cpu / 100)
    ram_progress_bar.set(current_ram_pct / 100)
    
    cpu_usage_label.configure(text=f"CPU Usage: {current_cpu}%")
    ram_usage_label.configure(text=f"RAM Usage: {current_ram_pct}%")
    ram_details_label.configure(text=f"Used RAM: {used_ram_gb:.2f} GB / {total_ram_gb:.1f} GB")
    
    # GPU Update (Sadece varsa)
    if gpu_available:
        try:
            utilization = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle)
            memory_info = pynvml.nvmlDeviceGetMemoryInfo(gpu_handle)
            
            gpu_pct = utilization.gpu
            vram_used = memory_info.used / (1024 ** 3)
            vram_total = memory_info.total / (1024 ** 3)
            
            gpu_progress_bar.set(gpu_pct / 100)
            gpu_usage_label.configure(text=f"GPU Usage: {gpu_pct}%")
            vram_usage_label.configure(text=f"VRAM Usage: {vram_used:.2f} GB / {vram_total:.2f} GB")
        except:
            pass

    app.after(1000, update_system_stats)

update_system_stats()
app.mainloop()

# Uygulama kapandığında NVIDIA kütüphanesini düzgünce kapat
if gpu_available:
    pynvml.nvmlShutdown()