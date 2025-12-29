# analysis_app/utils.py
import joblib
import os
import numpy as np
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR.parent, 'model_3.pkl')
LABEL_ENCODER_PATH = os.path.join(settings.BASE_DIR.parent, 'label_encoder.pkl')

# Load model
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

# Load label encoder if exists
label_encoder = None
if os.path.exists(LABEL_ENCODER_PATH):
    try:
        label_encoder = joblib.load(LABEL_ENCODER_PATH)
    except Exception as e:
        print(f"Error loading label encoder: {e}")

def encode_gender(gender):
    """Encode gender: Male=1, Female=0"""
    return 1 if gender.lower() == 'male' else 0

def encode_division(division):
    """Encode division using label encoder if available, otherwise return hash"""
    if label_encoder is not None:
        try:
            return label_encoder.transform([division])[0]
        except:
            pass
    # Fallback: simple hash-based encoding
    divisions = [
        'Bagerhat', 'Bandarban', 'Barguna', 'Barishal', 'Bhola', 'Bogura', 'Brahmanbaria',
        'Chandpur', 'Chapainawabganj', 'Chattogram', 'Chuadanga', "Cox's Bazar", 'Cumilla',
        'Dhaka', 'Dinajpur', 'Faridpur', 'Feni', 'Gaibandha', 'Gazipur', 'Gopalganj',
        'Habiganj', 'Jamalpur', 'Jashore', 'Jhalokathi', 'Jhenaidah', 'Joypurhat',
        'Khagrachhari', 'Khulna', 'Kishoreganj', 'Kurigram', 'Kushtia', 'Lakshmipur',
        'Lalmonirhat', 'Madaripur', 'Magura', 'Manikganj', 'Meherpur', 'Moulvibazar',
        'Munshiganj', 'Mymensingh', 'Naogaon', 'Narail', 'Narayanganj', 'Narsingdi',
        'Natore', 'Netrokona', 'Nilphamari', 'Noakhali', 'Pabna', 'Panchagarh',
        'Patuakhali', 'Pirojpur', 'Rajbari', 'Rajshahi', 'Rangamati', 'Rangpur',
        'Satkhira', 'Shariatpur', 'Sherpur', 'Sirajganj', 'Sunamganj', 'Sylhet',
        'Tangail', 'Thakurgaon'
    ]
    try:
        return divisions.index(division) if division in divisions else 0
    except:
        return 0

def prepare_features(gender, age, ns1, igg, igm, division, area, house_type):
    """
    Prepare features for model prediction
    Returns: numpy array of features
    """
    features = []
    
    # Encode gender (Male=1, Female=0)
    features.append(encode_gender(gender))
    
    # Age (numeric)
    features.append(float(age))
    
    # Test results (0/1)
    features.append(int(ns1))
    features.append(int(igg))
    features.append(int(igm))
    
    # Encode division
    features.append(encode_division(division))
    
    # Area (simple encoding - length or hash)
    features.append(len(str(area)) if area else 0)
    
    # House type (0/1/2)
    features.append(int(house_type))
    
    return np.array(features)

def predict_dengue(gender, age, ns1, igg, igm, division, area, house_type):
    """
    Predict dengue using ML model
    Returns: prediction result (True/False or probability)
    """
    if model is None:
        # Fallback to simple rule-based prediction
        return (int(ns1) + int(igg) + int(igm)) >= 2
    
    try:
        # Prepare features
        features = prepare_features(gender, age, ns1, igg, igm, division, area, house_type)
        
        # Make prediction
        prediction = model.predict([features])[0]
        
        # If prediction is probability, convert to boolean
        if isinstance(prediction, (float, np.floating)):
            return prediction > 0.5
        elif isinstance(prediction, (int, np.integer)):
            return bool(prediction)
        else:
            return bool(prediction)
            
    except Exception as e:
        print(f"Error in prediction: {e}")
        # Fallback to simple rule-based prediction
        return (int(ns1) + int(igg) + int(igm)) >= 2
