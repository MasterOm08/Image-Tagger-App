import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, jsonify
from google.cloud import storage, vision, firestore

# Initialize GCP clients
# On App Engine, these automatically authenticate via default IAM permissions
storage_client = storage.Client()
vision_client = vision.ImageAnnotatorClient()
db = firestore.Client(database="image-tagger-database")

BUCKET_NAME = "image-tagger-app"
bucket = storage_client.bucket(BUCKET_NAME)

# Initialize Flask App
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload limit


def analyze_image_with_vision(image_bytes):
    image = vision.Image(content=image_bytes)
    response = vision_client.label_detection(image=image)
    
    tags = []
    for label in response.label_annotations:
        tags.append({
            "description": label.description,
            "confidence": round(label.score * 100)  # Convert float (e.g. 0.95) to int percentage (95)
        })
    return tags


@app.route("/")
def index():
    # Fetch all uploaded images from Firestore sorted by upload time
    docs = db.collection("images").order_by("created_at", direction=firestore.Query.DESCENDING).stream()
    
    images_list = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id  # Add document ID for reference
        images_list.append(data)

    return render_template("index.html", images=images_list)

@app.route("/delete/<doc_id>", methods=["POST"])
def delete_image(doc_id):
    try:
        doc_ref = db.collection("images").document(doc_id)
        doc = doc_ref.get()

        if not doc.exists:
            return jsonify({"error": "Document not found"}), 404

        data = doc.to_dict()
        filename = data.get("filename")

        # 1. Delete the targeted Firestore document first
        doc_ref.delete()

        # 2. Check if any other records still use this exact filename
        if filename:
            matching_docs = db.collection("images").where("filename", "==", filename).limit(1).get()
            
            # Only delete from Cloud Storage if NO other Firestore records reference it
            if len(matching_docs) == 0:
                blob = bucket.blob(filename)
                if blob.exists():
                    blob.delete()

        return redirect("/")
    except Exception as e:
        print(f"Error deleting image: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/upload", methods=["POST"])
def upload_file():
    """Handles image upload, storage, Vision tagging, and Firestore saving."""
    # 1. Match HTML input name="file"
    if "file" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        filename = file.filename
        file_bytes = file.read()

        # Step A: Upload Image to Cloud Storage
        blob = bucket.blob(filename)
        blob.upload_from_string(file_bytes, content_type=file.content_type)
        image_url = blob.public_url

        # Step B: Get AI Tags from Cloud Vision API
        tags = analyze_image_with_vision(file_bytes)

        # Step C: Save Metadata into Firestore
        doc_data = {
            "filename": filename,
            "url": image_url,
            "tags": tags,
            "created_at": firestore.SERVER_TIMESTAMP,
        }
        db.collection("images").add(doc_data)

        # 2. Redirect back to home page so the HTML gallery re-renders with the new image
        return redirect("/")

    except Exception as e:
        print(f"Error processing upload: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/gallery", methods=["GET"])
def get_gallery():
    """Fetches all uploaded images and their tags from Firestore."""
    try:
        images_ref = db.collection("images").order_by(
            "created_at", direction=firestore.Query.DESCENDING
        )
        docs = images_ref.stream()

        gallery_data = []
        for doc in docs:
            item = doc.to_dict()
            item["id"] = doc.id
            gallery_data.append(item)

        return jsonify(gallery_data), 200

    except Exception as e:
        print(f"Error fetching gallery: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)