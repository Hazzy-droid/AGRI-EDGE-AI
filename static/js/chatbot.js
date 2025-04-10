// Climate-Smart Agriculture Platform - AI Chatbot Assistant

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const chatbox = document.getElementById('chatbox');
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatToggle = document.getElementById('chat-toggle');
    const chatContainer = document.getElementById('chat-container');
    const closeChat = document.getElementById('close-chat');
    const contextSelector = document.getElementById('context-selector');
    
    // Chat state
    let conversationHistory = [];
    let currentContext = 'general_farming';
    
    // Initialize chatbot
    function initChatbot() {
        // Add welcome message
        addBotMessage("👋 Hello! I'm your Climate-Smart Agriculture assistant. How can I help with your farming questions today?");
        
        // Event listeners
        if (sendButton) {
            sendButton.addEventListener('click', sendMessage);
        }
        
        if (messageInput) {
            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        }
        
        if (chatToggle) {
            chatToggle.addEventListener('click', toggleChat);
        }
        
        if (closeChat) {
            closeChat.addEventListener('click', toggleChat);
        }
        
        if (contextSelector) {
            contextSelector.addEventListener('change', function() {
                currentContext = this.value;
                
                // Add context-switch notification
                const contextLabels = {
                    'general_farming': 'General Farming Advice',
                    'weather': 'Weather Interpretation',
                    'soil_health': 'Soil Health Management',
                    'crop_advice': 'Crop-Specific Advice',
                    'livestock': 'Livestock Management',
                    'platform_help': 'Platform Help'
                };
                
                addSystemMessage(`Context switched to: ${contextLabels[currentContext]}`);
            });
        }
    }
    
    // Toggle chat visibility
    function toggleChat() {
        if (chatContainer) {
            chatContainer.classList.toggle('chat-hidden');
            
            // If opening the chat, scroll to bottom
            if (!chatContainer.classList.contains('chat-hidden')) {
                scrollToBottom();
            }
        }
    }
    
    // Send message to backend
    function sendMessage() {
        if (!messageInput || !messageInput.value.trim()) return;
        
        const userMessage = messageInput.value.trim();
        
        // Add user message to chat
        addUserMessage(userMessage);
        
        // Clear input
        messageInput.value = '';
        
        // Add typing indicator
        const typingElement = addTypingIndicator();
        
        // Update conversation history
        conversationHistory.push({
            role: "user",
            content: userMessage
        });
        
        // Call backend API
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: userMessage,
                context: currentContext,
                conversation_history: conversationHistory.slice(-10) // Only send last 10 messages
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            if (typingElement) {
                typingElement.remove();
            }
            
            if (data.success) {
                // Add bot response to chat
                addBotMessage(data.message);
                
                // Update conversation history
                conversationHistory.push({
                    role: "assistant",
                    content: data.message
                });
                
                // Add citations if available
                if (data.citations && data.citations.length > 0) {
                    addCitations(data.citations);
                }
            } else {
                // Add error message
                addSystemMessage(`Sorry, I encountered an error: ${data.error || 'Unable to process your request'}`);
            }
        })
        .catch(error => {
            // Remove typing indicator
            if (typingElement) {
                typingElement.remove();
            }
            
            // Add error message
            addSystemMessage('Sorry, there was a connection problem. Please try again later.');
            console.error('Error:', error);
        });
    }
    
    // Add user message to chat
    function addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message user-message';
        
        const avatar = document.createElement('div');
        avatar.className = 'chat-avatar';
        avatar.innerHTML = '<i class="fas fa-user"></i>';
        
        const content = document.createElement('div');
        content.className = 'chat-content';
        content.textContent = message;
        
        messageElement.appendChild(avatar);
        messageElement.appendChild(content);
        
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Add bot message to chat
    function addBotMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message bot-message';
        
        const avatar = document.createElement('div');
        avatar.className = 'chat-avatar';
        avatar.innerHTML = '<i class="fas fa-robot"></i>';
        
        const content = document.createElement('div');
        content.className = 'chat-content';
        content.innerHTML = formatMessage(message);
        
        messageElement.appendChild(avatar);
        messageElement.appendChild(content);
        
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Add system message to chat
    function addSystemMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'chat-message system-message';
        messageElement.textContent = message;
        
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Add typing indicator
    function addTypingIndicator() {
        const element = document.createElement('div');
        element.className = 'chat-message bot-message typing-indicator';
        
        const avatar = document.createElement('div');
        avatar.className = 'chat-avatar';
        avatar.innerHTML = '<i class="fas fa-robot"></i>';
        
        const content = document.createElement('div');
        content.className = 'chat-content';
        content.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
        
        element.appendChild(avatar);
        element.appendChild(content);
        
        chatMessages.appendChild(element);
        scrollToBottom();
        
        return element;
    }
    
    // Add citations to chat
    function addCitations(citations) {
        if (!citations || citations.length === 0) return;
        
        const citationsElement = document.createElement('div');
        citationsElement.className = 'chat-citations';
        
        const citationsTitle = document.createElement('div');
        citationsTitle.className = 'citations-title';
        citationsTitle.textContent = 'Sources:';
        
        const citationsList = document.createElement('ol');
        citationsList.className = 'citations-list';
        
        citations.forEach((citation, index) => {
            const citationItem = document.createElement('li');
            
            // Check if citation is a URL or text
            if (typeof citation === 'string' && (citation.startsWith('http://') || citation.startsWith('https://'))) {
                const citationLink = document.createElement('a');
                citationLink.href = citation;
                citationLink.target = '_blank';
                citationLink.textContent = `Source ${index + 1}`;
                citationItem.appendChild(citationLink);
            } else {
                citationItem.textContent = citation;
            }
            
            citationsList.appendChild(citationItem);
        });
        
        citationsElement.appendChild(citationsTitle);
        citationsElement.appendChild(citationsList);
        
        chatMessages.appendChild(citationsElement);
        scrollToBottom();
    }
    
    // Format message with markdown-like syntax
    function formatMessage(message) {
        // Replace URLs with links
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        message = message.replace(urlRegex, function(url) {
            return `<a href="${url}" target="_blank">${url}</a>`;
        });
        
        // Add line breaks
        message = message.replace(/\n/g, '<br>');
        
        // Bold text (with *)
        message = message.replace(/\*([^*]+)\*/g, '<strong>$1</strong>');
        
        // Italic text (with _)
        message = message.replace(/\_([^_]+)\_/g, '<em>$1</em>');
        
        // List items
        message = message.replace(/^\s*[\-\*]\s+(.*)/gm, '<li>$1</li>');
        
        // Wrap list items in ul tags
        if (message.includes('<li>')) {
            message = '<ul>' + message + '</ul>';
            // Fix nested ul tags
            message = message.replace(/<\/ul>(\s*)<ul>/g, '$1');
        }
        
        return message;
    }
    
    // Scroll chat to bottom
    function scrollToBottom() {
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    // Quick responses
    const quickResponses = [
        {
            text: "How do I improve soil fertility?",
            context: "soil_health"
        },
        {
            text: "Best practices for maize growing?",
            context: "crop_advice"
        },
        {
            text: "How to manage drought?",
            context: "weather"
        },
        {
            text: "Signs of tomato diseases?",
            context: "crop_advice"
        }
    ];
    
    // Add quick responses to UI
    function addQuickResponses() {
        const quickResponsesContainer = document.getElementById('quick-responses');
        if (!quickResponsesContainer) return;
        
        quickResponses.forEach(response => {
            const button = document.createElement('button');
            button.className = 'btn btn-sm btn-outline-primary quick-response-btn';
            button.textContent = response.text;
            button.dataset.context = response.context;
            
            button.addEventListener('click', function() {
                if (contextSelector && response.context) {
                    contextSelector.value = response.context;
                    currentContext = response.context;
                }
                
                messageInput.value = response.text;
                sendMessage();
            });
            
            quickResponsesContainer.appendChild(button);
        });
    }
    
    // Initialize the chatbot
    initChatbot();
    addQuickResponses();
});