let apiKey = window.OPENWEATHER_API_KEY || "";

function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

const city = getQueryParam('destination');

async function search(city) {
    if (!apiKey) {
        document.querySelector(".error-message").style.display = "block";
        document.querySelector(".error-message").textContent = "Weather API key not configured.";
        return;
    }

    try {
        let response = await fetch(`https://api.openweathermap.org/data/2.5/weather?units=metric&q=${encodeURIComponent(city)}&appid=${apiKey}`);

        if (response.ok) {
            let data = await response.json();

            let box = document.querySelector(".return");
            box.style.display = "block";

            document.querySelector(".message").style.display = "none";
            document.querySelector(".error-message").style.display = "none";

            document.querySelector(".city-name").innerHTML = data.name;
            document.querySelector(".weather-temp").innerHTML = Math.floor(data.main.temp) + '&deg;';
            document.querySelector(".wind").innerHTML = Math.floor(data.wind.speed) + " m/s";
            document.querySelector(".pressure").innerHTML = Math.floor(data.main.pressure) + " hPa";
            document.querySelector('.humidity').innerHTML = Math.floor(data.main.humidity) + "%";
            document.querySelector(".sunrise").innerHTML = new Date(data.sys.sunrise * 1000).toLocaleTimeString([], {hour: "2-digit", minute: "2-digit"});
            document.querySelector(".sunset").innerHTML = new Date(data.sys.sunset * 1000).toLocaleTimeString([], {hour: "2-digit", minute: "2-digit"});

            let weatherImg = document.querySelector(".weather-img");
            weatherImg.src = `https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png`;
            weatherImg.alt = data.weather[0].description;
        } else {
            document.querySelector(".return").style.display = "none";
            document.querySelector(".message").style.display = "none";
            document.querySelector(".error-message").style.display = "block";
        }
    } catch (error) {
        document.querySelector(".return").style.display = "none";
        document.querySelector(".message").style.display = "none";
        document.querySelector(".error-message").style.display = "block";
        document.querySelector(".error-message").textContent = "Network error: " + error.message;
    }
}

if (city) {
    search(city);
}
