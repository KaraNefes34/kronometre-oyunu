import tkinter as tk
import time
import pygame

pygame.init()
try:
    siren = pygame.mixer.Sound("siren.wav")
except:
    siren = None

LEVELS = [("Kolay", 0.15), ("Orta", 0.05), ("Zor", 0.01), ("Efsanevi", 0.0)]

def get_funny_comment(diff):
    abs_diff = abs(diff)
    if abs_diff < 0.01:
        return "🚨 TAM İSABET! 🚨"
    elif diff < 0:
        return f"⏱ {abs_diff:.2f} sn erken bastın!"
    else:
        return f"⏱ {abs_diff:.2f} sn geç kaldın!"

class StopwatchGame:
    def __init__(self, root):
        self.root = root
        self.root.title("LED Zaman Oyunu")
        self.root.geometry("820x480")
        self.root.configure(bg="black")

        self.running = False
        self.start_time = None
        self.elapsed = 0

        self.level_index = 1  # Orta seviye
        self.level_name, self.tolerance = LEVELS[self.level_index]
        self.target_seconds = 5
        self.target_millis = 90

        self.create_menu()

        # Ana çerçeve
        self.frame = tk.Frame(root, bg="gray20", bd=30, relief="ridge")
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)

        # LED ekran
        self.label = tk.Label(self.frame, text="00:00", font=("Courier", 180, "bold"),
                              fg="red", bg="black")
        self.label.pack(pady=(1, 0))

        # Butonlar
        self.button = tk.Button(self.frame, text="▶ BAŞLAT / ⏹ DUR / 🔄 SIFIRLA", command=self.toggle,
                                bg="white", fg="green", font=("Arial", 20, "bold"))
        self.button.pack(pady=3)

        # Sonuç etiketi
        self.result = tk.Label(self.frame, text="", font=("Arial", 18, "bold"),
                               fg="red", bg="black", wraplength=1100, justify="center")
        self.result.pack(pady=(5, 10))

        self.update()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="⚙ Ayarlar", menu=settings_menu)
        settings_menu.add_command(label="Seviye Ayarı", command=self.open_level_dialog)
        settings_menu.add_command(label="Hedef Süre Ayarı", command=self.open_target_dialog)

    def open_level_dialog(self):
        window = tk.Toplevel(self.root)
        window.title("Seviye Ayarı")
        window.configure(bg="black")
        window.geometry("300x180")

        tk.Label(window, text="Seviye Seç:", font=("Arial", 15), bg="black", fg="white").pack(pady=10)
        level_var = tk.StringVar(value=self.level_name)

        for name, _ in LEVELS:
            tk.Radiobutton(window, text=name, variable=level_var, value=name,
                           font=("Arial", 12), bg="black", fg="white", selectcolor="gray20").pack(anchor="w")

        def apply_level():
            for i, (name, tol) in enumerate(LEVELS):
                if level_var.get() == name:
                    self.level_index = i
                    self.level_name, self.tolerance = name, tol
                    break
            window.destroy()

        tk.Button(window, text="Uygula", command=apply_level,
                  font=("Arial", 12, "bold")).pack(pady=10)

    def open_target_dialog(self):
        window = tk.Toplevel(self.root)
        window.title("Hedef Süre Ayarı")
        window.configure(bg="red")
        window.geometry("300x150")

        tk.Label(window, text="Hedef Süre (SS:MS)", font=("Arial", 14), bg="black", fg="white").pack(pady=10)
        frame = tk.Frame(window, bg="black")
        frame.pack()

        sec_spin = tk.Spinbox(frame, from_=0, to=99, width=3, font=("Arial", 14))
        sec_spin.delete(0, "end")
        sec_spin.insert(0, f"{self.target_seconds:02}")
        sec_spin.pack(side="left", padx=5)

        tk.Label(frame, text=":", font=("Arial", 14), bg="black", fg="white").pack(side="left")

        millis_spin = tk.Spinbox(frame, from_=0, to=99, width=3, font=("Arial", 14))
        millis_spin.delete(0, "end")
        millis_spin.insert(0, f"{self.target_millis:02}")
        millis_spin.pack(side="left", padx=5)

        def apply_target():
            self.target_seconds = int(sec_spin.get())
            self.target_millis = int(millis_spin.get())
            window.destroy()

        tk.Button(window, text="Uygula", command=apply_target,
                  font=("Arial", 12, "bold")).pack(pady=10)

    def toggle(self):
        if not self.running and self.elapsed == 0:
            self.start()
        elif self.running:
            self.stop()
        else:
            self.reset()

    def start(self):
        self.running = True
        self.start_time = time.time() - self.elapsed
        self.result.config(text="")

    def stop(self):
        self.running = False
        self.elapsed = time.time() - self.start_time
        diff = self.elapsed - (self.target_seconds + self.target_millis / 100)
        comment = get_funny_comment(diff)
        self.result.config(text=comment)
        if abs(diff) <= self.tolerance and siren:
            siren.play()

    def reset(self):
        self.elapsed = 0
        self.label.config(text="00:00")
        self.result.config(text="")

    def update(self):
        if self.running:
            self.elapsed = time.time() - self.start_time
        secs = int(self.elapsed % 100)
        millisec = int((self.elapsed * 100) % 100)
        self.label.config(text=f"{secs:02}:{millisec:02}")
        self.root.after(50, self.update)

# Uygulama başlat
root = tk.Tk()
app = StopwatchGame(root)
root.mainloop()
