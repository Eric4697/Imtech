"""
Module de traduction Malagasy <-> Français
Utilise un dictionnaire bidirectionnel
"""
import json
import os

class Translator:
    def __init__(self):
        """Initialise le traducteur"""
        self.mg_to_fr = self._load_dictionary()
        self.fr_to_mg = {v: k for k, v in self.mg_to_fr.items()}
    
    def _load_dictionary(self):
        """Charge le dictionnaire malagasy-français"""
        dict_path = os.path.join('data', 'translations.json')
        
        if os.path.exists(dict_path):
            with open(dict_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Dictionnaire de base
        return {
            # Salutations et expressions courantes
            'salama': 'bonjour',
            'veloma': 'au revoir',
            'misaotra': 'merci',
            'misaotra betsaka': 'merci beaucoup',
            'azafady': 'excusez-moi / s\'il vous plaît',
            'manao ahoana': 'comment allez-vous',
            'tsara': 'bien / bon',
            'ratsy': 'mauvais',
            'eny': 'oui',
            'tsia': 'non',
            
            # Famille
            'fianakaviana': 'famille',
            'ray': 'père',
            'reny': 'mère',
            'zanaka': 'enfant',
            'anadahy': 'frère (pour une femme)',
            'anabavy': 'sœur (pour un homme)',
            'rahalahy': 'frère (pour un homme)',
            'rahavavy': 'sœur (pour une femme)',
            'dadabe': 'grand-père',
            'nenibe': 'grand-mère',
            'zafy': 'petit-enfant',
            'razana': 'ancêtre',
            
            # Mots de base
            'trano': 'maison',
            'tanana': 'ville / main',
            'vary': 'riz',
            'rano': 'eau',
            'sakafo': 'nourriture',
            'mofo': 'pain',
            'hena': 'viande',
            'voninkazo': 'fleur',
            'hazo': 'arbre / bois',
            'tany': 'terre / pays',
            'lanitra': 'ciel',
            'masoandro': 'soleil',
            'volana': 'lune / mois',
            'kintana': 'étoile',
            'orana': 'pluie',
            'rivotra': 'vent',
            
            # Taille et quantité
            'lehibe': 'grand',
            'kely': 'petit',
            'maro': 'beaucoup',
            'vitsy': 'peu',
            'iray': 'un',
            'roa': 'deux',
            'telo': 'trois',
            'efatra': 'quatre',
            'dimy': 'cinq',
            
            # Temps
            'ankehitriny': 'maintenant',
            'omaly': 'hier',
            'rahampitso': 'demain',
            'maraina': 'matin',
            'tolakandro': 'midi',
            'hariva': 'soir',
            'alina': 'nuit',
            
            # Verbes
            'manao': 'faire',
            'mandeha': 'partir / aller',
            'mihinana': 'manger',
            'misotro': 'boire',
            'miteny': 'parler',
            'mihaino': 'écouter',
            'mijery': 'regarder',
            'manoratra': 'écrire',
            'mamaky': 'lire',
            'mianatra': 'étudier / apprendre',
            'manabe': 'enseigner',
            'miasa': 'travailler',
            'matory': 'dormir',
            'mifoha': 'se réveiller',
            'mipetraka': 'rester / habiter',
            'mihira': 'chanter',
            'mandihy': 'danser',
            'milalao': 'jouer',
            
            # Lieux malgaches
            'antananarivo': 'Antananarivo (capitale)',
            'antsirabe': 'Antsirabe',
            'toamasina': 'Toamasina',
            'mahajanga': 'Mahajanga',
            'fianarantsoa': 'Fianarantsoa',
            'toliary': 'Toliary (Tuléar)',
            'antsiranana': 'Antsiranana (Diego-Suarez)',
            
            # Culture
            'fihavanana': 'solidarité familiale / lien social',
            'famadihana': 'retournement des morts (cérémonie)',
            'kabary': 'discours traditionnel',
            'mpikabary': 'orateur traditionnel',
            'hira gasy': 'chanson malgache',
            'vary amin\'anana': 'riz aux brèdes (plat)',
            'romazava': 'soupe malgache',
            
            # Adjectifs
            'tsara fanahy': 'gentil',
            'be fitiavana': 'aimant',
            'mahay': 'capable / habile',
            'hendry': 'sage / intelligent',
            'marina': 'vrai / honnête',
            'diso': 'faux / erreur',
            'fotsy': 'blanc',
            'mainty': 'noir',
            'mena': 'rouge',
            'maitso': 'vert',
            
            # Autres
            'vahiny': 'étranger / invité',
            'olona': 'personne / gens',
            'zavatra': 'chose',
            'fotoana': 'temps / moment',
            'toerana': 'lieu / place',
            'fitiavana': 'amour',
            'fiadanana': 'paix',
            'fahasoavana': 'bonheur / grâce',
            'fahamarinana': 'vérité',
            'rariny': 'justice'
        }
    
    def translate(self, word, to_french=True):
        """
        Traduit un mot
        
        Args:
            word: mot à traduire
            to_french: True pour MG->FR, False pour FR->MG
        
        Returns:
            traduction ou None si non trouvé
        """
        word_lower = word.lower().strip()
        
        if to_french:
            return self.mg_to_fr.get(word_lower)
        else:
            return self.fr_to_mg.get(word_lower)
    
    def get_all_translations(self, word):
        """Retourne toutes les traductions possibles"""
        word_lower = word.lower().strip()
        results = {
            'mg_to_fr': self.mg_to_fr.get(word_lower),
            'fr_to_mg': self.fr_to_mg.get(word_lower)
        }
        return results
