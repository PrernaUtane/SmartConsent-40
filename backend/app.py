from flask import Flask, request, jsonify
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
import os

app = Flask(__name__)

# Load model
model_path = "ml-model/saved_model/"
print("Loading model...")
model = DistilBertForSequenceClassification.from_pretrained(model_path)
tokenizer = DistilBertTokenizer.from_pretrained(model_path)
print("Model loaded!")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        text = data.get("text", "")
        
        # Predict
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
        outputs = model(**inputs)
        prob = torch.softmax(outputs.logits, dim=1)
        
        # Result
        is_unfair = prob[0][1] > 0.5
        confidence = prob[0][1].item() if is_unfair else prob[0][0].item()
        
        if is_unfair:
            risk = "HIGH" if confidence > 0.8 else "MEDIUM"
        else:
            risk = "LOW"
        
        return jsonify({
            "label": "UNFAIR" if is_unfair else "FAIR",
            "confidence": round(confidence, 2),
            "risk": risk
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)