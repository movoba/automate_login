
from gui import LoginFrame
import tkinter as tk
import time
import schedule

def main():
    root = tk.Tk()
    gui = LoginFrame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
