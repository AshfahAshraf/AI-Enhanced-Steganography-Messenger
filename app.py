import cv2
import tkinter as tk
from tkinter import *
import numpy as np
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from PIL import Image, ImageTk
from lsb import LSB
from aes import AESCipher


class Activity:
    master = tk.Tk()
    image = None
    imgPanel = None
    keyInput = None
    messageInput = None
    path = "./dst.png"

    clicked = '0'

    def __init__(self):
        self.master.title('StegoCrypt')
        self.image = np.zeros(shape=[100, 100, 3], dtype=np.uint8)
        self.updateImage()
        openBtn = tk.Button(self.master, text='Open', command=self.openImage)
        openBtn.pack()
        btnFrame = tk.Frame(self.master)
        btnFrame.pack()
        encodeBtn = tk.Button(btnFrame, text='Encode', command=self.encode)
        encodeBtn.pack(side=tk.LEFT)
        decodeBtn = tk.Button(btnFrame, text='Decode', command=self.decode)
        decodeBtn.pack(side=tk.LEFT)
        savebtnFrame = tk.Frame(self.master)
        savebtnFrame.pack()
        saveBtn = tk.Button(savebtnFrame, text='Save Image', command=self.saveImage)
        saveBtn.pack(side=tk.LEFT)
        tk.Label(self.master, text='Key').pack()
        self.keyInput = tk.Entry(self.master)
        self.keyInput.pack()
        tk.Label(self.master, text='Secret Message').pack()
        self.messageInput = tk.Text(self.master, height=15, width=60)
        self.messageInput.pack()

    def updateImage(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = image.resize((250, 250), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        if self.imgPanel == None:
            self.imgPanel = tk.Label(image=image)
            self.imgPanel.image = image
            self.imgPanel.pack(side="top", padx=10, pady=10)
        else:
            self.imgPanel.configure(image=image)
            self.imgPanel.image = image

    def cipher(self):
        key = self.keyInput.get()
        if len(key) != 16:
            messagebox.showwarning("Warning", "Key must be 16 character")
            return

        return AESCipher(self.keyInput.get())

    def encode(self):
        try:
            message = self.messageInput.get("1.0", 'end-1c')
            if self.clicked == '0':
                messagebox.showwarning("Warning", "Open an Image!!")
            elif len(message) == 0:
                messagebox.showwarning("Warning", "Input message to encode!!")
            else:
                if len(message) % 16 != 0:
                    message += (" " * (16 - len(message) % 16))
                cipher = self.cipher()
                if cipher == None:
                    return
                cipherText = cipher.encrypt(message)
                obj = LSB(self.image)
                obj.embed(cipherText)
                self.messageInput.delete(1.0, tk.END)
                self.image = obj.image
                self.updateImage()

        except ValueError:
            messagebox.showwarning("Warning", "Reduce message size!!")

    def decode(self):
        cipher = self.cipher()
        if cipher == None:
            return
        obj = LSB(self.image)
        cipherText = obj.extract()
        msg = cipher.decrypt(cipherText)
        self.messageInput.delete(1.0, tk.END)
        self.messageInput.insert(tk.INSERT, msg)

    def openImage(self):
        try:
            self.clicked ='1'
            path = askopenfilename()
            if not isinstance(path, str):
                return
            self.image = cv2.imread(path)
            self.updateImage()
        except:
            messagebox.showwarning("Warning", "Image is not selected!")

    def saveImage(self):
        path = asksaveasfilename(title="Select file", filetypes=[("png files", "*.png")])
        if path == '':
            return
        if ".png" not in path:
            path = path + ".png"
        obj = LSB(self.image)
        obj.save(path)
        messagebox.showinfo("Info", "Saved")

    def startLoop(self):
        self.master.mainloop()


if __name__ == "__main__":
    app = Activity()
    app.startLoop()
