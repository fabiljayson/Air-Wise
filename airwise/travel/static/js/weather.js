console.log('Weather script loaded successfully');

// Attendre que le DOM soit complètement chargé
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');
    
    // Trouver le formulaire
    const searchForm = document.getElementById('searchForm');
    
    if (searchForm) {
        console.log('Form found');
        
        // Ajouter l'écouteur d'événement
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Form submitted');
            
            // Récupérer la destination
            const destinationInput = document.getElementById('destination');
            const destination = destinationInput ? destinationInput.value : null;
            
            console.log('Destination value:', destination);
            
            if (destination && destination.trim() !== '') {
                console.log('Getting weather for:', destination);
                getWeather(destination.trim());
            } else {
                alert('Veuillez saisir une destination valide');
            }
        });
    } else {
        console.error('Form with ID "searchForm" not found');
        alert('Erreur: Formulaire non trouvé');
    }
});

// Fonction principale pour obtenir la météo
async function getWeather(city) {
    console.log('Starting weather fetch for:', city);
    
    const apiKey = window.OPENWEATHER_API_KEY || "";
    
    try {
        // Afficher le message de chargement
        showWeatherMessage('Chargement des données météo...');
        hideWeatherError();
        hideWeatherInfo();
        
        // Faire la requête API
        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?units=metric&q=${encodeURIComponent(city)}&appid=${apiKey}`);
        
        console.log('API response status:', response.status);
        
        if (response.ok) {
            const data = await response.json();
            console.log('Weather data received:', data);
            
            // Afficher les données météo
            displayWeatherData(data);
            
            // Mettre à jour l'estimation du prix
            updatePriceEstimation(data);
            
        } else if (response.status === 404) {
            throw new Error('Ville non trouvée');
        } else {
            throw new Error('Erreur API: ' + response.status);
        }
        
    } catch (error) {
        console.error('Error in getWeather:', error);
        showWeatherError('Erreur: ' + error.message);
        hideWeatherInfo();
        hideWeatherMessage();
        
        // Réinitialiser l'impact météo
        document.getElementById('weather-impact').textContent = '+0% (erreur météo)';
    }
}

// Fonctions d'affichage
function displayWeatherData(data) {
    document.getElementById('weather-city').textContent = data.name;
    document.querySelector('.weather-temp').textContent = Math.floor(data.main.temp) + '°C';
    document.querySelector('.weather-condition').textContent = data.weather[0].description;
    document.querySelector('.wind').textContent = Math.floor(data.wind.speed) + ' m/s';
    document.querySelector('.humidity').textContent = Math.floor(data.main.humidity) + '%';
    
    // Déterminer l'icône météo
    const weatherImg = document.querySelector('.weather-img');
    const weatherMain = data.weather[0].main.toLowerCase();
    
    // Utiliser les icônes d'OpenWeatherMap directement
    weatherImg.src = `https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png`;
    weatherImg.alt = data.weather[0].description;
    
    // Afficher les informations
    showWeatherInfo();
    hideWeatherMessage();
    hideWeatherError();
}

function updatePriceEstimation(weatherData) {
    const basePrice = 340;
    let weatherImpact = 0;
    let impactText = '';
    
    // Calculer l'impact météo
    const weatherMain = weatherData.weather[0].main.toLowerCase();
    
    if (weatherMain.includes('rain') || weatherMain.includes('storm')) {
        weatherImpact = 0.15;
        impactText = '+15% (mauvais temps)';
    } else if (weatherMain.includes('snow')) {
        weatherImpact = 0.12;
        impactText = '+12% (neige)';
    } else if (weatherMain.includes('cloud')) {
        weatherImpact = 0.05;
        impactText = '+5% (ciel couvert)';
    } else if (weatherMain.includes('clear')) {
        weatherImpact = -0.08;
        impactText = '-8% (beau temps)';
    } else {
        weatherImpact = 0.03;
        impactText = '+3% (conditions normales)';
    }
    
    // Impact supplémentaire basé sur la température
    if (weatherData.main.temp < 0) {
        weatherImpact += 0.07;
        impactText += ', très froid';
    } else if (weatherData.main.temp > 30) {
        weatherImpact += 0.05;
        impactText += ', très chaud';
    }
    
    // Mettre à jour l'affichage
    document.getElementById('weather-impact').textContent = impactText;
    
    // Calculer le prix final
    const finalPrice = Math.round(basePrice * (1 + weatherImpact));
    document.getElementById('final-price').textContent = finalPrice;
}

// Fonctions utilitaires
function showWeatherInfo() {
    document.querySelector('.weather-info').style.display = 'block';
}

function hideWeatherInfo() {
    document.querySelector('.weather-info').style.display = 'none';
}

function showWeatherMessage(message) {
    const element = document.querySelector('.weather-message');
    element.textContent = message;
    element.style.display = 'block';
}

function hideWeatherMessage() {
    document.querySelector('.weather-message').style.display = 'none';
}

function showWeatherError(message) {
    const element = document.querySelector('.weather-error');
    element.textContent = message;
    element.style.display = 'block';
}

function hideWeatherError() {
    document.querySelector('.weather-error').style.display = 'none';
}

// Test manuel - décommentez pour tester directement
// getWeather('Paris');