# Gestion des étudiants (Streamlit + MongoDB)

Courte application Web pour gérer des étudiants (numéro, prénom, âge, classe, moyenne) avec Streamlit et MongoDB.

Prérequis
- Python 3.8+
- MongoDB local ou cloud (URI via `MONGODB_URI`)

Installation

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Démarrage

```bash
set MONGODB_URI="mongodb://localhost:27017"
streamlit run app.py
```

Remarques
- Le champ `numéro` est utilisé comme identifiant unique.
- Pour une base MongoDB Atlas, exportez votre URI et placez-le dans la variable d'environnement `MONGODB_URI`.
# Gestion des étudiants (Streamlit + MongoDB)

Application minimale de gestion des étudiants avec Streamlit en frontend et MongoDB en backend.

Champs: `numero`, `prenom`, `age`, `classe`, `moyenne`.

Commandes:

- Installer dépendances:

```
pip install -r requirements.txt
```

- Lancer l'application:

```
streamlit run app.py
```

Si vous utilisez une base distante setez `MONGO_URI` avant de lancer, exemple:

Windows (cmd):

```
set MONGO_URI="mongodb+srv://<user>:<pass>@cluster0.mongodb.net"
streamlit run app.py
```

ou PowerShell:

```
$env:MONGO_URI = "mongodb+srv://<user>:<pass>@cluster0.mongodb.net"
streamlit run app.py
```
