import customtkinter as ctk
import random
import socket
import pywinstyles
import sys
import os
from Classes import Datahandler
from Classes import Extras
from tkinter import filedialog
import pathlib
from CTkMessagebox import *
from Classes import ctk_components
from Classes import window_position
import tkinter as tk

class Mariechen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mariechen")
        self.geometry("400x200")
        window_position.center_window(self,400,200)
        self.datahandler = Datahandler.Datahandler()
        self.style = self.datahandler.getINI(section="Customization",key="style")
        self.protocol("WM_DELETE_WINDOW",self.SaveINIValues)
        if self.style == "":
            pywinstyles.apply_style(self,"optimised")
            self.datahandler.writeInI(section="Customization",key="style",value="optimised")
        else:
            pywinstyles.apply_style(self,self.style)
        
        self.editor = False
        self.questions = {}
        self.questionsRef:list[Extras.Question] = []

        # UI Elemente
        self.startupscreen = ctk.CTkFrame(self)
        self.TitleLabel = ctk.CTkLabel(self.startupscreen,text="Quizzzz")
        self.TitleLabel.pack()
        self.ButtonsFrame = ctk.CTkFrame(self.startupscreen,bg_color="transparent")
        self.save = ctk.CTkButton(self.ButtonsFrame,text="Save Quiz",cursor= "hand2", command=lambda: self.SaveQuiz(quiz=self.quiz))
        #self.save.pack(side="left",padx=10,pady=5)
        self.load = ctk.CTkButton(self.ButtonsFrame,text="Load Quiz",cursor= "hand2",command=self.LoadQuiz)
        self.load.pack(side="left",padx=10,pady=5)
        self.create = ctk.CTkButton(self.ButtonsFrame,text="Create Quiz",cursor= "hand2", command=self.showNameEntry)
        self.create.pack(side="left",padx=10,pady=5)
        self.ButtonsFrame.pack()
        self.startupscreen.pack(fill="both",expand=True)

        self.entryframe = ctk.CTkFrame(self.startupscreen,width=200,height=50)
        self.nameentry = ctk.CTkEntry(self.entryframe,placeholder_text="Name your quiz")
        self.confirmname = ctk.CTkButton(self.entryframe,text="Confirm",command=self.createQuiz)
        self.nameentry.pack()
        self.confirmname.pack()

        self.QuizEditor = ctk.CTkFrame(self)
        self.addQuestionButton = ctk.CTkButton(self.QuizEditor,text="Add Question",cursor="hand2",command=self.addQuestion)
        self.addQuestionButton.place(relx=1,rely=0,anchor="ne")
        self.LeaveEditorButton = ctk.CTkButton(self.QuizEditor,text="Leave Quiz editor",cursor="hand2",command=self.LeaveEditor)
        self.LeaveEditorButton.place(relx=0,rely=0,anchor="nw")
        

    def SaveINIValues(self):
        self.datahandler.SaveINI()
        self.destroy()

    def SaveQuiz(self,quiz:Extras.Quiz,defaultfile:str = ""):
        if os.path.exists(quiz.path):
            if quiz:
                self.datahandler.saveQuiz(quiz,quiz.path)
        else:
            if quiz:
                path = filedialog.asksaveasfilename(
                    initialfile= defaultfile + ".pkl",
                    defaultextension=".pkl",
                    title="Speicherort wählen"
                )
                if path:
                    self.datahandler.saveQuiz(quiz,path)
    
    def LoadQuiz(self):
        path = filedialog.askopenfilename()
        if path:
            with open(path,"rb"):
                self.quiz = self.datahandler.getQuiz(path)

    def showNameEntry(self):
        if self.ButtonsFrame.winfo_viewable():
            self.ButtonsFrame.pack_forget()
            self.entryframe.pack()
        else:
            self.entryframe.pack_forget()
            self.ButtonsFrame.pack()
        
    def createQuiz(self):
        if self.nameentry.get():
            self.quiz = Extras.Quiz(Name=self.nameentry.get())
            self.SaveQuiz(quiz=self.quiz,defaultfile=self.nameentry.get())
            self.nameentry.delete(0,tk.END)
            self.startupscreen.pack_forget()
            self.QuizEditor.pack(fill="both",expand=True)
            window_position.center_window(self,900,450)
            self.editor = True

    def addQuestion(self):
        if self.editor:
            Dialog = Extras.InputDialog(title="Question Name",Buttontext="Confirm",PlaceholderInput="Enter a Name")
            self.wait_window(Dialog)
            result = Dialog.get_result()
            if result not in self.questions:
                if self.editor:
                    newQuestion = Extras.Question(self.QuizEditor,height=100)
                    newQuestion.pack(fill="x",expand=True)
                    self.questions[result] = []
                    self.questionsRef.append(newQuestion)
    
    def LeaveEditor(self):
        self.editor = False
        self.QuizEditor.pack_forget()
        self.startupscreen.pack(fill="both",expand=True)
        window_position.center_window(self,400,200)
        if self.entryframe.winfo_viewable:
            self.entryframe.pack_forget()
            self.ButtonsFrame.pack()
        
        for Name,child in self.QuizEditor.children:
            self.QuizEditor.