"""
MÓDULO DE PERCEPCIÓN Y APRENDIZAJE AUTOMÁTICO
Maneja la carga de datos, preprocesamiento, entrenamiento y predicción del modelo de red neuronal.
"""
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

class SistemaPercepcion:
    def __init__(self, ruta_modelo=None):
        if ruta_modelo is None:
            ruta_modelo = os.path.join(MODELS_DIR, "modelo_personalidad.h5")
        self.ruta_modelo = os.path.abspath(ruta_modelo)
        self.modelo = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()

    def cargar_dataset(self, ruta_csv=None):
        if ruta_csv is None:
            ruta_csv = os.path.join(DATA_DIR, "16P.csv")
        df = pd.read_csv(ruta_csv, encoding="latin1")
        print(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
        return df

    def preprocesar_datos(self, df):

        df.drop('Response Id', axis=1, inplace=True)

        X = df.drop(columns=["Personalidad"])
        y = df["Personalidad"]

        # Codificar etiquetas
        y_encoded = self.label_encoder.fit_transform(y)

        # Crear carpeta de modelos si no existe
        os.makedirs(MODELS_DIR, exist_ok=True)

        # Guardar el mapeo de etiquetas solo si ya existe el atributo
        if hasattr(self.label_encoder, "classes_"):
            np.save(os.path.join(MODELS_DIR, "label_mapping.npy"), self.label_encoder.classes_)
        else:
            print("Advertencia: El LabelEncoder aún no tiene clases definidas.")

        # Escalar características
        X_scaled = self.scaler.fit_transform(X)
        np.save(os.path.join(MODELS_DIR, "scaler_mean.npy"), self.scaler.mean_)
        np.save(os.path.join(MODELS_DIR, "scaler_scale.npy"), self.scaler.scale_)

        # División estratificada
        X_train, X_temp, y_train, y_temp = train_test_split(
            X_scaled, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
        )

        print(f"Train: {X_train.shape[0]} | Val: {X_val.shape[0]} | Test: {X_test.shape[0]}")

        # One-hot encoding
        y_train_cat = to_categorical(y_train)
        y_val_cat = to_categorical(y_val)
        y_test_cat = to_categorical(y_test)

        return X_train, X_val, X_test, y_train_cat, y_val_cat, y_test_cat

    def construir_modelo(self, input_dim, num_classes):
        modelo = Sequential([
            Dense(128, activation="relu", input_shape=(input_dim,)),
            BatchNormalization(),
            Dropout(0.3),
            Dense(64, activation="relu"),
            BatchNormalization(),
            Dropout(0.3),
            Dense(num_classes, activation="softmax")
        ])
        modelo.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
        return modelo

    def entrenar(self, ruta_csv="../data/16P.csv"):
        """Pipeline completo de entrenamiento"""
        df = self.cargar_dataset(ruta_csv)
        X_train, X_val, X_test, y_train, y_val, y_test = self.preprocesar_datos(df)

        self.modelo = self.construir_modelo(X_train.shape[1], y_train.shape[1])

        early_stop = EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)

        history = self.modelo.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=100,
            batch_size=64,
            callbacks=[early_stop],
            verbose=1
        )

        # Evaluación final
        test_loss, test_acc = self.modelo.evaluate(X_test, y_test)
        print(f"\nEvaluación: Accuracy = {test_acc:.3f}")

        # Reporte detallado
        y_pred = np.argmax(self.modelo.predict(X_test), axis=1)
        y_true = np.argmax(y_test, axis=1)
        print("\nReporte de clasificación:")
        print(classification_report(y_true, y_pred, target_names=self.label_encoder.classes_))

        # Guardar modelo
        self.modelo.save(self.ruta_modelo)
        print(f"Modelo guardado en {self.ruta_modelo}")

        return history

    def cargar_modelo(self):
        if os.path.exists(self.ruta_modelo):
            self.modelo = load_model(self.ruta_modelo)
            self.label_encoder.classes_ = np.load(os.path.join(MODELS_DIR, "label_mapping.npy"), allow_pickle=True)
            self.scaler.mean_ = np.load(os.path.join(MODELS_DIR, "scaler_mean.npy"))
            self.scaler.scale_ = np.load(os.path.join(MODELS_DIR, "scaler_scale.npy"))
            print("Modelo cargado correctamente")
        else:
            raise FileNotFoundError(f"No se encontró el modelo en {self.ruta_modelo}")

    def predecir(self, respuestas):
        if self.modelo is None:
            self.cargar_modelo()

        if len(respuestas) != 60:
            raise ValueError("Debe ingresar exactamente 60 respuestas")

        X = np.array(respuestas).reshape(1, -1)
        X_scaled = self.scaler.transform(X)
        pred = self.modelo.predict(X_scaled, verbose=0)
        tipo_predicho = self.label_encoder.classes_[np.argmax(pred)]
        confianza = np.max(pred) * 100

        return tipo_predicho, confianza


if __name__ == "__main__":
    sistema = SistemaPercepcion()
    sistema.entrenar()
