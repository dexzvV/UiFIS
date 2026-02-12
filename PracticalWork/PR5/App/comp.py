import tkinter as tk
from tkinter import scrolledtext
import random
import time
import threading
from datetime import datetime


class NetworkTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("Сетевой терминал")
        self.root.geometry("800x650")
        self.running = False
        self.packet_count = 0
        self.devices = {
            "ПК1": (100, 100),
            "ПК2": (100, 300),
            "ПК3": (700, 100),
            "ПК4": (700, 300),
            "SWITCH": (400, 200),
        }
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, bg="white", height=400)
        self.canvas.pack(fill=tk.X, padx=10, pady=5)
        sw_x, sw_y = self.devices["SWITCH"]
        for name, pos in self.devices.items():
            if name != "SWITCH":
                self.canvas.create_line(
                    pos[0], pos[1], sw_x, sw_y, dash=(4, 4), fill="gray"
                )
        self.nodes = {}
        for name, (x, y) in self.devices.items():
            color = "#0078d7" if name == "SWITCH" else "#cccccc"
            node = self.canvas.create_rectangle(
                x - 25, y - 25, x + 25, y + 25, fill=color, outline="black"
            )
            self.canvas.create_text(x, y + 40, text=name, font=("Arial", 10, "bold"))
            self.nodes[name] = node
        self.console = scrolledtext.ScrolledText(
            self.root, bg="black", fg="#00ff00", height=10, font=("Consolas", 10)
        )
        self.console.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        self.btn_start = tk.Button(
            control_frame, text="Старт", command=self.start_simulation, width=10
        )
        self.btn_start.pack(side=tk.LEFT, padx=5)
        self.btn_stop = tk.Button(
            control_frame,
            text="Стоп",
            command=self.stop_simulation,
            width=10,
            state=tk.DISABLED,
        )
        self.btn_stop.pack(side=tk.LEFT, padx=5)
        tk.Label(control_frame, text="Пакетов в сек.:").pack(side=tk.LEFT, padx=5)
        self.speed_scale = tk.Spinbox(control_frame, from_=1, to=10, width=5)
        self.speed_scale.delete(0, "end")
        self.speed_scale.insert(0, "2")
        self.speed_scale.pack(side=tk.LEFT, padx=5)
        self.btn_clear = tk.Button(
            control_frame, text="Очистить", command=self.clear_console, width=10
        )
        self.btn_clear.pack(side=tk.RIGHT, padx=5)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.console.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console.see(tk.END)

    def animate_packet(self, p_id, start_node, end_node, size):
        start_coords = self.devices[start_node]
        sw_coords = self.devices["SWITCH"]
        end_coords = self.devices[end_node]
        p_color = random.choice(["#ff5722", "#4caf50", "#2196f3", "#9c27b0"])
        packet = self.canvas.create_oval(
            start_coords[0] - 10,
            start_coords[1] - 10,
            start_coords[0] + 10,
            start_coords[1] + 10,
            fill=p_color,
        )
        p_text = self.canvas.create_text(
            start_coords[0],
            start_coords[1],
            text=str(p_id),
            fill="white",
            font=("Arial", 8, "bold"),
        )
        self.log(f"Пакет #{p_id}: {start_node} -> {end_node}, Размер: {size} байт")
        self.move_object(packet, p_text, start_coords, sw_coords)
        if not self.running:
            return
        self.log(f"Пакет #{p_id} достиг SWITCH")
        start_time = time.time()
        self.move_object(packet, p_text, sw_coords, end_coords)
        if not self.running:
            return
        delay = int((time.time() - start_time) * 1000 + random.randint(50, 200))
        self.log(f"Пакет #{p_id} доставлен на {end_node} (задержка: {delay} мс)")
        self.canvas.delete(packet)
        self.canvas.delete(p_text)

    def move_object(self, obj, text, start, end, steps=15):
        dx = (end[0] - start[0]) / steps
        dy = (end[1] - start[1]) / steps
        for _ in range(steps):
            if not self.running:
                break
            self.canvas.move(obj, dx, dy)
            self.canvas.move(text, dx, dy)
            self.root.update()
            time.sleep(0.02)

    def simulation_loop(self):
        while self.running:
            self.packet_count += 1
            src = random.choice(["ПК1", "ПК2", "ПК3", "ПК4"])
            dest = random.choice([n for n in ["ПК1", "ПК2", "ПК3", "ПК4"] if n != src])
            size = random.randint(64, 1500)
            self.animate_packet(self.packet_count, src, dest, size)
            try:
                interval = 1.0 / int(self.speed_scale.get())
            except:
                interval = 0.5
            time.sleep(interval)

    def start_simulation(self):
        self.running = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        threading.Thread(target=self.simulation_loop, daemon=True).start()

    def stop_simulation(self):
        self.running = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.log("Передача пакетов остановлена")
        self.log(f"Всего передано пакетов: {self.packet_count}")

    def clear_console(self):
        self.console.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkTerminal(root)
    root.mainloop()
