from interface_custom_widgets import (
    CustomText,
    DeleteButton,
    EditButton,
    CopyButton,
    ShowButton,
)
from password_generator import cryptor
import pyqrcode
import customtkinter as ctk
from tkinter import (
    BitmapImage,
    messagebox,
    Frame,
    LEFT,
    Label,
    Grid,
)
from database import DatabaseHelper as db
import pyotp


def display_passwords(id: int, widgets_list: Frame = None, app=None) -> None:
    db1 = db()
    passwords = db1.show_user_passwords(id)
    for num, password in enumerate(passwords):
        pid, name, pwd = password
        usr = db1.selectById(id, "users")
        pwd = cryptor.decrypt(pwd, usr["password"])
        password_frame = ctk.CTkCanvas(widgets_list, border=0, highlightthickness=0)
        password_frame.grid(row=num, column=0, sticky="news", pady=5, ipadx=8)

        password_frame.configure(background="#121212")
        Grid.columnconfigure(password_frame, 0, weight=1)
        Grid.rowconfigure(password_frame, 1, weight=1)
        e = Label(
            password_frame,
            borderwidth=0,
            text=f"{name}",
            font=("Arial", 14),
            wraplength=70,
            justify=LEFT,
            bg="#121212",
            fg="#B3B3B3",
        )
        if len(pwd) <= 70:
            f = CustomText(
                str(pid), password_frame, height=1, border=0, highlightthickness=0
            )
        elif len(pwd) <= 150:
            f = CustomText(
                str(pid), password_frame, height=2, border=0, highlightthickness=0
            )
        elif len(pwd) <= 230:
            f = CustomText(
                str(pid), password_frame, height=3, border=0, highlightthickness=0
            )
        elif len(pwd) <= 310:
            f = CustomText(
                str(pid), password_frame, height=4, border=0, highlightthickness=0
            )
        elif len(pwd) <= 390:
            f = CustomText(
                str(pid), password_frame, height=5, border=0, highlightthickness=0
            )
        elif len(pwd) > 390:
            f = CustomText(
                str(pid), password_frame, height=8, border=0, highlightthickness=0
            )
        g = DeleteButton(
            str(pid),
            password_frame,
            text="Delete",
            width=25,
        )
        h = EditButton(master=password_frame, tag=str(pid), user_id=id)
        j = CopyButton(app=app, master=password_frame, text="Copy")
        k = ShowButton(master=password_frame, text="Show")

        f.insert(1.0, f"{pwd}")
        f.config(state="disabled", background="#121212")
        e.grid(row=num, column=1, columnspan=2, pady=10, sticky="news")
        f.grid(row=num, column=3, pady=10, padx=20, sticky="ew")
        g.grid(row=num, column=4, pady=10, padx=3, ipadx=3, ipady=3)
        h.grid(row=num, column=5, pady=10, padx=3, ipadx=3, ipady=3)
        j.grid(row=num, column=6, pady=10, padx=3, ipadx=3, ipady=3)
        k.grid(row=num, column=7, pady=10, padx=3, ipadx=3, ipady=3)


def raise_frame(frame) -> None:
    frame.tkraise()


def qr_show(id: int, widget: Label) -> None:
    db1 = db()
    id = id
    user = db1.selectById(id, "users")

    if user["tfa"] == 1:
        if widget.cget("image") == "":
            tfa_key = db1.getUserTfaKey(id)
            u_name = user["email"]
            uri = pyotp.totp.TOTP(tfa_key).provisioning_uri(
                name=u_name, issuer_name="Password Manager"
            )
            qr = pyqrcode.create(uri)
            encoded = qr.xbm(scale=2)
            img = BitmapImage(data=encoded)

            widget.configure(image=img, fg_color="white")
        else:
            widget.configure(image="", fg_color="transparent")
    else:
        messagebox.showerror("Error", "2FA is not enabled!")
