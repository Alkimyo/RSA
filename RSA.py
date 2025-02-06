import tkinter as tk
from tkinter import messagebox
import random

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    d, x1, x2, y1 = 0, 0, 1, 1
    temp_phi = phi
    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi, e = e, temp2
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2, x1 = x1, x
        d, y1 = y1, y
    if temp_phi == 1:
        return d + phi

def is_prime(num):
    if num < 2 or (num > 2 and num % 2 == 0):
        return False
    for n in range(3, int(num**0.5) + 1, 2):
        if num % n == 0:
            return False
    return True

def generate_key_pair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Har ikkala son tub bo'lishi kerak!")
    if p == q:
        raise ValueError("p va q bir xil bo'lmasligi kerak!")

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    d = multiplicative_inverse(e, phi)

    output_text.set(f""" RSA algoritmi bosqichlari:
 Tub sonlar: p = {p}, q = {q}
 Ko'paytma (n): n = {n}
 Euler funksiyasi: φ(n) = {phi}
 Ochiq kalit eksponenti: e = {e}
 Maxfiy kalit: d = {d}

 Ochiq kalit (e, n) = ({e}, {n})
 Maxfiy kalit (d, n) = ({d}, {n})
""")

    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    encrypted_data = [pow(ord(char), key, n) for char in plaintext]
    
    output_text.set(output_text.get() + f"\n Shifrlash jarayoni:\nMatn: {plaintext}\nShifrlangan: {encrypted_data}")
    
    return encrypted_data

def decrypt(pk, ciphertext):
    key, n = pk
    decrypted_data = ''.join([chr(pow(char, key, n)) for char in ciphertext])

    output_text.set(output_text.get() + f"\n Deshifrlash jarayoni:\nShifrlangan: {ciphertext}\nDeshifrlangan: {decrypted_data}")

    return decrypted_data

# === GUI Funksiyalar ===
def generate_keys():
    try:
        p, q = int(entry_p.get()), int(entry_q.get())
        public, private = generate_key_pair(p, q)
        entry_public.delete(0, tk.END)
        entry_public.insert(0, str(public))
        entry_private.delete(0, tk.END)
        entry_private.insert(0, str(private))
    except ValueError as e:
        messagebox.showerror("Xato!", str(e))

def encrypt_message():
    try:
        message = entry_message.get()
        public_key = eval(entry_public.get())
        encrypted = encrypt(public_key, message)
        entry_encrypted.delete(0, tk.END)
        entry_encrypted.insert(0, str(encrypted))
    except Exception:
        messagebox.showerror("Xato!", "Iltimos, avval kalitlarni yarating!")

def decrypt_message():
    try:
        private_key = eval(entry_private.get())
        encrypted_msg = eval(entry_encrypted.get())
        decrypted = decrypt(private_key, encrypted_msg)
        entry_decrypted.delete(0, tk.END)
        entry_decrypted.insert(0, decrypted)
    except Exception:
        messagebox.showerror("Xato!", "Xabar noto'g'ri yoki kalit kiritilmagan!")

# === GUI Oynasini Yaratish ===
root = tk.Tk()
root.title("RSA Shifrlash Dasturi")
root.geometry("1200x700")  
root.state("zoomed")  
root.configure(bg="#e6f7ff")

output_text = tk.StringVar()
output_text.set("RSA algoritmi ishlash jarayoni bu yerdan ko‘rinadi.")

# === UI Dizayni ===
def create_label(text, color="black"):
    return tk.Label(root, text=text, bg="#e6f7ff", fg=color, font=("Arial", 10, "bold"))

def create_entry(width=50, border=3):
    return tk.Entry(root, width=width, bg="white", fg="black", font=("Arial", 10), relief="solid", bd=border)

def create_button(text, command, bg, fg):
    return tk.Button(root, text=text, command=command, bg=bg, fg=fg, font=("Arial", 10, "bold"), padx=10, pady=5)

# === P va Q Qiymatlari ===
create_label("p (tub son):", "blue").pack()
entry_p = create_entry(border=2)
entry_p.pack()

create_label("q (tub son):", "blue").pack()
entry_q = create_entry(border=2)
entry_q.pack()

create_button("Kalit yaratish", generate_keys, "green", "white").pack(pady=5)

# === Ochiq va Yashirin Kalitlar ===
create_label("Ochiq kalit:").pack()
entry_public = create_entry(border=2)
entry_public.pack()

create_label("Yashirin kalit:").pack()
entry_private = create_entry(border=2)
entry_private.pack()

# === Xabarni kiritish ===
create_label("Xabarni kiriting:", "red").pack()
entry_message = create_entry(border=3)
entry_message.pack()

create_button("Shifrlash", encrypt_message, "blue", "white").pack(pady=5)

# === Shifrlangan Xabar ===
create_label("Shifrlangan xabar:").pack()
entry_encrypted = create_entry(border=3)
entry_encrypted.pack()

create_button("Deshifrlash", decrypt_message, "red", "white").pack(pady=5)

# === Deshifrlangan Xabar ===
create_label("Deshifrlangan xabar:").pack()
entry_decrypted = create_entry(border=4)
entry_decrypted.pack()

# === Chiqarish Maydoni ===
output_label = tk.Label(root, textvariable=output_text, wraplength=550, justify="left", bg="white", fg="black", font=("Arial", 10), relief="solid", bd=2)
output_label.pack(pady=10, fill="both", expand=True)

# === Oynani Ishga Tushirish ===
root.mainloop()
