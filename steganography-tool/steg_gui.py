from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
import stepic

# -------- FUNCTIONS --------

def encode():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    message = text_input.get("1.0", END).strip()
    if not message:
        messagebox.showerror("Error", "Enter message to hide")
        return

    img = Image.open(file_path)

    encoded_img = stepic.encode(img, message.encode())

    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    if save_path:
        encoded_img.save(save_path)
        messagebox.showinfo("Success", "Message hidden successfully!")

def decode():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    img = Image.open(file_path)

    try:
        decoded_msg = stepic.decode(img)
        text_input.delete("1.0", END)
        text_input.insert(END, decoded_msg)
    except:
        messagebox.showerror("Error", "No hidden message found")

# -------- GUI --------

root = Tk()
root.title("🔐 Steganography Tool")
root.geometry("400x300")

Label(root, text="Enter Message:", font=("Arial", 12)).pack()

text_input = Text(root, height=8)
text_input.pack()

Button(root, text="Hide Message", command=encode, bg="green", fg="white").pack(pady=5)
Button(root, text="Extract Message", command=decode, bg="blue", fg="white").pack(pady=5)

root.mainloop()
