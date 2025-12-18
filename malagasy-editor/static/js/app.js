// Application JavaScript pour l'Éditeur Malagasy Intelligent

// Initialisation de Quill Editor
const quill = new Quill('#editor', {
    theme: 'snow',
    placeholder: 'Manoratra eto... (Écrivez ici...)',
    modules: {
        toolbar: [
            ['bold', 'italic', 'underline', 'strike'],
            ['blockquote', 'code-block'],
            [{ 'header': 1 }, { 'header': 2 }],
            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
            [{ 'indent': '-1'}, { 'indent': '+1' }],
            [{ 'size': ['small', false, 'large', 'huge'] }],
            [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
            [{ 'color': [] }, { 'background': [] }],
            [{ 'align': [] }],
            ['clean']
        ]
    }
});

// Variables globales
let autocompleteEnabled = true;
let currentText = '';

// Mise à jour des statistiques
function updateStats() {
    const text = quill.getText();
    const words = text.trim().split(/\s+/).filter(w => w.length > 0);
    const chars = text.length;
    const lines = text.split('\n').length;

    document.getElementById('wordCount').textContent = words.length;
    document.getElementById('charCount').textContent = chars;
    document.getElementById('lineCount').textContent = lines;
}

// Notification
function showNotification(message, isError = false) {
    const notif = document.getElementById('notification');
    notif.textContent = message;
    notif.className = 'notification show' + (isError ? ' error' : '');
    
    setTimeout(() => {
        notif.classList.remove('show');
    }, 3000);
}

// API Helper
async function apiRequest(endpoint, data) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Correcteur Orthographique
document.getElementById('checkSpelling').addEventListener('click', async () => {
    const text = quill.getText();
    const words = text.trim().split(/\s+/).filter(w => w.length > 0);
    
    if (words.length === 0) {
        showNotification('Veuillez écrire du texte d\'abord', true);
        return;
    }

    showNotification('Vérification en cours...');
    
    let errorsFound = 0;
    for (const word of words) {
        try {
            const result = await apiRequest('/api/check-spelling', { word });
            if (!result.correct) {
                errorsFound++;
                console.log(`Erreur: ${word}`, result);
            }
        } catch (error) {
            console.error('Erreur vérification:', error);
        }
    }

    if (errorsFound === 0) {
        showNotification('✓ Aucune erreur détectée !');
    } else {
        showNotification(`⚠ ${errorsFound} erreur(s) détectée(s)`, true);
    }
});

// Autocomplétion
let autocompleteTimeout;
document.getElementById('autocompleteToggle').addEventListener('change', (e) => {
    autocompleteEnabled = e.target.checked;
    document.getElementById('autocompleteSuggestions').classList.remove('show');
});

quill.on('text-change', async () => {
    updateStats();
    
    if (!autocompleteEnabled) return;

    clearTimeout(autocompleteTimeout);
    autocompleteTimeout = setTimeout(async () => {
        const text = quill.getText().trim();
        if (text.length < 2) return;

        try {
            const result = await apiRequest('/api/autocomplete', { context: text });
            if (result.suggestions && result.suggestions.length > 0) {
                showAutocompleteSuggestions(result.suggestions);
            }
        } catch (error) {
            console.error('Erreur autocomplétion:', error);
        }
    }, 500);
});

function showAutocompleteSuggestions(suggestions) {
    const container = document.getElementById('autocompleteSuggestions');
    container.innerHTML = '';
    
    suggestions.forEach(word => {
        const item = document.createElement('div');
        item.className = 'suggestion-item';
        item.textContent = word;
        item.addEventListener('click', () => {
            const currentLength = quill.getLength();
            quill.insertText(currentLength - 1, ' ' + word);
            container.classList.remove('show');
        });
        container.appendChild(item);
    });

    // Position le container
    container.style.top = '200px';
    container.style.left = '400px';
    container.classList.add('show');
}

// Traduction au clic droit
quill.root.addEventListener('contextmenu', async (e) => {
    e.preventDefault();
    
    const selection = quill.getSelection();
    if (!selection || selection.length === 0) return;

    const text = quill.getText(selection.index, selection.length).trim();
    if (!text) return;

    try {
        const result = await apiRequest('/api/translate', { word: text });
        const translationDiv = document.getElementById('translationResult');
        
        if (result.translation) {
            translationDiv.innerHTML = `
                <strong>${text}</strong><br>
                <i class="fas fa-arrow-right"></i> ${result.translation}
            `;
        } else {
            translationDiv.innerHTML = `
                <em>Traduction non trouvée pour "${text}"</em>
            `;
        }
    } catch (error) {
        console.error('Erreur traduction:', error);
    }
});

// Analyse de Sentiment
document.getElementById('analyzeSentiment').addEventListener('click', async () => {
    const text = quill.getText().trim();
    
    if (!text) {
        showNotification('Veuillez écrire du texte d\'abord', true);
        return;
    }

    try {
        const result = await apiRequest('/api/analyze-sentiment', { text });
        const resultDiv = document.getElementById('sentimentResult');
        
        const sentimentClass = `sentiment-${result.sentiment}`;
        const icon = result.sentiment === 'positif' ? '😊' : 
                     result.sentiment === 'négatif' ? '😞' : '😐';
        
        resultDiv.innerHTML = `
            <div class="${sentimentClass}">
                ${icon} <strong>${result.sentiment.toUpperCase()}</strong><br>
                Score: ${result.score} | Confiance: ${result.confidence * 100}%<br>
                Positif: ${result.positive_count} | Négatif: ${result.negative_count}
            </div>
        `;
        
        showNotification('Analyse terminée !');
    } catch (error) {
        console.error('Erreur analyse sentiment:', error);
        showNotification('Erreur lors de l\'analyse', true);
    }
});

// Lemmatisation
document.getElementById('getLemma').addEventListener('click', async () => {
    const word = document.getElementById('lemmaInput').value.trim();
    
    if (!word) {
        showNotification('Veuillez entrer un mot', true);
        return;
    }

    try {
        const result = await apiRequest('/api/lemmatize', { word });
        const resultDiv = document.getElementById('lemmaResult');
        
        resultDiv.innerHTML = `
            <strong>Mot:</strong> ${result.lemma.original}<br>
            <strong>Racine:</strong> ${result.lemma.lemma}<br>
            ${result.lemma.prefix ? `<strong>Préfixe:</strong> ${result.lemma.prefix}<br>` : ''}
            ${result.lemma.suffix ? `<strong>Suffixe:</strong> ${result.lemma.suffix}<br>` : ''}
            <strong>Type:</strong> ${result.lemma.type}
        `;
        
        showNotification('Lemmatisation effectuée !');
    } catch (error) {
        console.error('Erreur lemmatisation:', error);
        showNotification('Erreur lors de la lemmatisation', true);
    }
});

// Extraction d'Entités
document.getElementById('extractEntities').addEventListener('click', async () => {
    const text = quill.getText().trim();
    
    if (!text) {
        showNotification('Veuillez écrire du texte d\'abord', true);
        return;
    }

    try {
        const result = await apiRequest('/api/extract-entities', { text });
        
        if (result.entities.length === 0) {
            showNotification('Aucune entité détectée');
            return;
        }

        console.log('Entités trouvées:', result.entities);
        showNotification(`${result.entities.length} entité(s) détectée(s) !`);
        
        // Afficher les entités dans la console
        result.entities.forEach(entity => {
            console.log(`${entity.type}: ${entity.text}`, entity.info);
        });
    } catch (error) {
        console.error('Erreur extraction entités:', error);
        showNotification('Erreur lors de l\'extraction', true);
    }
});

// Text-to-Speech
document.getElementById('textToSpeech').addEventListener('click', async () => {
    const selection = quill.getSelection();
    let text;
    
    if (selection && selection.length > 0) {
        text = quill.getText(selection.index, selection.length).trim();
    } else {
        text = quill.getText().trim();
    }
    
    if (!text) {
        showNotification('Veuillez écrire ou sélectionner du texte', true);
        return;
    }

    showNotification('Génération audio en cours...');

    try {
        const result = await apiRequest('/api/text-to-speech', { text });
        
        if (result.audio_url) {
            const audio = new Audio(result.audio_url);
            audio.play();
            showNotification('Lecture audio démarrée !');
        } else {
            showNotification('Erreur génération audio', true);
        }
    } catch (error) {
        console.error('Erreur TTS:', error);
        showNotification('Erreur lors de la génération audio', true);
    }
});

// Effacer l'éditeur
document.getElementById('clearEditor').addEventListener('click', () => {
    if (confirm('Voulez-vous vraiment effacer tout le texte ?')) {
        quill.setText('');
        showNotification('Éditeur effacé');
    }
});

// Sauvegarder
document.getElementById('saveText').addEventListener('click', () => {
    const text = quill.getText();
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'texte_malagasy.txt';
    a.click();
    showNotification('Texte sauvegardé !');
});

// Charger exemple
document.getElementById('loadExample').addEventListener('click', () => {
    const exampleText = `Salama e!

Malagasy aho ary faly aho manoatra amin'ity fanaovan-javatra ity. Ny fihavanana no maha-Malagasy. Ny razana dia lehilahy mahay sy hendry.

Ny tanana Antananarivo dia tanana lehibe indrindra eto Madagasikara. Misy olona maro any Antsirabe sy Toamasina koa.

Misaotra betsaka amin'ny fanahy tsara! Tonga soa amin'ny fanabeazana malagasy.`;
    
    quill.setText(exampleText);
    showNotification('Exemple chargé !');
});

// Initialisation
updateStats();
showNotification('Bienvenue ! Éditeur prêt à l\'usage 🚀');
