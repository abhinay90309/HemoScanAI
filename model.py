def predict_risk(hemoglobin, gender):
    # Basic WHO-style classification adjustments
    # Normal is typically >13 for men and >12 for women
    threshold = 13 if gender.lower() == "male" else 12
    
    if hemoglobin < 7:
        return "Severe"
    elif hemoglobin < 10:
        return "Moderate"
    elif hemoglobin < threshold:
        return "Mild"
    else:
        return "Normal"