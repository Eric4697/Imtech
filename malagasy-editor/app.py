"""
Éditeur de Texte Augmenté par l'IA pour le Malagasy
Application Flask principale
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from modules.spell_checker import SpellChecker
from modules.autocomplete import AutoComplete
from modules.translator import Translator
from modules.sentiment_analyzer import SentimentAnalyzer
from modules.lemmatizer import Lemmatizer
from modules.ner import NamedEntityRecognizer
from modules.tts import TextToSpeech

app = Flask(__name__)
CORS(app)

# Initialisation des modules IA
spell_checker = SpellChecker()
autocomplete = AutoComplete()
translator = Translator()
sentiment_analyzer = SentimentAnalyzer()
lemmatizer = Lemmatizer()
ner = NamedEntityRecognizer()
tts = TextToSpeech()

@app.route('/')
def index():
    """Page principale de l'éditeur"""
    return render_template('index.html')

@app.route('/api/check-spelling', methods=['POST'])
def check_spelling():
    """Vérifie l'orthographe d'un mot"""
    data = request.get_json()
    word = data.get('word', '')
    
    result = spell_checker.check(word)
    return jsonify(result)

@app.route('/api/autocomplete', methods=['POST'])
def get_autocomplete():
    """Suggestions de mots suivants"""
    data = request.get_json()
    context = data.get('context', '')
    
    suggestions = autocomplete.predict_next_word(context)
    return jsonify({'suggestions': suggestions})

@app.route('/api/translate', methods=['POST'])
def translate_word():
    """Traduit un mot malagasy vers français"""
    data = request.get_json()
    word = data.get('word', '')
    
    translation = translator.translate(word)
    return jsonify({'translation': translation})

@app.route('/api/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyse le sentiment d'un texte"""
    data = request.get_json()
    text = data.get('text', '')
    
    sentiment = sentiment_analyzer.analyze(text)
    return jsonify(sentiment)

@app.route('/api/lemmatize', methods=['POST'])
def lemmatize_word():
    """Trouve la racine d'un mot"""
    data = request.get_json()
    word = data.get('word', '')
    
    lemma = lemmatizer.get_lemma(word)
    return jsonify({'lemma': lemma})

@app.route('/api/extract-entities', methods=['POST'])
def extract_entities():
    """Extrait les entités nommées"""
    data = request.get_json()
    text = data.get('text', '')
    
    entities = ner.extract(text)
    return jsonify({'entities': entities})

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    """Génère l'audio du texte"""
    data = request.get_json()
    text = data.get('text', '')
    
    audio_url = tts.generate(text)
    return jsonify({'audio_url': audio_url})

@app.route('/api/validate-phonetics', methods=['POST'])
def validate_phonetics():
    """Valide les règles phonotactiques malagasy"""
    data = request.get_json()
    word = data.get('word', '')
    
    is_valid, errors = spell_checker.validate_phonetics(word)
    return jsonify({
        'is_valid': is_valid,
        'errors': errors
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
