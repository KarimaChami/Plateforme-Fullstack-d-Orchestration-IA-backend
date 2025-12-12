# Plateforme-Fullstack-d-Orchestration-IA



# Backend

## 📋 Description

Backend Python pour l'orchestration de services d'IA permettant la classification Zero-Shot (Hugging Face) et la synthèse contextuelle (Gemini API).

##  Architecture

```
backend/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py            # Modèles SQLAlchemy
│   │   └── analyze.py   
│   ├── routes/
│   │   ├── __init__.py
│   │   └── auth.py            # Routes d'authentification
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── gemini_client.py          
│   │   └── hf_client.py   
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée FastAPI
│   ├── config.py               # Configuration et variables d'environnement  
│   └── database.py           
├── tests/
│   ├── __init__.py
│   ├── gemi_test.py
│   └── hf_test.py
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

## 🚀 Installation

### Prérequis

- Python 
- PostgreSQL 
- Clés API : Hugging Face & Google Gemini

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone https://github.com/KarimaChami/Plateforme-Fullstack-d-Orchestration-IA-backend.git
cd ./backend
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
venv\Scripts\activate   
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
cp .env.example .env
```

5. **Initialiser la base de données**
```bash
python -m app.database init
```

6. **Lancer le serveur**
```bash
uvicorn app.main:app --reload 
```

## 📡 API Endpoints

### Authentification

#### POST /register
Créer un nouveau compte utilisateur.

**Request:**
```json
{
  "username": "john_doe",
  "password": "SecureP@ssw0rd"
}
```

**Response:**
```json
{
  "message": "User created successfully",
  "user_id": 1
}
```

#### POST /login
Se connecter et obtenir un token JWT.

**Request:**
```json
{
  "username": "john_doe",
  "password": "SecureP@ssw0rd"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Analyse

#### POST /analyze
Analyser un texte (requiert authentification JWT).

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "text": "Le marché boursier a connu une forte hausse aujourd'hui..."
}
```

**Response:**
```json
{
  "category": "Finance",
  "score": 0.92,
  "summary": "Analyse positive des marchés financiers montrant une tendance haussière avec des volumes d'échanges élevés.",
  "tone": "positif"
}
```

## 🔧 Configuration des Services IA

### Hugging Face

Le service utilise le modèle `facebook/bart-large-mnli` pour la classification Zero-Shot.

**Catégories supportées:**
- Finance
- Ressources Humaines
- Technologies de l'Information
- Opérations
- Marketing
- Juridique
- Sales
- Legal
- Support
- Logistique


### Gemini

Prompt Engineering pour une synthèse contextualisée :

```python
prompt = f"""
Tu dois OBLIGATOIREMENT répondre en JSON strict.
Aucun texte hors du JSON.
Même si le texte est court, donne un résumé et un ton.

Répond EXACTEMENT comme ceci :

{{
    "summary": "...",
    "tone": "positif" 
}}

Texte : {text}
"""
```

## 🧪 Tests

### Lancer tous les tests
```bash
pytest
```

### Tests spécifiques
```bash
pytest tests/hf_test.py -v
pytest tests/gemi_test.py -v
```

### Structure des tests

- **hf_test.py** : Tests de l'intégration HF
- **gemi_test.py** : Tests de l'intégration Gemini

## 📊 Logs

Les logs sont configurés dans `app/utils/logger.py` et incluent :

- **INFO** : Requêtes API, orchestration des services
- **WARNING** : Scores de classification faibles, timeouts
- **ERROR** : Erreurs critiques, échecs d'API
- **DEBUG** : Détails techniques (mode développement uniquement)


## 🔒 Sécurité

### JWT
- Token signé avec HS256
- Expiration configurable (défaut: 30 minutes)
- Validation sur tous les endpoints protégés

### Passwords
- Hashage avec argon2
- Validation de la complexité minimale
- Jamais stockés en clair

### API Keys
- Stockées dans variables d'environnement
- Jamais commitées dans le code
- Rotation régulière recommandée

## 🐳 Docker

### Build de l'image
```bash
docker build -t backend .
```

### Lancer avec Docker Compose
```bash
docker-compose up -d
```

## 🛠️ Dépendances principales

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
requests==2.31.0
python-dotenv==1.0.0
google-generativeai==0.3.1
pytest==7.4.3
pytest-cov==4.1.0
```

## 🚨 Gestion des erreurs

### Erreurs courantes

| Code | Description | Solution |
|------|-------------|----------|
| 401 | Non autorisé | Vérifier le token JWT |
| 422 | Validation échouée | Vérifier le format de la requête |
| 500 | Erreur serveur | Consulter les logs |
| 503 | Service indisponible | API externe down (HF/Gemini) |


## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request


## 👥 Auteurs

- Karima Chami - Dévloppeuse Fullstack & Ai

## 🔗 Liens utiles

- [Documentation Hugging Face Inference API](https://huggingface.co/docs/api-inference/index)
- [Documentation Gemini API](https://ai.google.dev/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)