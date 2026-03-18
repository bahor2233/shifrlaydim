import tkinter as tk
from tkinter import ttk, messagebox
import re

class PlayfairAdvancedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Playfair Cryptography Suite - I/J Edition")
        self.root.geometry("900x950")
        self.root.configure(bg="#1a1b26") # Zamonaviy Dark Theme

        self.alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" # J olib tashlangan

        self.setup_ui()
        
    def setup_ui(self):
        # 1. Sarlavha
        title_label = tk.Label(self.root, text="PLAYFAIR CIPHER ENGINE", 
                               font=("Helvetica", 24, "bold"), fg="#7aa2f7", bg="#1a1b26")
        title_label.pack(pady=20)

        # 2. Kirish Paneli
        input_frame = tk.Frame(self.root, bg="#24283b", padx=20, pady=20, highlightbackground="#414868", highlightthickness=1)
        input_frame.pack(pady=10, padx=40, fill="x")

        tk.Label(input_frame, text="Kalit so'z (Key):", bg="#24283b", fg="#c0caf5", font=("Arial", 11)).grid(row=0, column=0, sticky="w")
        self.key_entry = tk.Entry(input_frame, font=("Consolas", 13), bg="#1a1b26", fg="#cfc9c2", borderwidth=0, insertbackground="white")
        self.key_entry.grid(row=0, column=1, pady=10, padx=15, sticky="ew")
        input_frame.columnconfigure(1, weight=1)

        tk.Label(input_frame, text="Matn (Plaintext):", bg="#24283b", fg="#c0caf5", font=("Arial", 11)).grid(row=1, column=0, sticky="w")
        self.text_entry = tk.Entry(input_frame, font=("Consolas", 13), bg="#1a1b26", fg="#cfc9c2", borderwidth=0, insertbackground="white")
        self.text_entry.grid(row=1, column=1, padx=15, sticky="ew")

        # 3. Tugmalar
        btn_frame = tk.Frame(self.root, bg="#1a1b26")
        btn_frame.pack(pady=25)

        self.enc_btn = tk.Button(btn_frame, text="🔒 SHIFRLASH", command=lambda: self.process("encrypt"),
                                 bg="#9ece6a", fg="#1a1b26", font=("Arial", 12, "bold"), padx=30, pady=10, relief="flat", cursor="hand2")
        self.enc_btn.pack(side="left", padx=20)

        self.dec_btn = tk.Button(btn_frame, text="🔓 DESHIFRLASH", command=lambda: self.process("decrypt"),
                                 bg="#f7768e", fg="#1a1b26", font=("Arial", 12, "bold"), padx=30, pady=10, relief="flat", cursor="hand2")
        self.dec_btn.pack(side="left", padx=20)

        # 4. Jadvallar Paneli (Ikkita jadval yonma-yon)
        tables_main_frame = tk.Frame(self.root, bg="#1a1b26")
        tables_main_frame.pack(pady=10, padx=20, fill="x")

        # Standart Jadval (Chapda)
        std_container = tk.Frame(tables_main_frame, bg="#1a1b26")
        std_container.pack(side="left", expand=True)
        tk.Label(std_container, text="1. STANDART ALIFBO", fg="#bb9af7", bg="#1a1b26", font=("Arial", 10, "bold")).pack(pady=5)
        self.std_grid = tk.Frame(std_container, bg="#414868", padx=2, pady=2)
        self.std_grid.pack()
        self.fill_static_grid(self.std_grid)

        # Kalit Jadvali (O'ngda)
        key_container = tk.Frame(tables_main_frame, bg="#1a1b26")
        key_container.pack(side="right", expand=True)
        tk.Label(key_container, text="2. KALIT MATRITSASI", fg="#e0af68", bg="#1a1b26", font=("Arial", 10, "bold")).pack(pady=5)
        self.key_grid = tk.Frame(key_container, bg="#414868", padx=2, pady=2)
        self.key_grid.pack()
        self.key_cells = []
        self.init_key_grid()

        # 5. Natija Paneli
        res_label = tk.Label(self.root, text="NATIJA:", fg="#7dcfff", bg="#1a1b26", font=("Arial", 12, "bold"))
        res_label.pack(pady=(30, 5), padx=40, anchor="w")
        self.result_box = tk.Text(self.root, height=3, font=("Consolas", 16), bg="#24283b", fg="#9ece6a", borderwidth=0, padx=15, pady=15)
        self.result_box.pack(pady=5, padx=40, fill="x")

    def fill_static_grid(self, parent):
        # Standart alifbo jadvalini (J-siz) to'ldirish
        for i in range(5):
            for j in range(5):
                char = self.alphabet[i*5 + j]
                display = "I/J" if char == "I" else char
                lbl = tk.Label(parent, text=display, width=5, height=2, bg="#1a1b26", fg="#565f89", font=("Consolas", 14, "bold"))
                lbl.grid(row=i, column=j, padx=1, pady=1)

    def init_key_grid(self):
        # Kalit jadvali uchun bo'sh kataklar yaratish
        for i in range(5):
            row_list = []
            for j in range(5):
                lbl = tk.Label(self.key_grid, text="?", width=5, height=2, bg="#1a1b26", fg="#c0caf5", font=("Consolas", 14, "bold"))
                lbl.grid(row=i, column=j, padx=1, pady=1)
                row_list.append(lbl)
            self.key_cells.append(row_list)

    def generate_matrix(self, key):
        key = re.sub(r'[^A-Z]', '', key.upper()).replace('J', 'I')
        combined = ""
        for char in key + self.alphabet:
            if char not in combined:
                combined += char
        
        matrix = [list(combined[i:i+5]) for i in range(0, 25, 5)]
        
        # UI ni yangilash
        for r in range(5):
            for c in range(5):
                val = matrix[r][c]
                self.key_cells[r][c].config(text="I/J" if val == "I" else val, fg="#ff9e64")
        return matrix

    def process(self, mode):
        key_raw = self.key_entry.get()
        text_raw = self.text_entry.get()

        if not key_raw or not text_raw:
            messagebox.showwarning("Xato", "Iltimos, kalit va matnni to'liq kiriting!")
            return

        matrix = self.generate_matrix(key_raw)
        text = re.sub(r'[^A-Z]', '', text_raw.upper()).replace('J', 'I')
        
        # Juftliklarga ajratish
        pairs = []
        i = 0
        while i < len(text):
            a = text[i]
            if i + 1 < len(text):
                b = text[i+1]
                if a == b:
                    pairs.append(a + 'X')
                    i += 1
                else:
                    pairs.append(a + b)
                    i += 2
            else:
                pairs.append(a + 'X')
                i += 1

        result = ""
        shift = 1 if mode == "encrypt" else -1

        for pair in pairs:
            r1, c1 = next((r, c) for r, row in enumerate(matrix) for c, val in enumerate(row) if val == pair[0])
            r2, c2 = next((r, c) for r, row in enumerate(matrix) for c, val in enumerate(row) if val == pair[1])

            if r1 == r2: # Qator qoidasi
                result += matrix[r1][(c1 + shift) % 5]
                result += matrix[r2][(c2 + shift) % 5]
            elif c1 == c2: # Ustun qoidasi
                result += matrix[(r1 + shift) % 5][c1]
                result += matrix[(r2 + shift) % 5][c2]
            else: # To'rtburchak qoidasi
                result += matrix[r1][c2]
                result += matrix[r2][c1]

        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlayfairAdvancedApp(root)
    root.mainloop()