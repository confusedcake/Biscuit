import tkinter as tk
from tkinter.font import Font

from ...utils import Scrollbar
from ..editor import BaseEditor
from .linenumbers import LineNumbers
from .minimap import Minimap
from .text import Text


class TextEditor(BaseEditor):
    def __init__(self, master, path=None, exists=True, language=None, minimalist=False, *args, **kwargs) -> None:
        super().__init__(master, path, exists, *args, **kwargs)
        self.font: Font = self.base.settings.font
        self.minimalist = minimalist
        self.language = language
        self.exists = exists
        self.editable = True

        self.__buttons__ = [('sync', self.base.editorsmanager.reopen_active_editor),]

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.linenumbers = LineNumbers(self, font=self.font)
        self.scrollbar = Scrollbar(self, orient=tk.VERTICAL, style="EditorScrollbar")

        if not self.minimalist:
            self.minimap = Minimap(self)
            self.minimap.grid(row=0, column=2, sticky=tk.NS)

        self.text = Text(self, path=self.path, exists=self.exists, minimalist=minimalist, language=language)
        self.language = self.text.language

        if self.exists:
            self.text.load_file()
            self.text.update_idletasks()

            if c := self.base.exec_manager.get_command(self):
                self.run_command = c
                self.__buttons__.insert(0, ('run', self.run_file))
            
        self.linenumbers.attach(self.text)
        if not self.minimalist:
            self.minimap.attach(self.text)
        self.scrollbar.config(command=self.text.yview)

        self.text.config(font=self.font)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        self.linenumbers.grid(row=0, column=0, sticky=tk.NS)
        self.text.grid(row=0, column=1, sticky=tk.NSEW)
        self.scrollbar.grid(row=0, column=3, sticky=tk.NS)

        self.text.bind("<<Change>>", self.on_change)
        self.text.bind("<<Scroll>>", self.on_scroll)

        self.on_change()
        self.on_scroll()

        if self.base.settings.config.auto_save_enabled:
            self.auto_save()
    
    def run_file(self, *_):
        self.save()
        self.base.exec_manager.run_command(self)

    def on_change(self, *_):
        self.linenumbers.redraw()
        try:
            self.base.update_statusbar()
        except ValueError:
            pass
        if not self.minimalist:
            self.text.refresh()
            self.minimap.redraw_cursor()
        self.event_generate("<<Change>>")

    def on_scroll(self, *_):
        self.linenumbers.redraw()
        if not self.minimalist:
            self.minimap.redraw()
        self.event_generate("<<Scroll>>")

    def unsupported_file(self):
        self.text.show_unsupported_dialog()
        self.linenumbers.grid_remove()
        self.scrollbar.grid_remove()
        self.editable = False

    def focus(self):
        self.text.focus()
        self.on_change()

    def set_fontsize(self, size):
        self.font.configure(size=size)
        self.linenumbers.set_bar_width(size * 3)
        self.on_change()

    def save(self, path=None):
        if self.editable:
            self.text.save_file(path)

    def auto_save(self):
        self.save()
        self.base.after(self.base.settings.config.auto_save_timer_ms, self.auto_save)

    def cut(self, *_):
        if self.editable:
            self.text.event_cut()

    def copy(self, *_):
        if self.editable:
            self.text.event_copy()

    def goto(self, position):
        self.text.goto(position)

    def goto_line(self, line):
        self.text.goto_line(line)

    def paste(self, *_):
        if self.editable:
            self.text.event_paste()

    def write(self, *args, **kwargs):
        if self.editable:
            self.text.write(*args, **kwargs)

    def insert(self, *args, **kwargs):
        if self.editable:
            self.text.insert(*args, **kwargs)

    def get(self, *args, **kwargs):
        if self.editable:
            self.text.get(*args, **kwargs)

    def clear(self):
        self.delete("1.0", tk.END)

    def delete(self, *args, **kwargs):
        if self.editable:
            self.text.delete(*args, **kwargs)

    def mark_set(self, *args, **kwargs):
        if self.editable:
            self.text.mark_set(*args, **kwargs)

    def compare(self, *args, **kwargs):
        return self.text.compare(*args, **kwargs)

    def dlineinfo(self, index):
        return self.text.dlineinfo(index)

    def edit_modified(self, arg=None):
        return self.text.edit_modified(arg)

    def edit_redo(self):
        if self.editable:
            self.text.stack_redo()

    def edit_reset(self):
        if self.editable:
            self.text.edit_reset()

    def edit_separator(self):
        if self.editable:
            self.text.edit_separator()

    def edit_undo(self):
        if self.editable:
            self.text.stack_undo()

    def image_create(self, index, **kwargs):
        if self.editable:
            return self.text.image_create(index, **kwargs)

    def image_cget(self, index, option):
        return self.text.image_cget(index, option)

    def image_configure(self, index, **kwargs):
        if self.editable:
            return self.text.image_configure(index, **kwargs)

    def image_names(self):
        return self.text.image_names()

    def index(self, i):
        return self.text.index(i)

    def mark_gravity(self, mark, gravity=None):
        return self.text.mark_gravity(mark, gravity)

    def mark_names(self):
        return self.text.mark_names()

    def mark_next(self, index):
        return self.text.mark_next(index)

    def mark_previous(self, index):
        return self.text.mark_previous(index)

    def mark_set(self, mark, index):
        if self.editable:
            self.text.mark_set(mark, index)

    def mark_unset(self, mark):
        if self.editable:
            self.text.mark_unset(mark)

    def scan_dragto(self, x, y):
        self.text.scan_dragto(x, y)

    def scan_mark(self, x, y):
        self.text.scan_mark(x, y)

    def search(self, pattern, index, **kwargs):
        return self.text.search(pattern, index, **kwargs)

    def see(self, index):
        self.text.see(index)

    def tag_add(self, tagName, index1, index2=None):
        if self.editable:
            self.text.tag_add(tagName, index1, index2)

    def tag_bind(self, tagName, sequence, func, add=None):
        self.text.tag_bind(tagName, sequence, func, add)

    def tag_cget(self, tagName, option):
        return self.text.tag_cget(tagName, option)

    def tag_config(self, tagName, **kwargs):
        if self.editable:
            self.text.tag_config(tagName, **kwargs)

    def tag_names(self, index=None):
        return self.text.tag_names(index)

    def tag_nextrange(self, tagName, index1, index2=None):
        return self.text.tag_nextrange(tagName, index1, index2)

    def tag_prevrange(self, tagName, index1, index2=None):
        return self.text.tag_prevrange(tagName, index1, index2)

    def tag_raise(self, tagName, aboveThis=None):
        if self.editable:
            self.text.tag_raise(tagName, aboveThis)

    def tag_ranges(self, tagName):
        return self.text.tag_ranges(tagName)

    def tag_remove(self, tagName, index1, index2=None):
        if self.editable:
            self.text.tag_remove(tagName, index1, index2)

    def tag_unbind(self, tagName, sequence, funcid=None):
        self.text.tag_unbind(tagName, sequence, funcid)

    def window_cget(self, index, option):
        return self.text.window_cget(index, option)

    def window_configure(self, index, **kwargs):
        if self.editable:
            self.text.window_configure(index, **kwargs)

    def window_create(self, index, **kwargs):
        if self.editable:
            self.text.window_create(index, **kwargs)

    def window_names(self):
        return self.text.window_names()

    def xview_moveto(self, fraction):
        self.text.xview_moveto(fraction)

    def xview_scroll(self, n, what):
        self.text.xview_scroll(n, what)

    def yview_moveto(self, fraction):
        self.text.yview_moveto(fraction)

    def yview_scroll(self, n, what):
        self.text.yview_scroll(n, what)
