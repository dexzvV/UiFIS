import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect("proposals.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS proposal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT,
            suggestion TEXT,
            priority TEXT,
            cost REAL,
            justification TEXT,
            deadline TEXT
        )
    """
    )

    cursor.execute("SELECT COUNT(*) FROM proposal")
    if cursor.fetchone()[0] == 0:
        initial_data = [
            (
                "Отдел продаж",
                "Внедрение CRM системы",
                "Высокий",
                500000,
                "Улучшение взаимодействия с клиентами",
                "31.12.2024",
            ),
            (
                "Бухгалтерия",
                "Обновление 1С",
                "Средний",
                200000,
                "Соответствие законодательству",
                "15.10.2024",
            ),
            (
                "IT отдел",
                "Покупка серверного оборудования",
                "Высокий",
                1000000,
                "Требуется для обработки возрастающего объема данных",
                "30.11.2024",
            ),
        ]
        cursor.executemany(
            "INSERT INTO proposal (department, suggestion, priority, cost, justification, deadline) VALUES (?, ?, ?, ?, ?, ?)",
            initial_data,
        )
    conn.commit()
    conn.close()


class ExpansionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Предложения по расширению ИС")
        self.root.geometry("850x550")

        header = tk.Label(
            root,
            text="Формирование предложений о расширении информационной системы",
            font=("Arial", 14, "bold"),
            pady=10,
        )
        header.pack()

        cols = ("ID", "Подразделение", "Предложение", "Приоритет", "Стоимость")
        self.tree = ttk.Treeview(root, columns=cols, show="headings")

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, text="Добавить предложение", command=self.open_add_form
        ).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Просмотр деталей", command=self.open_details).grid(
            row=0, column=1, padx=5
        )
        tk.Button(btn_frame, text="Сформировать отчет", command=self.open_report).grid(
            row=0, column=2, padx=5
        )
        tk.Button(root, text="Выход", command=root.quit).pack(pady=5)

        self.load_data()

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = sqlite3.connect("proposals.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, department, suggestion, priority, cost FROM proposal"
        )
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def open_add_form(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("Добавление нового предложения")
        add_win.geometry("400x520")

        fields = {}
        labels = [
            "Подразделение",
            "Предложение",
            "Приоритет",
            "Стоимость",
            "Обоснование",
            "Срок реализации",
        ]

        for text in labels:
            tk.Label(add_win, text=f"{text}:").pack(anchor="w", padx=20)
            if text == "Приоритет":
                fields[text] = ttk.Combobox(
                    add_win, values=["Низкий", "Средний", "Высокий"], state="readonly"
                )
                fields[text].current(1)
            elif text == "Обоснование":
                fields[text] = tk.Text(add_win, height=4)
            else:
                fields[text] = tk.Entry(add_win)
            fields[text].pack(fill="x", padx=20, pady=2)

        def save():
            try:
                conn = sqlite3.connect("proposals.db")
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO proposal (department, suggestion, priority, cost, justification, deadline) 
                                  VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        fields["Подразделение"].get(),
                        fields["Предложение"].get(),
                        fields["Приоритет"].get(),
                        float(fields["Стоимость"].get() or 0),
                        fields["Обоснование"].get("1.0", "end-1c"),
                        fields["Срок реализации"].get(),
                    ),
                )
                conn.commit()
                conn.close()
                self.load_data()
                add_win.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректную стоимость")

        tk.Button(add_win, text="Сохранить", bg="#90EE90", command=save).pack(
            side="left", padx=40, pady=20
        )
        tk.Button(add_win, text="Отмена", bg="#FFB6C1", command=add_win.destroy).pack(
            side="right", padx=40, pady=20
        )

    def open_details(self):
        selected = self.tree.selection()
        if not selected:
            return messagebox.showwarning("Внимание", "Выберите запись")

        item_id = self.tree.item(selected[0])["values"][0]

        conn = sqlite3.connect("proposals.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proposal WHERE id=?", (item_id,))
        data = cursor.fetchone()
        conn.close()

        det_win = tk.Toplevel(self.root)
        det_win.title("Подробная информация")

        info_text = (
            f"ПОДРОБНАЯ ИНФОРМАЦИЯ О ПРЕДЛОЖЕНИИ\n\n"
            f"ID: {data[0]}\n"
            f"Подразделение: {data[1]}\n"
            f"Предложение: {data[2]}\n"
            f"Приоритет: {data[3]}\n"
            f"Стоимость: {data[4]:,.0f} ₽\n"
            f"Срок реализации: {data[6]}\n\n"
            f"ОБОСНОВАНИЕ:\n{data[5]}"
        )

        tk.Label(
            det_win,
            text=info_text,
            justify="left",
            font=("Consolas", 10),
            padx=20,
            pady=20,
        ).pack()
        tk.Button(det_win, text="Закрыть", command=det_win.destroy).pack(pady=10)

    def open_report(self):
        conn = sqlite3.connect("proposals.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proposal")
        rows = cursor.fetchall()
        conn.close()

        total_cost = sum(row[4] for row in rows)
        high_prio = len([row for row in rows if row[3] == "Высокий"])
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")

        rep_win = tk.Toplevel(self.root)
        rep_win.title("Отчет по предложениям")

        report_area = tk.Text(rep_win, width=60, height=25, font=("Consolas", 10))
        report_area.pack(padx=10, pady=10)

        header = (
            f"ОТЧЕТ ПО ПРЕДЛОЖЕНИЯМ О РАСШИРЕНИИ ИС\n"
            f"Дата формирования: {current_time}\n"
            f"Всего предложений: {len(rows)}\n"
            f"Высокоприоритетных: {high_prio}\n"
            f"Общая стоимость: {total_cost:,.0f} ₽\n"
            f"{'='*50}\n\nСПИСОК ПРЕДЛОЖЕНИЙ:\n"
        )
        report_area.insert("end", header)

        for r in rows:
            entry = (
                f"[ID: {r[0]}] {r[1]}\nПредложение: {r[2]}\n"
                f"Приоритет: {r[3]} | Стоимость: {r[4]:,.0f} ₽\n"
                f"Срок: {r[6]}\n{'-'*50}\n"
            )
            report_area.insert("end", entry)

        report_area.config(state="disabled")

        btn_frame = tk.Frame(rep_win)
        btn_frame.pack(pady=10)
        tk.Button(
            btn_frame,
            text="Печать",
            command=lambda: messagebox.showinfo("Печать", "Отправлено на принтер"),
        ).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Закрыть", command=rep_win.destroy).grid(
            row=0, column=1, padx=5
        )


if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = ExpansionApp(root)
    root.mainloop()
