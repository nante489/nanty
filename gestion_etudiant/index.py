import streamlit as st
from pymongo import MongoClient

# 1. Configuration de la connexion (sans les chevrons < > !)
@st.cache_resource
def init_connection():
    uri = "mongodb+srv://gestion_etudiants_db:Admin34@cluster0.prhtizv.mongodb.net/?appName=Cluster0"
    return MongoClient(uri)

# Initialisation du client MongoDB
client = init_connection()

# 2. Choix de la base de données et de la collection
db = client["ma_base_etudiants"]      # Nom de votre base de données
collection = db["etudiants"]         # Nom de votre collection

# 3. Exemple de votre interface Streamlit et de l'action d'ajout
st.title("Gestion des étudiants")

# Vos champs de saisie (adaptez selon vos variables existantes)
numero = st.number_input("Numéro", value=122, step=1)
prenom = st.text_input("Prénom", value="nanty")
age = st.number_input("Âge", value=18, step=1)
classe = st.text_input("Classe", value="M1")

# Bouton d'ajout
if st.button("Ajouter"):
    try:
        # Insertion directe du dictionnaire Python dans MongoDB
        etudiant_data = {
            "numero": int(numero),
            "prenom": prenom,
            "age": int(age),
            "classe": classe
        }
        
        # Enregistrement dans MongoDB Atlas
        collection.insert_one(etudiant_data)
        st.success("Étudiant ajouté avec succès dans MongoDB !")
        
    except Exception as e:
        # Affichage de l'erreur exacte en cas de souci réseau ou d'authentification
        st.error(f"Erreur exacte : {e}")

