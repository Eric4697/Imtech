"""
Module d'autocomplétion basé sur les N-grams
Prédit le mot suivant basé sur le contexte
"""
import json
import os
from collections import defaultdict, Counter
import re

class AutoComplete:
    def __init__(self, n=3):
        """
        Initialise le module d'autocomplétion
        n: taille du n-gram (par défaut trigram)
        """
        self.n = n
        self.ngrams = self._load_ngrams()
        self.word_freq = self._load_word_frequencies()
    
    def _load_ngrams(self):
        """Charge le modèle n-gram pré-calculé"""
        ngrams_path = os.path.join('data', 'ngrams.json')
        
        if os.path.exists(ngrams_path):
            with open(ngrams_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Modèle de base si le fichier n'existe pas
        return {
            ('ny',): {'trano': 5, 'tanana': 4, 'vary': 3, 'rano': 3},
            ('ny', 'trano'): {'lehibe': 3, 'kely': 2, 'tsara': 2},
            ('tsara', 'fanahy'): {'dia': 2, 'sy': 1},
            ('misy',): {'olona': 4, 'zavatra': 3, 'fotoana': 2},
            ('manao',): {'ahoana': 10, 'inona': 5, 'asa': 3},
            ('manao', 'ahoana'): {'ianao': 8, 'ry': 6, 'hianareo': 3},
            ('misaotra',): {'betsaka': 6, 'indrindra': 4, 'anao': 3},
            ('tonga',): {'soa': 5, 'eto': 4, 'any': 2},
            ('tonga', 'soa'): {'amin': 3, 'ianareo': 2},
            ('faly',): {'aho': 3, 'isika': 2, 'izy': 2},
            ('miteny',): {'malagasy': 6, 'frantsay': 3, 'anglisy': 2},
            ('mandeha',): {'any': 4, 'amin': 3, 'ho': 2},
            ('mihinana',): {'vary': 5, 'sakafo': 4, 'mofo': 2},
            ('fihavanana',): {'malagasy': 4, 'dia': 2, 'no': 2}
        }
    
    def _load_word_frequencies(self):
        """Charge les fréquences de mots"""
        freq_path = os.path.join('data', 'word_frequencies.json')
        
        if os.path.exists(freq_path):
            with open(freq_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Fréquences de base
        return {
            'ny': 100, 'sy': 80, 'amin': 70, 'dia': 65, 'fa': 60,
            'no': 55, 'tsy': 50, 'aho': 45, 'izy': 45, 'ianao': 40,
            'ho': 38, 'amin\'ny': 35, 'izany': 33, 'any': 30, 'eto': 28,
            'malagasy': 50, 'trano': 25, 'vary': 24, 'rano': 23,
            'fihavanana': 22, 'tsara': 30, 'ratsy': 15, 'lehibe': 20,
            'manao': 35, 'mihinana': 28, 'misotro': 26, 'miteny': 24,
            'ahoana': 32, 'inona': 30, 'aiza': 28, 'oviana': 20,
            'iza': 25, 'nahoana': 22, 'firy': 18
        }
    
    def predict_next_word(self, context, max_suggestions=5):
        """
        Prédit les mots suivants possibles basés sur le contexte
        
        Args:
            context: chaîne de texte (les derniers mots)
            max_suggestions: nombre maximum de suggestions
        
        Returns:
            liste de suggestions triées par probabilité
        """
        # Tokeniser et nettoyer le contexte
        tokens = self._tokenize(context)
        
        if not tokens:
            return self._get_most_frequent_words(max_suggestions)
        
        # Prendre les derniers (n-1) mots pour le n-gram
        context_key = tuple(tokens[-(self.n-1):])
        
        # Chercher les correspondances exactes
        predictions = self._find_predictions(context_key)
        
        # Si pas de correspondance exacte, essayer avec moins de contexte
        if not predictions and len(context_key) > 1:
            context_key = tuple(tokens[-1:])
            predictions = self._find_predictions(context_key)
        
        # Si toujours pas de prédiction, retourner les mots les plus fréquents
        if not predictions:
            return self._get_most_frequent_words(max_suggestions)
        
        # Trier par fréquence et retourner
        sorted_predictions = sorted(
            predictions.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return [word for word, _ in sorted_predictions[:max_suggestions]]
    
    def _tokenize(self, text):
        """Tokenise le texte en mots"""
        # Nettoyer et tokeniser
        text = text.lower().strip()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens
    
    def _find_predictions(self, context_key):
        """Trouve les prédictions pour une clé de contexte"""
        # Convertir le tuple en chaîne pour la recherche JSON
        key_str = str(context_key)
        
        # Chercher dans le dictionnaire
        for key, value in self.ngrams.items():
            if isinstance(key, str):
                # Convertir la clé string en tuple pour comparaison
                try:
                    key_tuple = eval(key)
                except:
                    continue
            else:
                key_tuple = key
            
            if key_tuple == context_key:
                return value
        
        return {}
    
    def _get_most_frequent_words(self, limit):
        """Retourne les mots les plus fréquents"""
        sorted_words = sorted(
            self.word_freq.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        return [word for word, _ in sorted_words[:limit]]
