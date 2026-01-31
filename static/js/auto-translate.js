/**
 * Script pour ajouter automatiquement les attributs data-translate
 * et traduire la page en temps réel
 */

(function() {
    'use strict';
    
    // Fonction pour ajouter l'attribut data-translate à un élément
    function addTranslateAttribute(element, text) {
        // Ne pas ajouter si déjà présent
        if (element.hasAttribute('data-translate')) {
            return;
        }
        
        // Vérifier si le texte existe dans notre dictionnaire
        if (window.translations && window.translations[text]) {
            element.setAttribute('data-translate', text);
            return true;
        }
        
        return false;
    }
    
    // Fonction pour scanner et ajouter les attributs
    function scanAndAddAttributes() {
        if (!window.translations) {
            console.warn('Dictionnaire de traductions non chargé');
            return;
        }
        
        // Liste des sélecteurs à traiter
        const selectors = [
            'button',
            'a.nav-link',
            'a.dropdown-item',
            'a.btn',
            'th',
            'label',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            '.card-header h6',
            '.badge',
            'option'
        ];
        
        selectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(element => {
                // Obtenir le texte de l'élément (sans les enfants)
                let text = '';
                
                // Pour les éléments avec icônes
                if (element.querySelector('i')) {
                    // Obtenir seulement le texte, pas les icônes
                    text = Array.from(element.childNodes)
                        .filter(node => node.nodeType === Node.TEXT_NODE)
                        .map(node => node.textContent.trim())
                        .join(' ')
                        .trim();
                } else {
                    text = element.textContent.trim();
                }
                
                // Ajouter l'attribut si le texte existe dans le dictionnaire
                if (text && addTranslateAttribute(element, text)) {
                    console.log(`Ajouté data-translate="${text}" à`, element);
                }
            });
        });
    }
    
    // Fonction pour traduire les placeholders
    function translatePlaceholders(lang) {
        document.querySelectorAll('input[placeholder], textarea[placeholder]').forEach(input => {
            const placeholder = input.getAttribute('placeholder');
            if (placeholder && window.translate) {
                const translated = window.translate(placeholder, lang);
                if (translated !== placeholder) {
                    input.setAttribute('data-original-placeholder', placeholder);
                    input.setAttribute('placeholder', translated);
                }
            }
        });
    }
    
    // Fonction pour restaurer les placeholders
    function restorePlaceholders() {
        document.querySelectorAll('[data-original-placeholder]').forEach(input => {
            const original = input.getAttribute('data-original-placeholder');
            input.setAttribute('placeholder', original);
            input.removeAttribute('data-original-placeholder');
        });
    }
    
    // Observer les changements de langue
    function observeLanguageChange() {
        // Écouter l'événement personnalisé de changement de langue
        document.addEventListener('languageChanged', function(e) {
            const lang = e.detail.language;
            console.log(`Langue changée vers: ${lang}`);
            
            // Traduire les placeholders
            if (lang === 'ar') {
                translatePlaceholders(lang);
            } else {
                restorePlaceholders();
            }
        });
    }
    
    // Initialiser au chargement de la page
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Auto-translate: Initialisation...');
        
        // Attendre que translations.js soit chargé
        const checkTranslations = setInterval(() => {
            if (window.translations) {
                clearInterval(checkTranslations);
                console.log('Auto-translate: Dictionnaire chargé');
                
                // Scanner et ajouter les attributs
                scanAndAddAttributes();
                
                // Observer les changements
                observeLanguageChange();
                
                // Appliquer la langue sauvegardée
                const savedLang = localStorage.getItem('language') || localStorage.getItem('pref_language') || 'fr';
                if (savedLang !== 'fr') {
                    translatePlaceholders(savedLang);
                }
            }
        }, 100);
        
        // Timeout après 5 secondes
        setTimeout(() => {
            clearInterval(checkTranslations);
        }, 5000);
    });
    
    // Exporter les fonctions
    window.autoTranslate = {
        scan: scanAndAddAttributes,
        translatePlaceholders: translatePlaceholders
    };
})();


