"""Here is the main window configuration of the app. All the others windows are based in this design.
"""
import tkinter as tk
from tkinter import ttk
from eprllib.gui.WorkSpaces import *

class EprllibMainWindow(tk.Tk):
    """This class define the main window of the program, where all
    the Frames are ordner and the diferents buttons are defined.
    This program has two Frames, one where the process of the configuration
    is perform (select input data, DRL models and so on) and where the
    user will be interact to. The second one is the work space used to
    configurate every step of the configuration.

    This second frame allocated diferents configurations of frames, 
    depending of the necessity of the step in the configuration process.
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)

        self.title("eprllib: EnergyPlus for RLlib experimentation.")
        self.size(600,400)

        # The Frames are defined
        process_section_frame = ProcessSections(self, padx=60, pady=30, sticky="w")
        work_space_frame = WorkSpace(self, padx=60, pady=30, sticky="nsew")

        # The frames are packed here into a Grid
        process_section_frame.grid(column=0, row=0)
        work_space_frame.grid(column=1, row=0)




class ProcessSections(tk.Frame):
    """
    """
    def __init__(self, container, **kwargs):
        """
        """
        super().__init__(container, **kwargs)

        start_config_window = ttk.Frame(self)
        start_config_window.grid(column=0, row=0, sticky="NSEW")

        # The widgets are defined
        new_project_start_button = ttk.Button(
            self,
            text="New Environment",
            command=self.start
        )

    def start(self):
        """This method start a frame into the work space frame that
        it use for define the start varaibles of the project.
        """
        self.start_config_window.tkraise()
        

class WorkSpace(tk.Frame):
    """
    """
    def __init__(self, container):
        """
        """
        super().__init__(container)
