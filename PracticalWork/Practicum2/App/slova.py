import tkinter as tk
import random

WORDS = ["компьютер", "программа", "алгоритм", "интерфейс", "разработка"]

BG = "#f4f6f8"
CARD = "#ffffff"
BTN = "#4f7cff"
BTN_DISABLED = "#cfd8dc"
TEXT = "#263238"


def random_word():
    entry.delete(0, tk.END)
    entry.insert(0, random.choice(WORDS))


def start_game():
    global word, shuffled, result, history, original_shuffled
    word = entry.get().lower()
    if not word:
        return

    result = ""
    history = []
    lbl_result.config(text="")
    lbl_word.config(text="")

    for btn in letter_buttons:
        btn.destroy()
    letter_buttons.clear()

    shuffled = list(word)
    random.shuffle(shuffled)
    original_shuffled = list(shuffled)

    for i, ch in enumerate(shuffled):
        btn = tk.Button(
            frame_letters,
            text=ch.upper(),
            font=("Segoe UI", 14, "bold"),
            width=3,
            height=2,
            bg=BTN,
            fg="white",
            activebackground="#3c63d9",
            relief="flat",
            command=lambda i=i: choose_letter(i),
        )
        btn.grid(row=0, column=i, padx=6)
        letter_buttons.append(btn)


def choose_letter(i):
    global result
    if shuffled[i] == "":
        return

    result += shuffled[i]
    history.append(i)
    shuffled[i] = ""

    letter_buttons[i].config(state="disabled", bg=BTN_DISABLED)
    lbl_word.config(text=result.upper())

    if len(result) == len(word):
        check_result()


def undo():
    global result
    if not history:
        return

    i = history.pop()
    result = result[:-1]
    lbl_word.config(text=result.upper())

    shuffled[i] = original_shuffled[i]
    letter_buttons[i].config(text=shuffled[i].upper(), state="normal", bg=BTN)
    lbl_result.config(text="")


def check_result():
    if result == word:
        lbl_result.config(text="Молодец бибизян!", fg="#2e7d32")
    else:
        lbl_result.config(text="Бибизян тупой", fg="#c62828")


root = tk.Tk()
root.title("Поле чудес")
root.geometry("800x500")
root.configure(bg=BG)
root.resizable(False, False)

card = tk.Frame(root, bg=CARD, padx=20, pady=20)
card.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(
    card, text="Игра «Поле обезьян»", font=("Segoe UI", 18, "bold"), bg=CARD, fg=TEXT
).pack(pady=(0, 10))

frame_top = tk.Frame(card, bg=CARD)
frame_top.pack()

entry = tk.Entry(frame_top, font=("Segoe UI", 12), width=18, relief="solid")
entry.grid(row=0, column=0, padx=5)

tk.Button(
    frame_top,
    text="Крути барабан",
    font=("Segoe UI", 11),
    bg="#e3f2fd",
    relief="flat",
    command=random_word,
).grid(row=0, column=1)

tk.Button(
    card,
    text="Начать игру",
    bg=BTN,
    fg="white",
    font=("Segoe UI", 12, "bold"),
    relief="flat",
    width=22,
    command=start_game,
).pack(pady=10)

frame_letters = tk.Frame(card, bg=CARD)
frame_letters.pack(pady=10)

lbl_word = tk.Label(card, text="", font=("Segoe UI", 16), bg=CARD, fg=TEXT)
lbl_word.pack()

tk.Button(card, text="Отменить", bg="#eceff1", relief="flat", command=undo).pack(pady=5)

lbl_result = tk.Label(card, text="", font=("Segoe UI", 13, "bold"), bg=CARD)
lbl_result.pack(pady=5)

letter_buttons = []
word = result = ""
history = []
original_shuffled = []

root.mainloop()
