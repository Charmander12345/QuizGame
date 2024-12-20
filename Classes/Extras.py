import customtkinter as ctk
from Classes import window_position

class InputDialog(ctk.CTkToplevel):
    def __init__(self, *args, fg_color=None, title: str = "TopLevel", PlaceholderInput: str = "Input", Buttontext: str = "Submit", **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
        self.grab_set()
        # window_position.center_window(self,400,200)
        self.resizable(False, False)
        self.Button = ctk.CTkButton(self, text=Buttontext, command=self._on_submit)
        self.Button.place(rely=0.7, relx=0.5, anchor="center")
        self.input_text = ctk.StringVar()
        self.result = None
        self.entry = ctk.CTkEntry(self, textvariable=self.input_text, placeholder_text=PlaceholderInput)
        self.entry.bind("<Return>", self._on_submit)  # Bind Enter key to _on_submit
        self.entry.place(rely=0.4, relx=0.5, anchor="center")

    def _on_submit(self, event=None):
        self.result = self.input_text.get()  # Speichere den Text in der Instanz
        self.grab_release()  # Modalität freigeben
        self.destroy()  # Fenster schließen

    def get_result(self):
        return self.result  # Rückgabe des Textes

# Quiz Elemente

class Quiz():
    def __init__(self, Name: str, Questions: dict = {}, path: str = ""):
        self.Name = Name
        self.Questions = Questions
        self.path = path

class Answer(ctk.CTkFrame):
    def __init__(self, master, width=200, height=200, corner_radius=None, border_width=None, bg_color="transparent", fg_color=None, border_color=None, background_corner_colors=None, overwrite_preferred_drawing_method=None, Answer: str = "", **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.Answer = Answer
        self.Button = ctk.CTkButton(self, text=self.Answer, fg_color="transparent", cursor="hand2")
        self.Button.pack(expand=True)

class Question(ctk.CTkFrame):
    def __init__(self, master, width=200, height=200, corner_radius=None, border_width=None, bg_color="transparent", fg_color=None, border_color=None, background_corner_colors=None, overwrite_preferred_drawing_method=None, Name: str = "", Answers: list[str] = [], mode: str = "play", **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.Name = Name
        self.Answers = []  # Initialize the Answers list
        self.NameEntry = ctk.CTkEntry(self, placeholder_text=self.Name)
        self.NameEntry.bind("<Return>", self.ChangeName)  # Bind Enter key to ChangeName
        self.NameEntry.place(relx=0, rely=0.5, anchor="w")
        for item in Answers:
            answer = Answer(self, Answer=item)
            self.Answers.append(answer)

    def ChangeName(self, event=None):
        new_name = self.NameEntry.get()
        self.Name = new_name
        self.NameEntry.configure(placeholder_text=new_name)
        self.NameEntry.delete(0, 'end')  # Clear the entry after setting the new name
        self.master.focus()  # Remove focus from the entry