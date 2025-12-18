# Éditeur de Texte Augmenté par l'IA pour le Malagasy
# membre du groupe
-**RASOLOFOARIJAONA Eric IMTIC5A n°02**


## 🎯 Description

Application web intelligente pour l'édition de texte en langue malagasy, intégrant plusieurs modules d'Intelligence Artificielle pour pallier le manque de ressources numériques pour cette langue.

## 🚀 Fonctionnalités IA Implémentées

### 1. 📝 Correcteur Orthographique
- **Distance de Levenshtein** : Utilisation de `rapidfuzz` pour trouver les suggestions de mots similaires
- **Validation Phonotactique** : Règles basées sur REGEX pour détecter les combinaisons interdites en malagasy (nb, mk, dt, bp, sz)
- **Dictionnaire** : Base de données de mots malagasy courants

### 2. ✨ Autocomplétion (Next Word Prediction)
- **Modèle N-grams** : Prédiction du mot suivant basée sur le contexte
- **Fréquence des mots** : Suggestions basées sur la fréquence d'utilisation
- **Activation/Désactivation** : Toggle pour activer/désactiver l'autocomplétion en temps réel

### 3. 🌐 Traducteur Mot-à-Mot
- **Dictionnaire Bidirectionnel** : Malagasy ↔ Français
- **Traduction au clic droit** : Sélectionnez un mot et faites un clic droit pour voir sa traduction
- **Plus de 100 mots** : Couvre le vocabulaire de base et culturel

### 4. 😊 Analyse de Sentiment
- **Bag of Words** : Classification basée sur des listes de mots positifs/négatifs
- **Gestion des négations** : Détecte "tsy" et inverse le sentiment
- **Intensificateurs** : Reconnaît les mots comme "be", "indrindra" qui amplifient le sentiment
- **Score et confiance** : Retourne un score de -1 à +1 et un niveau de confiance

### 5. 🌳 Lemmatisation
- **Décomposition morphologique** : Retire les préfixes (mi-, ma-, man-, maha-, etc.) et suffixes (-ana, -ina, -na)
- **Racine du mot** : Trouve le radical (ex: manosika → tosika)
- **Verbes irréguliers** : Base de données pour les cas spéciaux
- **Catégorisation grammaticale** : Devine la catégorie (verbe, nom, adjectif)

### 6. 🏷️ Reconnaissance d'Entités Nommées (NER)
- **Villes** : Détecte les villes malgaches (Antananarivo, Antsirabe, Toamasina, etc.)
- **Régions** : Reconnaît les 22 régions de Madagascar
- **Personnalités** : Identifie les figures historiques et contemporaines
- **Organisations** : Détecte les institutions malgaches

### 7. 🔊 Synthèse Vocale (TTS)
- **Google TTS** : Utilise `gTTS` avec support de la langue malagasy
- **Lecture sélective** : Lit le texte sélectionné ou tout le document
- **Cache audio** : Stocke les fichiers générés pour éviter les doublons

## 🛠️ Technologies Utilisées

### Backend
- **Flask** : Framework web Python
- **rapidfuzz** : Algorithme de distance de Levenshtein rapide
- **gTTS** : Google Text-to-Speech
- **Flask-CORS** : Gestion des requêtes cross-origin

### Frontend
- **Quill.js** : Éditeur de texte riche WYSIWYG
- **Vanilla JavaScript** : Pas de framework lourd, performance optimale
- **CSS3** : Design moderne et responsive
- **Font Awesome** : Icônes

### Approches IA
- **Symbolique** : Règles phonotactiques, décomposition morphologique
- **Algorithmique** : Distance de Levenshtein, N-grams, Bag of Words
- **Data-driven** : Dictionnaires, fréquences de mots, modèles N-grams

## 📦 Installation

### Prérequis
- Python 3.8+
- pip

### Étapes

1. **Extraire l'archive**
```bash
unzip malagasy-editor.zip
cd malagasy-editor
```

2. **Créer un environnement virtuel** (recommandé)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\\Scripts\\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application**
```bash
python app.py
```

5. **Ouvrir dans le navigateur**
```
http://localhost:5000
```

## 📖 Utilisation

### Interface Utilisateur

#### Zone d'Édition
- Éditeur de texte riche avec formatage (gras, italique, listes, etc.)
- Compteurs en temps réel : mots, caractères, lignes

#### Barre Latérale (Outils IA)

1. **Correcteur Orthographique**
   - Écrivez du texte
   - Cliquez sur "Vérifier"
   - Les erreurs sont détectées et affichées

2. **Autocomplétion**
   - Activée par défaut
   - Suggestions automatiques pendant la frappe
   - Toggle pour activer/désactiver

3. **Traducteur**
   - Sélectionnez un mot
   - Clic droit ou regardez la barre latérale
   - La traduction s'affiche

4. **Analyse Sentiment**
   - Écrivez un texte
   - Cliquez sur "Analyser"
   - Voir le sentiment (positif/négatif/neutre) avec score

5. **Lemmatisation**
   - Entrez un mot dans le champ
   - Cliquez sur "Analyser"
   - Voir la racine et la décomposition

6. **Entités Nommées**
   - Écrivez du texte contenant des noms de lieux ou personnes
   - Cliquez sur "Extraire"
   - Les entités sont détectées (voir console)

7. **Synthèse Vocale**
   - Sélectionnez du texte ou laissez tout le document
   - Cliquez sur "Lire"
   - L'audio se joue automatiquement

### Boutons de l'Éditeur
- **Effacer** : Supprime tout le contenu
- **Sauvegarder** : Télécharge le texte en .txt
- **Exemple** : Charge un texte exemple en malagasy

## 🏗️ Architecture du Projet

```
malagasy-editor/
├── app.py                      # Application Flask principale
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation
├── modules/                    # Modules IA
│   ├── __init__.py
│   ├── spell_checker.py       # Correcteur orthographique
│   ├── autocomplete.py        # Autocomplétion N-grams
│   ├── translator.py          # Traducteur bidirectionnel
│   ├── sentiment_analyzer.py  # Analyse de sentiment
│   ├── lemmatizer.py          # Lemmatisation
│   ├── ner.py                 # Reconnaissance entités
│   └── tts.py                 # Synthèse vocale
├── templates/
│   └── index.html             # Template HTML principal
├── static/
│   ├── css/
│   │   └── style.css          # Styles CSS
│   ├── js/
│   │   └── app.js             # JavaScript frontend
│   └── audio/                 # Fichiers audio TTS (généré)
└── data/                      # Données linguistiques
    ├── dictionary.json        # Dictionnaire malagasy
    ├── ngrams.json            # Modèle N-grams
    ├── word_frequencies.json  # Fréquences de mots
    └── translations.json      # Traductions MG-FR
```

## 🎓 Stratégies pour Contourner le Manque de Données

### 1. Approche Hybride
- **Symbolique** : Règles linguistiques codées en dur (phonotactique, morphologie)
- **Statistique** : Modèles simples (N-grams, fréquences) sur petits corpus
- **Dictionnaires** : Compilation manuelle de vocabulaire essentiel

### 2. Règles Linguistiques
- Exploitation des patterns réguliers du malagasy
- Préfixes/suffixes pour la lemmatisation
- Combinaisons phonotactiques interdites

### 3. Transfert de Connaissances
- Utilisation de gTTS (Google) pour la synthèse vocale
- Traduction basée sur dictionnaires plutôt que modèles neuronaux

### 4. Corpus Minimaux
- Bible, articles Wikipedia MG
- Vocabulaire culturel et géographique spécifique
- Focus sur qualité plutôt que quantité

## 👥 Équipe et Rôles

**Développeur Full-Stack IA**
- Architecture complète
- Implémentation des 7 modules IA
- Design UI/UX
- Documentation

## 📚 Bibliographie

### Sources de Données
- [Wikipedia Malagasy](https://mg.wikipedia.org) - Corpus de textes modernes
- [Teny Malagasy](https://tenymalagasy.org) - Dictionnaire en ligne
- Bible Protestante Malagasy - Corpus textuel

### Documentation Technique
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Quill.js Documentation](https://quilljs.com/docs/)
- [rapidfuzz Documentation](https://github.com/maxbachmann/RapidFuzz)
- [gTTS Documentation](https://gtts.readthedocs.io/)

### Références Linguistiques
- Rajaonarimanana, N. (2001). "Grammaire moderne de la langue malgache"
- Abinal & Malzac - "Dictionnaire malgache-français"

### Articles et Ressources
- "Low Resource Languages: A Review of Past Work and Future Challenges"
- "N-gram Language Models for Low Resource Languages"
- Règles phonotactiques du malagasy (INALCO)

## 🚧 Améliorations Futures

1. **Scraping Automatique**
   - Crawler pour Wikipedia MG
   - Extraction de corpus depuis tenymalagasy.org

2. **Modèles Plus Sophistiqués**
   - Word embeddings (Word2Vec) sur corpus malagasy
   - Fine-tuning de modèles multilingues (mBERT)

3. **Graphe de Connaissances**
   - Ontologie malagasy (famille, culture, géographie)
   - Suggestions sémantiques

4. **Conjugaison Interactive**
   - Assistant pour conjuguer les verbes
   - Règles de formation des mots

5. **Mode Collaboratif**
   - Édition multi-utilisateurs
   - Contribution communautaire au dictionnaire

## 📄 Licence

Projet académique - INSTITUT SUPERIEUR POLYTECHNIQUE DE MADAGASCAR

## 🙏 Remerciements

Merci aux communautés qui maintiennent les ressources malagasy en ligne et aux développeurs des outils open-source utilisés.

---

**Soyez ambitieux. Créez l'outil que Madagascar attend !** 🇲🇬
