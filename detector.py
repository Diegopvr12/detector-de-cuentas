# detector.py - VERSIÓN CORREGIDA
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import warnings
warnings.filterwarnings('ignore')

class SocialMediaFakeAccountDetector:
    """
    Sistema de detección de cuentas falsas para Instagram
    """
    
    def __init__(self, platform='instagram'):
        self.platform = platform
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.performance_metrics = {}
        
        # Características fijas para Instagram (19 características)
        self.instagram_features = [
            'follower_count', 'following_count', 'post_count', 
            'is_private', 'is_verified', 'has_profile_pic', 'has_bio',
            'follower_following_ratio', 'avg_likes_per_post', 'avg_comments_per_post',
            'engagement_rate', 'account_age_days', 'username_length',
            'username_has_numbers', 'username_has_special_chars', 'bio_length',
            'has_external_url', 'post_frequency_weekly', 'verified_badge_eligible'
        ]
        
        print(f"[OK] Detector inicializado para {platform}")
        print(f"[OK] Características esperadas: {len(self.instagram_features)}")
    
    def generate_synthetic_dataset(self, n_samples=1000, fake_ratio=0.3):
        """Genera dataset sintético para entrenamiento"""
        np.random.seed(42)
        
        data = []
        labels = []
        
        n_fake = int(n_samples * fake_ratio)
        
        for i in range(n_samples):
            is_fake = i < n_fake
            
            if is_fake:
                # Cuenta falsa
                features = [
                    np.random.randint(0, 500),           # follower_count
                    np.random.randint(500, 5000),        # following_count
                    np.random.randint(0, 20),            # post_count
                    np.random.choice([0, 1], p=[0.3, 0.7]), # is_private
                    0,                                    # is_verified
                    np.random.choice([0, 1], p=[0.4, 0.6]), # has_profile_pic
                    np.random.choice([0, 1], p=[0.6, 0.4]), # has_bio
                    0.1,                                  # follower_following_ratio
                    np.random.randint(0, 50),            # avg_likes_per_post
                    np.random.randint(0, 5),             # avg_comments_per_post
                    0.5,                                  # engagement_rate
                    np.random.randint(1, 180),           # account_age_days
                    np.random.randint(8, 20),            # username_length
                    np.random.choice([0, 1], p=[0.2, 0.8]), # username_has_numbers
                    np.random.choice([0, 1], p=[0.7, 0.3]), # username_has_special_chars
                    np.random.randint(0, 50),            # bio_length
                    0,                                    # has_external_url
                    0,                                    # post_frequency_weekly
                    0                                     # verified_badge_eligible
                ]
            else:
                # Cuenta real
                features = [
                    np.random.randint(1000, 50000),      # follower_count
                    np.random.randint(50, 2000),         # following_count
                    np.random.randint(50, 500),          # post_count
                    np.random.choice([0, 1], p=[0.8, 0.2]), # is_private
                    np.random.choice([0, 1], p=[0.95, 0.05]), # is_verified
                    1,                                    # has_profile_pic
                    1,                                    # has_bio
                    10.0,                                 # follower_following_ratio
                    np.random.randint(100, 1000),        # avg_likes_per_post
                    np.random.randint(10, 100),          # avg_comments_per_post
                    3.0,                                  # engagement_rate
                    np.random.randint(365, 2000),        # account_age_days
                    np.random.randint(5, 15),            # username_length
                    np.random.choice([0, 1], p=[0.6, 0.4]), # username_has_numbers
                    np.random.choice([0, 1], p=[0.9, 0.1]), # username_has_special_chars
                    np.random.randint(50, 300),          # bio_length
                    np.random.choice([0, 1], p=[0.5, 0.5]), # has_external_url
                    np.random.randint(2, 15),            # post_frequency_weekly
                    0                                     # verified_badge_eligible
                ]
            
            data.append(features)
            labels.append(1 if is_fake else 0)
        
        df = pd.DataFrame(data, columns=self.instagram_features)
        df['is_fake'] = labels
        
        print(f"[OK] Dataset generado: {n_samples} muestras")
        return df
    
    def prepare_data(self, df, test_size=0.2, use_smote=True):
        """Prepara datos para entrenamiento"""
        self.feature_columns = [col for col in df.columns if col != 'is_fake']
        X = df[self.feature_columns].values
        y = df['is_fake'].values
        
        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Escalar
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # SMOTE para balancear clases
        if use_smote:
            try:
                from imblearn.over_sampling import SMOTE
                smote = SMOTE(random_state=42)
                X_train_scaled, y_train = smote.fit_resample(X_train_scaled, y_train)
                print(f"[OK] SMOTE aplicado. Clases balanceadas: {np.bincount(y_train)}")
            except:
                print("[WARN] SMOTE no disponible")
        
        print(f"[OK] Datos preparados: Train: {len(X_train_scaled)} | Test: {len(X_test_scaled)}")
        return (X_train_scaled, y_train), (X_test_scaled, y_test)
    
    def train_models(self, train_data, val_data=None):
        """Entrena modelo Random Forest"""
        X_train, y_train = train_data
        
        # Si hay validación, usarla, sino usar train
        if val_data:
            X_val, y_val = val_data
        else:
            X_val, y_val = X_train, y_train
        
        # Modelo Random Forest
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        print("\n[INFO] Entrenando modelo Random Forest...")
        self.model.fit(X_train, y_train)
        
        # Evaluar
        y_pred = self.model.predict(X_val)
        accuracy = accuracy_score(y_val, y_pred)
        
        print(f"[OK] Modelo entrenado. Accuracy: {accuracy:.4f}")
        
        return {'Random Forest': {'accuracy': accuracy, 'model': self.model}}, {}
    
    def evaluate_model(self, test_data):
        """Evalúa el modelo"""
        X_test, y_test = test_data
        
        if self.model is None:
            raise ValueError("Modelo no entrenado")
        
        y_pred = self.model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        self.performance_metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
        
        print(f"\n[RESULTADOS]")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1:.4f}")
        
        return self.performance_metrics
    
    def predict_account(self, account_features):
        """Predice si una cuenta es falsa (versión corregida)"""
        if self.model is None:
            raise ValueError("Modelo no entrenado")
        
        # Asegurar que tenemos las características en el orden correcto
        if isinstance(account_features, dict):
            features_list = []
            for col in self.instagram_features:
                if col in account_features:
                    features_list.append(account_features[col])
                else:
                    # Si falta alguna, usar valor por defecto
                    features_list.append(0)
            
            features = np.array(features_list).reshape(1, -1)
        else:
            features = np.array(account_features).reshape(1, -1)
        
        # Verificar número de características
        if features.shape[1] != len(self.instagram_features):
            raise ValueError(f"Error: Se esperaban {len(self.instagram_features)} características, pero se recibieron {features.shape[1]}")
        
        # Escalar
        if self.scaler:
            features_scaled = self.scaler.transform(features)
        else:
            features_scaled = features
        
        # Predecir
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]
        
        return {
            'is_fake': bool(prediction),
            'probability_fake': float(probability[1]),
            'probability_real': float(probability[0]),
            'confidence': max(probability)
        }
    
    def save_model(self, filepath):
        """Guarda el modelo"""
        model_path = f"{filepath}_model.pkl"
        scaler_path = f"{filepath}_scaler.pkl"
        features_path = f"{filepath}_features.pkl"
        
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
        joblib.dump(self.instagram_features, features_path)
        
        print(f"[OK] Modelo guardado: {model_path}")
    
    def load_model(self, filepath):
        """Carga el modelo"""
        model_path = f"{filepath}_model.pkl"
        scaler_path = f"{filepath}_scaler.pkl"
        features_path = f"{filepath}_features.pkl"
        
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.instagram_features = joblib.load(features_path)
        
        print(f"[OK] Modelo cargado")
        return True
