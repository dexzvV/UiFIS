import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import pandas as pd
from fpdf import FPDF


class QualityAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ индексов качества процесса")
        self.root.geometry("1100x750")
        self.root.configure(bg="#e0e0e0")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#cccccc")
        style.configure("TNotebook.Tab", padding=[10, 5])
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#2ecc71")],
            foreground=[("selected", "white")],
        )

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        self.calc_tab = tk.Frame(self.notebook, bg="#d3d3d3")
        self.graph_tab = tk.Frame(self.notebook, bg="#d3d3d3")
        self.history_tab = tk.Frame(self.notebook, bg="#d3d3d3")

        self.notebook.add(self.calc_tab, text="Калькулятор")
        self.notebook.add(self.graph_tab, text="График распределения")
        self.notebook.add(self.history_tab, text="История расчетов")

        self.setup_calc_tab()
        self.setup_graph_tab()
        self.setup_history_tab()

    def setup_calc_tab(self):
        left_panel = tk.LabelFrame(
            self.calc_tab,
            text="Введите параметры процесса",
            bg="#d3d3d3",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=20,
        )
        left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.entries = {}
        fields = [
            ("Верхняя граница допуска (USL):", "10.5"),
            ("Нижняя граница допуска (LSL):", "9.5"),
            ("Среднее процесса (μ):", "10.2"),
            ("Стандартное отклонение (σ):", "0.1"),
        ]

        for i, (label, default) in enumerate(fields):
            tk.Label(left_panel, text=label, bg="#d3d3d3").grid(
                row=i, column=0, sticky="w", pady=10
            )
            entry = tk.Entry(left_panel, justify="center", width=25)
            entry.insert(0, default)
            entry.grid(row=i, column=1, padx=10)
            self.entries[label] = entry

        btn_style = {
            "font": ("Arial", 9, "bold"),
            "fg": "white",
            "bg": "#2c5f85",
            "pady": 5,
        }
        tk.Button(
            left_panel,
            text="Рассчитать индексы качества",
            command=self.calculate,
            **btn_style,
        ).grid(row=4, column=0, pady=10, padx=5)
        tk.Button(
            left_panel,
            text="Сохранить в историю",
            command=self.save_to_history,
            **btn_style,
        ).grid(row=4, column=1, pady=10)

        tk.Button(
            left_panel,
            text="Экспорт в Excel",
            command=self.export_current_excel,
            **btn_style,
        ).grid(row=5, column=0)
        tk.Button(
            left_panel, text="Экспорт в PDF", command=self.export_pdf, **btn_style
        ).grid(row=5, column=1)
        tk.Button(
            left_panel,
            text="Загрузить из Excel",
            command=self.load_from_excel,
            **btn_style,
        ).grid(row=6, column=0, columnspan=2, pady=10)

        right_panel = tk.LabelFrame(
            self.calc_tab,
            text="Результаты анализа",
            bg="#d3d3d3",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=20,
        )
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.res_label = tk.Label(
            right_panel,
            text="Рассчитайте данные",
            font=("Arial", 14),
            bg="#e0e0e0",
            relief="solid",
            bd=1,
            pady=40,
        )
        self.res_label.pack(fill="x")

    def setup_graph_tab(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_tab)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)

    def setup_history_tab(self):
        ctrl = tk.Frame(self.history_tab, bg="#cccccc")
        ctrl.pack(fill="x")

        tk.Button(
            ctrl,
            text="Очистить историю",
            bg="#c0392b",
            fg="white",
            command=self.clear_history,
        ).pack(side="left", padx=5, pady=5)
        tk.Button(
            ctrl,
            text="Загрузить выделенное",
            bg="#2c5f85",
            fg="white",
            command=self.load_selected,
        ).pack(side="left", padx=5)
        tk.Button(
            ctrl,
            text="Экспорт истории в Excel",
            bg="#2c5f85",
            fg="white",
            command=self.export_history_excel,
        ).pack(side="left", padx=5)

        cols = ("Дата", "USL", "LSL", "Среднее", "Сигма", "Cp", "Cpk", "Статус")
        self.tree = ttk.Treeview(self.history_tab, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

    def calculate(self):
        try:
            usl = float(self.entries["Верхняя граница допуска (USL):"].get())
            lsl = float(self.entries["Нижняя граница допуска (LSL):"].get())
            mu = float(self.entries["Среднее процесса (μ):"].get())
            sigma = float(self.entries["Стандартное отклонение (σ):"].get())

            cp = (usl - lsl) / (6 * sigma)
            cpk = min((usl - mu) / (3 * sigma), (mu - lsl) / (3 * sigma))

            status_map = {
                "Excellent": "Отлично",
                "Satisfactory": "Удовлетворительно",
                "Unsatisfactory": "Неудовлетворительно",
                "Critical": "Критично",
            }

            if cpk >= 1.33:
                status_eng, status_rus = "Excellent", "Отлично"
            elif cpk >= 1.0:
                status_eng, status_rus = "Satisfactory", "Удовлетворительно"
            elif cpk >= 0.67:
                status_eng, status_rus = "Unsatisfactory", "Неудовлетворительно"
            else:
                status_eng, status_rus = "Critical", "Критично"

            self.res_label.config(
                text=f"Cp: {cp:.3f}\nCpk: {cpk:.3f}\nСтатус: {status_rus}"
            )
            self.update_plot(usl, lsl, mu, sigma, cp, cpk)
            return {
                "USL": usl,
                "LSL": lsl,
                "Mean": mu,
                "Sigma": sigma,
                "Cp": round(cp, 3),
                "Cpk": round(cpk, 3),
                "Status": status_eng,
            }
        except:
            messagebox.showerror("Ошибка", "Некорректные данные")
            return None

    def update_plot(self, usl, lsl, mu, sigma, cp, cpk):
        self.ax.clear()
        x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 200)
        y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
        self.ax.plot(x, y, "b-", lw=2)
        self.ax.axvline(usl, color="r", ls="--")
        self.ax.axvline(lsl, color="r", ls="--")
        self.ax.fill_between(
            x, y, where=(x >= lsl) & (x <= usl), color="green", alpha=0.3
        )
        self.ax.fill_between(x, y, where=(x < lsl) | (x > usl), color="red", alpha=0.3)
        self.ax.set_title(f"Normal Distribution (Cp={cp:.3f}, Cpk={cpk:.3f})")
        self.canvas.draw()

    def save_to_history(self):
        res = self.calculate()
        if res:
            status_rus = {
                "Excellent": "Отлично",
                "Satisfactory": "Удовлетворительно",
                "Unsatisfactory": "Неудовлетворительно",
                "Critical": "Критично",
            }[res["Status"]]
            self.tree.insert(
                "",
                0,
                values=(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    res["USL"],
                    res["LSL"],
                    res["Mean"],
                    res["Sigma"],
                    res["Cp"],
                    res["Cpk"],
                    status_rus,
                ),
            )

    def clear_history(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def load_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Внимание", "Выберите строку")
            return
        v = self.tree.item(sel[0])["values"]
        keys = [
            "Верхняя граница допуска (USL):",
            "Нижняя граница допуска (LSL):",
            "Среднее процесса (μ):",
            "Стандартное отклонение (σ):",
        ]
        for i, key in enumerate(keys):
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, str(v[i + 1]))
        self.calculate()

    def export_current_excel(self):
        res = self.calculate()
        if res:
            pd.DataFrame([res]).to_excel("current_calculation.xlsx", index=False)
            messagebox.showinfo("Успех", "Файл current_calculation.xlsx сохранен")

    def export_history_excel(self):
        data = [self.tree.item(i)["values"] for i in self.tree.get_children()]
        if data:
            cols = ["Date", "USL", "LSL", "Mean", "Sigma", "Cp", "Cpk", "Status"]
            pd.DataFrame(data, columns=cols).to_excel(
                "history_export.xlsx", index=False
            )
            messagebox.showinfo("Успех", "Файл history_export.xlsx сохранен")

    def load_from_excel(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            df = pd.read_excel(path)
            keys = [
                "Верхняя граница допуска (USL):",
                "Нижняя граница допуска (LSL):",
                "Среднее процесса (μ):",
                "Стандартное отклонение (σ):",
            ]
            cols = ["USL", "LSL", "Mean", "Sigma"]
            for k, c in zip(keys, cols):
                if c in df.columns:
                    self.entries[k].delete(0, tk.END)
                    self.entries[k].insert(0, str(df.iloc[0][c]))
            self.calculate()

    def export_pdf(self):
        res = self.calculate()
        if res:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(200, 10, txt="Quality Analysis Report", ln=True, align="C")
                pdf.set_font("Arial", size=12)
                pdf.ln(10)
                for k, v in res.items():
                    # Выводим данные в формате ключ: значение (все на английском для PDF)
                    pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)
                pdf.output("report.pdf")
                messagebox.showinfo("Успех", "Файл report.pdf сохранен")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при создании PDF: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = QualityAnalysisApp(root)
    root.mainloop()
