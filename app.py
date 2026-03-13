import streamlit as st
import requests
import os
from datetime import datetime

# Το link σου από το SheetDB
API_URL = "https://sheetdb.io/api/v1/ncc7d3mzgjt97"

st.set_page_config(page_title="Sounio Garden House Check-in", page_icon="🏠")

# Εμφάνιση λογοτύπου αν υπάρχει το αρχείο
if os.path.exists("logo.jpg"):
    st.image("logo.jpg", use_container_width=True)

st.title("Sounio Garden House 🏠")
st.subheader("Φόρμα Check-in / Registration Form")

with st.form("checkin_form", clear_on_submit=True):
    # Ερώτηση για την εθνικότητα που καθορίζει τα πεδία
    residence = st.radio(
        "Είστε μόνιμος κάτοικος Ελλάδας; / Are you a Greek resident?", 
        ("Ναι / Yes", "Όχι / No")
    )
    
    name = st.text_input("Ονοματεπώνυμο / Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Τηλέφωνο / Phone Number")

    # Λογική εμφάνισης/εξαφάνισης πεδίων
    if residence == "Ναι / Yes":
        # Εμφανίζεται μόνο το ΑΦΜ για Έλληνες
        identity_val = st.text_input("ΑΦΜ (Υποχρεωτικό)")
        country = "Ελλάδα"
    else:
        # Εμφανίζονται Διαβατήριο και Χώρα για ξένους
        identity_val = st.text_input("Αριθμός Διαβατηρίου ή Ταυτότητας / Passport or ID Number")
        country = st.text_input("Χώρα Προέλευσης / Country of Origin")

    submit = st.form_submit_button("Υποβολή Στοιχείων / Submit")

if submit:
    # Έλεγχος αν έχουν συμπληρωθεί τα βασικά
    if name and identity_val:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Προετοιμασία δεδομένων για το Excel
        # Οι τίτλοι (κλειδιά) πρέπει να είναι ΙΔΙΟΙ με την πρώτη γραμμή του Excel
        data = {
            "Ημερομηνία": now,
            "Τύπος": residence,
            "Όνομα": name,
            "Χώρα": country,
            "Στοιχείο": identity_val,
            "Email": email,
            "Τηλέφωνο": phone
        }
        
        try:
            # Αποστολή στο SheetDB
            response = requests.post(API_URL, json={"data": [data]})
            if response.status_code == 201:
                st.success("Η υποβολή έγινε επιτυχώς! Σας ευχαριστούμε.")
                st.balloons()
            else:
                st.error("Κάτι πήγε στραβά με την αποθήκευση στο Excel. Ελέγξτε τους τίτλους των στηλών.")
        except Exception as e:
            st.error(f"Σφάλμα σύνδεσης: {e}")
    else:
        st.error("Παρακαλούμε συμπληρώστε το Ονοματεπώνυμο και το ΑΦΜ ή το Διαβατήριο.")
