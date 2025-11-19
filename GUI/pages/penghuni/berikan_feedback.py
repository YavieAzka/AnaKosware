import tkinter as tk
from tkinter import messagebox
from components.penghuni.star_rating import StarRating
from components.custom_widgets import StyledButton  # PlaceholderEntry tidak dipakai

class BerikanFeedback(tk.Frame):
    """Halaman untuk mengisi feedback dari pengguna"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.create_content()

    def create_content(self):
        print("Membuat konten Feedback Form...")

        # Judul Halaman
        title = tk.Label(
            self, 
            text="Feedback Kos Melati", 
            font=('Arial', 18, 'bold'), 
            bg='white', fg='#2D3142'
        )
        title.pack(pady=(30, 20), padx=40, anchor='w')

        # Deskripsi
        description = tk.Label(
            self, 
            text="Berikan rating dan feedback Anda terhadap layanan dan fasilitas Kos Melati agar kami dapat terus meningkatkan kualitas kos",
            font=('Arial', 12), bg='white', fg='#666666',
            wraplength=500, justify="left"
        )
        description.pack(padx=40, pady=(10, 30), anchor='w')

        # Rating
        rating_label = tk.Label(
            self, text="Rating", 
            font=('Arial', 12, 'bold'),  # dibuat tebal
            bg='white', fg='#333333'
        )
        rating_label.pack(padx=40, anchor='w')

        # Rating star component
        self.rating = tk.IntVar(value=0)
        star_rating = StarRating(self, self.rating)
        star_rating.pack(padx=40, pady=5)

        # Label Feedback
        feedback_label = tk.Label(
            self, text="Pesan Feedback", 
            font=('Arial', 12, 'bold'),  # dibuat tebal
            bg='white', fg='#333333'
        )
        feedback_label.pack(padx=40, anchor='w', pady=(30, 5))

        # TEXT AREA (multi-line input)
        self.feedback_text = tk.Text(
            self, 
            font=('Arial', 12),
            width=60,
            height=8,
            bd=1,
            relief="solid",
            wrap="word"
        )
        self.feedback_text.pack(padx=40, pady=(5, 20))

        # Placeholder manual
        self.placeholder = "Berikan feedback..."
        self.feedback_text.insert("1.0", self.placeholder)
        self.feedback_text.configure(fg="#999999")

        # Bind agar placeholder hilang saat user mulai mengetik
        self.feedback_text.bind("<FocusIn>", self.remove_placeholder)
        self.feedback_text.bind("<FocusOut>", self.add_placeholder)

        # Submit button
        submit_btn = StyledButton(
            self, 
            text="Submit Feedback", 
            font=('Arial', 12, 'bold'), 
            bg='#F8A80F', 
            fg='white', 
            hover_bg='#FFB84D',
            command=self.submit_feedback
        )
        submit_btn.pack(pady=20)

    # Placeholder functions
    def remove_placeholder(self, event):
        if self.feedback_text.get("1.0", tk.END).strip() == self.placeholder:
            self.feedback_text.delete("1.0", tk.END)
            self.feedback_text.configure(fg="black")

    def add_placeholder(self, event):
        if not self.feedback_text.get("1.0", tk.END).strip():
            self.feedback_text.insert("1.0", self.placeholder)
            self.feedback_text.configure(fg="#999999")

    def submit_feedback(self):
        response = messagebox.askyesno("Submit Feedback", "Apakah Anda yakin untuk submit feedback ini?")
        if response:
            rating = self.rating.get()
            feedback = self.feedback_text.get("1.0", tk.END).strip()

            if rating == 0 or not feedback or feedback == self.placeholder:
                messagebox.showwarning("Peringatan", "Rating dan Pesan Feedback harus diisi dengan benar!")
                return

            print(f"Rating: {rating} | Feedback: {feedback}")

            messagebox.showinfo("Submit Feedback Berhasil", "Terima kasih sudah memberikan feedback! 😊")

            # Reset
            self.rating.set(0)
            self.feedback_text.delete("1.0", tk.END)
            self.add_placeholder(None)

# Jalankan jika standalone
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Feedback Kos Melati")
    app = BerikanFeedback(root, None)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
