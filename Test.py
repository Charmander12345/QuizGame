import customtkinter as ctk

class InputDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Eingabe-Fenster")
        self.geometry("300x150")
        
        # Variable, um den Text zu speichern
        self.input_text = ctk.StringVar()

        # UI-Elemente
        label = ctk.CTkLabel(self, text="Bitte Text eingeben:")
        label.pack(pady=10)

        self.entry = ctk.CTkEntry(self, textvariable=self.input_text)
        self.entry.pack(pady=10)

        button = ctk.CTkButton(self, text="Bestätigen", command=self._on_submit)
        button.pack(pady=10)

        # Modalität einstellen
        self.grab_set()
        self.result = None  # Wird später den Text speichern

    def _on_submit(self):
        self.result = self.input_text.get()  # Speichere den Text in der Instanz
        self.grab_release()  # Modalität freigeben
        self.destroy()  # Fenster schließen

    def get_result(self):
        return self.result  # Rückgabe des Textes

# Hauptprogramm
def main():
    app = ctk.CTk()
    app.geometry("400x300")
    app.title("Hauptfenster")

    # Label, um den zurückgegebenen Text anzuzeigen
    output_label = ctk.CTkLabel(app, text="Kein Text eingegeben.")
    output_label.pack(pady=20)

    # Button, um das Eingabe-Fenster zu öffnen
    def handle_input():
        dialog = InputDialog(app)  # Öffnet das modale Fenster
        dialog.wait_window()  # Wartet, bis das Fenster geschlossen wird
        result = dialog.get_result()  # Holt den eingegebenen Text
        if result:  # Wenn ein Text eingegeben wurde
            output_label.configure(text=f"Eingegebener Text: {result}")

    button = ctk.CTkButton(app, text="Eingabe öffnen", command=handle_input)
    button.pack(pady=50)

    app.mainloop()

if __name__ == "__main__":
    main()
