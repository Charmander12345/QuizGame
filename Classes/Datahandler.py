import configparser
import os
import pickle
from tkinter import filedialog
from Classes import Extras

class Datahandler():
    def __init__(self):
        self.config = configparser.ConfigParser()
        if os.path.exists("Data\\joemama.ini"):
            self.config.read("Data\\joemama.ini")
        else:
            f = open("Data\\joemama.ini","x")
            f.close()
            self.config.read("Data\\joemama.ini")

    def writeInI(self,section,key,value):
        if section in self.config:
            self.config[section][key] = value
        else:
            self.config.add_section(section=section)
            self.config[section][key] = value

    def getINI(self,section,key):
        if section in self.config:
            if key in self.config[section]:
                return self.config[section][key]
            else:
                self.writeInI(section=section,key=key,value="")
                return ""
        else:
            self.writeInI(section=section,key=key,value="")
            return ""
        
    def SaveINI(self):
        with open("Data\\joemama.ini","w") as configfile:
            self.config.write(configfile)

    def getQuiz(self, path:str):
        with open(path,"rb") as file:
            quiz = pickle.load(file)
        return quiz
    
    def saveQuiz(self, quiz:Extras.Quiz,path):
        try:
            with open(path,"wb") as file:
                pickle.dump(quiz,file)
        except FileNotFoundError:
            print("Angegebene Datei ungültig")