# NEED TO INSTALL THE customtkinter
from tkinter import *
import customtkinter as ct
import sqlite3

# MAIN WINDOW FOR THE Tk()----------------------------------------------------------------------------------------------
root = Tk()
root.title('Calculator')
root.geometry("360x380")
root.resizable(False, False)

# TOP MENU TO SWITCH THE THEME OF THE APP-------------------------------------------------------------------------------
ct.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ct.set_default_color_theme("blue")
colour = StringVar(value='Light')

theme_menu = Menu(root)
theme_menu.add_command(label='Theme', command=lambda: theme_change(colour.get()))
root.config(menu=theme_menu)

# CREATE E MEMORY DATABASE TO USE WHILE THE APP IS OPEN-----------------------------------------------------------------
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS History (story text)""")


# FUNCTION TO CHANGE THE THEME------------------------------------------------------------------------------------------
def theme_change(color):
    if color == 'Light':
        ct.set_appearance_mode('Light')
        colour.set('Dark')
    elif color == 'Dark':
        ct.set_appearance_mode('Dark')
        colour.set('Light')


# MAIN AND ONLY CLASS OF THE APP----------------------------------------------------------------------------------------
class Calculator:
    def __init__(self):
        # TOP FRAME FOR THE ENTRY OF THE NUMBERS------------------------------------------------------------------------
        self.f_top = ct.CTkFrame(root, width=360, height=70)
        self.f_top.grid(row=0, column=0)
        self.f_top.grid_propagate(False)
        self.lbl = StringVar()
        self.lbl.set('')
        self.e_insert = ct.CTkLabel(self.f_top, text_font=('Comic Sans MS', 26), width=360, height=70,
                                    textvariable=self.lbl, anchor='e')
        self.e_insert.grid(row=0, column=0)

        # BOTTOM FRAME FOR THE NUMBERS AND THE OPERATORS----------------------------------------------------------------
        self.f_bot = ct.CTkFrame(root, width=360, height=311, bg='red')
        self.f_bot.grid(row=1, column=0)
        self.f_bot.grid_propagate(False)
        self.f_history = ct.CTkFrame(root, width=200, height=380)

        # HEIGHT-H, WIDTH-W, PAD X & Y FOR THE BUTTONS, ROW AND COLUMNS FOR THE GENERATED BUTTONS-----------------------
        w = 90
        h = 60
        x = y = 1
        row = 0
        column = 3
        keyboards = '/789*456-123+%0.'

        # GENERATE THE NUMBERS AND OPERATOR WITH A FOR LOOP FROM THE KEYBOARDS VAR--------------------------------------
        for i in keyboards:
            self.button = ct.CTkButton(self.f_bot, text=i, width=w, height=h, command=lambda j=i: self.click(j))
            self.button.grid(row=row, column=column, padx=x, pady=y)
            if column < 3:
                column += 1
            elif column == 3:
                column = 0
                row += 1

        # UNIQUE BUTTONS: CLEAR, HISTORY, DELETE AND EQUAL WITH EACH DIFFERENT FUNCTIONS--------------------------------
        self.bt_clear = ct.CTkButton(self.f_bot, text='C', width=w, height=h, command=self.clear)
        self.bt_clear.grid(row=0, column=0, padx=x, pady=y)
        self.bt_history = ct.CTkButton(self.f_bot, text='H', width=w, height=h, command=self.history)
        self.bt_history.grid(row=0, column=1, padx=x, pady=y)
        self.bt_delete = ct.CTkButton(self.f_bot, text='⌫', width=w, height=h, command=self.delete)
        self.bt_delete.grid(row=0, column=2, padx=x, pady=y)
        self.bt_equal = ct.CTkButton(self.f_bot, text='=', width=w, height=h, command=lambda: self.equal())
        self.bt_equal.grid(row=4, column=3, padx=x, pady=y)
        self.check_history = True
        self.delete_after = True

        # BIND THE KEYBOARD BUTTONS WITH THE NUMBERS AND OPERATORS------------------------------------------------------
        bind_key = '1234567890+-*/.'
        for i in bind_key:
            root.bind(i, lambda event, j=i: self.click(j))
        root.bind('<Return>', lambda event: self.equal())
        root.bind('<Delete>', self.clear)
        root.bind('<BackSpace>', self.delete)
        root.bind('h', self.history)

    # INSERT THE CLICKED BUTTON CHARACTER IN THE TOP LABEL--------------------------------------------------------------
    def click(self, number, *_):
        if self.delete_after:
            current = self.lbl.get()
            self.lbl.set(current + number)
        else:
            self.lbl.set('')
            current = self.lbl.get()
            self.lbl.set(current + number)
            self.delete_after = True

    # DELETE THE CHARACTERS ON THE TOP LABEL BY ONE, STARTING FROM THE RIGHT--------------------------------------------
    def delete(self, *_):
        self.lbl.set(self.lbl.get()[0:-1])

    # CLEAR COMPLETELY THE TOP LABEL------------------------------------------------------------------------------------
    def clear(self, *_):
        self.lbl.set('')

    # EVALUATE THE TOP LABEL INPUT AND INSERT THE RESULT IN THE DATABASE AND UPDATE THE LABEL---------------------------
    def equal(self, *_):
        current = self.lbl.get()
        try:
            result = round(eval(current), 2)
            self.lbl.set(result)
            self.delete_after = False
            cur.execute("INSERT INTO History VALUES(:story)", {'story': f'{current} = \n{result} \n{"-" * 28}\n'})
            if not self.check_history:
                self.check_history = True
                self.history()
            else:
                pass

        except SyntaxError:
            pass

    # CALL AND CLOSE THE HISTORY FRAME AND REFRESH IT WITHOUT CLOSING, HISTIRY IS STORED IN TEMPORARY MEMORY------------
    def history(self, *_):
        if self.check_history:
            self.check_history = False
            cur.execute('SELECT * FROM History')
            info = cur.fetchall()
            root.geometry('560x380')
            self.f_history.grid(row=0, column=1, rowspan=2)
            self.f_history.grid_propagate(False)

            def delete():
                cur.execute('DELETE FROM History;')
                self.check_history = True
                self.history()

            dlt = ct.CTkButton(self.f_history, text='Delete', width=200, command=delete)
            dlt.grid(row=0, column=0)
            box = ct.CTkTextbox(self.f_history, width=200, height=380)
            box.grid(row=1, column=0)
            x = 0
            for i in info:
                box.insert(END, i[0])
                x += 1
        else:
            self.check_history = True
            root.geometry('360x380')


if __name__ == '__main__':
    Calculator()

root.mainloop()
