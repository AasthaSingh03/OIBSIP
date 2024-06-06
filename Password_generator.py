import tkinter as tk
from tkinter import messagebox
import string
import random
import pyperclip as ppr

root = tk.Tk()
root.geometry('600x600+0+0')
root.title('Advanced Password Generator')

#for icon 
icon_path = 'Password_generator_img.png'
root.iconphoto(False, tk.PhotoImage(file=icon_path))

def password():
        length = length_.get()
        exclude_chars = set(exclude_var.get())
        
        characters = ""
        if uppercase.get():
            characters += string.ascii_uppercase
        if lowercase.get():
            characters += string.ascii_lowercase
        if digits.get():
            characters += string.digits
        if symbol.get():
            characters+=string.punctuation
        #if exclude_var.get():
         #  characters += string.punctuation

    #for removing excluded chars
        remove_characters = []
        for c in characters:
            if c not in exclude_chars:
                remove_characters.append(c)

        characters = ''.join(remove_characters)  

        result = []

        for c in characters:
            if c not in exclude_chars:
                result.append(c)

        characters = ''.join(result) 

        if not characters:
           messagebox.showerror("Error", "No characters available for password generation!")
           return  
        
        password = []
        for l in range(length):
            password.append(random.choice(characters))

        password = ''.join(password)
        password_var.set(password)

def copy_to_clipboard():
    password=password_var.get()
    if password:
        ppr.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")   

lb1=tk.Label(root,text="Generate Password",font=('Helvetica',20,'bold'),fg='red' ,activebackground='grey')
lb1.grid(row=0, column=0, columnspan=2, pady=20)


lb2=tk.Label(root,text='Password length:',font=('times new roman',15 ))
lb2.grid(row=1, column=0, pady=10, sticky='e')
length_=tk.IntVar(value=11)
tk.Spinbox(root, from_=4, to_=70,textvariable=length_,width=10,).grid(row=1, column=1)

#include uppercase
uppercase=tk.BooleanVar(value=True)
tk.Checkbutton(root,text='Include Uppercase(A-Z)',variable=uppercase,font=('times new roman',15 )).grid(row=2, column=0, columnspan=2, sticky='w', padx=20)

##include lowercase
lowercase=tk.BooleanVar(value=True)
tk.Checkbutton(root,text='Include Lowercase(a-z)',variable=lowercase,font=('times new roman',15 )).grid(row=3, column=0, columnspan=2, sticky='w', padx=20)

#include digits
digits=tk.BooleanVar(value=True)
tk.Checkbutton(root,text='Include Digits(0-9)',variable=digits,font=('times new roman',15 )).grid(row=4, column=0, columnspan=2, sticky='w', padx=20)

#include Symbols
symbol=tk.BooleanVar(value=True)
tk.Checkbutton(root,text='Include Symbols(!@#$%^&*()-_=+)',variable=symbol,font=('times new roman',15 )).grid(row=5, column=0, columnspan=2, sticky='w', padx=20)

#exclude characters
tk.Label(root, text="Exclude Characters:",font=('times new roman',15 )).grid(row=6, column=0, sticky='e', pady=10)
exclude_var = tk.StringVar()
tk.Entry(root, textvariable=exclude_var,width=45).grid(row=6, column=1, pady=10, sticky='w')

#for button
tk.Button(root,text='Generate Password',font=('times new roman',15 ),bg='yellow',fg='blue',command=password).grid(row=7, column=0, pady=10, sticky='e')
password_var = tk.StringVar()
tk.Entry(root, textvariable=password_var, width=50, state='readonly').grid(row=7, column=1, pady=5,padx=10)

#for copy clipboard
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard,bg='yellow',fg='blue').grid(row=9, column=0, columnspan=2, pady=10)



root.mainloop()
