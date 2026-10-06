// ======================================
// FARMCARE AI
// JAVASCRIPT
// ======================================


// BACKEND URL

const API_URL =
    "https://5000-gpu-t4-s-kkb-use1c0-3a9f39od7yby7-c.us-east1-0.prod.colab.dev";


// CROP DISEASE DETECTION

const diseaseButton =
    document.getElementById("diseaseButton");

const leafImageInput =
    document.getElementById("leafImageInput");

const leafPreview =
    document.getElementById("leafPreview");

const diseaseResult =
    document.getElementById("diseaseResult");


diseaseButton.addEventListener("click", function () {

    leafImageInput.click();

});


leafImageInput.addEventListener("change", async function () {

    const file = leafImageInput.files[0];

    if (!file) {
        return;
    }


    // Show selected image

    const imageURL = URL.createObjectURL(file);

    leafPreview.src = imageURL;
    leafPreview.style.display = "block";


    // Show loading message

    diseaseResult.textContent =
        "🔄 Analyzing your leaf image...";

    diseaseResult.style.display = "block";


    try {

        const formData = new FormData();

        formData.append("image", file);


        const response = await fetch(
            API_URL + "/predict",
            {
                method: "POST",
                body: formData
            }
        );


        if (!response.ok) {
            throw new Error(
                "Server returned an error."
            );
        }


        const result = await response.json();


        diseaseResult.textContent =
            "🌿 Possible result: " +
            result.disease +
            "\n\nConfidence: " +
            result.confidence +
            "%";


    } catch (error) {

        console.error(error);

        diseaseResult.textContent =
            "❌ Could not connect to the AI server. " +
            "Please make sure the Colab backend is running.";

    }

});


// SOIL HEALTH

const soilButton =
    document.getElementById("soilButton");

soilButton.addEventListener("click", function () {

    alert(
        "Soil Health Analyzer\n\n" +
        "This module will be added later."
    );

});


// MARKET PRICE

const marketButton =
    document.getElementById("marketButton");

marketButton.addEventListener("click", function () {

    alert(
        "Market Price Advisor\n\n" +
        "This module will be added later."
    );

});


// VOICE ASSISTANT

const voiceButton =
    document.getElementById("voiceButton");

voiceButton.addEventListener("click", function () {

    if ("speechSynthesis" in window) {

        const message =
            new SpeechSynthesisUtterance(
                "Welcome to FarmCare AI. Smart technology for better farming."
            );

        window.speechSynthesis.speak(message);

    } else {

        alert(
            "Voice support is not available in this browser."
        );

    }

});


// LANGUAGE BUTTON

const languageButton =
    document.getElementById("languageButton");

languageButton.addEventListener("click", function () {

    alert(
        "Language Support\n\n" +
        "English is currently selected.\n\n" +
        "Hindi and regional language support will be added later."
    );

});