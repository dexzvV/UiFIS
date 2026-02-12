import tkinter as tk
from tkinter import messagebox
import math


def calculate():
    try:
        t_sr = float(entry_tsr.get())
        t_work = float(entry_t.get())

        if t_sr <= 0:
            raise ValueError()

        lam = 1 / t_sr
        p_t = math.exp(-lam * t_work)
        a_t = lam * math.exp(-lam * t_work)

        result_text = (
            f"ИСХОДНЫЕ ДАННЫЕ:\n"
            f"• Среднее время (Tо): {t_sr} ч.\n"
            f"• Время работы (t): {t_work} ч.\n\n"
            f"РАСЧЕТНЫЕ ПОКАЗАТЕЛИ:\n"
            f"1. Интенсивность отказов (λ):\n"
            f"   λ = 1 / Tо = {lam:.6f} 1/ч\n\n"
            f"2. Вероятность безотказной работы:\n"
            f"   P({t_work}) = e^(-λt) = {p_t:.4f}\n\n"
            f"3. Частота отказов:\n"
            f"   a({t_work}) = λ * e^(-λt) = {a_t:.6f}"
        )

        lbl_result_display.config(text=result_text)
        messagebox.showinfo("Результат", f"P(t) = {p_t:.4f}")

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числовые значения")


root = tk.Tk()
root.title("Расчет показателей долговечности")
root.geometry("450x550")
root.configure(bg="#f4f6f8")

card = tk.Frame(root, bg="white", padx=20, pady=20, relief="flat", bd=0)
card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)

tk.Label(
    card, text="Вариант 13", font=("Segoe UI", 14, "bold"), bg="white", fg="#263238"
).pack(pady=(0, 15))

tk.Label(card, text="Среднее время (Tо), ч:", bg="white", fg="#263238").pack(anchor="w")
entry_tsr = tk.Entry(card, font=("Segoe UI", 11), relief="solid")
entry_tsr.insert(0, "640")
entry_tsr.pack(fill="x", pady=(5, 15))

tk.Label(card, text="Время работы (t), ч:", bg="white", fg="#263238").pack(anchor="w")
entry_t = tk.Entry(card, font=("Segoe UI", 11), relief="solid")
entry_t.insert(0, "120")
entry_t.pack(fill="x", pady=(5, 20))

tk.Button(
    card,
    text="Рассчитать",
    command=calculate,
    bg="#4f7cff",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    relief="flat",
    height=2,
).pack(fill="x", pady=(0, 20))

lbl_result_display = tk.Label(
    card,
    text="",
    justify="left",
    bg="#eceff1",
    font=("Consolas", 9),
    anchor="nw",
    padx=10,
    pady=10,
)
lbl_result_display.pack(fill="both", expand=True)

root.mainloop()
