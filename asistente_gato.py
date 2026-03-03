# asistente_gato.py - Asistente IA con botón de gato flotante (VERSIÓN CORREGIDA)
import streamlit as st
import random
from datetime import datetime

def init_asistente_gato():
    """Inicializa el asistente - VERSIÓN CORREGIDA"""
    
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
        
        /* Cabecera */
        .cloud-header {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 20px;
            display: flex;
            align-items: center;
            gap: 10px;
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
        .chat-message {
            padding: 10px 15px;
            border-radius: 15px;
            margin: 8px 0;
            max-width: 85%;
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
        .suggestion-chip {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 20px;
            padding: 5px 12px;
            font-size: 0.8rem;
            cursor: pointer;
            display: inline-block;
            margin: 4px;
        }
        
        .suggestion-chip:hover {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .ia-badge {
            background: rgba(255,255,255,0.2);
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: bold;
        }
    </style>
    
    <!-- SVG del gato -->
    <svg style="display: none;">
        <defs>
            <g id="cat-face">
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
            </g>
        </defs>
    </svg>
    
    <!-- Botón de gato -->
    <div class="cat-button" onclick="toggleChat()">
        <svg width="60" height="60" viewBox="0 0 60 60">
            <use href="#cat-face"/>
        </svg>
    </div>
    
    <!-- Nube de chat -->
    <div class="chat-cloud" id="chatCloud">
        <div class="cloud-header">
            <span>🐱 Asistente Gatuno</span>
            <span class="ia-badge">IA</span>
            <button class="close-btn" onclick="closeChat()">×</button>
        </div>
        
        <div class="chat-messages" id="chatMessages" style="padding: 20px; max-height: 350px; overflow-y: auto; background: #f8f9fa;">
            <div class="chat-message bot-message" style="background: white; padding: 10px 15px; border-radius: 15px; margin: 8px 0; max-width: 85%;">
                🐱 ¡Hola! Soy tu asistente gatuno. ¿Quieres saber qué hace esta página o cómo funciona el detector?
                <div class="timestamp" style="font-size:0.6rem; opacity:0.7; margin-top:4px;">12:00</div>
            </div>
        </div>
        
        <div style="display: flex; flex-wrap: wrap; gap: 8px; padding: 10px 15px; background: #f8f9fa; border-top: 1px solid #eee;">
            <span class="suggestion-chip" onclick="useSuggestion('¿Qué es esta página?')">📌 ¿Qué es?</span>
            <span class="suggestion-chip" onclick="useSuggestion('¿Cómo funciona?')">⚙️ ¿Cómo funciona?</span>
            <span class="suggestion-chip" onclick="useSuggestion('¿Qué plataformas soporta?')">📱 Plataformas</span>
            <span class="suggestion-chip" onclick="useSuggestion('¿Qué precisión tiene?')">📊 Precisión</span>
        </div>
        
        <div class="chat-input-area">
            <input type="text" class="chat-input" id="chatInput" placeholder="Escribe tu pregunta...">
            <button class="send-btn" onclick="sendMessage()">➤</button>
        </div>
    </div>
    
    <script>
        function toggleChat() {
            var chat = document.getElementById('chatCloud');
            if (chat.style.display === 'none' || chat.style.display === '') {
                chat.style.display = 'block';
            } else {
                chat.style.display = 'none';
            }
        }
        
        function closeChat() {
            document.getElementById('chatCloud').style.display = 'none';
        }
        
        function sendMessage() {
            var input = document.getElementById('chatInput');
            var message = input.value.trim();
            if (message === '') return;
            
            var messages = document.querySelector('.chat-messages');
            var now = new Date();
            var time = now.getHours().toString().padStart(2,'0') + ':' + now.getMinutes().toString().padStart(2,'0');
            
            // Mensaje del usuario
            var userMsg = document.createElement('div');
            userMsg.className = 'chat-message user-message';
            userMsg.style.cssText = 'background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 10px 15px; border-radius: 15px; margin: 8px 0; max-width: 85%; margin-left: auto;';
            userMsg.innerHTML = message + '<div style="font-size:0.6rem; opacity:0.7; margin-top:4px;">' + time + '</div>';
            messages.appendChild(userMsg);
            
            // Respuesta del bot
            setTimeout(function() {
                var botMsg = document.createElement('div');
                botMsg.className = 'chat-message bot-message';
                botMsg.style.cssText = 'background: white; color: #333; padding: 10px 15px; border-radius: 15px; margin: 8px 0; max-width: 85%; margin-right: auto; box-shadow: 0 2px 5px rgba(0,0,0,0.05);';
                
                var respuesta = '🐱 ';
                if (message.toLowerCase().includes('que es') || message.toLowerCase().includes('qué es')) {
                    respuesta += 'Este es un detector de cuentas falsas que usa Machine Learning para analizar perfiles de Instagram, TikTok y Facebook con más del 95% de precisión.';
                } else if (message.toLowerCase().includes('como funciona') || message.toLowerCase().includes('cómo funciona')) {
                    respuesta += 'El detector analiza 19 características como ratio seguidores/seguidos, engagement, antigüedad de la cuenta, patrones en el nombre, etc.';
                } else if (message.toLowerCase().includes('plataforma')) {
                    respuesta += 'Soporta Instagram, TikTok y Facebook con métricas específicas para cada plataforma.';
                } else if (message.toLowerCase().includes('precision') || message.toLowerCase().includes('precisión')) {
                    respuesta += 'La precisión es superior al 95% en Instagram y Facebook, y 93-95% en TikTok.';
                } else {
                    respuesta += '¡Gracias por tu pregunta! Puedes consultarme sobre qué es el detector, cómo funciona, qué plataformas soporta o su precisión.';
                }
                
                botMsg.innerHTML = respuesta + '<div style="font-size:0.6rem; opacity:0.7; margin-top:4px;">' + time + '</div>';
                messages.appendChild(botMsg);
                messages.scrollTop = messages.scrollHeight;
            }, 500);
            
            input.value = '';
            messages.scrollTop = messages.scrollHeight;
        }
        
        function useSuggestion(text) {
            document.getElementById('chatInput').value = text;
            sendMessage();
        }
    </script>
    """, unsafe_allow_html=True)
