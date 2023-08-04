import customtkinter as ctk
from tkinter import (
    messagebox,
    Text,
    END,
)
from database import DatabaseHelper as db
from password_generator import cryptor


class MyLabel(ctk.CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(bg_color="#121212")
        if self.master == ".!frame4":
            self.configure(bg_color="#121212")


class Placeholder:
    def __init__(self, master, placeholder="", **kwargs):
        self.e = ctk.CTkEntry(master, **kwargs)
        self.e.bind("<FocusIn>", self.focus_in)
        self.e.bind("<FocusOut>", self.focus_out)
        self.e.insert(0, placeholder)
        self.placeholder = placeholder

    def pack(self, side=None, **kwargs):
        self.e.pack(side=side, **kwargs)

    def place(self, side=None, **kwargs):
        self.e.place(side=side, **kwargs)

    def grid(self, column=None, **kwargs):
        self.e.grid(column=column, **kwargs)

    def focus_in(self, e):
        if self.e.get() == self.placeholder:
            self.e.delete(0, END)

    def focus_out(self, e):
        if self.e.get() == "":
            self.e.delete(0, END)
            self.e.insert(0, self.placeholder)


class DeleteButton(ctk.CTkButton):
    def __init__(self, tag, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(command=self.callback)
        self.tag = tag
        self.configure(
            # hover_color="dark red",
        )

    def callback(self):
        try:
            db1 = db()
            db1.deleteById(self.tag, "passwords")
            db1.saveDatabase()
            db1.closeConnection()
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("Error", "Something went wrong!")


class EditButton(ctk.CTkButton):
    def __init__(self, tag=None, user_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = tag
        self.user_id = user_id
        self.configure(
            # hover_color="dark blue",
            text="Edit",
            width=25,
            command=self.callback,
        )

    def callback(self):
        if self.master.children["!customtext"].cget("state") == "disabled":
            if self.master.children["!customtext"].cget("fg") != "#FFFFFF":
                self.master.children["!customtext"].config(fg="#FFFFFF", state="normal")
            else:
                self.master.children["!customtext"].config(state="normal")
            self.configure(text="Save")
        elif self.master.children["!customtext"].cget("state") == "normal":
            self.configure(text="Edit")
            self.master.children["!showbutton"].configure(text="Show")
            self.master.children["!customtext"].config(fg="#121212", state="disabled")
            db1 = db()
            usr = db1.selectById(self.user_id, "users")
            pwd = cryptor.encrypt(
                self.master.children["!customtext"].get("1.0", END), usr["password"]
            )
            db1.UpdateById(
                pwd,
                self.tag,
                "passwords",
            )
            db1.saveDatabase()
            db1.closeConnection()

        else:
            messagebox.showerror("Error", "Something went wrong!")


class ShowButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            text="Show",
            width=25,
            command=self.callback,
        )

    def callback(self):
        txt_widget = self.master.children["!customtext"]
        fg = txt_widget.cget("fg")

        if fg == "#121212":  # B3B3B3
            self.master.children["!customtext"].configure(fg="#FFFFFF")
            self.configure(text="Hide")
        elif fg == "#FFFFFF":
            self.master.children["!customtext"].configure(fg="#121212")
            self.configure(text="Show")


class CopyButton(ctk.CTkButton):
    def __init__(self, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.configure(
            # fg_color="blue",
            # hover_color="dark green",
            width=25,
            command=self.callback,
        )

    def callback(self):
        self.app.clipboard_clear()
        self.app.clipboard_append(self.master.children["!customtext"].get("1.0", END))


class CustomText(Text):
    def __init__(self, tag, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = tag
        self.configure(fg="#121212")
