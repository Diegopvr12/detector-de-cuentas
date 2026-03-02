"""
SISTEMA DE DETECCIÓN DE CUENTAS FALSAS PARA INSTAGRAM
Versión CORREGIDA - Sin errores
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                           f1_score, roc_auc_score, confusion_matrix)
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
import joblib
import warnings
warnings.filterwarnings('ignore')


class SocialMediaFakeAccountDetector:
    """
    Sistema de detección de cuentas falsas para Instagram.
    """
    
    def __init__(self, platform='instagram'):
        """
        Inicializa el detector.
        """
        self.platform = platform.lower()
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.performance_metrics = {}
        
        # Características para Instagram
        self.platform_features = {
            'instagram': [
                'follower_count', 'following_count', 'post_count', 
                'is_private', 'is_verified', 'has_profile_pic', 'has_bio',
                'follower_following_ratio', 'avg_likes_per_post', 'avg_comments_per_post',
                'engagement_rate', 'account_age_days', 'username_length',
                'username_has_numbers', 'username_has_special_chars', 'bio_length',
                'has_external_url', 'post_frequency_weekly', 'verified_badge_eligible'
            ]
        }
        
        print(f"[OK] Detector inicializado para {self.platform.upper()}")
    
    def generate_synthetic_dataset(self, n_samples=1000, fake_ratio=0.3, random_state=42):
        """
        Genera un dataset sintético para entrenamiento.
        """
        np.random.seed(random_state)
        
        features = self.platform_features[self.platform]
        n_features = len(features)
        
        # Inicializar matrices
        data = np.zeros((n_samples, n_features))
        labels = np.zeros(n_samples)
        
        # Determinar número de cuentas falsas
        n_fake = int(n_samples * fake_ratio)
        fake_indices = np.random.choice(n_samples, n_fake, replace=False)
        
        # Generar características
        for i in range(n_samples):
            is_fake = i in fake_indices
            labels[i] = 1 if is_fake else 0
            data[i] = self._generate_instagram_features(is_fake)
        
        # Crear DataFrame
        df = pd.DataFrame(data, columns=features)
        df['is_fake'] = labels.astype(int)
        
        print(f"[OK] Dataset generado: {n_samples} muestras")
        print(f"    Reales: {n_samples - n_fake} | Falsas: {n_fake}")
        
        return df
    
    def _generate_instagram_features(self, is_fake):
        """Genera características para Instagram"""
        if is_fake:
            # Patrones de cuentas falsas
            follower_count = np.random.randint(0, 500) if np.random.random() < 0.7 else np.random.randint(500, 5000)
            following_count = np.random.randint(500, 5000) if follower_count < 500 else np.random.randint(0, 500)
            post_count = np.random.randint(0, 20)
            is_private = np.random.choice([0, 1], p=[0.3, 0.7])
            is_verified = 0
            has_profile_pic = np.random.choice([0, 1], p=[0.4, 0.6])
            has_bio = np.random.choice([0, 1], p=[0.6, 0.4])
            avg_likes = np.random.randint(0, 50) if post_count > 0 else 0
            avg_comments = np.random.randint(0, 5) if post_count > 0 else 0
            account_age = np.random.randint(1, 180)
            username_len = np.random.randint(8, 20)
            username_has_numbers = np.random.choice([0, 1], p=[0.2, 0.8])
            username_has_special = np.random.choice([0, 1], p=[0.7, 0.3])
            bio_len = np.random.randint(0, 50) if has_bio else 0
            has_url = np.random.choice([0, 1], p=[0.8, 0.2])
            post_freq = np.random.randint(0, 2)
        else:
            # Patrones de cuentas reales
            follower_count = np.random.randint(100, 50000)
            following_count = np.random.randint(50, 2000)
            while following_count > follower_count * 1.5 and follower_count > 1000:
                following_count = np.random.randint(50, 2000)
            
            post_count = np.random.randint(10, 500)
            is_private = np.random.choice([0, 1], p=[0.8, 0.2])
            is_verified = np.random.choice([0, 1], p=[0.95, 0.05])
            has_profile_pic = np.random.choice([0, 1], p=[0.05, 0.95])
            has_bio = np.random.choice([0, 1], p=[0.1, 0.9])
            avg_likes = np.random.randint(10, 1000) if post_count > 0 else 0
            avg_comments = np.random.randint(1, 50) if post_count > 0 else 0
            account_age = np.random.randint(180, 2000)
            username_len = np.random.randint(5, 15)
            username_has_numbers = np.random.choice([0, 1], p=[0.6, 0.4])
            username_has_special = np.random.choice([0, 1], p=[0.9, 0.1])
            bio_len = np.random.randint(50, 300) if has_bio else 0
            has_url = np.random.choice([0, 1], p=[0.5, 0.5])
            post_freq = np.random.randint(1, 15)
        
        # Calcular ratios
        follower_following_ratio = follower_count / (following_count + 1)
        engagement_rate = (avg_likes + avg_comments) / (follower_count + 1) * 100
        
        return [
            follower_count, following_count, post_count,
            is_private, is_verified, has_profile_pic, has_bio,
            follower_following_ratio, avg_likes, avg_comments,
            engagement_rate, account_age, username_len,
            username_has_numbers, username_has_special, bio_len,
            has_url, post_freq, is_verified
        ]
    
    def prepare_data(self, df, target_col='is_fake', test_size=0.2, val_size=0.1, use_smote=True):
        """
        Prepara los datos para entrenamiento.
        """
        self.feature_columns = [col for col in df.columns if col != target_col]
        X = df[self.feature_columns].values
        y = df[target_col].values
        
        # Dividir en train+val y test
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Dividir train_temp en train y val
        val_relative_size = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_relative_size, random_state=42, stratify=y_temp
        )
        
        # Escalar características
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Aplicar SMOTE
        if use_smote:
            smote = SMOTE(random_state=42)
            X_train_scaled, y_train = smote.fit_resample(X_train_scaled, y_train)
            print(f"[OK] SMOTE aplicado. Clases balanceadas: {np.bincount(y_train)}")
        
        print(f"\n[INFO] Datos preparados:")
        print(f"    Train: {len(X_train_scaled)} muestras")
        print(f"    Validación: {len(X_val_scaled)} muestras")
        print(f"    Test: {len(X_test_scaled)} muestras")
        
        return (X_train_scaled, y_train), (X_val_scaled, y_val), (X_test_scaled, y_test)
    
    def train_models(self, train_data, val_data):
        """
        Entrena múltiples modelos y selecciona el mejor.
        VERSIÓN CORREGIDA - Devuelve 2 valores
        """
        X_train, y_train = train_data
        X_val, y_val = val_data
        
        models = {
            'Random Forest': RandomForestClassifier(
                n_estimators=200, 
                max_depth=15,
                random_state=42,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=150,
                max_depth=5,
                random_state=42
            ),
            'XGBoost': XGBClassifier(
                n_estimators=200,
                max_depth=6,
                random_state=42,
                use_label_encoder=False,
                eval_metric='logloss'
            )
        }
        
        results = {}
        trained_models = {}
        
        print("\n" + "="*50)
        print("ENTRENANDO MODELOS")
        print("="*50)
        
        for name, model in models.items():
            print(f"\n>> Entrenando {name}...")
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_val)
            
            accuracy = accuracy_score(y_val, y_pred)
            precision = precision_score(y_val, y_pred)
            recall = recall_score(y_val, y_pred)
            f1 = f1_score(y_val, y_pred)
            
            print(f"    Accuracy: {accuracy:.4f}")
            print(f"    Precision: {precision:.4f}")
            print(f"    Recall: {recall:.4f}")
            print(f"    F1-Score: {f1:.4f}")
            
            results[name] = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'model': model
            }
            trained_models[name] = model
        
        # Seleccionar mejor modelo por F1
        best_model_name = max(results, key=lambda x: results[x]['f1'])
        self.model = results[best_model_name]['model']
        
        print(f"\n[OK] Mejor modelo: {best_model_name}")
        print(f"    F1-Score: {results[best_model_name]['f1']:.4f}")
        
        # DEVOLVEMOS 2 VALORES (NO 3)
        return results, trained_models
    
    def evaluate_model(self, test_data):
        """
        Evalúa el modelo final.
        """
        X_test, y_test = test_data
        
        if self.model is None:
            raise ValueError("Primero debe entrenar un modelo")
        
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)[:, 1]
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_proba)
        
        cm = confusion_matrix(y_test, y_pred)
        
        self.performance_metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': cm
        }
        
        print("\n" + "="*50)
        print("EVALUACIÓN FINAL")
        print("="*50)
        print(f"Accuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1-Score:  {f1:.4f}")
        print(f"ROC-AUC:   {roc_auc:.4f}")
        print(f"\nMatriz de Confusión:")
        print(f"    VP: {cm[1,1]} | FN: {cm[1,0]}")
        print(f"    FP: {cm[0,1]} | VN: {cm[0,0]}")
        
        return self.performance_metrics
    
    def predict_account(self, account_features):
        """
        Predice si una cuenta es falsa o real.
        VERSIÓN MEJORADA - Maneja mejor los diccionarios
        """
        if self.model is None:
            raise ValueError("Primero debe entrenar un modelo")
        
        # Si es diccionario, convertir a array en el orden correcto
        if isinstance(account_features, dict):
            features_list = []
            missing_features = []
            
            for col in self.feature_columns:
                if col in account_features:
                    features_list.append(account_features[col])
                else:
                    # Si falta alguna característica, poner 0
                    features_list.append(0)
                    missing_features.append(col)
            
            if missing_features:
                print(f"[AVISO] Características faltantes: {missing_features}")
            
            features = np.array(features_list).reshape(1, -1)
        else:
            features = np.array(account_features).reshape(1, -1)
        
        # Escalar
        features_scaled = self.scaler.transform(features)
        
        # Predecir
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]
        
        result = {
            'is_fake': bool(prediction),
            'probability_fake': float(probability[1]),
            'probability_real': float(probability[0]),
            'confidence': max(probability)
        }
        
        return result
    
    def save_model(self, filepath):
        """
        Guarda el modelo entrenado.
        """
        model_path = f"{filepath}_{self.platform}_model.pkl"
        scaler_path = f"{filepath}_{self.platform}_scaler.pkl"
        features_path = f"{filepath}_{self.platform}_features.pkl"
        
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
        joblib.dump(self.feature_columns, features_path)
        
        print(f"[OK] Modelo guardado: {model_path}")
        print(f"[OK] Scaler guardado: {scaler_path}")
        print(f"[OK] Features guardadas: {features_path}")
    
    def load_model(self, filepath):
        """
        Carga un modelo guardado.
        """
        model_path = f"{filepath}_{self.platform}_model.pkl"
        scaler_path = f"{filepath}_{self.platform}_scaler.pkl"
        features_path = f"{filepath}_{self.platform}_features.pkl"
        
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.feature_columns = joblib.load(features_path)
            print(f"[OK] Modelo cargado: {model_path}")
            print(f"[OK] Características: {len(self.feature_columns)}")
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo cargar el modelo: {e}")
            return False