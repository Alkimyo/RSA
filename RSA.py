import streamlit as st
import random
from math import gcd
from typing import Tuple, List

# === Foydali Funksiyalar ===
def multiplicative_inverse(e: int, phi: int) -> int:
    """Multiplikativ teskari funksiyasi"""
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

def is_prime(n: int) -> bool:
    """Tub sonni tekshirish"""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_random_prime(min_value: int = 100, max_value: int = 500) -> int:
    """Tasodifiy tub son yaratish"""
    while True:
        num = random.randint(min_value, max_value)
        if is_prime(num):
            return num

def generate_key_pair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int], int, int]:
    """Ochiq va maxfiy kalitlarni yaratish"""
    if p == q:
        raise ValueError("p va q bir xil bo'lmasligi kerak!")
    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    d = multiplicative_inverse(e, phi)

    return ((e, n), (d, n), n, phi)

def encrypt(public_key: Tuple[int, int], plaintext: str) -> List[int]:
    """Xabarni shifrlash"""
    key, n = public_key
    return [pow(ord(char), key, n) for char in plaintext]

def decrypt(private_key: Tuple[int, int], ciphertext: List[int]) -> str:
    """Shifrlangan xabarni deshifrlash"""
    key, n = private_key
    decrypted_chars = [pow(char, key, n) for char in ciphertext]
    return ''.join([chr(code) for code in decrypted_chars])

# === Streamlit Interfeysi ===
st.title("RSA Shifrlash Dasturi")

# P va Q qiymatlarini olish, random yaratish (tub sonlar)
random_p = generate_random_prime(min_value=100, max_value=500)
random_q = generate_random_prime(min_value=100, max_value=500)

# P va Q qiymatlarini ko'rsatish
st.write(f"Generated Random p (tub son): {random_p}")
st.write(f"Generated Random q (tub son): {random_q}")

# Foydalanuvchi uchun manual kiritish imkoniyati
p = st.number_input("p (tub son)ni o'zgartiring:", value=random_p, min_value=2, step=1)
q = st.number_input("q (tub son)ni o'zgartiring:", value=random_q, min_value=2, step=1)

# Global o'zgaruvchilar
publickey = None
privatekey = None

if st.button("Kalit yaratish"):
    try:
        # P va Q teng emasligini tekshirish
        if p == q:
            st.error("Xato! p va q bir xil bo'lmasligi kerak!")
        else:
            publickey, privatekey, n, phi = generate_key_pair(p, q)
            st.write(f"🔑 Ochiq kalit: {publickey}")
            st.write(f"🔐 Maxfiy kalit: {privatekey}")
            st.write(f"📌 Ko'paytma (n): {n}")
            st.write(f"📌 Euler funksiyasi (φ(n)): {phi}")
    except ValueError as e:
        st.error(str(e))

# Xabarni kiritish
message = st.text_area("Xabarni kiriting:")

if st.button("Shifrlash"):
    if publickey is not None and message:
        encrypted_message = encrypt(publickey, message)
        st.write(f"🔐 Shifrlangan xabar (ASCII kodlari): {encrypted_message}")
    elif publickey is None:
        st.warning("Iltimos, avval kalitlarni yarating!")
    else:
        st.warning("Iltimos, xabarni kiriting!")

# Shifrlangan xabarni kiritish va deshifrlash
encrypted_input = st.text_area("Shifrlangan xabar (ASCII kodlari):", help="Shifrlangan ASCII kodlarini kiriting.")

if st.button("Deshifrlash"):
    if privatekey is not None and encrypted_input:
        encrypted_data = list(map(int, encrypted_input.split(',')))
        decrypted_message = decrypt(privatekey, encrypted_data)
        st.write(f"🔓 Deshifrlangan xabar: {decrypted_message}")
    elif privatekey is None:
        st.warning("Iltimos, avval kalitlarni yarating!")
    else:
        st.warning("Iltimos, shifrlangan xabarni kiriting!")
