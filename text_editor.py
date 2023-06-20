#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from tkinter import messagebox
import enchant

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")

        self.text_list = None

        self.text_area = Text(self.root)
        self.text_area.pack(fill=BOTH, expand=True)

        self.menu_bar = Menu(self.root)                                          #creating menu

        self.file_menu = Menu(self.menu_bar, tearoff=0)                          #file menu
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.edit_menu = Menu(self.menu_bar, tearoff=0)                          #edit menu
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Redo", command=self.redo)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        
        self.format_menu = Menu(self.menu_bar, tearoff=0)                        #format menu
        self.format_menu.add_command(label="Uppercase", command=self.convert_to_uppercase)
        self.format_menu.add_command(label="Lowercase", command=self.convert_to_lowercase)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        
        self.check_menu = Menu(self.menu_bar, tearoff=0)                         #spell checker menu
        self.check_menu.add_command(label="Check Spelling", command=self.check_spelling)
        self.menu_bar.add_cascade(label="Check", menu=self.check_menu)
        
        self.root.config(menu=self.menu_bar)

        self.dictionary = enchant.Dict("en_US")     #enchant is the module used to check for correct spellings and words

        
    def new_file(self):                               #function to create new file                      
        self.text_area.delete(1.0, END) 
        self.text_list = None

    def open_file(self):                              #function to open file
        file = open("text.txt", "r")
        content = file.read()
        self.text_area.delete(1.0, END) #to delete the text in widget from line 1 to end line
        self.text_area.insert(END, content)
        file.close()

        self.text_list = self.create_linked_list(content)

    def save_file(self):                             #function to save file
        content = self.text_area.get(1.0, END)
        file = open("text.txt", "w")
        file.write(content)
        file.close()

        self.text_list = self.create_linked_list(content)

    def undo(self):                                  #function to perform undo operation
        if self.text_list is not None and self.text_list.prev is not None:
            self.text_list = self.text_list.prev
            self.text_area.delete(1.0, END)
            self.text_area.insert(END, self.text_list.data)

    def redo(self):                                 #function to perform redo operation
        if self.text_list is not None and self.text_list.next is not None:
            self.text_list = self.text_list.next
            self.text_area.delete(1.0, END)
            self.text_area.insert(END, self.text_list.data)
            
    def convert_to_uppercase(self):
        if self.text_list is not None:
            self.text_list.data = self.text_list.data.upper()
            self.update_text_area()

    def convert_to_lowercase(self):
        if self.text_list is not None:
            self.text_list.data = self.text_list.data.lower()
            self.update_text_area()

    def update_text_area(self):
        self.text_area.delete(1.0, END)
        current = self.text_list

        while current is not None:
            self.text_area.insert(END, current.data)
            current = current.next
            
        
    def check_spelling(self):                   #function to check for correct spelling and suggest for misspelled words
        if self.text_list is not None:          
            text = self.text_list.data
            words = text.split()
            misspelled = []

            for word in words:
                if not self.dictionary.check(word):
                    misspelled.append(word)

            if misspelled:
                messagebox.showinfo("Spelling Checker", "Misspelled words: " + ", ".join(misspelled))
                for word in misspelled:
                    messagebox.showinfo("Spelling Suggestion","Suggested words: "+ ","+str(self.dictionary.suggest(word)))
       
            else:
                messagebox.showinfo("Spelling Checker", "No misspelled words found.")

    @staticmethod
    def create_linked_list(content):    #function to create Linked list
        lines = content.split("\n")     #creating a list of lines
        head = Node(lines[0])
        current = head

        for line in lines[1:]:
            node = Node(line)           #creating a node for each line
            current.next = node
            node.prev = current
            current = node

        return head

root = Tk()
editor = TextEditor(root)
root.mainloop()


# In[ ]:




