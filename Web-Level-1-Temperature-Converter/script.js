// ==================== GET HTML ELEMENTS ====================

const temperatureInput = document.getElementById("temperature");

const unitSelect = document.getElementById("unit");

const convertButton = document.getElementById("convert-button");

const errorMessage = document.getElementById("error-message");

const celsiusResult = document.getElementById("celsius-result");

const fahrenheitResult = document.getElementById("fahrenheit-result");

const kelvinResult = document.getElementById("kelvin-result");


// ==================== CONVERT BUTTON ====================

convertButton.addEventListener("click", function () {

    // Get input value

    const inputValue = temperatureInput.value.trim();

    // Clear previous error

    errorMessage.textContent = "";


    // ==================== VALIDATE INPUT ====================

    if (inputValue === "") {

        errorMessage.textContent =
            "Please enter a temperature.";

        return;
    }


    const temperature = Number(inputValue);


    // Reject non-numeric input

    if (Number.isNaN(temperature)) {

        errorMessage.textContent =
            "Please enter a valid numeric temperature.";

        return;
    }


    // ==================== CONVERT TO CELSIUS ====================

    let celsius;


    if (unitSelect.value === "celsius") {

        celsius = temperature;

    } else if (unitSelect.value === "fahrenheit") {

        celsius = (temperature - 32) * 5 / 9;

    } else if (unitSelect.value === "kelvin") {

        celsius = temperature - 273.15;
    }


    // ==================== ABSOLUTE ZERO CHECK ====================

    if (celsius < -273.15) {

        errorMessage.textContent =
            "Temperature cannot be below absolute zero (-273.15°C).";

        clearResults();

        return;
    }


    // ==================== CONVERT TO ALL UNITS ====================

    const fahrenheit = (celsius * 9 / 5) + 32;

    const kelvin = celsius + 273.15;


    // ==================== DISPLAY RESULTS ====================

    celsiusResult.textContent =
        `${celsius.toFixed(2)} °C`;

    fahrenheitResult.textContent =
        `${fahrenheit.toFixed(2)} °F`;

    kelvinResult.textContent =
        `${kelvin.toFixed(2)} K`;

});


// ==================== CLEAR RESULTS ====================

function clearResults() {

    celsiusResult.textContent = "—";

    fahrenheitResult.textContent = "—";

    kelvinResult.textContent = "—";
}