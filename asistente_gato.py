# asistente_gato.py - Gato dibujado a mano flotante con chat
import streamlit as st
import random
from datetime import datetime

def init_asistente_gato():
    """Inicializa el asistente con gato flotante dibujado a mano"""
    
    # Inicializar estados
    if 'mostrar_chat_gato' not in st.session_state:
        st.session_state.mostrar_chat_gato = False
    
    if 'mensajes_gato' not in st.session_state:
        st.session_state.mensajes_gato = [
            {"tipo": "bot", "texto": "🐱 ¡Hola! Soy tu asistente gatuno. ¿Quieres saber qué hace esta página o cómo funciona el detector?"}
        ]
    
    # CSS para el gato flotante
    st.markdown("""
    <style>
        /* Gato flotante dibujado a mano */
        .gato-flotante {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 100px;
            height: 100px;
            cursor: pointer;
            z-index: 9999;
            filter: drop-shadow(0 10px 15px rgba(0,0,0,0.3));
            transition: transform 0.3s ease;
            animation: float 3s ease-in-out infinite;
        }
        
        .gato-flotante:hover {
            transform: scale(1.1) rotate(5deg);
        }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        
        /* Nube de chat */
        .nube-chat {
            position: fixed;
            bottom: 140px;
            right: 30px;
            width: 350px;
            background: white;
            border-radius: 25px 25px 25px 5px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            z-index: 10000;
            overflow: hidden;
            border: 2px solid #667eea;
            animation: aparecer 0.3s ease;
        }
        
        @keyframes aparecer {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .chat-header {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 20px;
            display: flex;
            align-items: center;
        }
        
        .chat-header span {
            font-weight: bold;
            font-size: 1.1rem;
        }
        
        .ia-badge {
            background: rgba(255,255,255,0.2);
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.8rem;
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
            margin-left: auto;
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }
        
        .close-btn:hover {
            background: rgba(255,255,255,0.3);
            transform: scale(1.1);
        }
        
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
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .timestamp {
            font-size: 0.6rem;
            opacity: 0.7;
            margin-top: 4px;
        }
        
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
            border: 1px solid #667eea;
            border-radius: 20px;
            padding: 5px 12px;
            font-size: 0.8rem;
            cursor: pointer;
            color: #667eea;
            transition: all 0.2s ease;
        }
        
        .suggestion-chip:hover {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Gato dibujado a mano en SVG
    gato_dibujado = """
    <svg class="gato-flotante" viewBox="0 0 100 100" onclick="toggleChatGato()">
        <!-- Cabeza del gato (dibujada a mano) -->
        <circle cx="50" cy="50" r="30" fill="none" stroke="#764ba2" stroke-width="3" stroke-dasharray="5,3" />
        
        <!-- Orejas (dibujadas a mano) -->
        <path d="M30,25 L20,10 L35,20" fill="none" stroke="#764ba2" stroke-width="3" stroke-dasharray="4,2" />
        <path d="M70,25 L80,10 L65,20" fill="none" stroke="#764ba2" stroke-width="3" stroke-dasharray="4,2" />
        
        <!-- Ojos (expresivos) -->
        <circle cx="40" cy="45" r="5" fill="#764ba2" />
        <circle cx="60" cy="45" r="5" fill="#764ba2" />
        <circle cx="42" cy="43" r="2" fill="white" />
        <circle cx="62" cy="43" r="2" fill="white" />
        
        <!-- Pupilas (dibujadas a mano) -->
        <line x1="40" y1="48" x2="44" y2="48" stroke="white" stroke-width="1" />
        <line x1="60" y1="48" x2="64" y2="48" stroke="white" stroke-width="1" />
        
        <!-- Nariz (triangulito) -->
        <polygon points="50,55 48,52 52,52" fill="#ff69b4" />
        
        <!-- Bigotes (dibujados a mano) -->
        <line x1="30" y1="55" x2="15" y2="50" stroke="#764ba2" stroke-width="1.5" stroke-dasharray="3,2" />
        <line x1="30" y1="58" x2="15" y2="58" stroke="#764ba2" stroke-width="1.5" stroke-dasharray="3,2" />
        <line x1="70" y1="55" x2="85" y2="50" stroke="#764ba2" stroke-width="1.5" stroke-dasharray="3,2" />
        <line x1="70" y1="58" x2="85" y2="58" stroke="#764ba2" stroke-width="1.5" stroke-dasharray="3,2" />
        
        <!-- Sonrisa (dibujada a mano) -->
        <path d="M40,65 Q50,72 60,65" fill="none" stroke="#764ba2" stroke-width="2" stroke-dasharray="4,2" />
        
        <!-- Patitas (dibujadas a mano) -->
        <ellipse cx="35" cy="80" rx="8" ry="5" fill="none" stroke="#764ba2" stroke-width="2" stroke-dasharray="3,2" />
        <ellipse cx="65" cy="80" rx="8" ry="5" fill="none" stroke="#764ba2" stroke-width="2" stroke-dasharray="3,2" />
        
        <!-- Cola (dibujada a mano) -->
        <path d="M85,50 Q95,40 90,30" fill="none" stroke="#764ba2" stroke-width="3" stroke-dasharray="5,3" />
    </svg>
    """
    
    # JavaScript para manejar el clic
    st.markdown("""
    <script>
    function toggleChatGato() {
        // Enviar evento a Streamlit
        const event = new CustomEvent('streamlit:chat_toggle');
        window.dispatchEvent(event);
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Mostrar el gato
    st.markdown(gato_dibujado, unsafe_allow_html=True)
    
    # Botón invisible de Streamlit para capturar el clic
    if st.button(" ", key="gato_clic", help="Haz clic en el gato"):
        st.session_state.mostrar_chat_gato = not st.session_state.mostrar_chat_gato
        st.rerun()
    
    # Nube de chat (si está activa)
    if st.session_state.mostrar_chat_gato:
        with st.container():
            st.markdown('<div class="nube-chat">', unsafe_allow_html=True)
            
            # Cabecera
            col1, col2, col3 = st.columns([6, 2, 1])
            with col1:
                st.markdown("🐱 **Asistente Gatuno**")
            with col2:
                st.markdown("`IA`")
            with col3:
                if st.button("✕", key="cerrar_chat"):
                    st.session_state.mostrar_chat_gato = False
                    st.rerun()
            
            # Mensajes
            for msg in st.session_state.mensajes_gato:
                if msg["tipo"] == "bot":
                    st.info(msg["texto"])
                else:
                    st.success(msg["texto"])
            
            # Sugerencias
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            with col_s1:
                if st.button("📌 ¿Qué es?", key="gato_q1"):
                    st.session_state.mensajes_gato.append({"tipo": "usuario", "texto": "¿Qué es esta página?"})
                    st.session_state.mensajes_gato.append({"tipo": "bot", "texto": "🐱 Este es un detector de cuentas falsas que usa Machine Learning para analizar perfiles de Instagram, TikTok y Facebook con más del 95% de precisión."})
                    st.rerun()
            with col_s2:
                if st.button("⚙️ ¿Cómo funciona?", key="gato_q2"):
                    st.session_state.mensajes_gato.append({"tipo": "usuario", "texto": "¿Cómo funciona?"})
                    st.session_state.mensajes_gato.append({"tipo": "bot", "texto": "🤖 El detector analiza 19 características como ratio seguidores/seguidos, engagement, antigüedad de la cuenta, patrones en el nombre, etc."})
                    st.rerun()
            with col_s3:
                if st.button("📱 Plataformas", key="gato_q3"):
                    st.session_state.mensajes_gato.append({"tipo": "usuario", "texto": "¿Qué plataformas soporta?"})
                    st.session_state.mensajes_gato.append({"tipo": "bot", "texto": "📷 Soporta Instagram, 🎵 TikTok y 👥 Facebook con métricas específicas."})
                    st.rerun()
            with col_s4:
                if st.button("📊 Precisión", key="gato_q4"):
                    st.session_state.mensajes_gato.append({"tipo": "usuario", "texto": "¿Qué precisión tiene?"})
                    st.session_state.mensajes_gato.append({"tipo": "bot", "texto": "📊 Precisión superior al 95% en Instagram y Facebook, 93-95% en TikTok."})
                    st.rerun()
            
            # Input de texto
            pregunta = st.text_input("Escribe tu pregunta:", key="gato_input")
            if st.button("Enviar", key="gato_enviar") and pregunta:
                st.session_state.mensajes_gato.append({"tipo": "usuario", "texto": pregunta})
                
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
                
                st.session_state.mensajes_gato.append({"tipo": "bot", "texto": respuesta})
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
