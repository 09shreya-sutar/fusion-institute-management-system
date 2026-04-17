# ============================================================
#   Fusion Institute of Computer Technology
#   Institute Management System
#   MySQL Version - All modules connected to MySQL
# ============================================================

# ---------- IMPORTS ----------
import os
import random
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from tkcalendar import DateEntry
import mysql.connector

# ============================================================
#   DATABASE CONNECTION & SETUP
# ============================================================

def get_connection():
    """Returns a fresh MySQL connection. Update credentials below."""
    return mysql.connector.connect(
        host="localhost",
        user="root",          # <-- change to your MySQL username
        password="",          # <-- change to your MySQL password
        database="fusion_institute"
    )


def setup_database():
    """Creates the database and all tables if they don't exist."""
    try:
        # Connect without specifying database first
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Shreya@2709"       # <-- change to your MySQL password
        )
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS fusion_institute")
        cursor.execute("USE fusion_institute")

        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(100),
                middle_name VARCHAR(100),
                last_name VARCHAR(100),
                mother_name VARCHAR(100),
                father_name VARCHAR(100),
                gender VARCHAR(20),
                dob VARCHAR(30),
                mobile VARCHAR(20),
                email VARCHAR(100),
                house_no VARCHAR(100),
                street VARCHAR(100),
                city VARCHAR(100),
                taluka VARCHAR(100),
                district VARCHAR(100),
                state VARCHAR(100),
                pincode VARCHAR(20),
                country VARCHAR(50),
                marks_10 VARCHAR(20),
                marks_12 VARCHAR(20),
                stream VARCHAR(100),
                college VARCHAR(150),
                passing_year VARCHAR(10),
                admission_year VARCHAR(10),
                course VARCHAR(100),
                roll_no VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Staff table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                salary VARCHAR(50),
                address TEXT,
                email VARCHAR(100),
                subject VARCHAR(100)
            )
        """)

        # Payments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                receipt_no VARCHAR(50),
                student_name VARCHAR(100),
                course VARCHAR(100),
                payment_mode VARCHAR(30),
                total_fees DECIMAL(10,2),
                fees_paid DECIMAL(10,2),
                pending_fees DECIMAL(10,2),
                date VARCHAR(50)
            )
        """)

        # Attendance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                course VARCHAR(100),
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                month VARCHAR(30),
                date VARCHAR(30),
                status VARCHAR(20)
            )
        """)

        # Users (login) table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE,
                password VARCHAR(100)
            )
        """)

        # Insert default admin if not exists
        cursor.execute("SELECT * FROM users WHERE username='admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'fusion123')")

        conn.commit()
        conn.close()
        print("✅ Database setup complete.")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Setup Error",
            f"Could not connect to MySQL.\n\n{e}\n\nMake sure MySQL is running and credentials are correct in get_connection().")


# ============================================================
#   MAIN WINDOW
# ============================================================

root = Tk()
root.withdraw()

# Run DB setup
setup_database()


# ============================================================
#   LOGIN WINDOW
# ============================================================

def open_login():
    login_win = Toplevel()
    login_win.title("Fusion Institute Login")
    login_win.geometry("500x550")
    login_win.configure(bg="#f0f4f7")
    login_win.resizable(False, False)

    Label(login_win, text="🔐 Fusion Institute Login",
          font=("Segoe UI", 20, "bold"), bg="#f0f4f7", fg="#003366").pack(pady=30)

    form_frame = Frame(login_win, bg="#f0f4f7")
    form_frame.pack(pady=10)

    Label(form_frame, text="Username", font=("Segoe UI", 12, "bold"),
          bg="#f0f4f7", anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=10)
    username_entry = Entry(form_frame, font=("Segoe UI", 12), width=30)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(form_frame, text="Password", font=("Segoe UI", 12, "bold"),
          bg="#f0f4f7", anchor="w").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    password_entry = Entry(form_frame, font=("Segoe UI", 12), show="*", width=30)
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def validate_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username, password)
            )
            user = cursor.fetchone()
            conn.close()
            if user:
                messagebox.showinfo("Login Successful", "Welcome to Fusion Institute!")
                login_win.destroy()
                root.deiconify()
                setup_main_gui()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        except mysql.connector.Error as e:
            messagebox.showerror("DB Error", str(e))

    def forgot_password():
        messagebox.showinfo("Forgot Password",
                            "Please contact admin at fusiontechnology09@gmail.com")

    Button(login_win, text="Login", font=("Segoe UI", 12, "bold"),
           bg="#006699", fg="white", width=20, command=validate_login).pack(pady=20)
    Button(login_win, text="Forgot Password?", font=("Segoe UI", 10, "underline"),
           bg="#f0f4f7", fg="blue", bd=0, command=forgot_password).pack()

    try:
        img = Image.open("logo resize.png").resize((400, 150))
        banner_img = ImageTk.PhotoImage(img)
        banner_label = Label(login_win, image=banner_img, bg="#f0f4f7")
        banner_label.image = banner_img
        banner_label.pack(pady=30)
    except Exception:
        Label(login_win, text="(Banner image not found)",
              font=("Segoe UI", 10), bg="#f0f4f7", fg="gray").pack(pady=30)


# ============================================================
#   MAIN GUI SETUP
# ============================================================

def setup_main_gui():
    root.title("Student Admission Platform")
    root.geometry("1366x768")
    root.state("zoomed")
    root["bg"] = "white"

    # Header
    frame1 = Frame(root, bd=5, bg="navy")
    frame1.place(x=0, y=0, height=210, width=1730)

    try:
        file1 = PhotoImage(file="logo resize.png")
        label_logo = Label(frame1, image=file1, bg="navy")
        label_logo.image = file1
        label_logo.place(y=0, x=0)
    except Exception:
        pass

    Label(frame1, text="          Fusion Institute Of Computer Technology",
          font="roboto 34 bold", bg="navy", fg="white").place(x=330, y=2)
    Label(frame1, text="                              IT Training & Software Institute",
          font="roboto 25 bold", bg="navy", fg="white").place(x=330, y=50)

    Frame(root, bg="dark orange", width=1300, height=50).place(x=280, y=159)

    # Marquee
    info_text = (
        "           🎁 ₹7000 Scholarship + 6-Month Internship Certificate (First 40 Students) "
        "           📍 Address: 1st floor, Near YC college, opposite Bus Stop, Kamathipura, Godoli, Satara | "
        "           📞 Phone: 9270508352 / 9112387480 | "
        "           📧 Email: fusiontechnology09@gmail.com"
    )
    marquee_label = Label(root, text=info_text, font=("roboto", 12), fg="blue4",
                          bg="dark orange", width=400, anchor="w", height=2)
    marquee_label.place(x=280, y=165)

    def scroll_text():
        current = marquee_label.cget("text")
        marquee_label.config(text=current[1:] + current[0])
        root.after(100, scroll_text)

    scroll_text()

    # Navbar
    nav_frame = Frame(root, bg="dark blue", height=50, width=1600)
    nav_frame.place(x=0, y=212)
    btn_font = ("Arial", 12, "bold")
    btn_fg = "white"
    btn_bg = "dark blue"
    btn_active_bg = "#16213e"

    Button(nav_frame, text="Admission",     font=btn_font, fg=btn_fg, bg=btn_bg, command=open_home,      activebackground=btn_active_bg, bd=0).place(x=100, y=10)
    Button(nav_frame, text="Payment",       font=btn_font, fg=btn_fg, bg=btn_bg, command=open_about,     activebackground=btn_active_bg, bd=0).place(x=250, y=10)
    Button(nav_frame, text="Courses",       font=btn_font, fg=btn_fg, bg=btn_bg, command=open_courses,   activebackground=btn_active_bg, bd=0).place(x=400, y=10)
    Button(nav_frame, text="Total Students",font=btn_font, fg=btn_fg, bg=btn_bg, command=open_addmision, activebackground=btn_active_bg, bd=0).place(x=550, y=10)
    Button(nav_frame, text="Attendance",    font=btn_font, fg=btn_fg, bg=btn_bg, command=open_Gallery,   activebackground=btn_active_bg, bd=0).place(x=750, y=10)
    Button(nav_frame, text="Staff Details", font=btn_font, fg=btn_fg, bg=btn_bg, command=open_contact,   activebackground=btn_active_bg, bd=0).place(x=900, y=10)

    # Background image
    try:
        file2 = PhotoImage(file="correct123 (1).png")
        label_bg = Label(root, bg="navy", image=file2)
        label_bg.image = file2
        label_bg.place(x=0, y=264, width=1600, height=546)
    except Exception:
        pass

    # Theme toggle
    light_theme = {"bg": "#ffffff", "fg": "#000000", "icon_bg": "#000000", "icon_fg": "#ffffff"}
    dark_theme  = {"bg": "#000000", "fg": "#ffffff", "icon_bg": "#ffffff", "icon_fg": "#000000"}
    current_theme = ["light"]

    def apply_theme(theme):
        root.configure(bg=theme["bg"])
        text_label.configure(bg=theme["bg"], fg=theme["fg"])
        canvas.configure(bg=theme["bg"])
        canvas.delete("all")
        canvas.create_oval(2, 2, 28, 28, fill=theme["icon_bg"], outline=theme["icon_fg"], width=2)
        canvas.create_arc(2, 2, 28, 28, start=270, extent=180, fill=theme["icon_fg"], outline=theme["icon_fg"])

    def toggle_theme(event=None):
        if current_theme[0] == "light":
            current_theme[0] = "dark"
            apply_theme(dark_theme)
        else:
            current_theme[0] = "light"
            apply_theme(light_theme)

    canvas = Canvas(root, width=30, height=30, highlightthickness=0, bd=2, bg=light_theme["bg"])
    canvas.place(x=1350, y=100)
    canvas.bind("<Button-1>", toggle_theme)
    text_label = Label(root, text="High Contrast", font=("roboto", 14, "bold"),
                       bg=light_theme["bg"], fg=light_theme["fg"])
    text_label.place(x=1390, y=100)
    text_label.bind("<Button-1>", toggle_theme)
    apply_theme(light_theme)

    root.resizable(False, False)


# ============================================================
#   ADMISSION (open_home) - MySQL
# ============================================================

def open_home():
    new_win = Toplevel(root)
    new_win.title("Student Admission Form")
    new_win.geometry("1450x900")
    new_win.configure(bg="#D7EAF9")

    header_frame = Frame(new_win, bg="#0047AB")
    header_frame.place(x=0, y=0, width=1450, height=80)
    Label(header_frame, text="💻 FUSION INSTITUTE OF COMPUTER TECHNOLOGY",
          font=("Arial", 22, "bold"), bg="#0047AB", fg="white").pack(pady=(10, 0))
    Label(header_frame, text="ADMISSION FORM",
          font=("Arial", 16, "bold"), bg="#0047AB", fg="white").pack()

    content_y = 90
    frame_bg = "#E8F0FE"

    # Search
    Label(new_win, text="Search Student by Name:", font=("Arial", 11, "bold"), bg="#D7EAF9").place(x=30, y=content_y)
    search_entry = Entry(new_win, width=30, font=("Arial", 10))
    search_entry.place(x=230, y=content_y)

    # Personal Details
    personal_frame = LabelFrame(new_win, text="Personal Details", font=("Arial", 12, "bold"), padx=10, pady=10, bg=frame_bg)
    personal_frame.place(x=30, y=content_y + 40, width=280, height=350)
    labels_personal = ["First Name", "Middle Name", "Last Name", "Mother Name", "Father Name",
                       "Gender", "Date of Birth", "Mobile No", "Email"]
    personal_entries = {}
    for i, lbl in enumerate(labels_personal):
        Label(personal_frame, text=lbl, font=("Arial", 10, "bold"), bg=frame_bg).grid(row=i, column=0, sticky="w", pady=3)
        entry = Entry(personal_frame, width=25)
        entry.grid(row=i, column=1, pady=3)
        personal_entries[lbl] = entry

    # Address Details
    address_frame = LabelFrame(new_win, text="Address Details", font=("Arial", 12, "bold"), padx=10, pady=10, bg=frame_bg)
    address_frame.place(x=340, y=content_y + 40, width=290, height=350)
    labels_address = ["House No / Name", "Street / Area", "City / Village", "Taluka", "District", "State", "Pincode", "Country"]
    address_entries = {}
    for i, lbl in enumerate(labels_address):
        Label(address_frame, text=lbl, font=("Arial", 10, "bold"), bg=frame_bg).grid(row=i, column=0, sticky="w", pady=3)
        entry = Entry(address_frame, width=25)
        entry.grid(row=i, column=1, pady=3)
        address_entries[lbl] = entry

    # Education Details
    education_frame = LabelFrame(new_win, text="Education Details", font=("Arial", 12, "bold"), padx=10, pady=10, bg=frame_bg)
    education_frame.place(x=650, y=content_y + 40, width=280, height=350)
    labels_edu = ["10th Marks (%)", "12th Marks (%)", "Stream", "College Name",
                  "Passing Year", "Admission Year", "Course", "Roll No"]
    education_entries = {}
    for i, lbl in enumerate(labels_edu):
        Label(education_frame, text=lbl, font=("Arial", 10, "bold"), bg=frame_bg).grid(row=i, column=0, sticky="w", pady=3)
        entry = Entry(education_frame, width=25)
        entry.grid(row=i, column=1, pady=3)
        education_entries[lbl] = entry

    # Document Upload
    doc_frame = LabelFrame(new_win, text="Document Upload", font=("Arial", 12, "bold"), padx=10, pady=10, bg=frame_bg)
    doc_frame.place(x=30, y=content_y + 410, width=900, height=210)
    docs = ["Aadhaar Card", "10th Marksheet", "12th Marksheet", "Transfer Certificate", "Passport Size Photo", "Signature"]
    uploaded_docs = {}

    def upload_file(doc_type):
        filename = filedialog.askopenfilename(parent=new_win, title=f"Select {doc_type}", filetypes=[("All Files", "*.*")])
        if filename:
            uploaded_docs[doc_type].config(text=os.path.basename(filename), fg="black")
            uploaded_docs[doc_type].file_path = filename
            new_win.lift()
            new_win.focus_force()
            update_preview()

    for i, doc in enumerate(docs):
        Label(doc_frame, text=doc, font=("Arial", 10, "bold"), bg=frame_bg).grid(row=i, column=0, sticky="w", pady=2)
        lbl = Label(doc_frame, text="No file selected", width=40, anchor="w", relief=SUNKEN, bg="white")
        lbl.grid(row=i, column=1, padx=5)
        Button(doc_frame, text="Upload", bg="#006B3C", fg="white", command=lambda d=doc: upload_file(d)).grid(row=i, column=2, padx=5)
        uploaded_docs[doc] = lbl

    # Preview Panel
    preview_frame = LabelFrame(new_win, text="Form Preview", font=("Arial", 14, "bold"), bg="#E9F3FF", relief="ridge", bd=3)
    preview_frame.place(x=950, y=content_y + 40, width=450, height=790)

    photo_label = Label(preview_frame, bg="white", relief="solid")
    photo_label.place(x=160, y=40, width=130, height=130)
    signature_label = Label(preview_frame, bg="white", relief="solid")
    signature_label.place(x=160, y=190, width=130, height=50)

    scrollbar = Scrollbar(preview_frame)
    scrollbar.place(x=420, y=260, height=500)
    preview_text = Text(preview_frame, wrap=WORD, font=("Arial", 10), bg="#F7FBFF",
                        relief="sunken", yscrollcommand=scrollbar.set)
    preview_text.place(x=20, y=260, width=400, height=500)
    scrollbar.config(command=preview_text.yview)

    def update_preview(event=None):
        preview_text.delete(1.0, END)
        preview_text.insert(END, "📄 FUSION INSTITUTE OF COMPUTER TECHNOLOGY\n")
        preview_text.insert(END, "-"*60 + "\n📝 STUDENT ADMISSION FORM\n\n")
        preview_text.insert(END, "🔹 PERSONAL DETAILS\n")
        for k, v in personal_entries.items():
            preview_text.insert(END, f"{k}: {v.get()}\n")
        preview_text.insert(END, "\n🔹 ADDRESS DETAILS\n")
        for k, v in address_entries.items():
            preview_text.insert(END, f"{k}: {v.get()}\n")
        preview_text.insert(END, "\n🔹 EDUCATION DETAILS\n")
        for k, v in education_entries.items():
            preview_text.insert(END, f"{k}: {v.get()}\n")
        preview_text.insert(END, "\n🔹 DOCUMENTS UPLOADED\n")
        for doc, lbl in uploaded_docs.items():
            preview_text.insert(END, f"{doc}: {lbl.cget('text')}\n")

        photo_path = getattr(uploaded_docs["Passport Size Photo"], "file_path", None)
        if photo_path and os.path.exists(photo_path):
            try:
                img = Image.open(photo_path).resize((130, 130))
                img = ImageTk.PhotoImage(img)
                photo_label.config(image=img, text="")
                photo_label.image = img
            except Exception:
                pass
        else:
            photo_label.config(image="", text="No Photo", font=("Arial", 9), fg="gray")

        sign_path = getattr(uploaded_docs["Signature"], "file_path", None)
        if sign_path and os.path.exists(sign_path):
            try:
                sign_img = Image.open(sign_path).resize((130, 50))
                sign_img = ImageTk.PhotoImage(sign_img)
                signature_label.config(image=sign_img, text="")
                signature_label.image = sign_img
            except Exception:
                pass
        else:
            signature_label.config(image="", text="No Signature", font=("Arial", 9), fg="gray")

    for entry_dict in [personal_entries, address_entries, education_entries]:
        for entry in entry_dict.values():
            entry.bind("<KeyRelease>", update_preview)

    # ---------- SAVE to MySQL ----------
    def save_data():
        name = personal_entries["First Name"].get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter student's First Name before saving.")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (
                    first_name, middle_name, last_name, mother_name, father_name,
                    gender, dob, mobile, email,
                    house_no, street, city, taluka, district, state, pincode, country,
                    marks_10, marks_12, stream, college, passing_year, admission_year, course, roll_no
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                personal_entries["First Name"].get(),
                personal_entries["Middle Name"].get(),
                personal_entries["Last Name"].get(),
                personal_entries["Mother Name"].get(),
                personal_entries["Father Name"].get(),
                personal_entries["Gender"].get(),
                personal_entries["Date of Birth"].get(),
                personal_entries["Mobile No"].get(),
                personal_entries["Email"].get(),
                address_entries["House No / Name"].get(),
                address_entries["Street / Area"].get(),
                address_entries["City / Village"].get(),
                address_entries["Taluka"].get(),
                address_entries["District"].get(),
                address_entries["State"].get(),
                address_entries["Pincode"].get(),
                address_entries["Country"].get(),
                education_entries["10th Marks (%)"].get(),
                education_entries["12th Marks (%)"].get(),
                education_entries["Stream"].get(),
                education_entries["College Name"].get(),
                education_entries["Passing Year"].get(),
                education_entries["Admission Year"].get(),
                education_entries["Course"].get(),
                education_entries["Roll No"].get(),
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Saved", f"Student '{name}' saved successfully!")
            update_preview()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    # ---------- SEARCH from MySQL ----------
    def search_student():
        name = search_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Needed", "Please enter a name to search.")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students WHERE first_name LIKE %s LIMIT 1", (f"%{name}%",))
            row = cursor.fetchone()
            conn.close()
            if not row:
                messagebox.showinfo("Not Found", f"No record found for '{name}'.")
                return
            # Fill personal entries
            personal_entries["First Name"].delete(0, END);    personal_entries["First Name"].insert(0, row["first_name"] or "")
            personal_entries["Middle Name"].delete(0, END);   personal_entries["Middle Name"].insert(0, row["middle_name"] or "")
            personal_entries["Last Name"].delete(0, END);     personal_entries["Last Name"].insert(0, row["last_name"] or "")
            personal_entries["Mother Name"].delete(0, END);   personal_entries["Mother Name"].insert(0, row["mother_name"] or "")
            personal_entries["Father Name"].delete(0, END);   personal_entries["Father Name"].insert(0, row["father_name"] or "")
            personal_entries["Gender"].delete(0, END);        personal_entries["Gender"].insert(0, row["gender"] or "")
            personal_entries["Date of Birth"].delete(0, END); personal_entries["Date of Birth"].insert(0, row["dob"] or "")
            personal_entries["Mobile No"].delete(0, END);     personal_entries["Mobile No"].insert(0, row["mobile"] or "")
            personal_entries["Email"].delete(0, END);         personal_entries["Email"].insert(0, row["email"] or "")
            # Fill address entries
            address_entries["House No / Name"].delete(0, END); address_entries["House No / Name"].insert(0, row["house_no"] or "")
            address_entries["Street / Area"].delete(0, END);   address_entries["Street / Area"].insert(0, row["street"] or "")
            address_entries["City / Village"].delete(0, END);  address_entries["City / Village"].insert(0, row["city"] or "")
            address_entries["Taluka"].delete(0, END);          address_entries["Taluka"].insert(0, row["taluka"] or "")
            address_entries["District"].delete(0, END);        address_entries["District"].insert(0, row["district"] or "")
            address_entries["State"].delete(0, END);           address_entries["State"].insert(0, row["state"] or "")
            address_entries["Pincode"].delete(0, END);         address_entries["Pincode"].insert(0, row["pincode"] or "")
            address_entries["Country"].delete(0, END);         address_entries["Country"].insert(0, row["country"] or "")
            # Fill education entries
            education_entries["10th Marks (%)"].delete(0, END);  education_entries["10th Marks (%)"].insert(0, row["marks_10"] or "")
            education_entries["12th Marks (%)"].delete(0, END);  education_entries["12th Marks (%)"].insert(0, row["marks_12"] or "")
            education_entries["Stream"].delete(0, END);           education_entries["Stream"].insert(0, row["stream"] or "")
            education_entries["College Name"].delete(0, END);     education_entries["College Name"].insert(0, row["college"] or "")
            education_entries["Passing Year"].delete(0, END);     education_entries["Passing Year"].insert(0, row["passing_year"] or "")
            education_entries["Admission Year"].delete(0, END);   education_entries["Admission Year"].insert(0, row["admission_year"] or "")
            education_entries["Course"].delete(0, END);           education_entries["Course"].insert(0, row["course"] or "")
            education_entries["Roll No"].delete(0, END);          education_entries["Roll No"].insert(0, row["roll_no"] or "")
            update_preview()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    # ---------- UPDATE in MySQL ----------
    def update_data():
        name = personal_entries["First Name"].get().strip()
        if not name:
            messagebox.showwarning("Missing Name", "Enter the student's first name to update.")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE students SET
                    middle_name=%s, last_name=%s, mother_name=%s, father_name=%s,
                    gender=%s, dob=%s, mobile=%s, email=%s,
                    house_no=%s, street=%s, city=%s, taluka=%s, district=%s, state=%s, pincode=%s, country=%s,
                    marks_10=%s, marks_12=%s, stream=%s, college=%s, passing_year=%s, admission_year=%s, course=%s, roll_no=%s
                WHERE first_name=%s
            """, (
                personal_entries["Middle Name"].get(),
                personal_entries["Last Name"].get(),
                personal_entries["Mother Name"].get(),
                personal_entries["Father Name"].get(),
                personal_entries["Gender"].get(),
                personal_entries["Date of Birth"].get(),
                personal_entries["Mobile No"].get(),
                personal_entries["Email"].get(),
                address_entries["House No / Name"].get(),
                address_entries["Street / Area"].get(),
                address_entries["City / Village"].get(),
                address_entries["Taluka"].get(),
                address_entries["District"].get(),
                address_entries["State"].get(),
                address_entries["Pincode"].get(),
                address_entries["Country"].get(),
                education_entries["10th Marks (%)"].get(),
                education_entries["12th Marks (%)"].get(),
                education_entries["Stream"].get(),
                education_entries["College Name"].get(),
                education_entries["Passing Year"].get(),
                education_entries["Admission Year"].get(),
                education_entries["Course"].get(),
                education_entries["Roll No"].get(),
                name
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Updated", f"Student '{name}' updated successfully!")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    # ---------- RESET ----------
    def reset_form():
        for entry_dict in [personal_entries, address_entries, education_entries]:
            for entry in entry_dict.values():
                entry.delete(0, END)
        for lbl in uploaded_docs.values():
            lbl.config(text="No file selected")
            if hasattr(lbl, "file_path"):
                del lbl.file_path
        preview_text.delete(1.0, END)
        photo_label.config(image="", text="No Photo", font=("Arial", 9), fg="gray")
        signature_label.config(image="", text="No Signature", font=("Arial", 9), fg="gray")
        messagebox.showinfo("Reset", "Form cleared!")

    Button(new_win, text="Search", bg="#0047AB", fg="white", command=search_student).place(x=420, y=content_y - 3, width=80)
    Button(new_win, text="Submit", font=("Arial", 12, "bold"), bg="#28A745", fg="white", command=save_data).place(x=200, y=content_y + 660, width=200, height=40)
    Button(new_win, text="Update", font=("Arial", 12, "bold"), bg="#007BFF", fg="white", command=update_data).place(x=440, y=content_y + 660, width=200, height=40)
    Button(new_win, text="Reset",  font=("Arial", 12, "bold"), bg="#FFC107", fg="black",  command=reset_form).place(x=680, y=content_y + 660, width=200, height=40)


# ============================================================
#   PAYMENT (open_about) - MySQL
# ============================================================

def open_about():
    course_fees = {
        "Python Fullstack": 30000,
        "Data Analytics":   35000,
        "Data Science":     40000,
        "AI":               45000
    }

    win = Toplevel(root)
    win.title("Fusion Tech - Student Fee Payment System")
    win.geometry("1000x720")
    win.config(bg="#f7f9fc")

    def on_enter(e): e.widget['bg'] = '#0052cc'
    def on_leave(e): e.widget['bg'] = e.widget.default_bg

    header = Frame(win, bg="#1e3d59", height=80)
    header.pack(fill=X)
    Label(header, text="💻 Fusion Tech - Student Fee Payment System",
          font=("Segoe UI", 22, "bold"), fg="white", bg="#1e3d59").pack(pady=20)

    form_frame = Frame(win, bg="white", bd=2, relief=GROOVE)
    form_frame.place(x=80, y=110, width=850, height=330)

    Label(form_frame, text="Student Name:", bg="white", font=("Segoe UI", 12)).grid(row=0, column=0, padx=20, pady=15, sticky=W)
    name_entry = Entry(form_frame, font=("Segoe UI", 12), width=30)
    name_entry.grid(row=0, column=1, padx=20, pady=15)

    Label(form_frame, text="Course:", bg="white", font=("Segoe UI", 12)).grid(row=1, column=0, padx=20, pady=15, sticky=W)
    course_var = StringVar()
    course_cb = ttk.Combobox(form_frame, textvariable=course_var, values=list(course_fees.keys()), font=("Segoe UI", 12), state="readonly", width=28)
    course_cb.grid(row=1, column=1, padx=20, pady=15)
    course_cb.current(0)

    Label(form_frame, text="Payment Mode:", bg="white", font=("Segoe UI", 12)).grid(row=2, column=0, padx=20, pady=15, sticky=W)
    mode_var = StringVar()
    mode_cb = ttk.Combobox(form_frame, textvariable=mode_var, values=["Cash", "UPI", "Card"], font=("Segoe UI", 12), state="readonly", width=28)
    mode_cb.grid(row=2, column=1, padx=20, pady=15)
    mode_cb.current(0)

    Label(form_frame, text="Fees Paid (₹):", bg="white", font=("Segoe UI", 12)).grid(row=3, column=0, padx=20, pady=15, sticky=W)
    paid_entry = Entry(form_frame, font=("Segoe UI", 12), width=28)
    paid_entry.grid(row=3, column=1, padx=20, pady=15)

    pending_label = Label(win, text="Pending Fees: ₹0", bg="#f7f9fc",
                          font=("Segoe UI", 14, "bold"), fg="#d90429")
    pending_label.place(x=100, y=460)

    def calculate_pending(*_):
        try:
            total = course_fees[course_var.get()]
            paid = float(paid_entry.get())
            pending_label.config(text=f"Pending Fees: ₹{total - paid:,.0f}")
        except Exception:
            pending_label.config(text="Pending Fees: ₹0")

    paid_entry.bind("<KeyRelease>", calculate_pending)

    def make_payment():
        name = name_entry.get().strip()
        course = course_var.get()
        mode = mode_var.get()
        total = course_fees.get(course, 0)
        date_now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        if not name:
            messagebox.showerror("Error", "Please enter student name")
            return
        try:
            paid = float(paid_entry.get())
        except Exception:
            messagebox.showerror("Error", "Enter valid amount")
            return
        if paid > total:
            messagebox.showerror("Error", "Paid amount cannot exceed total fees")
            return
        pending = max(total - paid, 0)
        receipt_no = f"FT{datetime.now().strftime('%Y%m%d%H%M%S')}"
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO payments (receipt_no, student_name, course, payment_mode, total_fees, fees_paid, pending_fees, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (receipt_no, name, course, mode, total, paid, pending, date_now))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Payment saved!\nReceipt No: {receipt_no}")
            name_entry.delete(0, END)
            paid_entry.delete(0, END)
            pending_label.config(text="Pending Fees: ₹0")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def open_history():
        history = Toplevel(win)
        history.title("Payment History")
        history.geometry("1100x650")
        history.config(bg="white")

        Label(history, text="📜 Payment History", font=("Segoe UI", 18, "bold"),
              bg="#1e3d59", fg="white", pady=10).pack(fill=X)

        search_frame = Frame(history, bg="white")
        search_frame.pack(pady=10)
        Label(search_frame, text="Search by Name:", bg="white", font=("Segoe UI", 12)).pack(side=LEFT, padx=10)
        search_entry = Entry(search_frame, font=("Segoe UI", 12), width=30)
        search_entry.pack(side=LEFT, padx=10)

        columns = ("Receipt No", "Name", "Course", "Mode", "Total", "Paid", "Pending", "Date")
        tree = ttk.Treeview(history, columns=columns, show="headings", height=15)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor=CENTER)
        tree.pack(fill=BOTH, expand=True, padx=20, pady=10)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=('Segoe UI', 10))
        style.map('Treeview', background=[('selected', '#0078D7')])
        tree.tag_configure('odd',  background='#f2f2f2')
        tree.tag_configure('even', background='#ffffff')

        def load_data():
            for i in tree.get_children():
                tree.delete(i)
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT receipt_no, student_name, course, payment_mode,
                           total_fees, fees_paid, pending_fees, date
                    FROM payments ORDER BY id DESC
                """)
                for i, row in enumerate(cursor.fetchall()):
                    tree.insert("", END, values=row, tags=('even' if i % 2 == 0 else 'odd',))
                conn.close()
            except mysql.connector.Error as e:
                messagebox.showerror("DB Error", str(e))

        def search_data():
            name = search_entry.get().strip()
            for i in tree.get_children():
                tree.delete(i)
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT receipt_no, student_name, course, payment_mode,
                           total_fees, fees_paid, pending_fees, date
                    FROM payments WHERE student_name LIKE %s ORDER BY id DESC
                """, (f'%{name}%',))
                for i, row in enumerate(cursor.fetchall()):
                    tree.insert("", END, values=row, tags=('even' if i % 2 == 0 else 'odd',))
                conn.close()
            except mysql.connector.Error as e:
                messagebox.showerror("DB Error", str(e))

        def print_receipt():
            selected = tree.focus()
            if not selected:
                messagebox.showerror("Error", "Select a record to print")
                return
            data = tree.item(selected, "values")
            receipt_no, name, course, mode, total, paid, pending, date = data
            filename = f"Receipt_{receipt_no}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            story.append(Paragraph("<b><font size=16>Fusion Tech Academy</font></b>", styles["Title"]))
            story.append(Spacer(1, 15))
            story.append(Paragraph("<b>OFFICIAL PAYMENT RECEIPT</b>", styles["Heading2"]))
            story.append(Spacer(1, 20))
            data_table = [
                ["Receipt No:", receipt_no], ["Date:", date], ["Student Name:", name],
                ["Course:", course], ["Payment Mode:", mode],
                ["Total Fees:", f"Rs.{float(total or 0):,.0f}"],
                ["Fees Paid:", f"Rs.{float(paid or 0):,.0f}"],
                ["Pending Fees:", f"Rs.{float(pending or 0):,.0f}"]
            ]
            tbl = Table(data_table, colWidths=[150, 300])
            tbl.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.grey),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.grey),
            ]))
            story.append(tbl)
            story.append(Spacer(1, 40))
            story.append(Paragraph("<b>Thank you for your payment!</b>", styles["Italic"]))
            story.append(Spacer(1, 60))
            story.append(Paragraph("Authorized Signature _______________________", styles["Normal"]))
            doc.build(story)
            messagebox.showinfo("Receipt Generated", f"Receipt saved as {filename}")

        btn_frame2 = Frame(history, bg="white")
        btn_frame2.pack(pady=10)
        for text, color, cmd in [("Show All", "#1e3d59", load_data), ("Search", "#0078D7", search_data), ("Print Receipt", "#6a0dad", print_receipt)]:
            b = Button(btn_frame2, text=text, bg=color, fg="white", font=("Segoe UI", 11, "bold"), padx=15, pady=5, command=cmd, relief=FLAT)
            b.default_bg = color
            b.bind("<Enter>", lambda e: e.widget.config(bg="#0052cc"))
            b.bind("<Leave>", lambda e: e.widget.config(bg=e.widget.default_bg))
            b.pack(side=LEFT, padx=10)

        load_data()

    btn_frame = Frame(win, bg="#f7f9fc")
    btn_frame.place(x=300, y=520)
    for text, color, cmd in [("💰 Make Payment", "#1e3d59", make_payment), ("📜 View History", "#0078D7", open_history)]:
        b = Button(btn_frame, text=text, bg=color, fg="white", font=("Segoe UI", 13, "bold"),
                   padx=20, pady=8, width=20, relief=FLAT, command=cmd)
        b.default_bg = color
        b.bind("<Enter>", on_enter)
        b.bind("<Leave>", on_leave)
        b.pack(pady=10)


# ============================================================
#   COURSES (open_courses) - No DB needed (static info)
# ============================================================

def open_courses():
    win = Toplevel(root)
    win.title("Courses Offered - Fusion Institute of Computer Technology")
    win.geometry("1000x700")
    win.configure(bg="#f0f4f7")

    Label(win, text="Fusion Institute of Computer Technology",
          font=("Helvetica", 24, "bold"), bg="#f0f4f7", fg="#003366").pack(pady=20)
    Label(win, text="IT Training & Software Institute",
          font=("Helvetica", 16), bg="#f0f4f7", fg="#006699").pack(pady=5)

    btn_frame = Frame(win, bg="#f0f4f7")
    btn_frame.pack(pady=30)

    def show_course(title, roadmap, syllabus, duration, fees):
        detail_win = Toplevel(win)
        detail_win.title(f"{title} - Course Details")
        detail_win.geometry("600x500")
        detail_win.configure(bg="#ffffff")
        Label(detail_win, text="Fusion Institute of Computer Technology", font=("Helvetica", 18, "bold"), bg="#ffffff", fg="#003366").pack(pady=10)
        Label(detail_win, text=title, font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#006699").pack(pady=5)
        for heading, content in [("📍 Roadmap:", roadmap), ("📘 Syllabus:", syllabus), ("⏳ Duration:", duration), ("💰 Fees:", fees)]:
            Label(detail_win, text=heading, font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#333333").pack(anchor="w", padx=20, pady=5)
            Label(detail_win, text=content, font=("Helvetica", 12), bg="#ffffff", wraplength=550, justify=LEFT).pack(anchor="w", padx=20)

    courses = [
        ("Artificial Intelligence",  "Learn AI fundamentals, neural networks, and real-world applications.", "Python, NumPy, TensorFlow, Deep Learning, NLP, Projects", "6 Months", "₹35,000"),
        ("Data Science",             "Master data analysis, visualization, and predictive modeling.",        "Python, Pandas, Matplotlib, ML Algorithms, Capstone Project", "5 Months", "₹30,000"),
        ("Machine Learning",         "Build intelligent systems using supervised and unsupervised learning.", "Scikit-learn, Regression, Classification, Clustering, Deployment", "4 Months", "₹28,000"),
        ("Web Development",          "Design responsive websites using modern technologies.",                 "HTML, CSS, JavaScript, Bootstrap, React, Hosting", "3 Months", "₹25,000"),
        ("Full Stack",               "Become a full-stack developer with frontend and backend skills.",       "HTML, CSS, JS, React, Node.js, MongoDB, APIs", "6 Months", "₹40,000"),
        ("Cyber Security",           "Protect systems and networks from digital attacks.",                   "Network Security, Ethical Hacking, Firewalls, Tools", "4 Months", "₹32,000"),
        ("Software Testing",         "Ensure software quality through manual and automated testing.",        "Manual Testing, Selenium, Test Cases, Bug Tracking", "3 Months", "₹22,000"),
        ("ChatGPT / Gemini (AI)",    "Explore conversational AI and generative models.",                     "Prompt Engineering, API Integration, Use Cases", "2 Months", "₹18,000"),
        ("C & C++ / Java / Python",  "Learn foundational programming languages for software development.",   "Syntax, OOPs, Projects, IDEs, Debugging", "3 Months", "₹20,000"),
        ("S/W Development",          "Develop desktop and mobile applications with real-world logic.",        "SDLC, UI Design, Backend Logic, Deployment", "5 Months", "₹30,000"),
        ("Data Analytics",           "Extract insights from data using analytical tools.",                   "Excel, Power BI, SQL, Dashboards, Reports", "3 Months", "₹25,000"),
        ("Hardware & Networking",    "Understand computer hardware and network configurations.",              "Hardware Setup, LAN/WAN, IP Config, Troubleshooting", "3 Months", "₹20,000"),
    ]

    for idx, (title, roadmap, syllabus, duration, fees) in enumerate(courses):
        r, c = divmod(idx, 2)
        Button(btn_frame, text=title, font=("Helvetica", 14), bg="#006699", fg="white", width=30,
               command=lambda t=title, ro=roadmap, sy=syllabus, du=duration, fe=fees: show_course(t, ro, sy, du, fe)
               ).grid(row=r, column=c, padx=10, pady=10)


# ============================================================
#   TOTAL STUDENTS (open_addmision) - MySQL
# ============================================================

def open_addmision():
    win = Toplevel(root)
    win.title("Total Students - Student Admission Platform")
    win.geometry("1200x650+200+80")
    win.config(bg="white")

    header = Frame(win, bg="#1e3d59", height=70)
    header.pack(fill=X)
    Label(header, text="📚 Admitted Students List", font=("Arial", 22, "bold"),
          bg="#1e3d59", fg="white", padx=20).pack(side=LEFT, pady=10)
    Button(header, text="⟳ Refresh", font=("Arial", 12, "bold"), bg="#0078D7", fg="white",
           padx=15, pady=5, bd=0, cursor="hand2",
           command=lambda: [win.destroy(), open_addmision()]).pack(side=RIGHT, padx=20, pady=15)

    search_frame = Frame(win, bg="white")
    search_frame.pack(pady=15, fill=X)
    Label(search_frame, text="🔍 Search by Name:", font=("Arial", 12, "bold"), bg="white").pack(side=LEFT, padx=20)
    search_var = StringVar()
    search_entry = Entry(search_frame, textvariable=search_var, font=("Arial", 12), width=30, bd=2, relief=SOLID)
    search_entry.pack(side=LEFT, padx=10)

    table_frame = Frame(win, bg="white", bd=2, relief=RIDGE)
    table_frame.pack(padx=20, pady=10, fill=BOTH, expand=True)

    columns = ("Name", "Mobile", "Email", "Course", "Admission Year")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#1e3d59", foreground="white")
    style.configure("Treeview", font=("Arial", 10), rowheight=28)
    style.map("Treeview", background=[("selected", "#0078D7")], foreground=[("selected", "white")])

    tree.tag_configure("oddrow",  background="white")
    tree.tag_configure("evenrow", background="#f2f2f2")

    scroll_y = Scrollbar(table_frame, orient=VERTICAL,   command=tree.yview)
    scroll_x = Scrollbar(table_frame, orient=HORIZONTAL, command=tree.xview)
    tree.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)
    scroll_y.pack(side=RIGHT,  fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)
    tree.pack(fill=BOTH, expand=True)

    col_widths = {"Name": 260, "Mobile": 150, "Email": 300, "Course": 250, "Admission Year": 160}
    for col, width in col_widths.items():
        tree.heading(col, text=col, anchor=CENTER)
        tree.column(col, anchor=CENTER, width=width, stretch=True)

    def load_data(filter_text=""):
        for row in tree.get_children():
            tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT first_name, mobile, email, course, admission_year
                FROM students WHERE first_name LIKE %s ORDER BY id DESC
            """, (f'%{filter_text}%',))
            for i, row in enumerate(cursor.fetchall()):
                tree.insert("", END, values=row, tags=("evenrow" if i % 2 == 0 else "oddrow",))
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("DB Error", str(e))

    load_data()

    def search_student(event=None):
        load_data(search_var.get())

    search_entry.bind("<KeyRelease>", search_student)

    def delete_student():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?")
        if not confirm:
            return
        values = tree.item(selected_item, "values")
        name_to_delete = values[0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE first_name=%s", (name_to_delete,))
            conn.commit()
            conn.close()
            tree.delete(selected_item)
            messagebox.showinfo("Deleted", f"Student '{name_to_delete}' deleted successfully.")
        except mysql.connector.Error as e:
            messagebox.showerror("DB Error", str(e))

    button_frame = Frame(win, bg="white")
    button_frame.pack(pady=10)
    Button(button_frame, text="🗑 Delete Selected Student", font=("Arial", 12, "bold"),
           bg="#d9534f", fg="white", padx=15, pady=6, bd=0, cursor="hand2",
           command=delete_student).pack()


# ============================================================
#   ATTENDANCE (open_Gallery) - MySQL
# ============================================================

def open_Gallery():
    win = Toplevel(root)
    win.title("Student Attendance Form")
    win.geometry("1000x600")
    win.config(bg="navy")

    main_frame = Frame(win, bg="navy")
    main_frame.pack(fill="both", expand=True)

    form_frame = Frame(main_frame, bg="navy")
    form_frame.pack(side="left", fill="y", padx=30, pady=20)

    tree_frame = Frame(main_frame)
    tree_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    Label(form_frame, text="Student Attendance Form",
          font=("Helvetica", 24, "bold"), bg="navy", fg="white").pack(pady=10, anchor="w")

    Label(form_frame, text="Course Name", font=("Helvetica", 14, "bold"), bg="navy", fg="white").pack(anchor="w", pady=(10, 0))
    course_var = StringVar()
    for text in ["Data Analytics", "Full Stack", "C", "Java", "Python"]:
        tk.Radiobutton(form_frame, text=text, variable=course_var, value=text,
                       font=("Helvetica", 12), bg="navy", fg="white",
                       selectcolor="navy").pack(anchor="w", padx=20)

    Label(form_frame, text="Student Name", font=("Helvetica", 14, "bold"), bg="navy", fg="white").pack(anchor="w", pady=(20, 0))
    name_frame = Frame(form_frame, bg="navy")
    name_frame.pack(anchor="w", pady=5)
    fname_entry = Entry(name_frame, width=25, font=("Helvetica", 12))
    fname_entry.grid(row=0, column=0, padx=10)
    Label(name_frame, text="First Name", bg="navy", fg="white", font=("Helvetica", 10)).grid(row=1, column=0)
    lname_entry = Entry(name_frame, width=25, font=("Helvetica", 12))
    lname_entry.grid(row=0, column=1, padx=10)
    Label(name_frame, text="Last Name", bg="navy", fg="white", font=("Helvetica", 10)).grid(row=1, column=1)

    Label(form_frame, text="Month & Date", font=("Helvetica", 14, "bold"), bg="navy", fg="white").pack(anchor="w", pady=(20, 0))
    datetime_frame = Frame(form_frame, bg="navy")
    datetime_frame.pack(anchor="w", pady=5)
    month_combo = ttk.Combobox(datetime_frame, values=["January","February","March","April","May","June",
                               "July","August","September","October","November","December"],
                               width=22, font=("Helvetica", 12), state="readonly")
    month_combo.grid(row=0, column=0, padx=10)
    month_combo.set("Please Select")
    Label(datetime_frame, text="Month", bg="navy", fg="white", font=("Helvetica", 10)).grid(row=1, column=0)
    date_entry = DateEntry(datetime_frame, width=20, font=("Helvetica", 12),
                           background='white', foreground='black', borderwidth=2, date_pattern='dd/mm/yyyy')
    date_entry.grid(row=0, column=1, padx=10)
    Label(datetime_frame, text="Date", bg="navy", fg="white", font=("Helvetica", 10)).grid(row=1, column=1)

    Label(form_frame, text="Status", font=("Helvetica", 14, "bold"), bg="navy", fg="white").pack(anchor="w", pady=(20, 0))
    status_var = StringVar()
    status_frame = Frame(form_frame, bg="navy")
    status_frame.pack(anchor="w", pady=5)
    for text in ["Attended", "Skipped"]:
        tk.Radiobutton(status_frame, text=text, variable=status_var, value=text,
                       font=("Helvetica", 12), bg="navy", fg="white",
                       selectcolor="navy").pack(anchor="w")

    # Treeview
    Label(tree_frame, text="Attendance Records", font=("Helvetica", 16, "bold")).pack(anchor="w")
    cols = ("Course", "First Name", "Last Name", "Month", "Date", "Status")
    tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=20)
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=120)
    tree.pack(fill="both", expand=True)

    def load_attendance():
        for row in tree.get_children():
            tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT course, first_name, last_name, month, date, status FROM attendance ORDER BY id DESC")
            for row in cursor.fetchall():
                tree.insert("", END, values=row)
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("DB Error", str(e))

    load_attendance()

    def on_tree_select(event):
        sel = tree.focus()
        if sel:
            v = tree.item(sel, "values")
            if v:
                course_var.set(v[0])
                fname_entry.delete(0, END); fname_entry.insert(0, v[1])
                lname_entry.delete(0, END); lname_entry.insert(0, v[2])
                month_combo.set(v[3])
                status_var.set(v[5])

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # ---------- CRUD with MySQL ----------
    def submit_form():
        data = (course_var.get(), fname_entry.get(), lname_entry.get(),
                month_combo.get(), date_entry.get(), status_var.get())
        if not all(data) or month_combo.get() == "Please Select":
            messagebox.showwarning("Missing Data", "Please fill all fields.")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attendance (course, first_name, last_name, month, date, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, data)
            conn.commit()
            conn.close()
            tree.insert("", END, values=data)
            messagebox.showinfo("Success", "Attendance record added!")
        except mysql.connector.Error as e:
            messagebox.showerror("DB Error", str(e))

    def delete_record():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Select Row", "Select a record to delete.")
            return
        v = tree.item(sel, "values")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM attendance WHERE course=%s AND first_name=%s AND last_name=%s AND date=%s LIMIT 1
            """, (v[0], v[1], v[2], v[4]))
            conn.commit()
            conn.close()
            tree.delete(sel)
        except mysql.connector.Error as e:
            messagebox.showerror("DB Error", str(e))

    def clear_form():
        course_var.set("")
        fname_entry.delete(0, END)
        lname_entry.delete(0, END)
        month_combo.set("Please Select")
        status_var.set("")

    b_frame = Frame(form_frame, bg="navy")
    b_frame.pack(anchor="w", pady=5)
    for text, color, cmd in [
        ("Submit", "#4CAF50", submit_form),
        ("Delete", "#f44336", delete_record),
        ("Clear",  "#FF9800", clear_form),
    ]:
        Button(b_frame, text=text, command=cmd, bg=color, fg="white",
               font=("Helvetica", 13, "bold"), width=10).pack(side=LEFT, padx=5, pady=10)


# ============================================================
#   STAFF (open_contact) - MySQL
# ============================================================

def open_contact():
    win = Toplevel(root)
    win.title("Fusion Institute | Staff Management")
    win.geometry("1100x650")
    win.configure(bg="#f4f6fa")

    header_frame = Frame(win, bg="#001f54", height=80)
    header_frame.pack(fill=X)
    Label(header_frame, text="Fusion Institute of Computer Technology",
          font=("Arial Rounded MT Bold", 22, "bold"), bg="#001f54", fg="white").place(x=30, y=10)
    Label(header_frame, text="Training & Software Institute",
          font=("Arial", 12, "italic"), bg="#001f54", fg="#f1c40f").place(x=35, y=48)

    sub_header = Frame(win, bg="#0078D7", height=45)
    sub_header.pack(fill=X, pady=(0, 10))
    Label(sub_header, text="👩‍🏫 Staff Management Panel",
          font=("Arial Rounded MT Bold", 15), bg="#0078D7", fg="white").pack(pady=5)

    search_frame = Frame(win, bg="#f4f6fa")
    search_frame.pack(fill=X, pady=5)
    Label(search_frame, text="🔍 Search:", bg="#f4f6fa", font=("Arial", 12, "bold")).pack(side=LEFT, padx=10)
    search_entry = Entry(search_frame, font=("Arial", 12), width=40, bd=2, relief=SOLID)
    search_entry.pack(side=LEFT, padx=5, pady=5)

    main_frame = Frame(win, bg="#f4f6fa")
    main_frame.pack(fill=BOTH, expand=True, pady=(10, 10), padx=10)

    # Form
    form_frame = Frame(main_frame, bg="white", bd=2, relief=GROOVE)
    form_frame.place(x=20, y=10, width=420, height=400)
    Label(form_frame, text="Add / Update Staff", font=("Arial Rounded MT Bold", 15),
          bg="white", fg="#001f54").pack(pady=10)

    def field(lbl, y):
        Label(form_frame, text=lbl, font=("Arial", 11, "bold"), bg="white", fg="#333").place(x=20, y=y)
        e = Entry(form_frame, font=("Arial", 11), width=27, bd=2, relief=SOLID)
        e.place(x=150, y=y)
        return e

    staff_name    = field("Name:",    60)
    staff_salary  = field("Salary:",  100)
    staff_address = field("Address:", 140)
    staff_email   = field("Email:",   180)
    staff_subject = field("Subject:", 220)

    # Table
    table_frame = Frame(main_frame, bg="white", bd=2, relief=GROOVE)
    table_frame.place(x=470, y=10, width=600, height=400)

    columns = ("Name", "Salary", "Address", "Email", "Subject")
    staff_table = ttk.Treeview(table_frame, columns=columns, show="headings")
    for col in columns:
        staff_table.heading(col, text=col)
        staff_table.column(col, width=110, anchor=W)
    staff_table.pack(fill=BOTH, expand=True)

    s = ttk.Style()
    s.theme_use("clam")
    s.configure("Treeview", font=("Arial", 11), rowheight=27, background="white",
                fieldbackground="white", foreground="#333")
    s.map("Treeview", background=[("selected", "#0078D7")], foreground=[("selected", "white")])

    def clear_fields():
        for e in [staff_name, staff_salary, staff_address, staff_email, staff_subject]:
            e.delete(0, END)

    def load_staff():
        for row in staff_table.get_children():
            staff_table.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name, salary, address, email, subject FROM staff")
            for row in cursor.fetchall():
                staff_table.insert("", END, values=row)
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("DB Error", str(e))

    load_staff()

    def add_staff():
        data = (staff_name.get(), staff_salary.get(), staff_address.get(),
                staff_email.get(), staff_subject.get())
        if not all(data):
            messagebox.showerror("Error", "All fields are required!", parent=win)
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO staff (name, salary, address, email, subject)
                VALUES (%s, %s, %s, %s, %s)
            """, data)
            conn.commit()
            conn.close()
            staff_table.insert("", END, values=data)
            clear_fields()
            messagebox.showinfo("Success", "Staff added successfully!", parent=win)
        except mysql.connector.Error as e:
            messagebox.showerror("DB Error", str(e))

    def select_row(event):
        selected = staff_table.focus()
        if selected:
            values = staff_table.item(selected, "values")
            clear_fields()
            if values:
                staff_name.insert(0, values[0])
                staff_salary.insert(0, values[1])
                staff_address.insert(0, values[2])
                staff_email.insert(0, values[3])
                staff_subject.insert(0, values[4])

    def update_staff():
        selected = staff_table.focus()
        if not selected:
            messagebox.showwarning("Select Row", "Please select a record to update.", parent=win)
            return
        values = (staff_name.get(), staff_salary.get(), staff_address.get(),
                  staff_email.get(), staff_subject.get())
        old_name = staff_table.item(selected, "values")[0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE staff SET name=%s, salary=%s, address=%s, email=%s, subject=%s
                WHERE name=%s
            """, (*values, old_name))
            conn.commit()
            conn.close()
            staff_table.item(selected, values=values)
            messagebox.showinfo("Updated", "Staff record updated!", parent=win)
            clear_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("DB Error", str(e))

    def delete_staff():
        selected = staff_table.focus()
        if not selected:
            messagebox.showwarning("Select Row", "Please select a record to delete.", parent=win)
            return
        name_to_del = staff_table.item(selected, "values")[0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM staff WHERE name=%s", (name_to_del,))
            conn.commit()
            conn.close()
            staff_table.delete(selected)
            messagebox.showinfo("Deleted", "Staff record deleted!", parent=win)
            clear_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("DB Error", str(e))

    def search_staff():
        query = search_entry.get().lower().strip()
        for row in staff_table.get_children():
            staff_table.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, salary, address, email, subject FROM staff
                WHERE LOWER(name) LIKE %s OR LOWER(email) LIKE %s
            """, (f'%{query}%', f'%{query}%'))
            for row in cursor.fetchall():
                staff_table.insert("", END, values=row)
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("DB Error", str(e))

    Button(search_frame, text="Search", bg="#0078D7", fg="white", font=("Arial", 10, "bold"),
           relief=FLAT, padx=10, pady=3, cursor="hand2", command=search_staff).pack(side=LEFT, padx=5)

    staff_table.bind("<ButtonRelease-1>", select_row)

    btn_frame = Frame(form_frame, bg="white")
    btn_frame.place(x=25, y=280)

    def make_btn(text, color, cmd):
        btn = Button(btn_frame, text=text, font=("Arial", 10, "bold"), bg=color,
                     fg="white", width=9, relief=FLAT, command=cmd, cursor="hand2")
        btn.bind("<Enter>", lambda e: btn.config(bg="#005fa3"))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        return btn

    make_btn("Add",    "#28a745", add_staff).grid(row=0, column=0, padx=5, pady=3)
    make_btn("Update", "#0078D7", update_staff).grid(row=0, column=1, padx=5, pady=3)
    make_btn("Delete", "#dc3545", delete_staff).grid(row=0, column=2, padx=5, pady=3)
    make_btn("Clear",  "#ffc107", clear_fields).grid(row=0, column=3, padx=5, pady=3)


# ============================================================
#   LAUNCH
# ============================================================

root.resizable(False, False)
open_login()
root.mainloop()
