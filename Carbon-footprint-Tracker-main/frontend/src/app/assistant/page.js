"use client";

import { useState, useEffect, useRef } from "react";
import Sidebar from "@/components/Sidebar";
import api from "@/lib/api";
import styles from "./assistant.module.css";
import { Send, User as UserIcon, Bot, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";

export default function AssistantPage() {
  const [messages, setMessages] = useState([
    { role: "assistant", text: "Hello! I'm your Smart Carbon Assistant. How can I help you reduce your footprint today?" }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleAction = async (action) => {
    if (action.type === 'log_emission' && action.payload) {
      try {
        await api.post("/emissions/", action.payload);
        setMessages(prev => [...prev, { role: "assistant", text: "Done! I've logged that activity for you. 🌿" }]);
      } catch (err) {
        setMessages(prev => [...prev, { role: "assistant", text: "Sorry, I had trouble logging that. Please try again." }]);
      }
    }
    // Handle other navigate-only actions via Router if needed
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg = input;
    setInput("");
    setMessages(prev => [...prev, { role: "user", text: userMsg }]);
    setIsLoading(true);

    try {
      const res = await api.post("/assistant/chat", { message: userMsg });
      setMessages(prev => [...prev, { 
        role: "assistant", 
        text: res.data.text,
        actions: res.data.actions || []
      }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: "assistant", text: "I'm sorry, I'm having trouble connecting right now." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.layout}>
      <Sidebar />
      <main className={styles.content}>
        <div className={styles.chatContainer}>
          <header className={styles.header}>
            <div className={styles.botInfo}>
              <div className={styles.botAvatar}>
                <Bot size={24} />
              </div>
              <div>
                <h1>Smart Assistant</h1>
                <p>Rule-based Intelligent Advice</p>
              </div>
            </div>
          </header>

          <div className={styles.messages} ref={scrollRef}>
            {messages.map((m, i) => (
              <div key={i} className={cn(styles.messageLine, m.role === 'user' ? styles.userLine : styles.botLine)}>
                <div className={styles.avatar}>
                  {m.role === 'user' ? <UserIcon size={18} /> : <Bot size={18} />}
                </div>
                <div className={styles.bubble}>
                  <div className={styles.text}>{m.text}</div>
                  
                  {m.actions && m.actions.length > 0 && (
                    <div className={styles.actions}>
                      {m.actions.map((action, ai) => (
                        <button 
                          key={ai} 
                          className={styles.actionBtn}
                          onClick={() => handleAction(action)}
                        >
                          <span>{action.label}</span>
                          <ArrowRight size={14} />
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className={styles.loading}>
                <span></span><span></span><span></span>
              </div>
            )}
          </div>

          <form className={styles.inputArea} onSubmit={handleSend}>
            <input 
              type="text" 
              placeholder="Ask me: 'How am I doing this month?' or 'I drove 50km'..." 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading}>
              <Send size={20} />
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
