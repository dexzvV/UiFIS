import tkinter as tk
from tkinter import messagebox


def calculate():
    try:
        p_bez = float(entry_p_bez.get())
        p_lt = float(entry_p_lt.get())

        if not (0 <= p_bez <= 1) or not (0 <= p_lt <= 1):
            raise ValueError("Значения должны быть в диапазоне [0, 1]")

        p_pr = p_bez - p_lt

        if p_pr < 0:
            raise ValueError("P_лт не может превышать P_без")

        label_result.config(text=f"P_пр = {p_pr:.3f}")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))


root = tk.Tk()
root.title("Практическая работа №7")
root.geometry("450x380")

tk.Label(root, text="Вариант 13: Определение P_пр", font=("Arial", 12, "bold")).pack(
    pady=10
)

formula_frame = tk.LabelFrame(root, text="Формулы для решения", padx=10, pady=10)
formula_frame.pack(pady=5, fill="x", padx=20)
tk.Label(formula_frame, text="P_без = 1 - P_ош").pack(anchor="w")
tk.Label(formula_frame, text="P_пр = P_без - P_лт").pack(anchor="w")

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="P_без (вер. отсутствия ошибки):").grid(
    row=0, column=0, sticky="e"
)
entry_p_bez = tk.Entry(input_frame)
entry_p_bez.insert(0, "0.95")
entry_p_bez.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="P_лт (вер. ложной тревоги):").grid(
    row=1, column=0, sticky="e"
)
entry_p_lt = tk.Entry(input_frame)
entry_p_lt.insert(0, "0.03")
entry_p_lt.grid(row=1, column=1, padx=5, pady=5)

tk.Button(root, text="Вычислить", command=calculate, width=20).pack(pady=10)

label_result = tk.Label(root, text="P_пр = ?", font=("Arial", 12, "bold"), fg="green")
label_result.pack(pady=5)

root.mainloop()
