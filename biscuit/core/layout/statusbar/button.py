from __future__ import annotations

import tkinter as tk
import typing

from biscuit.core.components.utils import Bubble, Frame, get_codicon

if typing.TYPE_CHECKING:
    from . import Statusbar


class SBubble(Bubble):
    def get_pos(self) -> str:
        return (f"+{int(self.master.winfo_rootx() + (self.master.winfo_width() - self.winfo_width())/2)}" + 
                f"+{self.master.winfo_rooty() - self.master.winfo_height() - 10}")


class SButton(Frame):
    def __init__(self, master: Statusbar, text: str=None, icon: str=None, function=None, 
                 description: str=None, padx: int=5, pady: int=1, *args, **kwargs) -> None:
        super().__init__(master, padx=padx, pady=pady, *args, **kwargs)
        self.function = function or (lambda *_: None)

        self.bg, self.fg, self.hbg, self.hfg = self.base.theme.layout.statusbar.button.values()
        self.config(bg=self.bg)
        self.text = text
        self.icon = icon

        self.bubble = SBubble(self, text=description)

        if icon:
            self.icon_label = tk.Label(self, text=get_codicon(self.icon), anchor=tk.CENTER, 
                bg=self.bg, fg=self.fg, font=("codicon", 12))
            self.icon_label.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        if text:
            self.text_label = tk.Label(self, text=self.text, anchor=tk.CENTER, 
                    bg=self.bg, fg=self.fg, pady=2, font=("Segoe UI", 9))
            self.text_label.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        self.config_bindings()
        self.visible = False

    def config_bindings(self) -> None:
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.bind("<Button-1>", self.on_click)
        if self.text:
            self.text_label.bind("<Button-1>", self.on_click)
        if self.icon:
            self.icon_label.bind("<Button-1>", self.on_click)

    def on_enter(self, *_) -> None:
        self.bubble.show()
        self.config(bg=self.hbg)
        if self.text:
            self.text_label.config(bg=self.hbg, fg=self.hfg)
        if self.icon:
            self.icon_label.config(bg=self.hbg, fg=self.hfg)

    def on_leave(self, *_) -> None:
        self.bubble.hide()
        self.config(bg=self.bg)
        if self.text:
            self.text_label.config(bg=self.bg, fg=self.fg)
        if self.icon:
            self.icon_label.config(bg=self.bg, fg=self.fg)

    def on_click(self, *_) -> None:
        self.function()
        self.bubble.hide()

    def change_text(self, text: str) -> None:
        self.text_label.config(text=text)

    def change_description(self, text: str) -> None:
        self.bubble.change_text(text)

    def change_icon(self, icon: str) -> None:
        self.icon_label.config(text=get_codicon(icon))

    def change_function(self, function: typing.Callable) -> None:
        self.function = function

    def set_pack_data(self, **kwargs) -> None:
        self.pack_data = kwargs

    def get_pack_data(self) -> None:
        return self.pack_data

    def show(self) -> None:
        if not self.visible:
            self.lift()
            self.visible = True
            self.pack(**self.get_pack_data())

    def hide(self) -> None:
        if self.visible:
            self.visible = False
            self.pack_forget()

class TerminalButton(SButton):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.bg = self.base.theme.biscuit
        self.hbg = self.base.theme.biscuit_dark
        self.fg = "white"
        self.hfg = "white"        
        self.on_leave()
