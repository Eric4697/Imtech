"""
Module de reconnaissance d'entités nommées (NER) pour le Malagasy
Détecte les villes, régions, personnalités, etc.
"""
import re

class NamedEntityRecognizer:
    def __init__(self):
        """Initialise le NER"""
        self.cities = self._load_cities()
        self.regions = self._load_regions()
        self.personalities = self._load_personalities()
        self.organizations = self._load_organizations()
    
    def _load_cities(self):
        """Charge la liste des villes malgaches"""
        return {
            'antananarivo': {'type': 'ville', 'region': 'Analamanga', 'label': 'Capitale'},
            'antsirabe': {'type': 'ville', 'region': 'Vakinankaratra'},
            'toamasina': {'type': 'ville', 'region': 'Atsinanana', 'label': 'Port principal'},
            'mahajanga': {'type': 'ville', 'region': 'Boeny'},
            'fianarantsoa': {'type': 'ville', 'region': 'Haute Matsiatra'},
            'toliary': {'type': 'ville', 'region': 'Atsimo-Andrefana', 'alias': 'tuléar'},
            'antsiranana': {'type': 'ville', 'region': 'Diana', 'alias': 'diego-suarez'},
            'ambositra': {'type': 'ville', 'region': 'Amoron\'i Mania'},
            'morondava': {'type': 'ville', 'region': 'Menabe'},
            'nosy be': {'type': 'ville', 'region': 'Diana', 'label': 'Île touristique'},
            'manakara': {'type': 'ville', 'region': 'Vatovavy-Fitovinany'},
            'fort dauphin': {'type': 'ville', 'region': 'Anosy', 'alias': 'tôlanaro'},
            'tamatave': {'type': 'ville', 'alias': 'toamasina'}
        }
    
    def _load_regions(self):
        """Charge les régions de Madagascar"""
        return {
            'analamanga': {'type': 'region', 'capital': 'Antananarivo'},
            'vakinankaratra': {'type': 'region', 'capital': 'Antsirabe'},
            'itasy': {'type': 'region'},
            'bongolava': {'type': 'region'},
            'vatovavy-fitovinany': {'type': 'region'},
            'haute matsiatra': {'type': 'region'},
            'atsimo-atsinanana': {'type': 'region'},
            'ihorombe': {'type': 'region'},
            'atsimo-andrefana': {'type': 'region'},
            'menabe': {'type': 'region'},
            'boeny': {'type': 'region'},
            'sofia': {'type': 'region'},
            'diana': {'type': 'region'},
            'sava': {'type': 'region'}
        }
    
    def _load_personalities(self):
        """Charge des personnalités malgaches connues"""
        return {
            'andrianampoinimerina': {'type': 'personnalité', 'category': 'roi', 'period': 'historique'},
            'ranavalona': {'type': 'personnalité', 'category': 'reine', 'period': 'historique'},
            'radama': {'type': 'personnalité', 'category': 'roi', 'period': 'historique'},
            'rainilaiarivony': {'type': 'personnalité', 'category': 'premier ministre', 'period': 'historique'},
            'philibert tsiranana': {'type': 'personnalité', 'category': 'président', 'period': 'moderne'},
            'didier ratsiraka': {'type': 'personnalité', 'category': 'président', 'period': 'moderne'},
            'marc ravalomanana': {'type': 'personnalité', 'category': 'président', 'period': 'moderne'},
            'andry rajoelina': {'type': 'personnalité', 'category': 'président', 'period': 'contemporain'},
            'jean verdi salomon rakotomalala': {'type': 'personnalité', 'category': 'musicien'},
            'rakoto frah': {'type': 'personnalité', 'category': 'musicien'},
            'rossy': {'type': 'personnalité', 'category': 'musicien'}
        }
    
    def _load_organizations(self):
        """Charge les organisations malgaches"""
        return {
            'université d\'antananarivo': {'type': 'organisation', 'category': 'université'},
            'jirama': {'type': 'organisation', 'category': 'service public'},
            'air madagascar': {'type': 'organisation', 'category': 'compagnie aérienne'},
            'banque centrale de madagascar': {'type': 'organisation', 'category': 'banque'}
        }
    
    def extract(self, text):
        """
        Extrait les entités nommées du texte
        
        Returns:
            liste d'entités avec leurs types et positions
        """
        text_lower = text.lower()
        entities = []
        
        # Chercher les villes
        for city, info in self.cities.items():
            pattern = r'\b' + re.escape(city) + r'\b'
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                entities.append({
                    'text': text[match.start():match.end()],
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'VILLE',
                    'entity': city,
                    'info': info
                })
        
        # Chercher les régions
        for region, info in self.regions.items():
            pattern = r'\b' + re.escape(region) + r'\b'
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                entities.append({
                    'text': text[match.start():match.end()],
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'REGION',
                    'entity': region,
                    'info': info
                })
        
        # Chercher les personnalités
        for person, info in self.personalities.items():
            pattern = r'\b' + re.escape(person) + r'\b'
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                entities.append({
                    'text': text[match.start():match.end()],
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'PERSONNALITÉ',
                    'entity': person,
                    'info': info
                })
        
        # Chercher les organisations
        for org, info in self.organizations.items():
            pattern = r'\b' + re.escape(org) + r'\b'
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                entities.append({
                    'text': text[match.start():match.end()],
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'ORGANISATION',
                    'entity': org,
                    'info': info
                })
        
        # Trier par position dans le texte
        entities.sort(key=lambda x: x['start'])
        
        return entities
