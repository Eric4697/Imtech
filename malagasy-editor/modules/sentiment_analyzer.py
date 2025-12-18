"""
Module d'analyse de sentiment pour le Malagasy
Utilise un dictionnaire de mots positifs/négatifs (Bag of Words)
"""
import json
import os
import re

class SentimentAnalyzer:
    def __init__(self):
        """Initialise l'analyseur de sentiment"""
        self.positive_words = self._load_positive_words()
        self.negative_words = self._load_negative_words()
        self.intensifiers = ['be', 'indrindra', 'loatra', 'tokoa', 'mihitsy']
        self.negations = ['tsy', 'tsia']
    
    def _load_positive_words(self):
        """Charge les mots positifs"""
        return set([
            'tsara', 'faly', 'sambatra', 'mahafinaritra', 'tsara tarehy',
            'mendrika', 'mahay', 'hendry', 'marina', 'tsara fanahy',
            'be fitiavana', 'mahafaly', 'mahagaga', 'mahaliana',
            'fahasoavana', 'fiadanana', 'fitiavana', 'fahafaham-po',
            'fahombiazana', 'tanjona', 'soa', 'tonga soa', 'misaotra',
            'mahazatra', 'manam-pahaizana', 'mahomby', 'matanjaka',
            'fotsy', 'madio', 'manitra', 'mamy', 'tsara feo',
            'salama', 'fahasalamana', 'hafaliana', 'fihobiana',
            'fameperana', 'tombontsoa', 'manan-danja', 'sarobidy',
            'mendrika', 'mahafinaritra', 'manintona', 'mahavita'
        ])
    
    def _load_negative_words(self):
        """Charge les mots négatifs"""
        return set([
            'ratsy', 'malahelo', 'malahelo be', 'mahonena', 'tsy tsara',
            'mampalahelo', 'mahatsikaiky', 'mahasosotra', 'diso',
            'tsy marina', 'mahadiso', 'mampidi-doza', 'mampatahotra',
            'mampitebiteby', 'manahirana', 'sarotra', 'mora voan',
            'malemy', 'maharary', 'marary', 'manaintaina', 'maizina',
            'maloto', 'maimbo', 'mangidy', 'maditra', 'mahamenatra',
            'mahonena', 'kivy', 'latsaka', 'very', 'tapaka',
            'simba', 'tsy misy', 'tsy azo', 'tsy hay', 'tsy vita',
            'fahatezerana', 'hatezerana', 'fahavinirana', 'faniratsirana',
            'fahadisoana', 'tsy fahaizana', 'tsy fahombiazana'
        ])
    
    def analyze(self, text):
        """
        Analyse le sentiment d'un texte
        
        Returns:
            dictionnaire avec score et classification
        """
        # Nettoyer et tokeniser
        tokens = self._tokenize(text)
        
        if not tokens:
            return {
                'sentiment': 'neutre',
                'score': 0,
                'confidence': 0,
                'positive_count': 0,
                'negative_count': 0,
                'details': []
            }
        
        # Compter les mots positifs et négatifs
        positive_count = 0
        negative_count = 0
        details = []
        
        for i, token in enumerate(tokens):
            # Vérifier si le mot est précédé d'une négation
            is_negated = (i > 0 and tokens[i-1] in self.negations)
            
            # Vérifier si le mot est suivi d'un intensificateur
            intensifier_boost = 1
            if i < len(tokens) - 1 and tokens[i+1] in self.intensifiers:
                intensifier_boost = 1.5
            
            if token in self.positive_words:
                if is_negated:
                    negative_count += intensifier_boost
                    details.append({
                        'word': token,
                        'base_type': 'positive',
                        'actual_effect': 'negative',
                        'reason': 'negated',
                        'weight': intensifier_boost
                    })
                else:
                    positive_count += intensifier_boost
                    details.append({
                        'word': token,
                        'type': 'positive',
                        'weight': intensifier_boost
                    })
            
            elif token in self.negative_words:
                if is_negated:
                    positive_count += intensifier_boost
                    details.append({
                        'word': token,
                        'base_type': 'negative',
                        'actual_effect': 'positive',
                        'reason': 'negated',
                        'weight': intensifier_boost
                    })
                else:
                    negative_count += intensifier_boost
                    details.append({
                        'word': token,
                        'type': 'negative',
                        'weight': intensifier_boost
                    })
        
        # Calculer le score (-1 à +1)
        total_count = positive_count + negative_count
        if total_count == 0:
            score = 0
            confidence = 0
        else:
            score = (positive_count - negative_count) / total_count
            confidence = min(total_count / len(tokens), 1.0)
        
        # Classifier le sentiment
        if score > 0.2:
            sentiment = 'positif'
        elif score < -0.2:
            sentiment = 'négatif'
        else:
            sentiment = 'neutre'
        
        return {
            'sentiment': sentiment,
            'score': round(score, 2),
            'confidence': round(confidence, 2),
            'positive_count': int(positive_count),
            'negative_count': int(negative_count),
            'details': details
        }
    
    def _tokenize(self, text):
        """Tokenise le texte"""
        text = text.lower().strip()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens
