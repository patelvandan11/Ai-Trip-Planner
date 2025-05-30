import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { FaComment } from 'react-icons/fa';

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [isOpen, setIsOpen] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, loading]);

    const handleSend = async () => {
        if (input.trim()) {
            const userMessage = { text: input, sender: 'user' };
            setMessages(prev => [...prev, userMessage]);
            setInput('');
            setLoading(true);

            try {
                const response = await axios.post('http://localhost:8000/chat', { message: input });
                const botMessage = { text: response.data.reply, sender: 'bot' };
                setMessages(prev => [...prev, botMessage]);
            } catch (error) {
                console.error('Error fetching chatbot response:', error);
                setMessages(prev => [...prev, { text: 'Error: Failed to get response.', sender: 'bot' }]);
            }

            setLoading(false);
        }
    };

    return (
        <div className="fixed bottom-4 right-4 z-50">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="bg-teal-500 text-white p-3 rounded-full shadow-lg focus:outline-none"
            >
                <FaComment size={24} />
            </button>

            {isOpen && (
                <div className="w-80 bg-white shadow-lg border rounded-lg flex flex-col mt-2 max-h-[700px]">
                    <div className="bg-teal-500 text-white p-4 font-bold rounded-t-md">Chatbot</div>

                    <div className="p-3 h-64 overflow-y-auto flex flex-col">
                        {messages.map((message, index) => (
                            <div
                                key={index}
                                className={`p-2 m-1 rounded text-sm ${
                                    message.sender === 'user'
                                        ? 'bg-blue-100 self-end'
                                        : 'bg-gray-200 self-start'
                                }`}
                            >
                                {message.text}
                            </div>
                        ))}
                        {loading && (
                            <div className="text-gray-500 text-sm mt-1">Bot is typing...</div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <div className="flex p-2 border-t">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                            className="flex-grow border p-2 rounded-l focus:outline-none"
                            placeholder="Type a message..."
                        />
                        <button
                            onClick={handleSend}
                            className="bg-teal-500 text-white p-2 rounded-r hover:bg-teal-600"
                        >
                            Send
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Chatbot;
