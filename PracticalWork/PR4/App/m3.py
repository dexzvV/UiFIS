import tkinter as tk
from tkinter import messagebox
import math


def calculate():
    try:
        lam = float(entry_lam.get())
        mu = float(entry_mu.get())
        t_work = float(entry_t.get())

        if lam < 0 or mu <= 0:
            raise ValueError()

        k_got = mu / (lam + mu)
        k_pros = lam / (lam + mu)
        k_op_got = k_got * math.exp(-lam * t_work)

        t_mean = 1 / lam
        t_rec = 1 / mu

        result_text = (
            f"РЕЗУЛЬТАТЫ РАСЧЕТА:\n"
            f"------------------------------\n"
            f"Коэф. готовности (Кг): {k_got:.4f}\n"
            f"Коэф. простоя (Кп): {k_pros:.4f}\n"
            f"Коэф. опер. готовности (Ког): {k_op_got:.4f}\n\n"
            f"Средняя наработка (T): {t_mean:.1f} ч.\n"
            f"Время восстановления (Tв): {t_rec:.1f} ч."
        )

        lbl_result.config(text=result_text)

    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числовые значения")


root = tk.Tk()
root.title("Надежность систем: Практическая 4")
root.geometry("450x550")
root.configure(bg="#f0f2f5")

card = tk.Frame(root, bg="white", padx=25, pady=25, relief="flat")
card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=500)

tk.Label(
    card, text="Комплексные показатели", font=("Arial", 14, "bold"), bg="white"
).pack(pady=(0, 20))

tk.Label(card, text="Интенсивность отказов (λ):", bg="white").pack(anchor="w")
entry_lam = tk.Entry(card, font=("Arial", 11))
entry_lam.insert(0, "0.005")
entry_lam.pack(fill="x", pady=(5, 15))

tk.Label(card, text="Интенсивность восст. (μ):", bg="white").pack(anchor="w")
entry_mu = tk.Entry(card, font=("Arial", 11))
entry_mu.insert(0, "0.2")
entry_mu.pack(fill="x", pady=(5, 15))

tk.Label(card, text="Время работы (t) для Ког:", bg="white").pack(anchor="w")
entry_t = tk.Entry(card, font=("Arial", 11))
entry_t.insert(0, "100")
entry_t.pack(fill="x", pady=(5, 20))

tk.Button(
    card,
    text="РАССЧИТАТЬ",
    command=calculate,
    bg="#28a745",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    height=2,
).pack(fill="x", pady=(0, 20))

lbl_result = tk.Label(
    card,
    text="",
    justify="left",
    bg="#f8f9fa",
    font=("Consolas", 10),
    anchor="nw",
    padx=10,
    pady=10,
    relief="solid",
    bd=1,
)
lbl_result.pack(fill="both", expand=True)

root.mainloop()
