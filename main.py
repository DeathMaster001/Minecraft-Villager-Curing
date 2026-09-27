import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import sys

# ============================================================
# SETTINGS
# ============================================================

CURE_DISCOUNT = 20
ONE_EMERALD_CUTOFF = 21

if getattr(sys, "frozen", False):
    # Running as a bundled .exe
    SAVE_FILE = os.path.join(
        os.path.dirname(sys.executable),
        "librarian_checklist.json"
    )
else:
    # Running as a .py file
    SAVE_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "librarian_checklist.json"
    )


# ============================================================
# LIBRARIAN ENCHANTMENTS - MINECRAFT JAVA 26.2
#
# Format:
# ("Enchantment Name", Maximum Level)
# ============================================================

ENCHANTMENTS = [
    ("Aqua Affinity", 1),
    ("Bane of Arthropods", 5),
    ("Blast Protection", 4),
    ("Breach", 4),
    ("Channeling", 1),
    ("Curse of Binding", 1),
    ("Curse of Vanishing", 1),
    ("Density", 5),
    ("Depth Strider", 3),
    ("Efficiency", 5),
    ("Feather Falling", 4),
    ("Fire Aspect", 2),
    ("Fire Protection", 4),
    ("Flame", 1),
    ("Fortune", 3),
    ("Frost Walker", 2),
    ("Impaling", 5),
    ("Infinity", 1),
    ("Knockback", 2),
    ("Looting", 3),
    ("Loyalty", 3),
    ("Luck of the Sea", 3),
    ("Lunge", 3),
    ("Lure", 3),
    ("Mending", 1),
    ("Multishot", 1),
    ("Piercing", 4),
    ("Power", 5),
    ("Projectile Protection", 4),
    ("Protection", 4),
    ("Punch", 2),
    ("Quick Charge", 3),
    ("Respiration", 3),
    ("Riptide", 3),
    ("Sharpness", 5),
    ("Silk Touch", 1),
    ("Smite", 5),
    ("Sweeping Edge", 3),
    ("Thorns", 3),
    ("Unbreaking", 3),
]


# ============================================================
# ROMAN NUMERALS
# ============================================================

def to_roman(number):
    values = [
        (5, "V"),
        (4, "IV"),
        (1, "I")
    ]

    result = ""

    for value, numeral in values:
        while number >= value:
            result += numeral
            number -= value

    return result


# ============================================================
# SAVE / LOAD CHECKLIST
# ============================================================

def default_checklist():
    return {
        enchantment: False
        for enchantment, max_level in ENCHANTMENTS
    }


def load_checklist():
    if not os.path.exists(SAVE_FILE):
        return default_checklist()

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            saved_data = json.load(file)

        checklist = default_checklist()

        for enchantment in checklist:
            if enchantment in saved_data:
                checklist[enchantment] = bool(
                    saved_data[enchantment]
                )

        return checklist

    except (OSError, json.JSONDecodeError):
        return default_checklist()


def save_checklist():
    data = {
        enchantment: variable.get()
        for enchantment, variable in checklist_vars.items()
    }

    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4
            )

    except OSError:
        messagebox.showerror(
            "Save Error",
            "Could not save the checklist."
        )

def save_checklist_as():
    data = {
        enchantment: variable.get()
        for enchantment, variable in checklist_vars.items()
    }

    file_path = filedialog.asksaveasfilename(
        title="Save Librarian Checklist",
        defaultextension=".json",
        initialfile="librarian_checklist.json",
        filetypes=[
            ("JSON Files", "*.json"),
            ("All Files", "*.*")
        ]
    )

    if not file_path:
        return

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4
            )

        messagebox.showinfo(
            "Checklist Saved",
            "Your checklist was saved successfully."
        )

    except OSError:
        messagebox.showerror(
            "Save Error",
            "Could not save the checklist."
        )

def load_checklist_from_file():
    file_path = filedialog.askopenfilename(
        title="Load Librarian Checklist",
        filetypes=[
            ("JSON Files", "*.json"),
            ("All Files", "*.*")
        ]
    )

    if not file_path:
        return

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            saved_data = json.load(file)

        for enchantment, variable in checklist_vars.items():
            variable.set(
                bool(
                    saved_data.get(
                        enchantment,
                        False
                    )
                )
            )

        update_progress()

        messagebox.showinfo(
            "Checklist Loaded",
            "Your checklist was loaded successfully."
        )

    except (OSError, json.JSONDecodeError):
        messagebox.showerror(
            "Load Error",
            "Could not load the checklist."
        )


# ============================================================
# PRICE CALCULATOR
# ============================================================

def calculate():
    try:
        base_price = int(price_entry.get())

        if base_price <= 0:
            raise ValueError

        # A base price of 21 or less becomes 1 emerald.
        if base_price <= ONE_EMERALD_CUTOFF:
            cured_price = 1
        else:
            cured_price = base_price - CURE_DISCOUNT

        if cured_price == 1:
            result_label.config(
                text="1 EMERALD!",
                font=("Arial", 18, "bold")
            )
        else:
            result_label.config(
                text=f"{cured_price} EMERALDS",
                font=("Arial", 18, "bold")
            )

    except ValueError:
        messagebox.showerror(
            "Invalid Price",
            "Please enter a whole-number emerald price."
        )


# ============================================================
# CHECKLIST
# ============================================================

saved_checklist = load_checklist()
checklist_vars = {}


def update_progress():
    completed = sum(
        variable.get()
        for variable in checklist_vars.values()
    )

    total = len(ENCHANTMENTS)

    progress_label.config(
        text=f"{completed} / {total} Complete"
    )

    save_checklist()


def reset_checklist():
    answer = messagebox.askyesno(
        "Reset Checklist",
        "Are you sure you want to uncheck every book?"
    )

    if not answer:
        return

    for variable in checklist_vars.values():
        variable.set(False)

    update_progress()


# ============================================================
# MAIN WINDOW
# ============================================================

window = tk.Tk()

window.title("Librarian Curing Calculator")
window.geometry("700x750")


# ============================================================
# CALCULATOR SECTION
# ============================================================

calculator_frame = tk.Frame(window)
calculator_frame.pack(
    fill="x",
    padx=20,
    pady=20
)

title_label = tk.Label(
    calculator_frame,
    text="Librarian Curing Calculator",
    font=("Arial", 20, "bold")
)

title_label.pack(
    pady=(0, 15)
)

description_label = tk.Label(
    calculator_frame,
    text="Enter the base emerald price of the enchanted book:",
    font=("Arial", 11)
)

description_label.pack()

price_entry = tk.Entry(
    calculator_frame,
    font=("Arial", 16),
    justify="center",
    width=8
)

price_entry.pack(
    pady=10
)

calculate_button = tk.Button(
    calculator_frame,
    text="Calculate",
    font=("Arial", 11, "bold"),
    command=calculate
)

calculate_button.pack()

result_label = tk.Label(
    calculator_frame,
    text="Enter a price above.",
    font=("Arial", 18, "bold")
)

result_label.pack(
    pady=15
)


# ============================================================
# SEPARATOR
# ============================================================

separator = tk.Frame(
    window,
    height=2,
    bg="gray"
)

separator.pack(
    fill="x",
    padx=20,
    pady=5
)


# ============================================================
# CHECKLIST HEADER
# ============================================================

checklist_title = tk.Label(
    window,
    text="1-Emerald Book Checklist",
    font=("Arial", 17, "bold")
)

checklist_title.pack(
    pady=(15, 5)
)

progress_label = tk.Label(
    window,
    text=f"0 / {len(ENCHANTMENTS)} Complete",
    font=("Arial", 11)
)

progress_label.pack(
    pady=(0, 10)
)

# ============================================================
# FOUR-COLUMN CHECKLIST
# ============================================================

checklist_frame = tk.Frame(window)

checklist_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=5
)

# Make the three columns expand evenly.
for column in range(4):
    checklist_frame.columnconfigure(
        column,
        weight=1
    )


# Divide the enchantments into three columns.
items_per_column = (len(ENCHANTMENTS) + 2) // 4

for index, (enchantment, max_level) in enumerate(ENCHANTMENTS):

    column = index // items_per_column
    row = index % items_per_column

    variable = tk.BooleanVar(
        value=saved_checklist.get(
            enchantment,
            False
        )
    )

    checklist_vars[enchantment] = variable

    checkbox = tk.Checkbutton(
        checklist_frame,
        text=f"{enchantment} {to_roman(max_level)}",
        variable=variable,
        command=update_progress,
        font=("Arial", 10),
        anchor="w"
    )

    checkbox.grid(
        row=row,
        column=column,
        sticky="w",
        padx=8,
        pady=2
    )


# ============================================================
# INITIAL PROGRESS
# ============================================================

completed = sum(
    variable.get()
    for variable in checklist_vars.values()
)

progress_label.config(
    text=f"{completed} / {len(ENCHANTMENTS)} Complete"
)


# ============================================================
# BUTTONS
# ============================================================

button_frame = tk.Frame(window)

button_frame.pack(
    pady=15
)

reset_button = tk.Button(
    button_frame,
    text="Reset Checklist",
    command=reset_checklist
)

reset_button.pack(
    side="left",
    padx=5
)

save_button1 = tk.Button(
    button_frame,
    text="Save",
    command=save_checklist
)

save_button1.pack(
    side="left",
    padx=5
)

save_button = tk.Button(
    button_frame,
    text="Save As...",
    command=save_checklist_as
)

save_button.pack(
    side="left",
    padx=5
)

load_button = tk.Button(
    button_frame,
    text="Load",
    command=load_checklist_from_file
)

load_button.pack(
    side="left",
    padx=5
)


# ============================================================
# KEYBOARD SHORTCUTS
# ============================================================

price_entry.bind(
    "<Return>",
    lambda event: calculate()
)

price_entry.focus()


# ============================================================
# START PROGRAM
# ============================================================

window.mainloop()