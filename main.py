from tkinter import Tk
from src.password_generator_gui import PasswordGeneratorGUI

def main():
    master = Tk()
    generator_gui = PasswordGeneratorGUI(master, 'Password generator 1.0')
    generator_gui.create_widgets()
    generator_gui.add_style()
    master.mainloop()

if __name__ == '__main__':
    main()