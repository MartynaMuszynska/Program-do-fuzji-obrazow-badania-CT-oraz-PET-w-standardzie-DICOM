import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
import pydicom as dicom
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

"""GUI_TK
This script allows the user to display fusion of pet and ct images.
The interface allows you to select the displayed files and go through different layers.

    Imports
    --------------
        pydicom
        os
        matplotlib
        numpy
        tkinter

    Methods
    ----------
    open_ct(fusion)
        makes a list of sorted images from ct
    open_ct(fusion)
        makes a list of sorted images from pet
    graph(fusion, i)
        creates a graph by putting two specific layers of ct and pet images
    update(fusion, i)
         updates the selected layer
     
    Class
    ----------
    Fusion
        a class that creates a fusion of computed tomography and positron emission tomography
            Methods
            ----------
            __init__(self)
                constructor with no parameters


"""


# Window properties
root = Tk()
root.title("Fuzja PET/CT")
# root.iconbitmap("brain.ico")
root.geometry("750x600")
fig = Figure(figsize=(5, 5), dpi=100)
ax = fig.add_subplot()
ax.axis('off')


def open_ct(fusion):
    """loads and sorts layers of ct from a folder to list

    :param fusion: the object in which the sorted list is placed
    """

    path = filedialog.askdirectory(initialdir="source-images", title="Select a folder with CT images")
    img_ct = os.listdir(path)
    slices_ct = [dicom.read_file(path + '/' + s, force=True) for s in img_ct]
    slices_ct = sorted(slices_ct, key=lambda x: x.ImagePositionPatient[2])
    fusion.ct_slices = slices_ct
    select_pet_button.configure(state=NORMAL)
    status.configure(text="Image " + str(slider.get()) + " of " + str(len(my_fusion.ct_slices)))


def open_pet(fusion):
    """loads and sorts layers of pet from a folder to list

        :param fusion: the object in which the sorted list is placed
        """

    path = filedialog.askdirectory(initialdir="source-images/", title="Select a folder with PET images")
    img_pet = os.listdir(path)
    slices_pet = [dicom.read_file(path + '/' + s, force=True) for s in img_pet]
    slices_pet = sorted(slices_pet, key=lambda x: x.ImagePositionPatient[2])
    fusion.pet_slices = slices_pet
    slider.configure(to=len(my_fusion.ct_slices))
    update(fusion, slider.get())


class Fusion:
    """stores two sorted lists of ct and pet images
    """

    def __init__(self):
        """constructor with no parameters
        """

        self.ct_slices = []
        self.pet_slices = []


def graph(fusion, i):
    """displays a graph of the selected layers of pet and ct fusion images
    determines the ct layer from the pet layer
    sets the dimensions of the graph
    performs image interpolation

    :param fusion: object that stores ct and pet images
    :param i: selected layer of pet
    """

    ax.cla()
    ax.axis('off')
    status.configure(text="Image " + str(slider.get()) + " of " + str(len(my_fusion.ct_slices)))
    j = int((len(fusion.ct_slices)/len(fusion.pet_slices)) * i)

    if fusion.ct_slices[j].Rows > fusion.pet_slices[i].Rows:
        width = fusion.ct_slices[j].Rows
    else:
        width = fusion.ct_slices[i].Rows

    if fusion.ct_slices[j].Columns > fusion.pet_slices[i].Columns:
        height = fusion.ct_slices[j].Columns
    else:
        height = fusion.pet_slices[j].Columns

    extent = np.min(0), np.max(width-1), np.min(0), np.max(height-1)
    ax.imshow(fusion.ct_slices[j].pixel_array, cmap=plt.cm.gray, interpolation='nearest', extent=extent)
    ax.imshow(fusion.pet_slices[i].pixel_array, cmap=plt.cm.magma, alpha=0.6, interpolation='nearest', extent=extent)

    canvas.draw()


def update(fusion, i):
    """updates the selected layer
    draws a graph for selected layers

    :param fusion: object that stores ct and pet images
    :param i: currently selected layer ct
    """

    i = int(i)
    graph(fusion, i)


my_fusion = Fusion()

# Definitions
button_quit = Button(root, text="Exit", command=root.quit, anchor=E, padx=15, pady=5)
select_ct_button = Button(root, text="Choose CT images", command=lambda: open_ct(my_fusion), padx=3, pady=5)
select_pet_button = Button(root, text="Choose PET images", command=lambda: open_pet(my_fusion), pady=5, state=DISABLED)
slider = Scale(root, from_=0, to=len(my_fusion.ct_slices), orient=VERTICAL, command=lambda i: update(my_fusion, i))
status = Label(root, text="Image " + str(slider.get()) + " of " + str(len(my_fusion.ct_slices)), bd=1, relief=SUNKEN, anchor=E)
canvas = FigureCanvasTkAgg(fig, master=root)

# Pushing to GUI
canvas.get_tk_widget().grid(column=1, row=0, columnspan=3, rowspan=14, pady=10)
status.grid(column=1, row=15, columnspan=5, padx=5, pady=10, sticky=W+E)
button_quit.grid(column=4, row=16, sticky=E, padx=10)
select_ct_button.grid(column=0, row=0, padx=10)
select_pet_button.grid(column=0, row=1, padx=10)
slider.grid(column=4, row=0, rowspan=14, sticky=N+S+E, padx=10)

# Main loop
root.mainloop()
