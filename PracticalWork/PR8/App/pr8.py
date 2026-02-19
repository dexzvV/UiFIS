import tkinter as tk
from tkinter import messagebox, ttk
import requests
from datetime import datetime


class DeliveryService:
    def get_coordinates(self, address):
        if (
            "," in address
            and address.replace(".", "").replace(",", "").replace(" ", "").isdigit()
        ):
            return address.strip()

        url = f"https://nominatim.openstreetmap.org/search?format=json&q={address}"
        headers = {"User-Agent": "DeliveryCalcApp/1.0"}
        response = requests.get(url, headers=headers).json()

        if response:
            return f"{response[0]['lat']},{response[0]['lon']}"
        raise Exception(f"Адрес '{address}' не найден")

    def get_route(self, start_coords, end_coords):
        start = ",".join(reversed(start_coords.split(",")))
        end = ",".join(reversed(end_coords.split(",")))

        url = f"http://router.project-osrm.org/route/v1/driving/{start};{end}?overview=false"
        response = requests.get(url).json()

        if response["code"] == "Ok":
            route = response["routes"][0]
            distance_km = route["distance"] / 1000
            duration_min = route["duration"] / 60
            return distance_km, duration_min
        raise Exception("Не удалось проложить маршрут")


class DeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор доставки")
        self.service = DeliveryService()

        self.tariffs = {
            "Автомобиль (40 руб./км)": 40,
            "Грузовик (60 руб./км)": 60,
            "Мотоцикл (25 руб./км)": 25,
        }

        self.setup_ui()

    def setup_ui(self):
        frame_input = tk.LabelFrame(
            self.root, text="Параметры доставки", padx=10, pady=10
        )
        frame_input.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_input, text="Пункт отправления:").grid(
            row=0, column=0, sticky="w"
        )
        self.entry_from = tk.Entry(frame_input, width=50)
        self.entry_from.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_input, text="Пункт назначения:").grid(
            row=1, column=0, sticky="w"
        )
        self.entry_to = tk.Entry(frame_input, width=50)
        self.entry_to.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_input, text="Тип транспорта:").grid(row=2, column=0, sticky="w")
        self.combo_transport = ttk.Combobox(
            frame_input, values=list(self.tariffs.keys()), state="readonly"
        )
        self.combo_transport.current(0)
        self.combo_transport.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        btn_calc = tk.Button(frame_input, text="Рассчитать", command=self.calculate)
        btn_calc.grid(row=2, column=1, sticky="e")

        self.txt_result = tk.Text(self.root, height=8, width=70)
        self.txt_result.pack(padx=10, pady=5)

        tk.Label(self.root, text="История расчетов:").pack(anchor="w", padx=10)
        self.history_tree = ttk.Treeview(
            self.root,
            columns=("Time", "From", "To", "Vehicle", "Cost"),
            show="headings",
            height=5,
        )
        for col in ("Time", "From", "To", "Vehicle", "Cost"):
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
        self.history_tree.pack(fill="both", padx=10, pady=5)

    def calculate(self):
        try:
            start_addr = self.entry_from.get()
            end_addr = self.entry_to.get()

            if not start_addr or not end_addr:
                messagebox.showwarning("Ошибка", "Заполните оба пункта!")
                return

            start_coords = self.service.get_coordinates(start_addr)
            end_coords = self.service.get_coordinates(end_addr)
            dist, duration = self.service.get_route(start_coords, end_coords)

            tariff_name = self.combo_transport.get()
            price_per_km = self.tariffs[tariff_name]
            total_cost = dist * price_per_km

            res_text = (
                f"Откуда: {start_addr}\nКуда: {end_addr}\n"
                f"Дистанция: {dist:.2f} км\nВремя: {int(duration)} мин\n"
                f"Стоимость: {total_cost:.2f} руб."
            )
            self.txt_result.delete("1.0", tk.END)
            self.txt_result.insert(tk.END, res_text)

            now = datetime.now().strftime("%H:%M:%S")
            self.history_tree.insert(
                "",
                0,
                values=(
                    now,
                    start_addr[:15],
                    end_addr[:15],
                    tariff_name.split()[0],
                    f"{total_cost:.0f} руб.",
                ),
            )

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = DeliveryApp(root)
    root.mainloop()
