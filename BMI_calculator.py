from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
import sqlite3
import webbrowser

#connecting database
conn = sqlite3.connect('bmi_calculator.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS bmi_data (
        id INTEGER PRIMARY KEY,name TEXT,weight REAL,height REAL,bmi REAL,date TEXT)''')
conn.commit()

root=Tk()
root.title("Advanced BMI calculator")
root.geometry("800x800+0+0")
icon_path = 'BMI_img.png'
root.iconphoto(False, PhotoImage(file=icon_path))


def BMI_calculate():
    try:
        name=name_entry.get()
        height=float(height_entry.get())
        weight=float(weight_entry.get())
        BMI=float(weight/(height)**2)
        BMI=round(BMI,2)

        result_label.config(text=f"{name}, your BMI is: {BMI}")
        messagebox.showinfo("BMI Result", f"{name}, your BMI is {BMI}")

        if BMI < 18.5:
            messagebox.showinfo("BMI Result", "You are underweight.")
        elif 18.5 <= BMI < 24.9:
            messagebox.showinfo("BMI Result", "You have a normal weight.")
        elif 25 <= BMI < 29.9:
            messagebox.showinfo("BMI Result", "You are overweight.")
        else:
            messagebox.showinfo("BMI Result", "You are obese.")

        # Insert data into the database
        c.execute('INSERT INTO bmi_data (name, weight, height, bmi, date) VALUES (?, ?, ?, ?, date("now"))',
                  (name, weight, height, BMI))
        conn.commit()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

def instrutions_underweight():
    #mylink=Label(root,text='underweight',font=('times on roman',15))
    #mylink.grid(row=0, column=0, columnspan=2, pady=11)
    webbrowser.open(f"https://www.google.com/search?q=underweight+balance+diet&rlz=1C1PRFI_enIN1022IN1022&oq=u&gs_lcrp=EgZjaHJvbWUqBggAEEUYOzIGCAAQRRg7MgYIARBFGDsyEwgCEC4YgwEYxwEYsQMY0QMYgAQyBggDEEUYOTINCAQQABiDARixAxiABDINCAUQABiDARixAxiABDITCAYQLhiDARjHARixAxjRAxiABDIWCAcQLhiDARjHARixAxjRAxiABBiKBTITCAgQLhiDARjHARixAxjRAxiABDIHCAkQABiPAtIBCjQ1ODUyajBqMTWoAgiwAgE&sourceid=chrome&ie=UTF-8") 

def instrutions_overweight():
    #mylink=Label(root,text='underweight',font=('times on roman',15))
    #mylink.grid(row=0, column=0, columnspan=2, pady=11)
    webbrowser.open(f"https://www.google.com/search?q=overweight+balance+diet&sca_esv=9a83bf99618973ac&rlz=1C1PRFI_enIN1022IN1022&sxsrf=ADLYWILpzgHb7x2UWHiY52zRmo42jaHUmg%3A1717670286159&ei=jpFhZrikCc3f2roP38qUyQE&ved=0ahUKEwi4o_255MaGAxXNr1YBHV8lJRkQ4dUDCBA&uact=5&oq=overweight+balance+diet&gs_lp=Egxnd3Mtd2l6LXNlcnAaAhgCIhdvdmVyd2VpZ2h0IGJhbGFuY2UgZGlldDIIEAAYFhgeGA8yCxAAGIAEGIYDGIoFMgsQABiABBiGAxiKBTILEAAYgAQYhgMYigUyCxAAGIAEGIYDGIoFMgsQABiABBiGAxiKBTIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYgAQYogRIjfkDULwCWI7qA3AUeAGQAQKYAfQEoAHcMKoBCjAuNy4xNy41LTK4AQPIAQD4AQGYAiSgAsIiwgIKEAAYsAMY1gQYR8ICBRAAGIAEwgIGEAAYFhgewgIKEAAYgAQYQxiKBcICCxAAGIAEGLEDGIMBwgIIEAAYgAQYsQPCAgsQABiABBiRAhiKBcICCxAAGIAEGKIEGIsDwgIIEAAYiwMY7wXCAgcQABiABBgNwgIGEAAYDRgewgIKEAAYFhgKGB4YD5gDAIgGAZAGCJIHDTIwLjMuMTAuMS4xLjGgB9arAQ&sclient=gws-wiz-serp")
def history_view():
        history_window = Toplevel(root)

        c.execute('SELECT * FROM bmi_data')
        records = c.fetchall()
        history_window.title("BMI History")

        Label(history_window, text="ID").grid(row=0, column=0)
        Label(history_window, text="Name").grid(row=0, column=1)
        Label(history_window, text="Weight (kg)").grid(row=0, column=2)
        Label(history_window, text="Height (m)").grid(row=0, column=3)
        Label(history_window, text="BMI").grid(row=0, column=4)
        Label(history_window, text="Date").grid(row=0, column=5)
        
        for i, record in enumerate(records):
            for j, value in enumerate(record):
                Label(history_window, text=value).grid(row=i + 1, column=j) 

    

def plot_BMI():
    name = name_entry.get()
    
    # Fetching data for all users
    c.execute('SELECT name, date, bmi FROM bmi_data ORDER BY date')
    records = c.fetchall()

    if not records:
        messagebox.showerror("No Data", "No data available in the database.")
        return

    all_dates = {}
    user_dates = []
    user_bmis = []

    for record in records:
        user_name, date, bmi = record
        if user_name not in all_dates:
            all_dates[user_name] = ([], [])
        all_dates[user_name][0].append(date)
        all_dates[user_name][1].append(bmi)
        
        if user_name == name:
            user_dates.append(date)
            user_bmis.append(bmi)

    plt.figure()

    # Plot data for all users
    flag=0
    for user_name, (dates, bmis) in all_dates.items():
        if flag==0:
            plt.plot(dates, bmis, marker='o',color='blue',linestyle='--' , label="Others") 
            flag=1
        elif user_name == name:
            plt.plot(dates, bmis, marker='o', color='yellow',linestyle='-' , label=user_name)
        else:
            plt.plot(dates, bmis, marker='o',color='blue')

    # Highlight the current user's data
    #plt.plot(user_dates, user_bmis, marker='o', linestyle='-', color='red', linewidth=2, label=f'{name} (highlighted)')
    
    plt.xlabel('Date')
    plt.ylabel('BMI')
    plt.title('BMI Trends')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

lb=Label(root,text="BMI Calculation",font=('Helvetica',25,'bold'),fg='red')
lb.grid(row=0, column=0, columnspan=2, pady=11)

lb1=Label(root,text='Name',font=('times on roman',15))
lb1.grid(row=1,column=0,padx=11,pady=11)
name_entry = Entry(root,font=('times on roman',12))
name_entry.grid(row=1, column=1, padx=11, pady=11)

lb1=Label(root,text='Height(m)',font=('times on roman',15))
lb1.grid(row=2,column=0,padx=11,pady=11)
height_entry = Entry(root,font=('times on roman',12))
height_entry.grid(row=2, column=1, padx=11, pady=11)

lb1=Label(root,text='Weight(Kg)',font=('times on roman',15))
lb1.grid(row=3,column=0,padx=11,pady=11)
weight_entry = Entry(root,font=('times on roman',12))
weight_entry.grid(row=3, column=1, padx=11, pady=11)

calculate_button = Button(root, text="Calculate BMI",font=('times on roman',15),fg='blue',bg='yellow' ,command=BMI_calculate)
calculate_button.grid(row=4, column=0, columnspan=1, pady=11,padx=3)

result_label = Label(root, text=" :Your BMI will be displayed here.",font=('times on roman',15))
result_label.grid(row=4, column=1, columnspan=2, pady=11)

history_button = Button(root, text="View History",font=('times on roman',15),fg='blue',bg='yellow', command=history_view)
history_button.grid(row=5, column=0, columnspan=1, pady=11)

plot_button = Button(root, text="Plot BMI Trends",font=('times on roman',15),fg='blue',bg='yellow', command=plot_BMI)
plot_button.grid(row=5, column=1, columnspan=1, pady=11)

link_button=Button(root, text="Instructions underweight",font=('times on roman',12),fg='black',bg='blue' ,command=instrutions_underweight)
link_button.grid(row=6, column=0, columnspan=1, pady=11,padx=3)

link_button=Button(root, text="Instructions overweight",font=('times on roman',12),fg='black',bg='blue' ,command=instrutions_overweight)
link_button.grid(row=6, column=1, columnspan=1, pady=11,padx=3)

root.mainloop()
conn.close()

