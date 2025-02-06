import streamlit as st
import random

# === Foydali Funksiyalar ===
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

    return ((e, n), (d, n), n, phi)

def encrypt(pk, plaintext):
    key, n = pk
    encrypted_data = [pow(ord(char), key, n) for char in plaintext]
    return encrypted_data

def decrypt(pk, ciphertext):
    key, n = pk
    decrypted_chars = [pow(char, key, n) for char in ciphertext]
    decrypted_text = ''.join([chr(code) for code in decrypted_chars])
    return decrypted_text, decrypted_chars

# === Streamlit Interfeysi ===
st.title("RSA Shifrlash Dasturi")

# P va Q qiymatlarini olish
p = st.number_input("p (tub son):", min_value=2, step=1)
q = st.number_input("q (tub son):", min_value=2, step=1)

if st.button("Kalit yaratish"):
    try:
        public, private, n, phi = generate_key_pair(p, q)
        st.write(f"🔑 Ochiq kalit: {public}")
        st.write(f"🔐 Maxfiy kalit: {private}")
        st.write(f"📌 Ko'paytma (n): {n}")
        st.write(f"📌 Euler funksiyasi (φ(n)): {phi}")
    except ValueError as e:
        st.error(str(e))

# Xabarni kiritish
message = st.text_area("Xabarni kiriting:")

if st.button("Shifrlash"):
    if message:
        encrypted_message = encrypt(public, message)
        st.write(f"🔐 Shifrlangan xabar (ASCII kodlari): {encrypted_message}")
    else:
        st.warning("Iltimos, xabarni kiriting!")

# Shifrlangan xabarni kiritish va deshifrlash
encrypted_input = st.text_area("Shifrlangan xabar (ASCII kodlari):", help="Shifrlangan ASCII kodlarini kiriting.")

if st.button("Deshifrlash"):
    if encrypted_input:
        encrypted_data = list(map(int, encrypted_input.split(',')))
        decrypted_message, decrypted_ascii = decrypt(private, encrypted_data)
        st.write(f"🔓 Deshifrlangan xabar: {decrypted_message}")
        st.write(f"🔢 Deshifrlangan ASCII kodlari: {decrypted_ascii}")
    else:
        st.warning("Iltimos, shifrlangan xabarni kiriting!")
