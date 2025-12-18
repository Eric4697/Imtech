# 🚀 Guide d'Installation et de Démarrage

## Installation Rapide

### Étape 1 : Extraire l'archive
```bash
unzip malagasy-editor.zip
cd malagasy-editor
```

### Étape 2 : Créer un environnement virtuel (recommandé)

**Sur Linux/Mac :**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Sur Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

### Étape 3 : Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 4 : Lancer l'application
```bash
python app.py
```

### Étape 5 : Ouvrir dans le navigateur
```
http://localhost:5000
```

## ✅ Vérification de l'Installation

Si tout fonctionne, vous devriez voir :
- ✅ Message "Running on http://127.0.0.1:5000"
- ✅ Page web avec l'éditeur et les outils IA sur le côté
- ✅ Possibilité d'écrire du texte et d'utiliser les fonctionnalités

## 🛠️ Résolution de Problèmes

### Erreur : "Module not found"
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Erreur : Port 5000 déjà utilisé
Modifiez `app.py` ligne finale :
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Changez 5000 en 8080
```

### Erreur TTS (gTTS)
Si la synthèse vocale ne fonctionne pas :
- Vérifiez votre connexion internet
- gTTS nécessite un accès à Google

## 📝 Premier Test

1. Cliquez sur "Exemple" pour charger du texte
2. Testez chaque outil IA de la barre latérale
3. Vérifiez que tout fonctionne

## 🎥 Démonstration Vidéo

Pour créer votre vidéo de présentation (3 min max) :

1. **Montrer l'interface** (15 sec)
2. **Démontrer chaque fonctionnalité IA** (2 min) :
   - Correcteur orthographique
   - Autocomplétion
   - Traduction
   - Sentiment
   - Lemmatisation
   - Entités nommées
   - Synthèse vocale
3. **Expliquer les stratégies Low Resource** (30 sec)
4. **Architecture technique** (15 sec)

## 🎯 Points Clés à Mentionner

- ✅ 7 modules IA fonctionnels
- ✅ Approche hybride (symbolique + data-driven)
- ✅ Gestion intelligente du manque de données
- ✅ Interface utilisateur intuitive
- ✅ Technologies modernes (Flask, Quill.js)

Bon courage ! 🇲🇬
