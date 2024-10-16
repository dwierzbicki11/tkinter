import os.path
import tempfile
import tkinter as tk
from tkinter import font
from tkinter.ttk import *

import mysql.connector
from fontTools.ttLib import TTFont

# Połączenie z bazą danych
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="gastro"
)

root = tk.Tk()
root.geometry("400x500")



def ala():
    pass

def main():
    def load_font(ttf_file):
        font = TTFont(ttf_file)

        temp_font_path = os.path.join(tempfile.gettempdir(), os.path.basename(ttf_file))
        font.save(temp_font_path)

        return temp_font_path

    def order_food(dish_name):
        order_win = tk.Toplevel(root)
        order_win.geometry("400x500")
        order_win.title("Zamawianie")

    font_path = "res/Pacifico.ttf"
    custom_font = font.Font(size=20, weight="normal")
    custom_font.configure()

    header = Label(root,
                   text="Zamów jedzenie",
                   background="#0000ff",
                   foreground="#ffffff",
                   width="300",
                  anchor="center",
                   font=custom_font)
    header.pack()

    # Utworzenie Canvas i Scrollbar
    canvas = tk.Canvas(root)
    scroll_y = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    # Ustawienia Scrollable Frame
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Dodanie Canvas do Frame
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Ustawienia Scrollbar
    canvas.configure(yscrollcommand=scroll_y.set)

    # Umieszczanie Canvas i Scrollbar w głównym oknie
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    sql = db.cursor()
    sql.execute("SELECT * FROM dania")

    # Dodawanie wierszy do Scrollable Frame
    for row in sql.fetchall():
        dish_name = row[1]
        price = f'{row[2]} zł'

        # Utworzenie ramki dla dania i przycisku
        item_frame = Frame(scrollable_frame)
        item_frame.pack(fill=tk.X, padx=5, pady=5)

        # Dodanie Label z nazwą dania i ceną
        label = Label(item_frame, text=f"{dish_name} {price}", anchor='w', width=30)
        label.pack(side=tk.LEFT)

        # Dodanie przycisku "Zamów"
        order_button = Button(item_frame, text="Zamów", command=lambda name=dish_name: order_food(name))
        order_button.pack(side=tk.RIGHT)

    root.mainloop()

if db.is_connected():
    print("Connected to MySQL database")
    main()
else:
    print("Failed to connect to MySQL")