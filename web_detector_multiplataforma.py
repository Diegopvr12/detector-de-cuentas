# web_detector_multiplataforma.py - VERSIÓN CORREGIDA
import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# Asegurar que podemos importar detector.py
sys.path.append(os.path.dirname(__file__))
from detector import SocialMediaFakeAccountDetector

# Configuración de la página
st.set_page_config(
    page_title="Detector de Cuentas Falsas",
    page_icon="🛡️",
    layout="wide"
)

# Título
st.title("🛡️ DETECTOR DE CUENTAS FALSAS")
st.markdown("---")

# ==============================================
# CARGAR DETECTOR (VERSIÓN CORREGIDA)
# ==============================================
@st.cache_resource
def load_detector():
    """Carga el detector - VERSIÓN SIMPLIFICADA"""
    try:
        detector = SocialMediaFakeAccountDetector(platform='instagram')
        
        # Intentar cargar modelo existente
        try:
            detector.load_model("modelo_deteccion")
            st.sidebar.success("✅ Modelo cargado")
        except:
            with st.sidebar.status("🔄 Entrenando modelo básico..."):
                # Generar datos
                df = detector.generate_synthetic_dataset(n_samples=500)
                
                # Preparar datos
                train, test = detector.prepare_data(df, use_smote=True)
                
                # Entrenar modelo (AHORA RECIBE SOLO 2 VALORES)
                results = detector.train_models(train, test)  # ← CAMBIO IMPORTANTE
                
                # Evaluar
                detector.evaluate_model(test)
                
                # Guardar
                detector.save_model("modelo_deteccion")
                st.sidebar.success("✅ Modelo listo")
        
        return detector
    except Exception as e:
        st.error(f"Error cargando detector: {e}")
        return None

# Cargar detector
detector = load_detector()

if detector is None:
    st.stop()

# ==============================================
# INTERFAZ PRINCIPAL
# ==============================================
st.header("📝 Análisis de cuenta de Instagram")

# Formulario de entrada
with st.form("detector_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("👤 Nombre de usuario:", placeholder="ej: usuario123")
        followers = st.number_input("👥 Seguidores:", min_value=0, value=1000, step=100)
        following = st.number_input("👤 Seguidos:", min_value=0, value=500, step=10)
        posts = st.number_input("📸 Publicaciones:", min_value=0, value=100, step=10)
    
    with col2:
        is_private = st.checkbox("🔒 Cuenta privada")
        is_verified = st.checkbox("✅ Verificada")
        has_photo = st.checkbox("🖼️ Tiene foto de perfil", value=True)
        has_bio = st.checkbox("📝 Tiene biografía", value=True)
        
        likes = st.number_input("❤️ Likes promedio:", min_value=0, value=50)
        comments = st.number_input("💬 Comentarios promedio:", min_value=0, value=5)
        account_age = st.number_input("📅 Días desde creación:", min_value=1, value=365)
    
    # Botón de análisis
    submitted = st.form_submit_button("🔍 ANALIZAR CUENTA", type="primary", use_container_width=True)

# Procesar análisis
if submitted:
    if not username:
        st.warning("⚠️ Por favor ingresa un nombre de usuario")
    else:
        with st.spinner("🤖 Analizando cuenta con Machine Learning..."):
            
            clean_username = username.strip().replace('@', '')
            
            # Calcular ratios
            ratio = followers / (following + 1)
            engagement = (likes + comments) / (followers + 1) * 100
            
            # Preparar características (19 exactamente)
            features = {
                'follower_count': followers,
                'following_count': following,
                'post_count': posts,
                'is_private': 1 if is_private else 0,
                'is_verified': 1 if is_verified else 0,
                'has_profile_pic': 1 if has_photo else 0,
                'has_bio': 1 if has_bio else 0,
                'follower_following_ratio': ratio,
                'avg_likes_per_post': likes,
                'avg_comments_per_post': comments,
                'engagement_rate': engagement,
                'account_age_days': account_age,
                'username_length': len(clean_username),
                'username_has_numbers': 1 if any(c.isdigit() for c in clean_username) else 0,
                'username_has_special_chars': 1 if any(not c.isalnum() for c in clean_username) else 0,
                'bio_length': 100 if has_bio else 0,
                'has_external_url': 0,
                'post_frequency_weekly': posts // 52 if posts > 0 else 0,
                'verified_badge_eligible': 0
            }
            
            # Verificar número de características
            st.write(f"**Características:** {len(features)}")
            
            # Predecir
            result = detector.predict_account(features)
            
            # Mostrar resultados
            st.markdown("---")
            st.header("📊 RESULTADO DEL ANÁLISIS")
            
            # Resultado principal
            col_a, col_b, col_c = st.columns(3)
            with col_b:
                if result['is_fake']:
                    st.error(f"### 🚨 ¡CUENTA SOSPECHOSA!")
                    st.markdown(f"### Probabilidad de ser falsa: **{result['probability_fake']:.1%}**")
                else:
                    st.success(f"### ✅ CUENTA LEGÍTIMA")
                    st.markdown(f"### Probabilidad de ser real: **{result['probability_real']:.1%}**")
                
                st.info(f"**Confianza:** {result['confidence']:.1%}")
            
            # Métricas
            st.subheader("📈 Métricas calculadas")
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("Ratio S/S", f"{ratio:.2f}")
            with col_m2:
                st.metric("Engagement", f"{engagement:.2f}%")
            with col_m3:
                st.metric("Longitud username", len(clean_username))
            with col_m4:
                st.metric("Tiene números", "Sí" if features['username_has_numbers'] else "No")
