import tkinter as tk
from tkinter import messagebox, ttk

# 🌸 Create the main window
root = tk.Tk()
root.title("Stylique 🌸 - Virtual Try-On Assistant")
root.geometry("500x600")
root.configure(bg="#fff5f7")  # soft sakura pink background

# 🌸 Fonts and Styles
title_font = ("Segoe Script", 20, "bold")
label_font = ("Comic Sans MS", 12)
entry_font = ("Comic Sans MS", 12)

# 🌸 Title Label
title = tk.Label(root, text="Stylique 🌸", font=title_font, fg="#d6336c", bg="#fff5f7")
title.pack(pady=(20, 10))

# 🌸 Subtitle
subtitle = tk.Label(root, text="Your Cute Virtual Try-On Assistant", font=("Arial", 12), bg="#fff5f7")
subtitle.pack(pady=(0, 20))

# 🌸 Input Frame
input_frame = tk.Frame(root, bg="#fff5f7")
input_frame.pack(pady=10)

# Height
tk.Label(input_frame, text="Height (cm):", font=label_font, bg="#fff5f7").grid(row=0, column=0, sticky="w", pady=5)
height_entry = tk.Entry(input_frame, font=entry_font, width=20)
height_entry.grid(row=0, column=1, pady=5)

# Weight
tk.Label(input_frame, text="Weight (kg):", font=label_font, bg="#fff5f7").grid(row=1, column=0, sticky="w", pady=5)
weight_entry = tk.Entry(input_frame, font=entry_font, width=20)
weight_entry.grid(row=1, column=1, pady=5)

# Gender
tk.Label(input_frame, text="Gender:", font=label_font, bg="#fff5f7").grid(row=2, column=0, sticky="w", pady=5)
gender_var = tk.StringVar(value="Female")
gender_frame = tk.Frame(input_frame, bg="#fff5f7")
gender_frame.grid(row=2, column=1, pady=5)
tk.Radiobutton(gender_frame, text="♀️ Female", variable=gender_var, value="Female", bg="#fff5f7", font=entry_font).pack(side="left")
tk.Radiobutton(gender_frame, text="♂️ Male", variable=gender_var, value="Male", bg="#fff5f7", font=entry_font).pack(side="left")
tk.Radiobutton(gender_frame, text="⚧ Other", variable=gender_var, value="Other", bg="#fff5f7", font=entry_font).pack(side="left")

# Occasion
tk.Label(input_frame, text="Occasion:", font=label_font, bg="#fff5f7").grid(row=3, column=0, sticky="w", pady=5)
occasion_var = tk.StringVar()
occasion_menu = ttk.Combobox(input_frame, textvariable=occasion_var, font=entry_font, width=18)
occasion_menu['values'] = ("Casual", "Formal", "Party", "Date", "Vacation")
occasion_menu.grid(row=3, column=1, pady=5)
occasion_menu.set("Casual")

# 🌸 Output Box
output_label = tk.Label(root, text="", font=label_font, bg="#fff5f7", fg="#6b2e45", wraplength=400)
output_label.pack(pady=20)

# 🌸 Style Suggestion Function
def reveal_style():
    try:
        height = int(height_entry.get())
        weight = int(weight_entry.get())
        gender = gender_var.get()
        occasion = occasion_var.get()

        # Simple logic for style suggestion
        if gender == "Female":
            if occasion == "Formal":
                suggestion = "A pastel blazer set with kitten heels and a sakura-pink clutch 🌸"
            elif occasion == "Casual":
                suggestion = "Oversized sweatshirt with mom jeans and hair clips 🌸"
            elif occasion == "Date":
                suggestion = "Flowy floral dress with soft waves and nude flats 🌸"
            elif occasion == "Party":
                suggestion = "Glitter crop top, high-waist skirt, and bold earrings 🌸"
            else:
                suggestion = "Maxi dress and sunhat for that breezy holiday feel 🌸"
        else:
            suggestion = f"Smart {occasion.lower()} look with soft pastels and clean lines 🌸"

        output_label.config(text=f"✨ Your Stylique Look: \n{suggestion}")
    except ValueError:
        messagebox.showerror("Oops!", "Please enter valid height and weight 🌸")

# 🌸 Reveal Button
reveal_btn = tk.Button(root, text="Reveal My Style 🌸", font=("Arial Rounded MT Bold", 12), bg="#f8d7da", fg="#8a1546",
                       activebackground="#f1c1cc", relief="raised", command=reveal_style)
reveal_btn.pack(pady=10)

# Run the App
root.mainloop()
