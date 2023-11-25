#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tkinter as tk
import webbrowser
import pyperclip
from Crypto.Hash import keccak


private_key=" "
# Parámetros de la curva secp256k1
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F  # Característica del campo primo
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798  # Coordenada x del punto generador
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8  # Coordenada y del punto generador
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141  # Orden del subgrupo generado por G

# Función para convertir un entero grande en formato de bytes

def int_to_bytes(value, length):
    return value.to_bytes((value.bit_length() + 7) // 8, byteorder="big") or b'\0'

def ECadd(a, b):
    LamAdd = ((b[1] - a[1]) * modinv(b[0] - a[0], p)) % p
    x = (LamAdd**2 - a[0] - b[0]) % p
    y = (LamAdd * (a[0] - x) - a[1]) % p
    return (x, y)

def ECdouble(a):
    Lam = ((3 * a[0]**2) * modinv((2 * a[1]), p)) % p
    x = (Lam**2 - 2 * a[0]) % p
    y = (Lam * (a[0] - x) - a[1]) % p
    return (x, y)

def modinv(a, n):
    lm, hm = 1, 0
    low, high = a % n, n
    while low > 1:
        ratio = high // low
        nm, new = hm - lm * ratio, high - low * ratio
        lm, low, hm, high = nm, new, lm, low
    return lm % n

def copiar_al_portapapeles():
    texto = public_key_text.get("1.0", "end-1c")  # Obtiene el texto del widget Text
    pyperclip.copy(texto)  # Copia el texto al portapapeles
    
def copiar_al_portapapeles_2():
    # Obtiene el texto del widget Text
    pyperclip.copy(eth_private_key)

def cambiar_cursor(event):
    blank_space.config(cursor="hand2")

def restaurar_cursor(event):
    blank_space.config(cursor="")

def generate_on_enter(event):
    generate_address()


def base58_a(address_hex):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    b58_string = ''
    # Get the number of leading zeros
    leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
    # Convert hex to decimal
    address_int = int(address_hex, 16)
    # Append digits to the start of string
    while address_int > 0:
        digit = address_int % 58
        digit_char = alphabet[digit]
        b58_string = digit_char + b58_string
        address_int //= 58
    # Add ‘1’ for each 2 leading zeros
    ones = leading_zeros // 2
    for one in range(ones):
        b58_string = '1' + b58_string
    return b58_string
    
def toggle_private_key():
    # Verifica si el Checkbutton está seleccionado
    if show_hide_checkbox_var.get():
        private_key_text.config(state="normal")
        # Clear existing text in Text widgets
        private_key_text.delete('1.0', tk.END)
        # Insert new text in Text widgets
        secrets="*"*len(eth_private_key)
        private_key_text.insert(tk.END, secrets)
        # Configura una etiqueta de estilo para centrar el texto
        private_key_text.tag_configure("center", justify="center")
        # Aplica la etiqueta de estilo al rango de texto
        private_key_text.tag_add("center", "1.0", "end")
        private_key_text.config(state="disabled")
    else:
        private_key_text.config(state="normal")
        # Clear existing text in Text widgets
        private_key_text.delete('1.0', tk.END)
        # Insert new text in Text widgets
        private_key_text.insert(tk.END, eth_private_key)
        # Configura una etiqueta de estilo para centrar el texto
        private_key_text.tag_configure("center", justify="center")
        # Aplica la etiqueta de estilo al rango de texto
        private_key_text.tag_add("center", "1.0", "end")
        private_key_text.config(state="disabled")

############################################################

    #text = input ("what text you wanna hash? ")
    
#abrir enlace


def abrir_enlace(event):
    webbrowser.open("https://etherscan.io/")
    
    
def generate_address():
    text = text_entry.get()
    
    #now we need to process a hash of the text variable
    # Calcular el hash Keccak-256
    hashed_output = keccak.new(digest_bits=256)
    try:
        hashed_output.update(text.encode('utf-8'))
    except:
        hashed_output.update("".encode('utf-8'))

    #Individual Transaction/Personal Information

    hash_hex = hashed_output.hexdigest()

    # Utilizar el hash como semilla para generar la clave privada
    private_key = int(hash_hex, 16)

    # Obtén la clave privada en formato de bytes
    private_key_bytes = private_key.to_bytes(32, byteorder="big")

    # Convierte la clave privada a un objeto int
    private_key_int = int.from_bytes(private_key_bytes, byteorder="big")

    # Comprueba que la clave privada sea válida
    # Calcula la clave pública utilizando multiplicación de puntos en la curva secp256k1
    G = (Gx, Gy)
    public_key_point = None

    # Algoritmo de multiplicación de puntos (double and add)
    for i in range(256):
        if (private_key_int >> i) & 1:
            if public_key_point is None:
                public_key_point = G
            else:
                public_key_point = ECadd(public_key_point, G)

        G = ECdouble(G)

    # La clave pública es el resultado de la multiplicación de puntos
    public_key_bytes = (int_to_bytes(public_key_point[0], 32) +
                        int_to_bytes(public_key_point[1], 32))

    public_key_hex = public_key_bytes.hex()
    
    global eth_private_key
    eth_private_key=hex(private_key)[2:]

    # Obtener la dirección Ethereum
    ethereum_address = keccak.new(digest_bits=256)
    ethereum_address.update(bytes.fromhex(public_key_hex))
    ethereum_address_hex = ethereum_address.hexdigest()[24:]
    ethereum_address= "0x" + ethereum_address_hex
    
    
    # Clear existing text in Text widgets
    public_key_text.config(state="normal")
    # Clear existing text in Text widgets
    public_key_text.delete('1.0', tk.END)
    # Insert new text in Text widgets
    public_key_text.insert(tk.END, ethereum_address)
    public_key_text.config(state="disabled")
    # Configura una etiqueta de estilo para centrar el texto
    public_key_text.tag_configure("center", justify="center")
    # Aplica la etiqueta de estilo al rango de texto
    public_key_text.tag_add("center", "1.0", "end")

    
    if show_hide_checkbox_var.get():
        private_key_text.config(state="normal")
        # Clear existing text in Text widgets
        private_key_text.delete('1.0', tk.END)
        # Insert new text in Text widgets
        secrets="*"*len(eth_private_key)
        private_key_text.insert(tk.END, secrets)
        # Configura una etiqueta de estilo para centrar el texto
        private_key_text.tag_configure("center", justify="center")
        # Aplica la etiqueta de estilo al rango de texto
        private_key_text.tag_add("center", "1.0", "end")
        private_key_text.config(state="disabled")
        
        
    else:
        private_key_text.config(state="normal")
        # Clear existing text in Text widgets
        private_key_text.delete('1.0', tk.END)
        # Insert new text in Text widgets
        private_key_text.insert(tk.END, eth_private_key)
        # Configura una etiqueta de estilo para centrar el texto
        private_key_text.tag_configure("center", justify="center")
        # Aplica la etiqueta de estilo al rango de texto
        private_key_text.tag_add("center", "1.0", "end")
        private_key_text.config(state="disabled")

root = tk.Tk()
root.title("Ethereum Wallet Generator")

root.geometry("500x380")


# Crear y posicionar widgets en la ventana
text_label = tk.Label(root, text="Insert Text:", font=("Helvetica", 12))
text_label.grid(row=0, column=0, columnspan=2, pady=10)

text_entry = tk.Entry(root, width=50, font=("Helvetica", 12), justify="center")
text_entry.grid(row=1, column=0, columnspan=2, pady=1)

generate_button = tk.Button(root, text="GENERATE WALLET",  width = 15, height = 2, command=generate_address, fg='white', bg='black')
generate_button.grid(row=2, column=0, columnspan=2, pady=10)

public_key_label = tk.Label(root, text="Ethereum Address:", font=("Helvetica", 12))
public_key_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="s")

# Crear un botón para copiar al portapapeles
boton_copiar = tk.Button(root, text="copy", width = 4, height = 1, command=copiar_al_portapapeles, fg='black', bg='white', font=("Helvetica", 8))
boton_copiar.grid(row=3, column=1, columnspan=2, pady=2)

# Create Text widgets for displaying public and private keys
public_key_text = tk.Text(root, height=1, width=50, wrap=tk.WORD, bg='lavender', font=("Helvetica"))
public_key_text.grid(row=4, column=0, columnspan=2, pady=10)
public_key_text.tag_configure("center", justify="center")

blank_space = tk.Label(root, text="https://etherscan.io/",fg="blue", font=("Helvetica", 10))
blank_space.grid(row=5, column=0,columnspan=3, pady=0)

private_key_label = tk.Label(root, text="Private Key:", font=("Helvetica", 12))
private_key_label.grid(row=6, column=0, pady=10)

# Crear un botón para copiar al portapapeles
boton_copiar = tk.Button(root, text="copy", width = 4, height = 1, command=copiar_al_portapapeles_2, fg='black', bg='white', font=("Helvetica", 8))
boton_copiar.grid(row=6, column=1, pady=2, sticky="W")

show_hide_checkbox_var = tk.BooleanVar(value=True)
show_hide_checkbox = tk.Checkbutton(root, text="Hide/Show", variable=show_hide_checkbox_var, command=toggle_private_key, font=("Helvetica", 11))
show_hide_checkbox.grid(row=6, column=1, pady=10)

private_key_text = tk.Text(root, height=1, width=70, wrap=tk.WORD, bg='lavender', font=("Helvetica", 10))
private_key_text.grid(row=7, column=0, columnspan=2, pady=10, sticky="s")

blank_space_2 = tk.Label(root, text="")
blank_space_2.grid(row=8, column=0,columnspan=3, pady=0)

donate_me_1 = tk.Label(root, text="Donate me =)", font=("Helvetica", 8))
donate_me_1.grid(row=9, column=0, pady=0, sticky="w")

donate_me = tk.Text(root, height=1, width=45, wrap=tk.WORD, bg='alice blue', font=("Helvetica", 8))
donate_me.grid(row=9, column=1, pady=10, sticky="e")
donate_me.insert(tk.END, "0x3d90Eb79C1e753Ca51D1447791C07e7CcC219e5C")
donate_me.config(state="disabled")

#ejecucion al presionar enter
text_entry.bind("<Return>", generate_on_enter)

# Asocia la función abrir_enlace al evento de clic
blank_space.bind("<Button-1>", abrir_enlace)

# Cambia el cursor cuando el ratón entra en el área del widget
blank_space.bind("<Enter>", cambiar_cursor)

# Restaura el cursor cuando el ratón sale del área del widget
blank_space.bind("<Leave>", restaurar_cursor)
# ... (rest of your code remains unchanged)

# Iniciar el bucle de la GUI
root.mainloop()


# In[ ]:




