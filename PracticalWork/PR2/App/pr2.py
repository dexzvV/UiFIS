import tkinter as tk
from tkinter import ttk


class ReliabilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Практическая работа №2 - Вариант 13")
        self.root.geometry("850x750")

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Arial", 10))

        self.tabs = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)

        self.tabs.add(self.tab1, text="Задание 1")
        self.tabs.add(self.tab2, text="Задание 2")
        self.tabs.add(self.tab3, text="Задание 3")
        self.tabs.pack(expand=1, fill="both")

        self.init_task1()
        self.init_task2()
        self.init_task3()

    def init_task1(self):
        main_label = tk.Label(
            self.tab1,
            text="Расчет средней наработки на отказ системы",
            font=("Arial", 14, "bold"),
            fg="darkblue",
        )
        main_label.pack(pady=10)

        top_frame = tk.Frame(self.tab1)
        top_frame.pack(fill="x", padx=20)

        input_data = tk.Label(
            top_frame,
            text="Исходные данные:\nСистема отказала 6 раз.\nВремя работы до отказов:\n"
            "• 1-й отказ: 185 ч\n• 2-й отказ: 342 ч\n• 3-й отказ: 268 ч\n"
            "• 4-й отказ: 220 ч\n• 5-й отказ: 96 ч\n• 6-й отказ: 102 ч",
            justify="left",
            bg="#e0f2f1",
            relief="solid",
            bd=1,
            padx=10,
            pady=10,
        )
        input_data.pack(side="left", padx=10)

        canvas = tk.Canvas(
            top_frame,
            width=450,
            height=300,
            bg="white",
            highlightthickness=1,
            highlightbackground="black",
        )
        canvas.pack(side="right", padx=10)

        btn = tk.Button(
            self.tab1,
            text="Рассчитать MTBF",
            bg="#90ee90",
            font=("Arial", 10, "bold"),
            command=lambda: self.calc_t1(res_text, canvas),
        )
        btn.place(x=30, y=250)

        res_text = tk.Text(self.tab1, height=12, width=100, bg="#f0f0f0")
        res_text.pack(pady=40, padx=20)

    def calc_t1(self, text_widget, canvas):
        times = [185, 342, 268, 220, 96, 102]
        n = 6
        sum_t = sum(times)
        mtbf = sum_t / n

        text_widget.delete("1.0", tk.END)
        res = f"РЕЗУЛЬТАТ РАСЧЕТА\n\n"
        res += f"1. Сумма времени работы:\n   Σt = {' + '.join(map(str, times))} = {sum_t} часов\n\n"
        res += f"2. Количество отказов:\n   n = {n}\n\n"
        res += f"3. Формула расчета:\n   MTBF = Σt / n = {sum_t} / {n} = {mtbf:.2f} час"
        text_widget.insert("1.0", res)

        canvas.delete("all")
        canvas.create_text(
            225,
            20,
            text="График времени до отказа",
            font=("Arial", 11, "bold"),
            fill="darkblue",
        )
        max_h = 342
        for i, val in enumerate(times):
            x0, x1 = 60 + i * 60, 100 + i * 60
            y_val = 250 - (val / max_h * 180)
            color = "#90ee90" if val > mtbf else "#ffcccb"
            canvas.create_rectangle(x0, y_val, x1, 250, fill=color)
            canvas.create_text((x0 + x1) / 2, y_val - 10, text=str(val))
            canvas.create_text((x0 + x1) / 2, 265, text=str(i + 1))

        line_y = 250 - (mtbf / max_h * 180)
        canvas.create_line(40, line_y, 420, line_y, fill="red", dash=(4, 4), width=2)
        canvas.create_text(380, line_y - 10, text=f"MTBF = {mtbf:.2f} час", fill="red")

    def init_task2(self):
        tk.Label(
            self.tab2,
            text="Наработка на отказ по данным наблюдения",
            font=("Arial", 14, "bold"),
            fg="darkblue",
        ).pack(pady=10)

        f = tk.Frame(self.tab2)
        f.pack(fill="x", padx=20)

        tk.Label(
            f,
            text="Исходные данные:\nt1 = 358 час, n1 = 4\nt2 = 385 час, n2 = 3\nt3 = 400 час, n3 = 2",
            justify="left",
            bg="#e0f2f1",
            bd=1,
            relief="solid",
            padx=10,
        ).pack(side="left")

        tree = ttk.Treeview(
            f, columns=("Sys", "Time", "Fail", "MTBF"), show="headings", height=4
        )
        for col, head in zip(
            tree["columns"],
            ["Система", "Время работы", "Количество отказов", "MTBF системы"],
        ):
            tree.heading(col, text=head)
            tree.column(col, width=120)
        tree.pack(side="right", padx=10)

        data = [
            ("Система 1", 358, 4, 89.50),
            ("Система 2", 385, 3, 128.33),
            ("Система 3", 400, 2, 200.00),
        ]
        for d in data:
            tree.insert("", "end", values=d)

        res_text = tk.Text(self.tab2, height=15, width=100, bg="#f0f8ff")
        res_text.pack(pady=20)

        tk.Button(
            self.tab2,
            text="Рассчитать общий MTBF",
            bg="#90ee90",
            command=lambda: self.calc_t2(res_text),
        ).place(x=30, y=140)

    def calc_t2(self, text_widget):
        sum_t = 358 + 385 + 400
        sum_n = 4 + 3 + 2
        total_mtbf = sum_t / sum_n

        res = "РАСЧЕТ НАРАБОТКИ НА ОТКАЗ\n\n1. ДАННЫЕ ПО СИСТЕМАМ:\n"
        res += "Система 1: t1=358, n1=4; Система 2: t2=385, n2=3; Система 3: t3=400, n3=2\n\n"
        res += f"2. ОБЩИЙ РАСЧЕТ:\nОбщее время: Σt = {sum_t} час\nОбщее число отказов: Σn = {sum_n}\n"
        res += f"Общий MTBF = Σt / Σn = {sum_t} / {sum_n} = {total_mtbf:.2f} час"
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", res)

    def init_task3(self):
        tk.Label(
            self.tab3,
            text="Анализ безотказности и восстанавливаемости (Вариант 13)",
            font=("Arial", 14, "bold"),
            fg="darkblue",
        ).pack(pady=10)

        tree = ttk.Treeview(
            self.tab3,
            columns=("V", "t01", "tb1", "t02", "tb2"),
            show="headings",
            height=2,
        )
        for col, head in zip(
            tree["columns"], ["№", "t0¹, час", "tв¹, час", "t0², час", "tв², час"]
        ):
            tree.heading(col, text=head)
            tree.column(col, width=100)
        tree.pack(pady=10)
        tree.insert("", "end", values=("13", "29", "4", "370", "8"))

        res_text = tk.Text(self.tab3, height=18, width=100, bg="#f5f5f5")
        res_text.pack(pady=10)

        tk.Button(
            self.tab3,
            text="Выполнить анализ",
            bg="#90ee90",
            command=lambda: self.calc_t3(res_text),
        ).pack()

    def calc_t3(self, text_widget):
        t01, tb1 = 29, 4
        t02, tb2 = 370, 8
        kg1 = t01 / (t01 + tb1)
        kg2 = t02 / (t02 + tb2)

        res = "СРАВНИТЕЛЬНЫЙ АНАЛИЗ ДВУХ СИСТЕМ (ВАРИАНТ 13)\n\n"
        res += f"СИСТЕМА 1: t0={t01}, tв={tb1} => Kr = {t01}/({t01}+{tb1}) = {kg1:.4f} ({kg1*100:.2f}%)\n"
        res += f"СИСТЕМА 2: t0={t02}, tв={tb2} => Kr = {t02}/({t02}+{tb2}) = {kg2:.4f} ({kg2*100:.2f}%)\n\n"
        winner = "Система 2" if kg2 > kg1 else "Система 1"
        res += (
            f"ВЫВОД: {winner} является более надежной по коэффициенту готовности (Kг)."
        )
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", res)


if __name__ == "__main__":
    root = tk.Tk()
    app = ReliabilityApp(root)
    root.mainloop()
