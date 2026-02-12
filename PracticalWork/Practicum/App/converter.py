import tkinter as tk
from tkinter import ttk, messagebox
import requests
import xml.etree.ElementTree as ET


class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер валют")
        self.root.geometry("400x500")

        self.rates = {"RUB": 1.0, "USD": 77.7, "EUR": 90.34, "CNY": 10.96, "KRW": 0.067}
        self.currencies = [
            "Российский рубль",
            "Доллар США",
            "Евро",
            "Китайский юань",
            "Южнокорейская вона",
        ]
        self.code_map = {
            "Российский рубль": "RUB",
            "Доллар США": "USD",
            "Евро": "EUR",
            "Китайский юань": "CNY",
            "Южнокорейская вона": "KRW",
        }

        self.setup_ui()
        self.update_rates()

    def setup_ui(self):
        tk.Label(self.root, text="Конвертер валют", font=("Arial", 18, "bold")).pack(
            pady=10
        )

        tk.Label(self.root, text="Из:").pack()
        self.combo_from = ttk.Combobox(self.root, values=self.currencies, width=30)
        self.combo_from.current(0)
        self.combo_from.pack(pady=5)

        tk.Button(self.root, text="⇄", command=self.reverse_currencies).pack()

        tk.Label(self.root, text="В:").pack()
        self.combo_to = ttk.Combobox(self.root, values=self.currencies, width=30)
        self.combo_to.current(1)
        self.combo_to.pack(pady=5)

        tk.Label(self.root, text="Сумма:").pack(pady=(10, 0))
        self.entry_amount = tk.Entry(self.root, width=33)
        self.entry_amount.insert(0, "100")
        self.entry_amount.pack(pady=5)
        self.entry_amount.bind("<KeyRelease>", lambda e: self.convert())

        tk.Label(self.root, text="Результат:").pack(pady=(10, 0))
        self.result_label = tk.Entry(self.root, width=33, state="readonly")
        self.result_label.pack(pady=5)

        self.rates_frame = tk.LabelFrame(
            self.root, text="Курсы валют к RUB", padx=10, pady=10
        )
        self.rates_frame.pack(pady=20, fill="x", padx=20)

        self.rates_display = tk.Label(self.rates_frame, text="", justify="left")
        self.rates_display.pack()

        tk.Button(self.root, text="Обновить курсы", command=self.update_rates).pack(
            side="bottom", pady=15
        )

    def update_rates(self):
        try:
            response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")
            tree = ET.fromstring(response.content)

            for valute in tree.findall("Valute"):
                char_code = valute.find("CharCode").text
                if char_code in self.rates:
                    value = float(valute.find("Value").text.replace(",", "."))
                    nominal = int(valute.find("Nominal").text)
                    self.rates[char_code] = value / nominal

            self.refresh_rates_display()
            self.convert()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить курсы: {e}")

    def refresh_rates_display(self):
        text = ""
        for code in ["USD", "EUR", "CNY", "KRW"]:
            text += f"1 {code} = {self.rates[code]:.4f} RUB\n"
        self.rates_display.config(text=text)

    def convert(self):
        try:
            amount = float(self.entry_amount.get())
            code_from = self.code_map[self.combo_from.get()]
            code_to = self.code_map[self.combo_to.get()]

            result = (amount * self.rates[code_from]) / self.rates[code_to]

            self.result_label.config(state="normal")
            self.result_label.delete(0, tk.END)
            self.result_label.insert(0, f"{result:.2f}")
            self.result_label.config(state="readonly")
        except ValueError:
            pass

    def reverse_currencies(self):
        idx1, idx2 = self.combo_from.current(), self.combo_to.current()
        self.combo_from.current(idx2)
        self.combo_to.current(idx1)
        self.convert()


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()
