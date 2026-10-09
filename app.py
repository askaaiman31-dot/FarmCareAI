 (
        image,
        dtype=np.float32
    )

    image_array = np.expand_dims(
        image_array,
        axis=0
    )


    predictions = model.predict(
        image_array,
        verbose=0
    )


    predicted_index = int(
        np.argmax(predictions[0])
    )


    predicted_class = class_names[
        predicted_index
    ]


    confidence = float(
        predictions[0][predicted_index] * 100
    )


    return jsonify({

        "disease": predicted_class,

        "confidence": round(
            confidence,
            2
        )

    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
