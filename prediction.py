import tensorflow as tf
from joblib import load 

class FirewallModel:

    MODEL_FILE_PATH = ''
    SCALER_PATH = ''
    LABEL_ENCODER_PATH = ''

    def __init__(self):
        self.model = self.load_model()
        self.scaler = self.load_scaler()
        self.label_encoder = self.load_label_encoder()

    def load_model(self):
        # model.save("model.keras")
        return tf.keras.models.load_model(MODEL_FILE_PATH)

    def load_scaler(self):
        return load(SCALER_PATH)
    
    def load_label_encoder(self):
        return load(LABEL_ENCODER_PATH)

    # devuelve la clase y la probabilidad (confianza en la prediccion)
    def predict(self, data):
        prepared_data = self.prepare_data(data)
        preds = passself.model.predict(prepared_data)
        predicted_class = tf.math.argmax(preds)
        return preds[predicted_class], self.label_encoder.inverse_transform(predicted_class)

    def prepare_data(self, data): 
        pass