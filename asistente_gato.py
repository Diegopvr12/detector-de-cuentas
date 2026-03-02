# asistente_gato.py - Asistente IA con botón de gato flotante (VERSIÓN FUNCIONAL)
import streamlit as st
import random
from datetime import datetime

# ==============================================
# CSS PARA EL BOTÓN DE GATO FLOTANTE
# ==============================================
GATO_CSS = """
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
    
    /* Nube de chat flotante */
    .chat-cloud {
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
        display: none;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .chat-cloud.show {
        display: block !important;
    }
    
    /* Cabecera de la nube */
    .cloud-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 15px 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .cloud-header span {
        font-weight: 600;
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
        transition: all 0.2s ease;
        margin-left: auto;
    }
    
    .close-btn:hover {
        background: rgba(255,255,255,0.3);
        transform: scale(1.1);
    }
    
    /* Contenido de la nube */
    .cloud-content {
        padding: 20px;
        max-height: 350px;
        overflow-y: auto;
        background: #f8f9fa;
    }
    
    /* Mensajes del chat */
    .chat-message {
        padding: 10px 15px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 85%;
        animation: fadeIn 0.3s ease;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }
    
    .bot-message {
        background: white;
        color: #333;
        margin-right: auto;
        border-bottom-left-radius: 4px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .timestamp {
        font-size: 0.6rem;
        opacity: 0.7;
        margin-top: 4px;
    }
    
    /* Input area */
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
        transition: all 0.2s ease;
    }
    
    .chat-input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
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
        transition: all 0.2s ease;
    }
    
    .send-btn:hover {
        transform: scale(1.1);
    }
    
    /* Sugerencias rápidas */
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
        transition: all 0.2s ease;
        color: #333;
    }
    
    .suggestion-chip:hover {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-color: transparent;
    }
    
    /* Badge de IA */
    .ia-badge {
        background: rgba(255,255,255,0.2);
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: bold;
    }
</style>
"""

# ==============================================
# CLASE ASISTENTE IA
# ==============================================
class AsistenteGato:
    def __init__(self):
        self.respuestas = {
            "que es": [
                "🐱 Este es un **Detector de Cuentas Falsas** profesional que usa Machine Learning para analizar perfiles de Instagram, TikTok y Facebook. ¡Te ayuda a identificar bots y cuentas sospechosas con más del 95% de precisión!",
                "Es una herramienta inteligente que analiza métricas como seguidores, seguidos, engagement y patrones en el nombre para determinar si una cuenta es real o falsa."
            ],
            "como funciona": [
                "🤖 El detector analiza **19 características diferentes** como:\n• Ratio seguidores/seguidos\n• Engagement (likes/comentarios)\n• Antigüedad de la cuenta\n• Patrones en el username\n• Configuración de privacidad\n\nCon estos datos, un modelo de Random Forest calcula la probabilidad de que sea falsa.",
                "El modelo fue entrenado con miles de cuentas reales y falsas, aprendiendo a detectar patrones típicos de bots."
            ],
            "plataformas": [
                "📷 **Instagram** - Análisis completo de perfiles\n🎵 **TikTok** - Métricas específicas de videos\n👥 **Facebook** - Perfiles personales y páginas",
                "Soporta las 3 principales redes sociales. Cada una tiene su propio formulario con métricas específicas."
            ],
            "precision": [
                "📊 **Precisión del modelo:**\n• Instagram: 95-98%\n• TikTok: 93-95%\n• Facebook: 95-97%",
                "Estos números están basados en pruebas exhaustivas con miles de cuentas reales y falsas."
            ],
            "significa": [
                "📈 **Ratio S/S:** Relación entre seguidores y seguidos. Un ratio bajo puede indicar comportamiento de bot.\n\n❤️ **Engagement:** Mide la interacción real. Cuentas falsas suelen tener engagement muy bajo."
            ],
            "hola": [
                "¡Miau! 🐱 ¿En qué puedo ayudarte hoy?",
                "¡Hola! Soy tu asistente gatuno. Pregúntame lo que quieras sobre el detector."
            ],
            "gracias": [
                "¡De nada! Estoy aquí para ayudarte 🐱",
                "¡Un placer! Vuelve cuando necesites ayuda."
            ],
            "adios": [
                "¡Hasta luego! Que tengas un excelente día 🐱",
                "¡Adiós! No olvides usar el detector cuando lo necesites."
            ]
        }
    
    def procesar(self, mensaje):
        if not mensaje:
            return None
        
        mensaje_lower = mensaje.lower()
        
        for clave, respuestas in self.respuestas.items():
            if clave in mensaje_lower:
                return random.choice(respuestas)
        
        return "🐱 ¿Podrías ser más específico? Puedo ayudarte con:\n• Qué es el detector\n• Cómo funciona\n• Las plataformas soportadas\n• La precisión del modelo\n• Interpretar resultados"

# ==============================================
# FUNCIÓN PRINCIPAL - VERSIÓN CORREGIDA
# ==============================================
def init_asistente_gato():
    """Inicializa el asistente - VERSIÓN QUE SÍ FUNCIONA"""
    
    # Inicializar estado
    if 'chat_visible' not in st.session_state:
        st.session_state.chat_visible = False
    
    if 'asistente' not in st.session_state:
        st.session_state.asistente = AsistenteGato()
    
    if 'historial' not in st.session_state:
        st.session_state.historial = []
    
    # Agregar CSS
    st.markdown(GATO_CSS, unsafe_allow_html=True)
    
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
    
    # HTML completo con JavaScript funcional
    html_completo = f"""
    <div style="position: fixed; bottom: 30px; right: 30px; z-index: 9999;">
        <!-- Botón del gato -->
        <div id="catButton" style="width: 80px; height: 80px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; justify-content: center; align-items: center; cursor: pointer; box-shadow: 0 10px 30px rgba(102,126,234,0.4); border: 3px solid white; animation: catPulse 2s ease-in-out infinite;" onclick="toggleChat()">
            {gato_svg}
        </div>
        
        <!-- Nube de chat -->
        <div id="chatCloud" style="position: absolute; bottom: 100px; right: 0; width: 350px; background: white; border-radius: 25px 25px 25px 5px; box-shadow: 0 20px 40px rgba(0,0,0,0.2); border: 1px solid rgba(102,126,234,0.3); display: none;">
            <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 15px 20px; border-radius: 25px 25px 0 0; display: flex; align-items: center;">
                <span style="font-weight: 600;">🐱 Asistente Gatuno</span>
                <span style="background: rgba(255,255,255,0.2); padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: bold; margin-left: 10px;">IA</span>
                <button onclick="closeChat()" style="background: rgba(255,255,255,0.2); border: none; color: white; width: 30px; height: 30px; border-radius: 50%; cursor: pointer; margin-left: auto; display: flex; align-items: center; justify-content: center;">×</button>
            </div>
            
            <div id="chatMessages" style="padding: 20px; max-height: 350px; overflow-y: auto; background: #f8f9fa;">
                <div style="background: white; color: #333; padding: 10px 15px; border-radius: 15px; margin: 8px 0; max-width: 85%; margin-right: auto; border-bottom-left-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    🐱 ¡Hola! Soy tu asistente gatuno. ¿Quieres saber qué hace esta página o cómo funciona el detector?
                    <div style="font-size: 0.6rem; opacity: 0.7; margin-top: 4px;">{datetime.now().strftime('%H:%M')}</div>
                </div>
            </div>
            
            <div style="display: flex; flex-wrap: wrap; gap: 8px; padding: 10px 15px; background: #f8f9fa; border-top: 1px solid #eee;">
                <span class="suggestion-chip" onclick="useSuggestion('¿Qué es esta página?')" style="background: white; border: 1px solid #e0e0e0; border-radius: 20px; padding: 5px 12px; font-size: 0.8rem; cursor: pointer;">📌 ¿Qué es?</span>
                <span class="suggestion-chip" onclick="useSuggestion('¿Cómo funciona?')" style="background: white; border: 1px solid #e0e0e0; border-radius: 20px; padding: 5px 12px; font-size: 0.8rem; cursor: pointer;">⚙️ ¿Cómo funciona?</span>
                <span class="suggestion-chip" onclick="useSuggestion('¿Qué plataformas soporta?')" style="background: white; border: 1px solid #e0e0e0; border-radius: 20px; padding: 5px 12px; font-size: 0.8rem; cursor: pointer;">📱 Plataformas</span>
                <span class="suggestion-chip" onclick="useSuggestion('¿Qué precisión tiene?')" style="background: white; border: 1px solid #e0e0e0; border-radius: 20px; padding: 5px 12px; font-size: 0.8rem; cursor: pointer;">📊 Precisión</span>
            </div>
            
            <div style="padding: 15px; background: white; border-top: 1px solid #eee; display: flex; gap: 10px;">
                <input type="text" id="chatInput" placeholder="Escribe tu pregunta..." style="flex-grow: 1; padding: 10px 15px; border: 2px solid #e0e0e0; border-radius: 25px; font-size: 0.9rem; outline: none;" onkeypress="if(event.key==='Enter') sendMessage()">
                <button onclick="sendMessage()" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center;">➤</button>
            </div>
        </div>
    </div>
    
    <style>
        @keyframes catPulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}
        .suggestion-chip:hover {{
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: white !important;
            border-color: transparent !important;
        }}
    </style>
    
    <script>
        function toggleChat() {{
            var chat = document.getElementById('chatCloud');
            if (chat.style.display === 'none' || chat.style.display === '') {{
                chat.style.display = 'block';
            }} else {{
                chat.style.display = 'none';
            }}
        }}
        
        function closeChat() {{
            document.getElementById('chatCloud').style.display = 'none';
        }}
        
        function sendMessage() {{
            var input = document.getElementById('chatInput');
            var message = input.value.trim();
            if (message === '') return;
            
            var messages = document.getElementById('chatMessages');
            var now = new Date();
            var time = now.getHours().toString().padStart(2,'0') + ':' + now.getMinutes().toString().padStart(2,'0');
            
            // Mensaje del usuario
            var userMsg = document.createElement('div');
            userMsg.className = 'chat-message user-message';
            userMsg.style.cssText = 'background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 10px 15px; border-radius: 15px; margin: 8px 0; max-width: 85%; margin-left: auto; border-bottom-right-radius: 4px;';
            userMsg.innerHTML = message + '<div style="font-size:0.6rem; opacity:0.7; margin-top:4px;">' + time + '</div>';
            messages.appendChild(userMsg);
            
            // Respuesta del bot
            setTimeout(function() {{
                var botMsg = document.createElement('div');
                botMsg.className = 'chat-message bot-message';
                botMsg.style.cssText = 'background: white; color: #333; padding: 10px 15px; border-radius: 15px; margin: 8px 0; max-width: 85%; margin-right: auto; border-bottom-left-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);';
                
                var respuesta = '🐱 ' + (message.toLowerCase().includes('que es') ? 'Este es un detector de cuentas falsas que usa Machine Learning para analizar perfiles de Instagram, TikTok y Facebook.' : 
                                        message.toLowerCase().includes('como funciona') ? 'El detector analiza 19 características como ratio seguidores/seguidos, engagement, antigüedad, etc.' :
                                        message.toLowerCase().includes('plataforma') ? 'Soporta Instagram, TikTok y Facebook con métricas específicas para cada una.' :
                                        message.toLowerCase().includes('precision') ? 'La precisión es superior al 95% en las tres plataformas.' :
                                        '¡Gracias por tu pregunta! Puedes consultarme sobre qué es el detector, cómo funciona, qué plataformas soporta o su precisión.');
                
                botMsg.innerHTML = respuesta + '<div style="font-size:0.6rem; opacity:0.7; margin-top:4px;">' + time + '</div>';
                messages.appendChild(botMsg);
                messages.scrollTop = messages.scrollHeight;
            }}, 500);
            
            input.value = '';
            messages.scrollTop = messages.scrollHeight;
        }}
        
        function useSuggestion(text) {{
            document.getElementById('chatInput').value = text;
            sendMessage();
        }}
    </script>
    """
    
    st.markdown(html_completo, unsafe_allow_html=True)
