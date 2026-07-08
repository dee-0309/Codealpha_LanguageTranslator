import tkinter as tk
from tkinter import ttk, messagebox

from deep_translator import GoogleTranslator

# Common languages — name shown in dropdown, code used for translation
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Arabic": "ar",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Portuguese": "pt",
    "Russian": "ru",
    "Italian": "it",
    "Urdu": "ur",
    "Bengali": "bn",
    "Tamil": "ta",
}

SOURCE_LANGUAGES = {"Detect language": "auto", **LANGUAGES}


def translate(text, source_code, target_code):
    return GoogleTranslator(source=source_code, target=target_code).translate(text)


class TranslatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Translator")
        root.geometry("700x450")
        root.minsize(500, 350)

        # Language bar
        lang_frame = ttk.Frame(root, padding=10)
        lang_frame.pack(fill="x")

        self.source_lang = tk.StringVar(value="Detect language")
        self.target_lang = tk.StringVar(value="Spanish")

        ttk.Combobox(
            lang_frame, textvariable=self.source_lang,
            values=list(SOURCE_LANGUAGES.keys()), state="readonly", width=18,
        ).pack(side="left")

        ttk.Button(lang_frame, text="⇄", width=3, command=self.swap_languages).pack(side="left", padx=8)

        ttk.Combobox(
            lang_frame, textvariable=self.target_lang,
            values=list(LANGUAGES.keys()), state="readonly", width=18,
        ).pack(side="left")

        # Input box
        input_frame = ttk.LabelFrame(root, text="Enter text", padding=10)
        input_frame.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        self.input_box = tk.Text(input_frame, height=8, font=("Segoe UI", 12), wrap="word")
        self.input_box.pack(fill="both", expand=True)

        # Translate button
        ttk.Button(root, text="Translate", command=self.do_translate).pack(pady=5)

        # Output box
        output_frame = ttk.LabelFrame(root, text="Translation", padding=10)
        output_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        self.output_box = tk.Text(output_frame, height=8, font=("Segoe UI", 12), wrap="word", state="disabled")
        self.output_box.pack(fill="both", expand=True)

    def swap_languages(self):
        src = self.source_lang.get()
        tgt = self.target_lang.get()

        if src == "Detect language":
            self.source_lang.set(tgt)
            self.target_lang.set("English")
        else:
            self.source_lang.set(tgt)
            self.target_lang.set(src)

        # Also swap the text in the boxes
        input_text = self.input_box.get("1.0", "end").strip()
        self.output_box.config(state="normal")
        output_text = self.output_box.get("1.0", "end").strip()
        self.output_box.config(state="disabled")

        self.input_box.delete("1.0", "end")
        if output_text:
            self.input_box.insert("1.0", output_text)

        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        if input_text:
            self.output_box.insert("1.0", input_text)
        self.output_box.config(state="disabled")

    def do_translate(self):
        text = self.input_box.get("1.0", "end").strip()
        if not text:
            messagebox.showinfo("Translator", "Please enter some text to translate.")
            return

        source = SOURCE_LANGUAGES[self.source_lang.get()]
        target = LANGUAGES[self.target_lang.get()]

        try:
            result = translate(text, source, target)
        except Exception as e:
            messagebox.showerror("Error", f"Translation failed:\n{e}")
            return

        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", result)
        self.output_box.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    TranslatorApp(root)
    root.mainloop()