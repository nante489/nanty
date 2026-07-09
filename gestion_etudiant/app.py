import streamlit as st
from db import insert_student, find_student_by_numero, update_student, delete_student, list_students, use_mongodb
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Gestion des étudiants", layout="wide", initial_sidebar_state="collapsed")

# Initialisation du Session State pour maintenir l'affichage des listes et recherches
if "show_list" not in st.session_state:
    st.session_state.show_list = False
if "search_result" not in st.session_state:
    st.session_state.search_result = None

# Custom CSS for better design
st.markdown("""
<style>
* {font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
body {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh;}
.stApp {background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);}
.main {background-color: #f8fafc; border-radius: 10px;}
.card {background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin: 10px 0;}
.stButton > button {width: 100%; padding: 12px; font-size: 15px; font-weight: 600; border-radius: 8px; 
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; 
  cursor: pointer; transition: all 0.3s ease;}
.stButton > button:hover {transform: translateY(-2px); box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);}
.title {color: #2d3748; font-size: 32px; font-weight: 700; margin-bottom: 10px;}
.subtitle {color: #718096; font-size: 16px; margin-bottom: 20px;}
.data-label {color: #4a5568; font-weight: 600; font-size: 14px; margin-bottom: 5px;}
.input-section {background: #f7fafc; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea; margin-bottom: 20px;}
.status-badge {display: inline-block; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; margin-top: 10px;}
.status-ok {background-color: #c6f6d5; color: #22543d;}
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown('<div class="title">📚 Gestion des étudiants</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Système de gestion des données d\'étudiants avec recherche, ajout, modification et suppression</div>', unsafe_allow_html=True)

with col2:
    if use_mongodb:
        st.markdown('<div class="status-badge status-ok">✓ MongoDB Actif</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge status-ok">✓ SQLite fallback actif</div>', unsafe_allow_html=True)

st.divider()

# Input section
with st.container():
    # Correction de l'encapsulation HTML en combinant l'ouverture et la fermeture dans le même bloc de rendu
    st.markdown("""
    <div class="input-section">
        <h3 style="margin-top:0;">📝 Entrée de données</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 1])
    with col1:
        numero = st.text_input("Numéro", placeholder="Ex: E001", key="numero_input")
    with col2:
        prenom = st.text_input("Prénom", placeholder="Ex: Jean Dupont", key="prenom_input")
    with col3:
        age = st.number_input("Âge", min_value=0, max_value=150, value=18, key="age_input")
    with col4:
        classe = st.text_input("Classe", placeholder="Ex: 1A", key="classe_input")
    with col5:
        moyenne = st.number_input("Moyenne", min_value=0.0, max_value=20.0, step=0.1, value=10.0, format="%.2f", key="moyenne_input")

st.markdown("---")

# Action buttons
st.markdown("### Actions")
b1, b2, b3, b4, b5 = st.columns(5)

with b1:
    if st.button("➕ Ajouter", use_container_width=True):
        if not numero:
            st.error("❌ Le champ Numéro est requis.")
        elif not prenom:
            st.error("❌ Le champ Prénom est requis.")
        else:
            student = {
                "numero": numero, 
                "prenom": prenom, 
                "age": int(age), 
                "classe": classe, 
                "moyenne": float(moyenne)
            }
            res = insert_student(student)
            if res.get("success"):
                st.success(f"✅ Étudiant '{prenom}' (#{numero}) ajouté avec succès!")
                st.balloons()
                st.session_state.show_list = True  # Forcer le rafraîchissement de la liste si elle était ouverte
            else:
                error_msg = res.get("error", "Erreur lors de l'ajout")
                st.error(f"❌ Erreur : {error_msg}")

with b2:
    if st.button("🔍 Rechercher", use_container_width=True):
        if not numero:
            st.error("❌ Entrez le numéro à rechercher.")
        else:
            doc = find_student_by_numero(numero)
            if doc:
                st.session_state.search_result = doc
            else:
                st.session_state.search_result = None
                st.warning(f"⚠️ Aucun étudiant avec le numéro '{numero}'.")

with b3:
    if st.button("✏️ Modifier", use_container_width=True):
        if not numero:
            st.error("❌ Numéro requis pour modifier.")
        else:
            update_fields = {}
            if prenom:
                update_fields["prenom"] = prenom
            if age is not None:
                update_fields["age"] = int(age)
            if classe:
                update_fields["classe"] = classe
            update_fields["moyenne"] = float(moyenne)
            
            res = update_student(numero, update_fields)
            if res.get("matched"):
                st.success(f"✅ Étudiant #{numero} modifié ({res.get('modified')} champ(s) mis à jour).")
                if st.session_state.search_result and st.session_state.search_result['numero'] == numero:
                    st.session_state.search_result = find_student_by_numero(numero) # Mettre à jour la recherche visuelle
            else:
                st.warning(f"⚠️ Aucun étudiant trouvé avec le numéro '{numero}'.")

with b4:
    if st.button("🗑️ Supprimer", use_container_width=True):
        if not numero:
            st.error("❌ Numéro requis pour supprimer.")
        else:
            res = delete_student(numero)
            if res.get("deleted"):
                st.success(f"✅ Étudiant #{numero} supprimé.")
                st.session_state.search_result = None
            else:
                st.warning(f"⚠️ Aucun étudiant trouvé avec le numéro '{numero}'.")

with b5:
    # Le bouton bascule (toggle) simplement l'état d'affichage de la liste
    if st.button("📋 Voir/Masquer la liste", use_container_width=True):
        st.session_state.show_list = not st.session_state.show_list

# --- ZONE D'AFFICHAGE DES RÉSULTATS (Persistants grâce au Session State) ---

# Affichage du résultat de la recherche
if st.session_state.search_result:
    st.info("✅ Étudiant trouvé :")
    df_single = pd.DataFrame([st.session_state.search_result])
    # Optionnel : masquer l'id MongoDB de l'affichage s'il existe
    if '_id' in df_single.columns:
        df_single = df_single.drop(columns=['_id'])
    st.dataframe(df_single, use_container_width=True, hide_index=True)

# Affichage de la liste complète
if st.session_state.show_list:
    rows = list_students()
    if not rows:
        st.info("ℹ️ Aucun étudiant enregistré pour le moment.")
    else:
        st.subheader(f"📊 Liste des étudiants ({len(rows)} total)")
        df = pd.DataFrame(rows)
        if '_id' in df.columns:
            df = df.drop(columns=['_id'])
            
        df = df.sort_values(by=["numero"])
        df["Moyenne"] = df["moyenne"].apply(lambda x: f"{x:.2f}/20")
        df_display = df[["numero", "prenom", "age", "classe", "Moyenne"]].rename(columns={
            "numero": "N°",
            "prenom": "Prénom",
            "age": "Âge",
            "classe": "Classe",
            "Moyenne": "Moy."
        })
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Statistiques
        if len(df) > 0:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total étudiants", len(df))
            with col2:
                st.metric("Âge moyen", f"{df['age'].mean():.1f} ans")
            with col3:
                st.metric("Moyenne générale", f"{df['moyenne'].mean():.2f}/20")
            with col4:
                st.metric("Classe(s)", df['classe'].nunique())

st.markdown("---")
st.caption("🎨 Conçu avec Streamlit | 📦 Base de données: MongoDB" if use_mongodb else "🎨 Conçu avec Streamlit | 📦 Base de données: SQLite")