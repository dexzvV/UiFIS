import tkinter as tk
from tkinter import messagebox


class Question:
    def __init__(self, description, options, correct_answer):
        self.description = description
        self.options = options
        self.correct_answer = correct_answer


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Угадай стандарт")
        self.root.geometry("500x400")

        self.questions = [
            Question(
                "Какой стандарт определяет формат чисел с плавающей точкой?",
                ["ISO 9001", "IEEE 754", "ASCII", "USB 3.0"],
                "IEEE 754",
            ),
            Question(
                "Какой стандарт описывает базовый набор символов?",
                ["Unicode", "ASCII", "UTF-8", "ISO 8859-1"],
                "ASCII",
            ),
            Question(
                "Какой стандарт определяет требования к системе менеджмента качества?",
                ["ISO 9001", "IEEE 802.11", "GMP", "HACCP"],
                "ISO 9001",
            ),
            Question(
                "Какой стандарт описывает протоколы для Wi-Fi?",
                ["IEEE 802.3", "IEEE 802.11", "IEEE 1394", "Bluetooth"],
                "IEEE 802.11",
            ),
            Question(
                "Какой стандарт кодировки включает символы всех письменностей мира?",
                ["ASCII", "KOI-8", "Unicode", "Windows-1251"],
                "Unicode",
            ),
        ]

        self.current_q_index = 0
        self.score = 0
        self.selected_option = tk.StringVar()

        self.setup_ui()
        self.display_question()

    def setup_ui(self):
        self.lbl_header = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.lbl_header.pack(pady=10)

        self.lbl_question = tk.Label(
            self.root, text="", font=("Arial", 10), wraplength=400
        )
        self.lbl_question.pack(pady=10)

        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(
                self.root,
                text="",
                variable=self.selected_option,
                value="",
                font=("Arial", 10),
            )
            rb.pack(anchor="w", padx=50)
            self.radio_buttons.append(rb)

        self.btn_next = tk.Button(self.root, text="Далее", command=self.next_question)
        self.btn_next.pack(pady=20)

        self.lbl_score = tk.Label(self.root, text="Правильных ответов: 0 из 5")
        self.lbl_score.pack(side="bottom", pady=10)

    def display_question(self):
        q = self.questions[self.current_q_index]
        self.lbl_header.config(
            text=f"Вопрос {self.current_q_index + 1} из {len(self.questions)}"
        )
        self.lbl_question.config(text=q.description)

        self.selected_option.set(None)
        for i, option in enumerate(q.options):
            self.radio_buttons[i].config(text=option, value=option)

    def next_question(self):
        if self.selected_option.get() == "None":
            messagebox.showwarning("Внимание", "Выберите вариант ответа!")
            return

        if (
            self.selected_option.get()
            == self.questions[self.current_q_index].correct_answer
        ):
            self.score += 1

        self.current_q_index += 1
        self.lbl_score.config(text=f"Правильных ответов: {self.score} из 5")

        if self.current_q_index < len(self.questions):
            self.display_question()
        else:
            percent = (self.score / len(self.questions)) * 100
            res = messagebox.askyesno(
                "Результат теста",
                f"Тест завершен!\n\nПравильных ответов: {self.score} из 5\nПроцент: {percent}%\n\nХотите пройти тест заново?",
            )
            if res:
                self.restart_quiz()
            else:
                self.root.quit()

    def restart_quiz(self):
        self.current_q_index = 0
        self.score = 0
        self.lbl_score.config(text="Правильных ответов: 0 из 5")
        self.display_question()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
