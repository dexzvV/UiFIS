import tkinter as tk
from tkinter import messagebox
import requests


YANDEX_BASE_URL = ""
FREE_DICT_URL = ""


class DictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Электронный словарь бибизян")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        tk.Label(root, text="Введите слово (RU/EN):").place(x=10, y=10)
        self.entry_word = tk.Entry(root, width=40, font=("Arial", 11))
        self.entry_word.place(x=10, y=35)
        self.entry_word.bind("<Return>", lambda e: self.search_word())

        self.btn_search = tk.Button(
            root, text="Поиск", width=10, command=self.search_word
        )
        self.btn_search.place(x=340, y=32)

        self.btn_clear = tk.Button(
            root, text="Очистить", width=10, command=self.clear_fields
        )
        self.btn_clear.place(x=430, y=32)

        self.btn_copy = tk.Button(
            root, text="Копировать", width=10, command=self.copy_text
        )
        self.btn_copy.place(x=520, y=32)

        tk.Label(root, text="Результат:").place(x=10, y=70)
        self.txt_result = tk.Text(root, width=65, height=22, font=("Consolas", 10))
        self.txt_result.place(x=10, y=95)

        tk.Label(root, text="Части речи:").place(x=550, y=70)
        self.lst_meanings = tk.Listbox(root, width=35, height=22)
        self.lst_meanings.place(x=550, y=95)

    def is_russian(self, word):
        return any("а" <= char.lower() <= "я" for char in word)

    def search_word(self):
        word = self.entry_word.get().strip()
        if not word:
            messagebox.showwarning("Внимание", "Введите слово!")
            return

        self.clear_fields(only_results=True)

        try:
            lang = "ru-en" if self.is_russian(word) else "en-ru"
            self.fetch_yandex(word, lang)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Проблема: {e}")

    def fetch_yandex(self, word, lang):
        full_url = f"{YANDEX_BASE_URL}&lang={lang}&text={word}&ui=ru"

        try:
            res = requests.get(full_url, timeout=5)
            if res.status_code != 200:
                self.txt_result.insert(
                    tk.END, f"Ошибка API: {res.status_code}\nПроверьте лимиты или ключ."
                )
                return

            response = res.json()

            if not response.get("def"):
                if lang == "en-ru":
                    self.fetch_english_free(word)
                else:
                    self.txt_result.insert(
                        tk.END, "Слово не найдено в словаре Яндекса."
                    )
                return

            self.txt_result.insert(tk.END, f"СЛОВО: {word.upper()}\n" + "=" * 40 + "\n")

            for definition in response["def"]:
                pos = definition.get("pos", "n/a")
                if pos not in self.lst_meanings.get(0, tk.END):
                    self.lst_meanings.insert(tk.END, pos)

                self.txt_result.insert(tk.END, f"[{pos}] {definition.get('text')}\n")
                if "ts" in definition:
                    self.txt_result.insert(
                        tk.END, f"Транскрипция: [{definition['ts']}]\n"
                    )

                for i, tr in enumerate(definition.get("tr", []), 1):
                    self.txt_result.insert(tk.END, f"  {i}. {tr['text']}\n")
                    if "syn" in tr:
                        syns = ", ".join([s["text"] for s in tr["syn"]])
                        self.txt_result.insert(tk.END, f"     Синонимы: {syns}\n")
                    if "ex" in tr:
                        for ex in tr["ex"]:
                            tr_text = (
                                ex["tr"][0]["text"]
                                if "tr" in ex and ex["tr"]
                                else "---"
                            )
                            self.txt_result.insert(
                                tk.END, f"     Пример: {ex['text']} — {tr_text}\n"
                            )
                self.txt_result.insert(tk.END, "\n")
        except Exception as e:
            self.txt_result.insert(tk.END, f"Ошибка соединения: {e}")

    def fetch_english_free(self, word):
        try:
            res = requests.get(f"{FREE_DICT_URL}{word}", timeout=5)
            if res.status_code != 200:
                self.txt_result.insert(
                    tk.END, "Слово не найдено ни в одном из словарей."
                )
                return

            data = res.json()[0]
            self.txt_result.insert(
                tk.END, f"FREE DICTIONARY: {word.upper()}\n" + "-" * 40 + "\n"
            )
            for meaning in data.get("meanings", []):
                pos = meaning.get("partOfSpeech")
                self.lst_meanings.insert(tk.END, pos)
                for i, d in enumerate(meaning.get("definitions", []), 1):
                    self.txt_result.insert(tk.END, f"[{pos}] {i}. {d['definition']}\n")
        except:
            self.txt_result.insert(tk.END, "Ошибка при запросе к бесплатному словарю.")

    def clear_fields(self, only_results=False):
        if not only_results:
            self.entry_word.delete(0, tk.END)
        self.txt_result.delete("1.0", tk.END)
        self.lst_meanings.delete(0, tk.END)

    def copy_text(self):
        content = self.txt_result.get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("Ок", "Текст скопирован!")


if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()
