import pyqrcode
from screeninfo import get_monitors
import customtkinter as ctk
from tkinter import (
    messagebox,
    Frame,
    StringVar,
    Scrollbar,
    VERTICAL,
    YES,
    RIGHT,
    Y,
    Label,
    simpledialog,
)
from interface_custom_widgets import Placeholder, MyLabel
import pyotp
from interface_utils import display_passwords, qr_show, raise_frame
from login import login as log
from register import register as regist
from database import DatabaseHelper as db
from password import Password

# from smtp import send_email

ctk.set_appearance_mode("dark")
# ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Password Manager")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)
app.resizable(False, False)
app.minsize(800, 600)
user_id = None


def update_passwords(id: int):
    entry_list = main_page.pack_slaves()
    for entry in entry_list:
        if isinstance(entry, ctk.CTkEntry):
            entry.delete(0, "end")
    widgets = widgets_list.grid_slaves()
    for widget in widgets:
        widget.destroy()
    if id is not None:
        display_passwords(id, widgets_list=widgets_list, app=app)


def add_password():
    global user_id
    id = user_id
    length = int(pwd_length.get())
    name = pwd_name.get()

    if length is None or length < 3 or length > 390:
        messagebox.showerror(
            "Error", "Password length must be between 3 and 390 characters!"
        )
    elif name is None or name == "":
        messagebox.showerror("Error", "Password name must not be empty!")
    if id is None:
        messagebox.showerror("Error", "You must be logged in to add a password!")
    if Password(name, id, length) is None:
        messagebox.showerror("Error", "Password not added! Try again.")
    else:
        pwd = Password(name, id, length)
        db1 = db()
        db1.insertIntoDatabase(pwd, "passwords")
        db1.saveDatabase()
        db1.closeConnection()
        update_passwords(id)


def login():
    if (
        email.get() is not None
        and email.get().__contains__("@")
        and password.get() is not None
        and log(email.get(), password.get()) is not None
    ):
        global user_id
        usr = log(email.get(), password.get())
        user_id = usr["id"]
        if usr["tfa"] == 1:
            totp = pyotp.TOTP(usr["tfa_key"])
            # input_d = ctk.CTkInputDialog(title="2FA", text="Enter your authentication code:")
            input_d = simpledialog.askstring("2FA", "Enter your authentication code: ")
            if totp.verify(input_d):
                widgets = login_page.pack_slaves()
                for widget in widgets:
                    if isinstance(widget, ctk.CTkEntry):
                        widget.delete(0, "end")
                display_passwords(
                    usr["id"],
                    widgets_list=widgets_list,
                    app=app,
                )
                raise_frame(main_page)
            else:
                messagebox.showerror("Error", "Login failed!")
        elif usr["tfa"] == 0:
            widgets = login_page.pack_slaves()
            for widget in widgets:
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, "end")
            display_passwords(usr["id"], widgets_list=widgets_list, app=app)
            raise_frame(main_page)
    else:
        messagebox.showerror("Error", "Login failed!")


def log_out():
    global user_id
    user_id = None
    update_passwords(user_id)
    raise_frame(start_page)


def register():
    if (
        email.get() is not None
        and email.get().__contains__("@")
        and password.get() is not None
        and password_repeat.get() is not None
        and password.get() == password_repeat.get()
    ):
        usr = regist(email.get(), password.get(), bool(tfa.get()))

        if usr is None:
            messagebox.showerror("Error", "Email already exists!")
        else:
            global user_id
            user_id = usr.id

            if not bool(tfa.get()):
                messagebox.showinfo("Success", "Account created successfully!")
            else:
                messagebox.showinfo(
                    "Success", "Account created successfully! ADD YOUR QR TO AUTH APP "
                )
            # send_email(str(email.get()))
            widgets = register_page.pack_slaves()
            for widget in widgets:
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, "end")
            raise_frame(main_page)

    else:
        messagebox.showerror("Error", "Incorrect email or password!")


def back_to_start():
    widgets = register_page.pack_slaves()
    widgets.append(login_page.pack_slaves())
    for widget in widgets:
        if isinstance(widget, ctk.CTkEntry):
            widget.delete(0, "end")
    raise_frame(start_page)


def on_mousewheel(event):
    widgets_canvas.yview_scroll(int(-1 * event.delta), "units")


start_page = Frame(app)
register_page = Frame(app)
login_page = Frame(app)
main_page = Frame(app)
width_canvas = 1000
for monitor in get_monitors():
    if monitor.width > 1920:
        width_canvas = 1100
widgets_canvas = ctk.CTkCanvas(
    main_page, width=width_canvas, border=0, highlightthickness=0
)
widgets_canvas.pack(padx=30, side="left", fill="both", expand=YES)
scrollbar = Scrollbar(main_page, orient=VERTICAL, command=widgets_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)


def adjust_scrollregion(event):
    widgets_canvas.configure(scrollregion=widgets_canvas.bbox("all"))


widgets_canvas.configure(yscrollcommand=scrollbar.set)
widgets_canvas.bind(
    "<Configure>",
    lambda e: widgets_canvas.configure(scrollregion=widgets_canvas.bbox("all")),
)

widgets_list = Frame(widgets_canvas)
widgets_list.bind("<Configure>", adjust_scrollregion)

widgets_canvas.create_window((0, 0), window=widgets_list, anchor="nw")
widgets_canvas.bind_all("<MouseWheel>", on_mousewheel)
for item in (widgets_list, widgets_canvas):
    item.configure(background="#121212")
for frame in (start_page, register_page, login_page, main_page):
    frame.grid(
        row=0,
        column=0,
        sticky="news",
    )
    frame.configure(background="#121212")
# main_page.configure(background="#181818")
ctk.CTkButton(
    start_page,
    text="Login",
    command=lambda: raise_frame(login_page),
    font=("Arial", 16),
    width=280,
    height=46,
).pack(pady=(160, 60))
ctk.CTkButton(
    start_page,
    text="Register",
    command=lambda: raise_frame(register_page),
    font=("Arial", 16),
    width=280,
    height=46,
).pack(pady=(60, 0))

MyLabel(register_page, text="E-mail", font=("Arial", 16)).pack(pady=(80, 20))
email = StringVar()
ctk.CTkEntry(
    register_page, textvariable=email, width=280, height=46, font=("Arial", 16)
).pack()
MyLabel(register_page, text="Password", font=("Arial", 16)).pack(pady=(20, 20))
password = StringVar()
ctk.CTkEntry(
    register_page,
    textvariable=password,
    width=280,
    height=46,
    show="*",
    font=("Arial", 16),
).pack()
MyLabel(register_page, text="Repeat password", font=("Arial", 16)).pack(pady=(20, 20))
password_repeat = StringVar()
ctk.CTkEntry(
    register_page,
    textvariable=password_repeat,
    width=280,
    height=46,
    show="*",
    font=("Arial", 16),
).pack()

tfa = StringVar(value="on")

ctk.CTkCheckBox(
    master=register_page,
    text="Enable 2FA",
    variable=tfa,
    onvalue="on",
    fg_color="black",
    offvalue="",
).pack(padx=20, pady=10)
ctk.CTkButton(
    register_page,
    text="Register",
    command=register,
    width=160,
    height=36,
    font=("Arial", 16),
).pack(pady=30)
ctk.CTkButton(
    register_page,
    text="Back",
    command=back_to_start,
    font=("Arial", 16),
    width=160,
    height=36,
).pack(pady=(0, 30))

MyLabel(login_page, text="E-mail", font=("Arial", 16)).pack(pady=(120, 20))
ctk.CTkEntry(
    login_page, textvariable=email, width=280, height=46, font=("Arial", 16)
).pack()

MyLabel(login_page, text="Password", font=("Arial", 16)).pack(pady=(20, 20))
ctk.CTkEntry(
    login_page,
    textvariable=password,
    width=280,
    height=46,
    font=("Arial", 16),
    show="*",
).pack()
ctk.CTkButton(
    login_page,
    text="Login",
    command=login,
    font=("Arial", 16),
    width=160,
    height=36,
).pack(pady=30)
ctk.CTkButton(
    login_page,
    text="Back",
    command=back_to_start,
    font=("Arial", 16),
    width=160,
    height=36,
).pack(pady=(0, 30))
MyLabel(main_page, text="Passwords", font=("Arial", 20)).pack(
    side="top", padx=30, pady=(20, 0)
)
MyLabel(main_page, text="Password name: ").pack(side="top", padx=30, pady=(20, 0))
pwd_name = StringVar()
Placeholder(main_page, placeholder="eg. Facebook", textvariable=pwd_name).pack(
    side="top", padx=30, pady=(0, 0)
)

MyLabel(main_page, text="Password length: ").pack(side="top", padx=30, pady=(20, 0))
pwd_length = StringVar()
Placeholder(master=main_page, placeholder="0", textvariable=pwd_length).pack(
    side="top", padx=30, pady=(0, 20)
)

ctk.CTkButton(main_page, text="Add", command=add_password).pack(
    side="top", padx=30, pady=(20, 20)
)

ctk.CTkButton(
    main_page, text="Log out", command=log_out, fg_color="red", hover_color="dark red"
).pack(side="top", pady=(20, 20))

ctk.CTkButton(
    main_page, text="2fa QR code", command=lambda: qr_show(id=user_id, widget=lbl)
).pack(side="top", padx=30, pady=(20, 20))

lbl = ctk.CTkLabel(main_page, text="", fg_color="transparent")
lbl.pack(side="top", padx=30, pady=(20, 0))
raise_frame(start_page)
