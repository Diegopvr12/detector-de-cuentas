# asistente_gato.py - Botón circular con gato dibujado
import streamlit as st
from datetime import datetime

def init_asistente_gato():
    """Inicializa el asistente con botón circular de gato"""
    
    # Inicializar estados
    if 'chat_abierto' not in st.session_state:
        st.session_state.chat_abierto = False
    
    if 'mensajes_chat' not in st.session_state:
        st.session_state.mensajes_chat = [
            {"tipo": "bot", "texto": "🐱 ¡Hola! Soy tu asistente gatuno. ¿Quieres saber qué hace esta página o cómo funciona el detector?"}
        ]
    
    # CSS personalizado
    st.markdown("""
    <style>
        /* Botón circular con gato */
        .gato-boton {
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
            z-index: 9998;
            border: 3px solid white;
            animation: flotar 3s ease-in-out infinite;
            transition: all 0.3s ease;
        }
        
        .gato-boton:hover {
            transform: scale(1.1) rotate(5deg);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
        }
        
        @keyframes flotar {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        
        /* Nube de chat */
        .chat-nube {
            position: fixed;
            bottom: 120px;
            right: 30px;
            width: 380px;
            background: white;
            border-radius: 25px 25px 25px 5px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            z-index: 9999;
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
        
        /* Botón de cerrar con gato pequeño */
        .gato-cerrar {
            width: 30px;
            height: 30px;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            margin-left: auto;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: all 0.2s ease;
        }
        
        .gato-cerrar:hover {
            background: rgba(255,255,255,0.3);
            transform: scale(1.1);
        }
        
        .gato-cerrar svg {
            width: 20px;
            height: 20px;
        }
        
        .gato-cerrar path, .gato-cerrar circle {
            stroke: white;
            fill: white;
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
    
    # SVG del gato para el botón principal
    gato_principal_svg = """
    <svg width="50" height="50" viewBox="0 0 50 50">
        <!-- Cabeza -->
        <circle cx="25" cy="25" r="15" fill="white" stroke="white" stroke-width="2"/>
        
        <!-- Orejas -->
        <polygon points="15,12 20,8 23,12" fill="white" stroke="white" stroke-width="1.5"/>
        <polygon points="35,12 30,8 27,12" fill="white" stroke="white" stroke-width="1.5"/>
        
        <!-- Ojos -->
        <circle cx="20" cy="23" r="3" fill="#764ba2"/>
        <circle cx="30" cy="23" r="3" fill="#764ba2"/>
        <circle cx="21" cy="22" r="1" fill="white"/>
        <circle cx="31" cy="22" r="1" fill="white"/>
        
        <!-- Nariz -->
        <polygon points="25,28 24,26 26,26" fill="#ff69b4"/>
        
        <!-- Bigotes -->
        <line x1="15" y1="26" x2="8" y2="25" stroke="white" stroke-width="1"/>
        <line x1="15" y1="28" x2="8" y2="28" stroke="white" stroke-width="1"/>
        <line x1="35" y1="26" x2="42" y2="25" stroke="white" stroke-width="1"/>
        <line x1="35" y1="28" x2="42" y2="28" stroke="white" stroke-width="1"/>
        
        <!-- Sonrisa -->
        <path d="M20,32 Q25,35 30,32" stroke="white" stroke-width="1.5" fill="none"/>
    </svg>
    """
    
    # SVG del gato pequeño para cerrar
    gato_cerrar_svg = """
    <svg width="20" height="20" viewBox="0 0 20 20">
        <circle cx="10" cy="10" r="6" fill="white" stroke="white" stroke-width="1"/>
        <circle cx="7" cy="8" r="1.5" fill="#764ba2"/>
        <circle cx="13" cy="8" r="1.5" fill="#764ba2"/>
        <polygon points="10,12 9,11 11,11" fill="#ff69b4"/>
    </svg>
    """
    
    # Botón circular con gato
    gato_html = f"""
    <div class="gato-boton" onclick="toggleChat()">
        {gato_principal_svg}
    </div>
    
    <script>
    function toggleChat() {{
        const event = new CustomEvent('chat_toggle');
        window.dispatchEvent(event);
    }}
    </script>
    """
    
    st.markdown(gato_html, unsafe_allow_html=True)
    
    # Capturar clic del gato
    col1, col2, col3 = st.columns([10, 1, 1])
    with col2:
        if st.button(" ", key="gato_click", help="Abrir asistente"):
            st.session_state.chat_abierto = not st.session_state.chat_abierto
            st.rerun()
    
    # Mostrar chat si está abierto
    if st.session_state.chat_abierto:
        st.markdown('<div class="chat-nube">', unsafe_allow_html=True)
        
        # Cabecera con gato para cerrar
        col_h1, col_h2, col_h3 = st.columns([6, 2, 2])
        with col_h1:
            st.markdown("🐱 **Asistente Gatuno**")
        with col_h2:
            st.markdown("`IA`")
        with col_h3:
            # Botón de cerrar con gato
            cerrar_html = f"""
            <div class="gato-cerrar" onclick="closeChat()">
                {gato_cerrar_svg}
            </div>
            <script>
            function closeChat() {{
                const event = new CustomEvent('chat_close');
                window.dispatchEvent(event);
            }}
            </script>
            """
            st.markdown(cerrar_html, unsafe_allow_html=True)
            if st.button(" ", key="cerrar_click"):
                st.session_state.chat_abierto = False
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
                st.session_state.mensajes_chat.append({"tipo": "bot", "texto": "📷 Soporta Instagram, 🎵 TikTok y 👥 Facebook con métricas específicas."})
                st.rerun()
        with col_s4:
            if st.button("📊 Precisión", key="q4"):
                st.session_state.mensajes_chat.append({"tipo": "usuario", "texto": "¿Qué precisión tiene?"})
                st.session_state.mensajes_chat.append({"tipo": "bot", "texto": "📊 Precisión superior al 95% en Instagram y Facebook, 93-95% en TikTok."})
                st.rerun()
        
        # Input de texto
        pregunta = st.text_input("Escribe tu pregunta:", key="input_pregunta")
        if st.button("Enviar", key="enviar") and pregunta:
            st.session_state.mensajes_chat.append({"tipo": "usuario", "texto": pregunta})
            
            # Respuestas automáticas
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
        
        st.markdown('</div>', unsafe_allow_html=True)
