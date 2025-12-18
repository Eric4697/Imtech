"""
Module de synthèse vocale (Text-to-Speech) pour le Malagasy
"""
import os
from gtts import gTTS
import hashlib

class TextToSpeech:
    def __init__(self):
        """Initialise le module TTS"""
        self.audio_dir = os.path.join('static', 'audio')
        os.makedirs(self.audio_dir, exist_ok=True)
    
    def generate(self, text):
        """
        Génère un fichier audio à partir du texte
        
        Args:
            text: texte à convertir en audio
        
        Returns:
            URL du fichier audio généré
        """
        if not text or text.strip() == '':
            return None
        
        # Créer un hash du texte pour le nom de fichier
        text_hash = hashlib.md5(text.encode()).hexdigest()
        filename = f"{text_hash}.mp3"
        filepath = os.path.join(self.audio_dir, filename)
        
        # Vérifier si le fichier existe déjà
        if os.path.exists(filepath):
            return f"/static/audio/{filename}"
        
        try:
            # Utiliser gTTS avec la langue malagasy (mg)
            # Note: gTTS supporte le malagasy de manière basique
            tts = gTTS(text=text, lang='mg', slow=False)
            tts.save(filepath)
            
            return f"/static/audio/{filename}"
        
        except Exception as e:
            print(f"Erreur TTS: {e}")
            # Fallback vers le français si le malagasy n'est pas disponible
            try:
                tts = gTTS(text=text, lang='fr', slow=False)
                tts.save(filepath)
                return f"/static/audio/{filename}"
            except:
                return None
