from flask import Flask, render_template, request
from ultralytics import YOLO
from werkzeug.utils import secure_filename

import os
import shutil
import csv
from datetime import datetime


# =====================================================
# Flask App
# =====================================================

app = Flask(__name__)


# =====================================================
# Project Paths
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "uploads"
)

RESULT_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "results"
)

OUTPUT_FOLDER = os.path.join(
    BASE_DIR,
    "runs"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "yolo11n.pt"
)

HISTORY_FOLDER = os.path.join(
    BASE_DIR,
    "history"
)

HISTORY_FILE = os.path.join(
    HISTORY_FOLDER,
    "history.csv"
)


# =====================================================
# Create Required Folders
# =====================================================

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    RESULT_FOLDER,
    exist_ok=True
)

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

os.makedirs(
    HISTORY_FOLDER,
    exist_ok=True
)


# =====================================================
# Load YOLO Model (Only Once)
# =====================================================

print("Loading YOLO model...")

model = YOLO(MODEL_PATH)

print("YOLO model loaded successfully!")


# =====================================================
# Home Route
# =====================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =====================================================
# Detection Page Route
# =====================================================

@app.route("/detection")
def detection():

    return render_template(
        "detection.html"
    )


# =====================================================
# Analytics Route
# =====================================================

@app.route("/analytics")
def analytics():

    return render_template(
        "analytics.html"
    )


# =====================================================
# History Route
# =====================================================

@app.route("/history")
def history():

    history_records = []

    # -------------------------------------------------
    # Read Detection History
    # -------------------------------------------------

    if os.path.exists(HISTORY_FILE):

        try:

            with open(
                HISTORY_FILE,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(
                    file
                )

                history_records = list(
                    reader
                )

        except Exception as e:

            print(
                "Error reading detection history:"
            )

            print(e)


    # -------------------------------------------------
    # Show Newest Detection First
    # -------------------------------------------------

    history_records.reverse()


    # -------------------------------------------------
    # Calculate Total Scans
    # -------------------------------------------------

    total_scans = len(
        history_records
    )


    # -------------------------------------------------
    # Calculate Total Threats
    # -------------------------------------------------

    total_threats = sum(

        1

        for record in history_records

        if record.get(
            "threat_level"
        ) == "HIGH"

    )


    # -------------------------------------------------
    # Calculate Safe Scans
    # -------------------------------------------------

    safe_scans = sum(

        1

        for record in history_records

        if record.get(
            "threat_level"
        ) == "SAFE"

    )


    # -------------------------------------------------
    # Calculate Average Confidence
    # -------------------------------------------------

    confidence_values = []

    for record in history_records:

        confidence = record.get(
            "confidence",
            "--"
        )

        if confidence != "--":

            try:

                confidence_number = float(

                    confidence.replace(
                        "%",
                        ""
                    )

                )

                confidence_values.append(
                    confidence_number
                )

            except ValueError:

                pass


    if confidence_values:

        average_confidence = (

            f"{sum(confidence_values) / len(confidence_values):.2f}%"

        )

    else:

        average_confidence = "--"


    # -------------------------------------------------
    # Render History Page
    # -------------------------------------------------

    return render_template(

        "history.html",

        history_records=history_records,

        total_scans=total_scans,

        total_threats=total_threats,

        safe_scans=safe_scans,

        average_confidence=average_confidence

    )


# =====================================================
# About Route
# =====================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# =====================================================
# Detection Route
# =====================================================

@app.route(
    "/detect",
    methods=["POST"]
)
def detect():

    try:

        # =================================================
        # Check Uploaded Image
        # =================================================

        if "image" not in request.files:

            return "No image uploaded."


        image = request.files[
            "image"
        ]


        if image.filename == "":

            return "No image selected."


        # =================================================
        # Secure Filename
        # =================================================

        filename = secure_filename(
            image.filename
        )


        # =================================================
        # Save Uploaded Image
        # =================================================

        upload_path = os.path.join(

            UPLOAD_FOLDER,

            filename

        )


        image.save(
            upload_path
        )


        print(
            "Image saved:"
        )

        print(
            upload_path
        )


        # =================================================
        # Run YOLO Inference
        # =================================================

        print(
            "Running YOLO inference..."
        )


        results = model.predict(

            source=upload_path,

            save=True,

            project=OUTPUT_FOLDER,

            name="detect",

            exist_ok=True,

            conf=0.25,

            verbose=False

        )


        print(
            "YOLO inference completed!"
        )


        # =================================================
        # Copy Detection Result Image
        # =================================================

        result_path = os.path.join(

            OUTPUT_FOLDER,

            "detect",

            filename

        )


        static_result = os.path.join(

            RESULT_FOLDER,

            filename

        )


        if os.path.exists(
            result_path
        ):

            shutil.copy(

                result_path,

                static_result

            )


            print(
                "Detection image copied."
            )


        else:

            print(
                "Detection image NOT found."
            )


        # =================================================
        # Extract YOLO Predictions
        # =================================================

        detected_objects = []

        max_confidence = 0.0


        for box in results[0].boxes:

            cls = int(
                box.cls[0]
            )

            conf = float(
                box.conf[0]
            )


            detected_objects.append(

                model.names[
                    cls
                ]

            )


            if conf > max_confidence:

                max_confidence = conf


        # =================================================
        # Determine Detection Information
        # =================================================

        if detected_objects:

            detected_object = ", ".join(

                sorted(

                    set(
                        detected_objects
                    )

                )

            )


            confidence = (

                f"{max_confidence * 100:.2f}%"

            )


            threat_level = "HIGH"


        else:

            detected_object = (

                "No Threat Detected"

            )


            confidence = "--"


            threat_level = "SAFE"


        # =================================================
        # Get Inference Time
        # =================================================

        inference = (

            f"{results[0].speed['inference']:.2f} ms"

        )


        # =================================================
        # Save Detection to History CSV
        # =================================================

        history_exists = os.path.exists(
            HISTORY_FILE
        )


        with open(

            HISTORY_FILE,

            "a",

            newline="",

            encoding="utf-8"

        ) as file:


            fieldnames = [

                "image",

                "detected_object",

                "confidence",

                "threat_level",

                "inference",

                "datetime"

            ]


            writer = csv.DictWriter(

                file,

                fieldnames=fieldnames

            )


            # ---------------------------------------------
            # Write CSV Header
            # ---------------------------------------------

            if (

                not history_exists

                or os.path.getsize(
                    HISTORY_FILE
                ) == 0

            ):

                writer.writeheader()


            # ---------------------------------------------
            # Write Detection Record
            # ---------------------------------------------

            writer.writerow({

                "image":
                    filename,

                "detected_object":
                    detected_object,

                "confidence":
                    confidence,

                "threat_level":
                    threat_level,

                "inference":
                    inference,

                "datetime":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

            })


        print(
            "Detection history saved successfully!"
        )


        # =================================================
        # Render Detection Result Page
        # =================================================

        return render_template(

            "detection.html",

            uploaded_image=filename,

            result_image=filename,

            detected_object=detected_object,

            confidence=confidence,

            threat_level=threat_level,

            inference=inference

        )


    # =====================================================
    # Error Handling
    # =====================================================

    except Exception as e:

        print(
            "=" * 60
        )

        print(
            "ERROR"
        )

        print(
            e
        )

        print(
            "=" * 60
        )


        return (

            f"<h2>Error:</h2>"
            f"<pre>{e}</pre>"

        )


# =====================================================
# Run Flask Application
# =====================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        use_reloader=False

    )