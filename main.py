import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog

root = tk.Tk()
root.title("Disappearing Text App")
root.configure(background="white")
root.geometry("700x700")

MainFrame = Frame(root, bg="white", bd=0)
MainFrame.grid(row=0, column=0, padx=0)

title = Label(MainFrame, font=("Courier New", 28, "bold"), bg="white", text="Disappearing", fg="red")
title.grid(row=0, column=2, columnspan=2, pady=10, padx=20)

title = Label(MainFrame, font=("Courier New", 28, "bold"), bg="white", text="Text")
title.grid(row=0, column=3, columnspan=2, pady=10, padx=20)

display = Text(MainFrame, font=("Courier New", 16), bd=2, width=53, bg="white", state=DISABLED)
display.grid(row=2, column=2, columnspan=3, pady=10)

timer_label = Label(MainFrame, font=("Courier New", 16), bg="white", fg="black")
timer_label.grid(row=1, column=2, columnspan=3, pady=10)

timer = None
countdown_time = 0
difficulty = ""
save_enabled = False

def set_difficulty(value):
    global countdown_time, difficulty
    difficulty = value
    if difficulty == "Easy":
        countdown_time = 15
    elif difficulty == "Medium":
        countdown_time = 10
    else:  # Hard
        countdown_time = 5
    show_save_option()

def show_save_option():
    global save_option_window
    save_option_window = Toplevel(root)
    save_option_window.title("Save Option")
    save_option_window.geometry("300x150")
    Label(save_option_window, text="Enable saving?", font=("Courier New", 16)).pack(pady=20)

    Button(save_option_window, text="Yes", bg="green", font=("Courier New", 14), command=enable_save_and_close).pack(pady=5)
    Button(save_option_window, text="No", bg="red", font=("Courier New", 14), command=disable_save_and_close).pack(pady=5)

def enable_save_and_close():
    global save_enabled
    save_enabled = True
    save_option_window.destroy()
    difficulty_window.destroy()
    display.config(state=NORMAL)

def disable_save_and_close():
    global save_enabled
    save_enabled = False
    save_option_window.destroy()
    difficulty_window.destroy()
    display.config(state=NORMAL)

def start_timer(event):
    global timer, countdown_time
    remaining_time = countdown_time
    if timer:
        root.after_cancel(timer)
    update_timer(remaining_time)
    timer = root.after(1000, countdown, remaining_time - 1)

def countdown(remaining_time):
    global timer
    if remaining_time > 0:
        update_timer(remaining_time)
        timer = root.after(1000, countdown, remaining_time - 1)
    else:
        if save_enabled:
            prompt_save()
        else:
            clear_text()

def update_timer(remaining_time):
    timer_label.config(text=f"Time remaining: {remaining_time} seconds")

def prompt_save():
    user_response = messagebox.askyesno("Time's up!", "Do you want to save your text?")
    if user_response:
        save_text()
    clear_text()

def save_text():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(display.get("1.0", END))

def clear_text():
    display.delete('1.0', END)
    timer_label.config(text="")

def show_difficulty_window():
    global difficulty_window
    difficulty_window = Toplevel(root)
    difficulty_window.title("Choose Difficulty")
    difficulty_window.geometry("300x200")
    Label(difficulty_window, text="Select Difficulty", font=("Courier New", 16)).pack(pady=20)

    Button(difficulty_window, text="Easy", bg="green", font=("Courier New", 14), command=lambda: set_difficulty("Easy")).pack(pady=5)
    Button(difficulty_window, text="Medium", bg="yellow", font=("Courier New", 14), command=lambda: set_difficulty("Medium")).pack(pady=5)
    Button(difficulty_window, text="Hard", bg="red", font=("Courier New", 14), command=lambda: set_difficulty("Hard")).pack(pady=5)

display.bind('<Key>', start_timer)
show_difficulty_window()

root.mainloop()
