import tkinter as tk
from tkinter import filedialog, messagebox
from ai.ai_utils import get_explanation
from translate.translate_utils import translate_to_tamil
from ocr.ocr_utils import extract_text_from_image
from reportlab.pdfgen import canvas

# Theme
BG_COLOR = "#0f0f0f"
FG_COLOR = "#00ff00"
FONT = ("Courier New", 14)
ASCII_FONT = ("Courier New", 10, "bold")

# App Initialization
app = tk.Tk()
app.title("💻 EduEase - Hacker Edition")
app.configure(bg=BG_COLOR)

# Set the window size to maximum screen size
app.geometry("1920x1080")  # You can set this to the screen resolution of the device if necessary.

# Main Frame (Centered content)
main_frame = tk.Frame(app, bg=BG_COLOR)
main_frame.place(relx=0.5, rely=0.03, anchor="n")

# ASCII Banner
ascii_banner = r"""
   ______    _        _                        _             
  |  ____|  | |      (_)                      | |            
  | |__   __| |_   ___ _  ___ ___  _ __   ___ | |_ ___  _ __ 
  |  __| |_   _| / __| |/ __/ _ \| '_ \ / _ \| __/ _ \| '__|
  | |____  |_|   \__ \ | (_| (_) | | | | (_) | || (_) | |   
  |______|       |___/_|\___\___/|_| |_|\___/ \__\___/|_|   

            >>> EduEase: Intelligent Learning Assistant <<<
"""

ascii_label = tk.Label(main_frame, text=ascii_banner, font=ASCII_FONT, bg=BG_COLOR, fg=FG_COLOR, justify="left")
ascii_label.pack(pady=(10, 5))

# Question Entry
question_label = tk.Label(main_frame, text="📘 Enter your Question below:", font=FONT, bg=BG_COLOR, fg=FG_COLOR)
question_label.pack(anchor="center")

question_input = tk.Entry(main_frame, width=100, font=FONT, bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR)
question_input.pack(pady=5)

# Enter Button to Trigger Search
enter_button = tk.Button(main_frame, text="🔍 Search", command=lambda: get_answer(), font=FONT, bg=BG_COLOR, fg=FG_COLOR,
                         width=20)
enter_button.pack(pady=5)

# Bind Enter key to the search button function (same as clicking the button)
app.bind('<Return>', lambda event: get_answer())

# Buttons Row
button_frame = tk.Frame(main_frame, bg=BG_COLOR)
button_frame.pack(pady=10)

btn_style = {"font": FONT, "bg": BG_COLOR, "fg": FG_COLOR, "width": 20, "padx": 10, "pady": 8}

tk.Button(button_frame, text="📜 Get Explanation", command=lambda: get_answer(), **btn_style).grid(row=0, column=0)
tk.Button(button_frame, text="🖼️ Upload Image", command=lambda: upload_image(), **btn_style).grid(row=0, column=1)
tk.Button(button_frame, text="🌐 Translate to Tamil", command=lambda: translate_explanation(), **btn_style).grid(row=0,
                                                                                                                column=2)
tk.Button(button_frame, text="💾 Save as PDF", command=lambda: save_as_pdf(), **btn_style).grid(row=0, column=3)

# Output Section
output_label = tk.Label(main_frame, text="📎 Output:", font=FONT, bg=BG_COLOR, fg=FG_COLOR)
output_label.pack(anchor="center")

result_frame = tk.Frame(main_frame, bg=BG_COLOR)
result_frame.pack(padx=20, pady=(5, 20))

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side="right", fill="y")

result_text = tk.Text(result_frame, height=25, width=130, font=FONT, bg=BG_COLOR, fg=FG_COLOR,
                      wrap="word", yscrollcommand=scrollbar.set, insertbackground=FG_COLOR)
result_text.pack(side="left", fill="both", expand=True)

scrollbar.config(command=result_text.yview)

# Explanation Cache
explanation_text = ""


# Functions
def get_answer():
    global explanation_text
    query = question_input.get().strip()
    if not query:
        messagebox.showwarning("⚠️ Empty Input", "Please enter a question or upload an image.")
        return

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, ">>> Hacking the matrix... Please wait...\n")
    explanation_text = get_explanation(query)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f">>> {explanation_text}")


def translate_explanation():
    global explanation_text
    if not explanation_text:
        messagebox.showwarning("⚠️ No Explanation", "Please get an explanation first.")
        return

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, ">>> Translating to Tamil...\n")

    try:
        explanation_text = translate_to_tamil(explanation_text)
    except Exception as e:
        messagebox.showerror("❌ Translation Error", f"Failed to translate explanation to Tamil: {e}")
        return

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f">>> {explanation_text}")


def upload_image():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if file_path:
        try:
            extracted_text = extract_text_from_image(file_path)
            question_input.delete(0, tk.END)
            question_input.insert(0, extracted_text.strip())
        except Exception as e:
            messagebox.showerror("OCR Error", f"Failed to extract text: {e}")


def save_as_pdf():
    global explanation_text
    if not explanation_text:
        messagebox.showwarning("⚠️ Nothing to Save", "No explanation found to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if not file_path:
        return

    try:
        c = canvas.Canvas(file_path)
        text_obj = c.beginText(40, 800)
        text_obj.setFont("Courier", 12)
        for line in explanation_text.split('\n'):
            text_obj.textLine(line)
        c.drawText(text_obj)
        c.save()
        messagebox.showinfo("✅ Saved", f"Explanation saved to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("❌ PDF Error", f"Failed to save as PDF: {e}")


# Run
app.mainloop()
