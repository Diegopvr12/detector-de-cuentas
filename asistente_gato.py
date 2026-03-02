# asistente_gato.py - Asistente IA con botón de gato flotante
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
    
    /* Cara de gato en SVG */
    .cat-face {
        width: 60px;
        height: 60px;
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
        animation: slideIn 0.3s ease;
    }
    
    .chat-cloud.show {
        display: block;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
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
    
    .cloud-header h4 {
        margin: 0;
        flex-grow: 1;
        font-size: 1.1rem;
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
# SVG DE LA CARA DE GATO
# ==============================================
GATO_SVG = """
<svg class="cat-face" viewBox="0 0 60 60">
    <!-- Cabeza del gato -->
    <circle cx="30" cy="30" r="22" fill="white" stroke="#764ba2" stroke-width="2"/>
    
    <!-- Orejas -->
    <polygon points="18,15 22,10 26,15" fill="white" stroke="#764ba2" stroke-width="1.5"/>
    <polygon points="34,15 38,10 42,15" fill="white" stroke="#764ba2" stroke-width="1.5"/>
    
    <!-- Ojos -->
    <circle cx="22" cy="26" r="3" fill="#764ba2"/>
    <circle cx="38" cy="26" r="3" fill="#764ba2"/>
    
    <!-- Pupilas -->
    <circle cx="22" cy="26" r="1.5" fill="white"/>
    <circle cx="38" cy="26" r="1.5" fill="white"/>
    
    <!-- Nariz -->
    <polygon points="30,32 28,30 32,30" fill="#ff69b4"/>
    
    <!-- Bigotes (opcional) -->
    <line x1="15" y1="32" x2="8" y2="30" stroke="#764ba2" stroke-width="1" opacity="0.5"/>
    <line x1="15" y1="35" x2="8" y2="35" stroke="#764ba2" stroke-width="1" opacity="0.5"/>
    <line x1="45" y1="32" x2="52" y2="30" stroke="#764ba2" stroke-width="1" opacity="0.5"/>
    <line x1="45" y1="35" x2="52" y2="35" stroke="#764ba2" stroke-width="1" opacity="0.5"/>
</svg>
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
                "El modelo fue entrenado con miles de cuentas reales y falsas, aprendiendo a detectar patrones típicos de bots. La precisión supera el 95% en las tres plataformas."
            ],
            "plataformas": [
                "📷 **Instagram** - Análisis completo de perfiles\n🎵 **TikTok** - Métricas específicas de videos\n👥 **Facebook** - Perfiles personales y páginas",
                "Soporta las 3 principales redes sociales. Cada una tiene su propio formulario con métricas específicas optimizadas para esa plataforma."
            ],
            "precision": [
                "📊 **Precisión del modelo:**\n• Instagram: 95-98%\n• TikTok: 93-95%\n• Facebook: 95-97%\n\nEstos números están basados en pruebas exhaustivas con miles de cuentas."
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
        
        # Respuesta por defecto
        return "🐱 ¿Podrías ser más específico? Puedo ayudarte con:\n• Qué es el detector\n• Cómo funciona\n• Las plataformas soportadas\n• La precisión del modelo\n• Interpretar resultados"

# ==============================================
# FUNCIÓN PRINCIPAL - LLAMA A ESTO EN TU APP
# ==============================================
def agregar_asistente_gato():
    """Agrega el botón de gato flotante y el asistente a la página"""
    
    # Inicializar estado
    if 'chat_visible' not in st.session_state:
        st.session_state.chat_visible = False
    
    if 'asistente' not in st.session_state:
        st.session_state.asistente = AsistenteGato()
    
    if 'historial' not in st.session_state:
        st.session_state.historial = []
    
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0
    
    # Agregar CSS
    st.markdown(GATO_CSS, unsafe_allow_html=True)
    
    # Botón de gato flotante
    cat_button_html = f"""
    <div class="cat-button" onclick="toggleChat()" id="catButton">
        {GATO_SVG}
    </div>
    """
    st.markdown(cat_button_html, unsafe_allow_html=True)
    
    # JavaScript para controlar la visibilidad
    js_code = """
    <script>
    function toggleChat() {
        const chat = document.getElementById('chatCloud');
        if (chat) {
            chat.classList.toggle('show');
        }
    }
    
    function closeChat() {
        const chat = document.getElementById('chatCloud');
        if (chat) {
            chat.classList.remove('show');
        }
    }
    
    function sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value;
        if (message.trim()) {
            // Disparar evento de Streamlit
            const event = new CustomEvent('streamlit:message', {
                detail: {
                    type: 'chat_message',
                    message: message
                }
            });
            window.dispatchEvent(event);
            input.value = '';
        }
    }
    
    function handleKeyPress(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    }
    
    function useSuggestion(text) {
        const input = document.getElementById('chatInput');
        input.value = text;
        sendMessage();
    }
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)
    
    # Nube de chat
    with st.container():
        chat_html = f"""
        <div class="chat-cloud {'show' if st.session_state.chat_visible else ''}" id="chatCloud">
            <div class="cloud-header">
                <span>🐱 Asistente Gatuno</span>
                <span class="ia-badge">IA</span>
                <button class="close-btn" onclick="closeChat()">×</button>
            </div>
            
            <div class="cloud-content" id="chatMessages">
        """
        
        # Agregar mensajes del historial
        for msg in st.session_state.historial:
            if msg['tipo'] == 'usuario':
                chat_html += f"""
                <div class="chat-message user-message">
                    {msg['texto']}
                    <div class="timestamp">{msg['hora']}</div>
                </div>
                """
            else:
                chat_html += f"""
                <div class="chat-message bot-message">
                    {msg['texto']}
                    <div class="timestamp">{msg['hora']}</div>
                </div>
                """
        
        # Si no hay historial, agregar mensaje de bienvenida
        if not st.session_state.historial:
            bienvenida = "🐱 ¡Hola! Soy tu asistente gatuno. ¿Quieres saber qué hace esta página o cómo funciona el detector?"
            chat_html += f"""
            <div class="chat-message bot-message">
                {bienvenida}
                <div class="timestamp">{datetime.now().strftime('%H:%M')}</div>
            </div>
            """
            st.session_state.historial.append({
                'tipo': 'bot',
                'texto': bienvenida,
                'hora': datetime.now().strftime('%H:%M')
            })
        
        chat_html += """
            </div>
            
            <div class="suggestions">
                <span class="suggestion-chip" onclick="useSuggestion('¿Qué es esta página?')">📌 ¿Qué es?</span>
                <span class="suggestion-chip" onclick="useSuggestion('¿Cómo funciona?')">⚙️ ¿Cómo funciona?</span>
                <span class="suggestion-chip" onclick="useSuggestion('¿Qué plataformas soporta?')">📱 Plataformas</span>
                <span class="suggestion-chip" onclick="useSuggestion('¿Qué precisión tiene?')">📊 Precisión</span>
            </div>
            
            <div class="chat-input-area">
                <input type="text" class="chat-input" id="chatInput" placeholder="Escribe tu pregunta..." onkeypress="handleKeyPress(event)">
                <button class="send-btn" onclick="sendMessage()">➤</button>
            </div>
        </div>
        """
        
        st.markdown(chat_html, unsafe_allow_html=True)
    
    # Manejar mensajes del usuario (parte de Streamlit)
    def handle_chat():
        if 'chat_message' in st.session_state:
            mensaje = st.session_state.chat_message
            if mensaje:
                # Agregar mensaje del usuario
                st.session_state.historial.append({
                    'tipo': 'usuario',
                    'texto': mensaje,
                    'hora': datetime.now().strftime('%H:%M')
                })
                
                # Obtener respuesta
                respuesta = st.session_state.asistente.procesar(mensaje)
                
                # Agregar respuesta del bot
                st.session_state.historial.append({
                    'tipo': 'bot',
                    'texto': respuesta,
                    'hora': datetime.now().strftime('%H:%M')
                })
                
                # Limpiar
                st.session_state.chat_message = ""
                st.rerun()
    
    handle_chat()

# ==============================================
# FUNCIÓN PARA INTEGRAR EN CUALQUIER PÁGINA
# ==============================================
def init_asistente_gato():
    """Inicializa el asistente - Llama a esto en tu página principal"""
    agregar_asistente_gato()

# ==============================================
# EJEMPLO DE USO (si se ejecuta directamente)
# ==============================================
if __name__ == "__main__":
    st.set_page_config(
        page_title="Asistente Gatuno",
        page_icon="🐱"
    )
    
    st.title("🐱 Asistente Gatuno - Demostración")
    st.write("Este es un asistente flotante. Busca el botón de gato en la esquina inferior derecha.")
    
    init_asistente_gato()