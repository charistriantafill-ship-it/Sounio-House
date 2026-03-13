import streamlit as st
import pandas as pd
import os
from datetime import datetime
from gspread_pandas import Spread

SHEET_URL = "https://sheetdb.io/api/v1/ncc7d3mzgjt97"

st.set_page_config(page_title="Sounio Garden House Check-in", page_icon="🏠")

if os.path.exists("logo.jpg"):
    st.image("logo.jpg", use_container_width=True)

st.title("Καλώς ήρθατε στο Sounio Garden House 🏠")
st.subheader("Φόρμα Δήλωσης Στοιχείων / Check-in Form")

with st.form("checkin_form"):
    residence = st.radio("Είστε μόνιμος κάτοικος Ελλάδας; / Are you a permanent resident of Greece?", ("Ναι / Yes", "Όχι / No"))
    name = st.text_input("Ονοματεπώνυμο / Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Τηλέφωνο / Phone Number")

    if residence == "Ναι / Yes":
        tax_id = st.text_input("ΑΦΜ")
        id_number = st.text_input("Αριθμός Ταυτότητας")
        country = "Ελλάδα"
    else:
        passport = st.text_input("Passport Number")
        country = st.text_input("Country of Origin / Χώρα Προέλευσης")
        tax_id = "N/A"
        id_number = passport

    submit = st.form_submit_button("Υποβολή Στοιχείων / Submit")

if submit:
    if name and (id_number or tax_id):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        new_data = {"Ημερομηνία": [now], "Τύπος": [residence], "Όνομα": [name], "Χώρα": [country], "Στοιχείο": [tax_id if residence == "Ναι / Yes" else id_number], "Email": [email], "Τηλέφωνο": [phone]}
        df = pd.DataFrame(new_data)
        
        try:
            spread = Spread(SHEET_URL)
            spread.df_to_sheet(df, index=False, header=False, start="A2", replace=False)
            st.success("Η υποβολή έγινε επιτυχώς στο Excel! Καλή διαμονή!")
            st.balloons()
        except Exception as e:
            st.error(f"Πρόβλημα σύνδεσης με το Excel: {e}")
    else:
        st.error("Παρακαλούμε συμπληρώστε τα υποχρεωτικά πεδία.")