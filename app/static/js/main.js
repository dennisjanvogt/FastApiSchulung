// Hauptfunktionen für die Anwendung

// Prüfen, ob der Benutzer angemeldet ist
function isAuthenticated() {
    return localStorage.getItem('access_token') !== null;
}

// API-Anfragen mit Token-Authentifizierung
async function authenticatedFetch(url, options = {}) {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        window.location.href = '/login';
        return;
    }
    
    // Standard-Header und Optionen
    const defaultOptions = {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    };
    
    // Optionen zusammenführen
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...(options.headers || {})
        }
    };
    
    try {
        const response = await fetch(url, mergedOptions);
        
        // Bei 401 (Unauthorized) zur Login-Seite umleiten
        if (response.status === 401) {
            localStorage.removeItem('access_token');
            window.location.href = '/login';
            return;
        }
        
        return response;
    } catch (error) {
        console.error('Fehler bei der API-Anfrage:', error);
        throw error;
    }
}

// Abmelden
function logout() {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
}

// Formular-Validierung (Allgemein)
function validateForm(form, rules) {
    for (const field in rules) {
        const value = form[field].value.trim();
        const rule = rules[field];
        
        if (rule.required && !value) {
            return { valid: false, message: `${rule.label} ist erforderlich.` };
        }
        
        if (rule.minLength && value.length < rule.minLength) {
            return { valid: false, message: `${rule.label} muss mindestens ${rule.minLength} Zeichen haben.` };
        }
        
        if (rule.pattern && !rule.pattern.test(value)) {
            return { valid: false, message: rule.message || `${rule.label} hat ein ungültiges Format.` };
        }
    }
    
    return { valid: true };
}

// Daten aus Formular sammeln
function getFormData(form, fields) {
    const data = {};
    
    fields.forEach(field => {
        const element = form[field];
        if (element) {
            data[field] = element.value.trim() || null;
        }
    });
    
    return data;
}

// Prüfen, ob der Benutzer auf geschützte Seiten zugreifen darf
document.addEventListener('DOMContentLoaded', function() {
    // Logout-Link
    const logoutLink = document.querySelector('a[href="/logout"]');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
    
    // Prüfen, ob der Benutzer angemeldet ist (außer für Login-Seite)
    if (!window.location.pathname.includes('/login')) {
        if (!isAuthenticated()) {
            window.location.href = '/login';
        }
    }
});