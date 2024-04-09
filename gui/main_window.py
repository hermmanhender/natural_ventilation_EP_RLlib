"""Here is the main window configuration of the app. All the others windows are based in this design.
"""
import tkinter as tk
from tkinter import ttk

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
    def __init__(self):
        """
        """
        super().__init__()

        # The Frames are defined
        process_section_frame = ProcessSections(self)
        work_space_frame = WorkSpace(self)

        # The widgets are defined



class ProcessSections(tk.Frame):
    """
    """
    def __init__(self, container):
        """
        """
        super().__init__(container)


class WorkSpace(tk.Frame):
    """
    """
    def __init__(self, container):
        """
        """
        super().__init__(container)
