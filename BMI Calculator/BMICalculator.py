import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

# Database setup
conn = sqlite3.connect("bmi_data.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bmi_records (name TEXT, weight REAL, height REAL, bmi REAL)''')
conn.commit()


# BMI calculation and classification functions
def calculate_bmi(weight, height):
    return weight / (height ** 2)


def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"


def save_bmi():
    try:
        name = entry_name.get()
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)

        c.execute("INSERT INTO bmi_records (name, weight, height, bmi) VALUES (?, ?, ?, ?)",
                  (name, weight, height, bmi))
        conn.commit()

        messagebox.showinfo("Result", f"BMI: {bmi:.2f}\nCategory: {category}")
        entry_name.delete(0, tk.END)
        entry_weight.delete(0, tk.END)
        entry_height.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for weight and height.")


def show_trend():
    try:
        c.execute("SELECT bmi FROM bmi_records")
        bmi_values = [row[0] for row in c.fetchall()]
        if bmi_values:
            plt.plot(bmi_values, marker='o', linestyle='-', color='b')
            plt.title("BMI Trend")
            plt.xlabel("Record Number")
            plt.ylabel("BMI Value")
            plt.show()
        else:
            messagebox.showinfo("Info", "No data to display.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI setup
root = tk.Tk()
root.title("BMI Calculator")

# Widgets
tk.Label(root, text="Name").grid(row=0, column=0)
tk.Label(root, text="Weight (kg)").grid(row=1, column=0)
tk.Label(root, text="Height (m)").grid(row=2, column=0)

entry_name = tk.Entry(root)
entry_weight = tk.Entry(root)
entry_height = tk.Entry(root)

entry_name.grid(row=0, column=1)
entry_weight.grid(row=1, column=1)
entry_height.grid(row=2, column=1)

tk.Button(root, text="Calculate and Save BMI", command=save_bmi).grid(row=3, column=0, columnspan=2)
tk.Button(root, text="Show BMI Trend", command=show_trend).grid(row=4, column=0, columnspan=2)

root.mainloop()

# Close the database connection when the app closes
conn.close()
