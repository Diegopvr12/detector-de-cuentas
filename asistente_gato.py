# asistente_gato.py - Asistente IA con botón de gato flotante (VERSIÓN FUNCIONAL)
import streamlit as st
import random
from datetime import datetime

def init_asistente_gato():
    """Inicializa el asistente - VERSIÓN QUE SÍ FUNCIONA"""
    
    # Inicializar estados en session_state
    if 'mostrar_chat' not in st.session_state:
        st.session_state.mostrar_chat = False
    
    if 'mensajes_chat' not in st.session_state:
        st.session_state.mensajes_chat = [
            {"tipo": "bot", "texto": "🐱 ¡Hola! Soy tu asistente gatuno. ¿Quieres saber qué hace esta página o cómo funciona el detector?"}
        ]
    
    # CSS para el botón y la nube
    st.markdown("""
    <style>
        /* Botón flotante de gato */
        .cat-button {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
            z-index: 9998;
            border: 3px solid white;
            animation: catPulse 2s ease-in-out infinite;
        }
        
        .cat-button:hover {
            transform: scale(1.1) rotate(5deg);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
        }
        
        @keyframes catPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        /* Nube de chat */
        .chat-container {
            position: fixed;
            bottom: 120px;
            right: 30px;
            width: 350px;
            max-height: 500px;
            background: white;
            border-radius: 25px 25px 25px 5px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            z-index: 9999;
            overflow: hidden;
            border: 1px solid rgba(102, 126, 234, 0.3);
        }
        
        /* Cabecera */
        .chat-header {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 20px;
            display: flex;
            align-items: center;
        }
        
        .chat-header span {
            font-weight: 600;
        }
        
        .ia-badge {
            background: rgba(255,255,255,0.2);
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: bold;
            margin-left: 10px;
        }
        
        .close-btn {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-left: auto;
            transition: all 0.2s ease;
        }
        
        .close-btn:hover {
            background: rgba(255,255,255,0.3);
            transform: scale(1.1);
        }
        
        /* Mensajes */
        .chat-messages {
            padding: 20px;
            max-height: 350px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        
        .message {
            padding: 10px 15px;
            border-radius: 15px;
            margin: 8px 0;
            max-width: 85%;
            word-wrap: break-word;
        }
        
        .user-message {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            margin-left: auto;
        }
        
        .bot-message {
            background: white;
            color: #333;
            margin-right: auto;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        .timestamp {
            font-size: 0.6rem;
            opacity: 0.7;
            margin-top: 4px;
        }
        
        /* Input */
        .chat-input-area {
            padding: 15px;
            background: white;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
        }
        
        .chat-input {
            flex-grow: 1;
            padding: 10px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 0.9rem;
            outline: none;
        }
        
        .chat-input:focus {
            border-color: #667eea;
        }
        
        .send-btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Sugerencias */
        .suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 10px 15px;
            background: #f8f9fa;
            border-top: 1px solid #eee;
        }
        
        .suggestion-chip {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 20px;
            padding: 5px 12px;
            font-size: 0.8rem;
            cursor: pointer;
            display: inline-block;
            transition: all 0.2s ease;
        }
        
        .suggestion-chip:hover {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # SVG del gato
    gato_svg = """
    <svg width="60" height="60" viewBox="0 0 60 60">
        <circle cx="30" cy="30" r="22" fill="white" stroke="#764ba2" stroke-width="2"/>
        <polygon points="18,15 22,10 26,15" fill="white" stroke="#764ba2" stroke-width="1.5"/>
        <polygon points="34,15 38,10 42,15" fill="white" stroke="#764ba2" stroke-width="1.5"/>
        <circle cx="22" cy="26" r="3" fill="#764ba2"/>
        <circle cx="38" cy="26" r="3" fill="#764ba2"/>
        <circle cx="22" cy="26" r="1.5" fill="white"/>
        <circle cx="38" cy="26" r="1.5" fill="white"/>
        <polygon points="30,32 28,30 32,30" fill="#ff69b4"/>
        <line x1="15" y1="32" x2="8" y2="30" stroke="#764ba2" stroke-width="1" opacity="0.5"/>
        <line x1="15" y1="35" x2="8" y2="35" stroke="#764ba2" stroke-width="1" opacity="0.5"/>
        <line x1="45" y1="32" x2="52" y2="30" stroke="#764ba2" stroke-width="1" opacity="0.5"/>
        <line x1="45" y1="35" x2="52" y2="35" stroke="#764ba2" stroke-width="1" opacity="0.5"/>
    </svg>
    """
    
    # Botón de gato (usando botón de Streamlit con HTML)
    col1, col2, col3 = st.columns([10, 1, 1])
    with col2:
        if st.button("🐱", key="gato_btn", help="Abrir asistente"):
            st.session_state.mostrar_chat = not st.session_state.mostrar_chat
            st.rerun()
    
    # Nube de chat (solo si mostrar_chat es True)
    if st.session_state.mostrar_chat:
        with st.container():
            st.markdown("""
            <div style="position: fixed; bottom: 120px; right: 30px; width: 350px; z-index: 9999;">
            """, unsafe_allow_html=True)
            
            # Cabecera
            col_c1, col_c2, col_c3 = st.columns([6, 1, 1])
            with col_c1:
                st.markdown("🐱 **Asistente Gatuno**")
            with col_c2:
                st.markdown("`IA`")
            with col_c3:
                if st.button("✕", key="close_chat"):
                    st.session_state.mostrar_chat = False
                    st.rerun()
            
            # Mensajes
            for msg in st.session_state.mensajes_chat:
                if msg["tipo"] == "bot":
                    st.info(msg["texto"])
                else:
                    st.success(msg["texto"])
            
            # Sugerencias
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            with col_s1:
                if st.button("📌 ¿Qué es?", key="q1"):
                    st.session_state.mensajes_chat.append({"tipo": "usuario", "texto": "¿Qué es esta página?"})
                    st.session_state.mensajes_chat.append({"tipo": "bot", "texto": "🐱 Este es un detector de cuentas falsas que usa Machine Learning para analizar perfiles de Instagram, TikTok y Facebook con más del 95% de precisión."})
                    st.rerun()
            with col_s2:
                if st.button("⚙️ ¿Cómo funciona?", key="q2"):
                    st.session_state.mensajes_chat.append({"tipo": "usuario", "texto": "¿Cómo funciona?"})
                    st.session_state.mensajes_chat.append({"tipo": "bot", "texto": "🤖 El detector analiza 19 características como ratio seguidores/seguidos, engagement, antigüedad de la cuenta, patrones en el nombre, etc."})
                    st.rerun()
            with col_s3:
                if st.button("📱 Plataformas", key="q3"):
                    st.session_state.mensajes_chat.append({"tipo": "usuario", "texto": "¿Qué plataformas soporta?"})
                    st.session_state.mensajes_chat.append({"tipo": "bot", "texto": "📷 Soporta Instagram, 🎵 TikTok y 👥 Facebook con métricas específicas para cada plataforma."})
                    st.rerun()
            with col_s4:
                if st.button("📊 Precisión", key="q4"):
                    st.session_state.mensajes_chat.append({"tipo": "usuario", "texto": "¿Qué precisión tiene?"})
                    st.session_state.mensajes_chat.append({"tipo": "bot", "texto": "📊 La precisión es superior al 95% en Instagram y Facebook, y 93-95% en TikTok."})
                    st.rerun()
            
            # Input de texto
            pregunta = st.text_input("Escribe tu pregunta:", key="pregunta_input")
            if st.button("Enviar", key="enviar_btn") and pregunta:
                st.session_state.mensajes_chat.append({"tipo": "usuario", "texto": pregunta})
                
                # Respuesta automática
                if "que es" in pregunta.lower() or "qué es" in pregunta.lower():
                    respuesta = "🐱 Este es un detector de cuentas falsas que usa Machine Learning para analizar perfiles de Instagram, TikTok y Facebook."
                elif "como funciona" in pregunta.lower() or "cómo funciona" in pregunta.lower():
                    respuesta = "🤖 El detector analiza 19 características como ratio seguidores/seguidos, engagement, antigüedad de la cuenta, patrones en el nombre, etc."
                elif "plataforma" in pregunta.lower():
                    respuesta = "📷 Soporta Instagram, 🎵 TikTok y 👥 Facebook con métricas específicas."
                elif "precision" in pregunta.lower() or "precisión" in pregunta.lower():
                    respuesta = "📊 Precisión superior al 95% en Instagram y Facebook, 93-95% en TikTok."
                else:
                    respuesta = "🐱 ¡Gracias por tu pregunta! Puedes consultarme sobre qué es el detector, cómo funciona, qué plataformas soporta o su precisión."
                
                st.session_state.mensajes_chat.append({"tipo": "bot", "texto": respuesta})
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
