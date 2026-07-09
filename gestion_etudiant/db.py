from pymongo import MongoClient, errors
from pathlib import Path

# URI de connexion (Modifier si vous utilisez MongoDB Atlas)
MONGO_URI = "mongodb://localhost:27017/"

# Initialisation du client MongoDB
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    # Forcer une connexion pour vérifier si le serveur est actif
    client.server_info() 
    
    # Définition de la base de données et de la collection
    db = client["gestion_etudiants_db"]
    collection = db["etudiants"]
    use_mongodb = True
except errors.ServerSelectionTimeoutError:
    # Au cas où MongoDB n'est pas lancé, on lève une alerte claire
    print("❌ Impossible de se connecter à MongoDB. Assurez-vous que le service est lancé.")
    use_mongodb = False

# 1. Ajouter un étudiant
def insert_student(student):
    if not use_mongodb:
        return {"success": False, "error": "Base de données MongoDB indisponible."}
    
    try:
        # On vérifie d'abord si le numéro d'étudiant (unique) existe déjà
        if collection.find_one({"numero": student["numero"]}):
            return {"success": False, "error": "Ce numéro d'étudiant existe déjà."}
        
        # Insertion dans MongoDB
        collection.insert_one(student)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

# 2. Rechercher un étudiant par son numéro
def find_student_by_numero(numero):
    if not use_mongodb:
        return None
    
    # MongoDB ajoute un champ '_id' de type ObjectId qui fait planter l'affichage Pandas.
    # On l'exclut de la recherche en utilisant la projection { "_id": 0 }
    student = collection.find_one({"numero": numero}, {"_id": 0})
    return student

# 3. Modifier un étudiant
def update_student(numero, update_fields):
    if not use_mongodb:
        return {"matched": 0, "modified": 0}
    
    try:
        # Dans MongoDB, les modifications se font via l'opérateur $set
        result = collection.update_one(
            {"numero": numero},
            {"$set": update_fields}
        )
        return {
            "matched": result.matched_count,
            "modified": result.modified_count
        }
    except Exception as e:
        print(f"Erreur lors de la modification : {e}")
        return {"matched": 0, "modified": 0}

# 4. Supprimer un étudiant
def delete_student(numero):
    if not use_mongodb:
        return {"deleted": False}
    
    result = collection.delete_one({"numero": numero})
    return {"deleted": result.deleted_count > 0}

# 5. Lister tous les étudiants
def list_students():
    if not use_mongodb:
        return []
    
    # On récupère tous les documents en excluant le champ '_id' pour Streamlit
    students_cursor = collection.find({}, {"_id": 0})
    return list(students_cursor)