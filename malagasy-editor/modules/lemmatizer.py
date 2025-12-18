"""
Module de lemmatisation pour le Malagasy
Trouve la racine d'un mot en retirant les préfixes et suffixes
"""
import re

class Lemmatizer:
    def __init__(self):
        """Initialise le lemmatiseur"""
        # Préfixes courants (ordonnés du plus long au plus court)
        self.prefixes = [
            'maha', 'mpam', 'mpan', 'mam', 'man', 'fam', 'fan', 'mi', 'ma', 'fi', 'f'
        ]
        
        # Suffixes courants (ordonnés du plus long au plus court)
        self.suffixes = [
            'ana', 'ina', 'na', 'a'
        ]
        
        # Règles spéciales pour certains verbes irréguliers
        self.irregular_verbs = {
            'mandeha': 'lasa',
            'mipetraka': 'petraka',
            'mihinana': 'hinana',
            'misotro': 'sotro',
            'mihira': 'hira',
            'miasa': 'asa',
            'manao': 'vita',
            'manosika': 'tosika'
        }
    
    def get_lemma(self, word):
        """
        Trouve la racine (lemme) d'un mot malagasy
        
        Args:
            word: mot à lemmatiser
        
        Returns:
            dictionnaire avec le lemme et les informations de décomposition
        """
        word_lower = word.lower().strip()
        
        # Vérifier les verbes irréguliers
        if word_lower in self.irregular_verbs:
            return {
                'lemma': self.irregular_verbs[word_lower],
                'original': word_lower,
                'prefix': None,
                'suffix': None,
                'type': 'irregular'
            }
        
        # Essayer de décomposer le mot
        prefix_found = None
        suffix_found = None
        root = word_lower
        
        # Retirer le préfixe
        for prefix in self.prefixes:
            if word_lower.startswith(prefix):
                prefix_found = prefix
                root = word_lower[len(prefix):]
                break
        
        # Retirer le suffixe
        if root:
            for suffix in self.suffixes:
                if root.endswith(suffix) and len(root) > len(suffix):
                    suffix_found = suffix
                    root = root[:-len(suffix)]
                    break
        
        # Si aucune décomposition n'a été trouvée
        if not prefix_found and not suffix_found:
            return {
                'lemma': word_lower,
                'original': word_lower,
                'prefix': None,
                'suffix': None,
                'type': 'base'
            }
        
        return {
            'lemma': root,
            'original': word_lower,
            'prefix': prefix_found,
            'suffix': suffix_found,
            'type': 'derived'
        }
    
    def analyze_morphology(self, word):
        """
        Analyse morphologique détaillée d'un mot
        
        Returns:
            informations sur la structure du mot
        """
        lemma_info = self.get_lemma(word)
        
        # Déterminer la catégorie grammaticale probable
        category = self._guess_category(lemma_info)
        
        return {
            **lemma_info,
            'category': category,
            'analysis': self._generate_analysis(lemma_info)
        }
    
    def _guess_category(self, lemma_info):
        """Devine la catégorie grammaticale basée sur les affixes"""
        prefix = lemma_info['prefix']
        suffix = lemma_info['suffix']
        
        # Verbes actifs
        if prefix in ['mi', 'man', 'mam', 'mpan', 'mpam']:
            return 'verbe_actif'
        
        # Verbes causatifs
        if prefix == 'maha':
            return 'verbe_causatif'
        
        # Noms dérivés
        if prefix in ['fi', 'fan', 'fam', 'f']:
            return 'nom_dérivé'
        
        # Formes passives/circonstancielles
        if suffix in ['ana', 'ina']:
            return 'forme_passive_circonstancielle'
        
        # Adjectifs/Noms simples
        if prefix == 'ma':
            return 'adjectif_stative'
        
        return 'base_word'
    
    def _generate_analysis(self, lemma_info):
        """Génère une explication textuelle de la décomposition"""
        if lemma_info['type'] == 'irregular':
            return f"Verbe irrégulier : '{lemma_info['original']}' → racine '{lemma_info['lemma']}'"
        
        if lemma_info['type'] == 'base':
            return f"Mot de base (pas de décomposition) : '{lemma_info['original']}'"
        
        parts = []
        if lemma_info['prefix']:
            parts.append(f"préfixe '{lemma_info['prefix']}'")
        parts.append(f"racine '{lemma_info['lemma']}'")
        if lemma_info['suffix']:
            parts.append(f"suffixe '{lemma_info['suffix']}'")
        
        return f"Décomposition : {' + '.join(parts)}"
