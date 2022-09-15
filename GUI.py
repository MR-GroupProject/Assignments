import tkinter as tk

from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.title('Tkinter OptionMenu Widget')

        # initialize data
        self.languages = ('Python', 'JavaScript', 'Java',
                        'Swift', 'GoLang', 'C#', 'C++', 'Scala')

        # initialize window sizes
        self.window_sizes = ('800*600', '400*300')
        self.window_size_var = tk.StringVar(self)

        # initialize resolution
        self.resolution = ('1920*1080', '1680*1050')
        self.resolution_var = tk.StringVar(self)

        # initialize renderer
        self.renderers = ('A','B')
        self.renderer_var = tk.StringVar(self)

        # set up variable
        self.option_var = tk.StringVar(self)

        # create widget
        self.create_wigets()
        
#*************************************************#
        
    def create_wigets(self):
        # padding for widgets using the grid layout
        paddings = {'padx': 5, 'pady': 5}

        # label
        label = ttk.Label(self,  text='  language:')
        label.grid(column=0, row=0, sticky=tk.W, **paddings)

        # option menu
        option_menu = ttk.OptionMenu(
            self,
            self.option_var,
            self.languages[0],
            *self.languages,
            command=self.option_changed)
        option_menu.grid(column=1, row=0, sticky=tk.W, **paddings)

        #window size label
        window_size_label = ttk.Label(self, text = 'window size')
        window_size_label.grid(column=0, row=1, sticky=tk.W, **paddings)

        #window size menu
        window_size_menu = ttk.OptionMenu(
            self,
            self.window_size_var,
            self.window_sizes[0],
            *self.window_sizes,
            command=self.change_window_size
            )
        window_size_menu.grid(column=1, row=1, sticky=tk.W, **paddings)

        #resolution label
        resolution_label = ttk.Label(self, text = 'Resolution')
        resolution_label.grid(column=0, row=2, sticky=tk.W, **paddings)

        #Resolution menu
        resolution_menu = ttk.OptionMenu(
            self,
            self.resolution_var,
            self.resolution[0],
            *self.resolution,
            command = self.change_resolution
            )
        resolution_menu.grid(column=1, row=2, sticky=tk.W, **paddings)

        #renderer label
        renderer_label = ttk.Label(self, text = 'Renderer')
        renderer_label.grid(column=0, row=3, sticky=tk.W, **paddings)

        #renderer menu
        renderer_menu = ttk.OptionMenu(
            self,
            self.renderer_var,
            self.renderers[0],
            *self.renderers,
            command = self.change_renderer
            )
        renderer_menu.grid(column=1, row=3, sticky=tk.W, **paddings)
        
        # output label
        self.output_label = ttk.Label(self, foreground='red')
        self.output_label.grid(column=0, row=0, sticky=tk.W, **paddings)
        

    def option_changed(self, *args):
        #self.output_label = '{self.option_var.get()}'
        return 0 
        
    #change window size
    def change_window_size(self, *args):
        print('Window size: ' + self.window_size_var.get())
        return 0

    #change resolution
    def change_resolution(self, *args):
        print('resolution: ' + self.resolution_var.get())
        return 0

    #change renderer
    def change_renderer(self, *args):
        print('renderer: ' + self.renderer_var.get() )
        return 0

if __name__ == "__main__":
    app = App()
    app.mainloop()
