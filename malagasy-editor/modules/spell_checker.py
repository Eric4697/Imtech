"""
Module de correction orthographique pour le Malagasy
Utilise la distance de Levenshtein et des règles phonotactiques
"""
import re
from rapidfuzz import fuzz, process
import json
import os

class SpellChecker:
    def __init__(self):
        """Initialise le correcteur orthographique"""
        self.dictionary = self._load_dictionary()
        
        # Règles phonotactiques malagasy - combinaisons interdites
        self.forbidden_patterns = [
            r'nb', r'mk', r'^nk', r'dt', r'bp', r'sz'
        ]
        
        # Préfixes courants
        self.prefixes = ['mi', 'ma', 'man', 'mam', 'maha', 'mpan', 'mpam', 'fi', 'fan', 'fam']
        
        # Suffixes courants
        self.suffixes = ['ana', 'ina', 'na']
    
    def _load_dictionary(self):
        """Charge le dictionnaire malagasy"""
        dict_path = os.path.join('data', 'dictionary.json')
        
        if os.path.exists(dict_path):
            with open(dict_path, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        
        # Dictionnaire de base si le fichier n'existe pas
        return set([
            'malagasy', 'teny', 'trano', 'vary', 'rano', 'fihavanana',
            'vahiny', 'tsara', 'ratsy', 'lehibe', 'kely', 'ankehitriny',
            'omaly', 'rahampitso', 'miaramila', 'mpanabe', 'mpianatra',
            'famadihana', 'razana', 'tanana', 'antsirabe', 'antananarivo',
            'toamasina', 'mahajanga', 'fianarantsoa', 'toliary', 'antsiranana',
            'manao', 'manosika', 'tosika', 'mihira', 'hira', 'miasa', 'asa',
            'mandeha', 'lasa', 'ho avy', 'mipetraka', 'mihinana', 'misotro',
            'miteny', 'manoratra', 'mamaky', 'mianatra', 'manabe', 'mikaroka',
            'mividy', 'mivarotra', 'mandoa', 'mandray', 'manome', 'mitondra',
            'sakafo', 'mofo', 'hena', 'voninkazo', 'legioma', 'voankazo',
            'fianakaviana', 'ray', 'reny', 'zanaka', 'anadahy', 'anabavy',
            'dadabe', 'nenibe', 'zafy', 'havana', 'namana', 'sakaizan',
            'fitiavana', 'fankasitrahana', 'fiadanana', 'fahasoavana',
            'tsara fanahy', 'be fitiavana', 'mahay', 'hendry', 'marina',
            'fahamarinana', 'rariny', 'fahamarinana', 'fahasoavana'
        ])
    
    def validate_phonetics(self, word):
        """
        Valide les règles phonotactiques du malagasy
        Retourne (is_valid, liste_erreurs)
        """
        word_lower = word.lower()
        errors = []
        
        for pattern in self.forbidden_patterns:
            if re.search(pattern, word_lower):
                errors.append(f"Combinaison interdite trouvée: {pattern}")
        
        return len(errors) == 0, errors
    
    def check(self, word):
        """
        Vérifie l'orthographe d'un mot
        Retourne un dictionnaire avec le statut et les suggestions
        """
        word_lower = word.lower()
        
        # Vérifier si le mot existe dans le dictionnaire
        if word_lower in self.dictionary:
            return {
                'correct': True,
                'suggestions': [],
                'phonetic_errors': []
            }
        
        # Vérifier les règles phonotactiques
        is_valid_phonetics, phonetic_errors = self.validate_phonetics(word)
        
        # Trouver les suggestions avec distance de Levenshtein
        suggestions = self._get_suggestions(word_lower)
        
        return {
            'correct': False,
            'suggestions': suggestions,
            'phonetic_errors': phonetic_errors,
            'phonetically_valid': is_valid_phonetics
        }
    
    def _get_suggestions(self, word, limit=5):
        """Trouve les suggestions basées sur la distance de Levenshtein"""
        if not self.dictionary:
            return []
        
        # Utiliser rapidfuzz pour trouver les mots similaires
        results = process.extract(
            word, 
            self.dictionary, 
            scorer=fuzz.ratio,
            limit=limit
        )
        
        # Filtrer les suggestions avec un score minimum de 70
        suggestions = [match[0] for match in results if match[1] >= 70]
        
        return suggestions
    
    def is_likely_malagasy(self, word):
        """
        Détermine si un mot est probablement malagasy
        basé sur les préfixes/suffixes courants
        """
        word_lower = word.lower()
        
        # Vérifier les préfixes
        for prefix in self.prefixes:
            if word_lower.startswith(prefix):
                return True
        
        # Vérifier les suffixes
        for suffix in self.suffixes:
            if word_lower.endswith(suffix):
                return True
        
        return False
