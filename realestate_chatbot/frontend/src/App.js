import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import AnalysisChart from './components/AnalysisChart';
import DataTable from './components/DataTable';

function App() {
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentChartData, setCurrentChartData] = useState(null);
  const [currentTableData, setCurrentTableData] = useState(null);
  
  // Auto-scroll to bottom of chat
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  const handleSend = async () => {
    if (!query.trim()) return;

    const userMessage = { sender: 'user', text: query };
    setChatHistory((prev) => [...prev, userMessage]);
    setLoading(true);
    setQuery(''); // Clear input immediately

    try {
      const res = await axios.post('https://sigmavalue-assignment-i2qy.onrender.com/api/chat/', { query: userMessage.text });
      
      const botMessage = { sender: 'bot', text: res.data.response };
      setChatHistory((prev) => [...prev, botMessage]);
      setCurrentChartData(res.data.chart_data);
      setCurrentTableData(res.data.table_data);
    } catch (error) {
      console.error("Error:", error);
      setChatHistory((prev) => [...prev, { sender: 'bot', text: "Unable to connect to the server." }]);
    }
    setLoading(false);
  };

  return (
    <div className="container-fluid py-4" style={{ maxWidth: '1200px' }}>
      
      {/* Header */}
      <header className="mb-5 text-center">
        <h2 className="fw-bold" style={{ color: '#2c3e50' }}>Real Estate Intelligence</h2>
        <p className="text-muted small">AI-Powered Market Analytics</p>
      </header>

      <div className="row g-4">
        
        {/* Left Column: Chat Interface */}
        <div className="col-lg-4">
          <div className="modern-card d-flex flex-column" style={{ height: '75vh' }}>
            
            {/* Chat History */}
            <div className="flex-grow-1 p-3 chat-window" style={{ overflowY: 'auto' }}>
              {chatHistory.length === 0 && (
                <div className="text-center text-muted mt-5 px-4">
                  <small>Try asking:</small><br/>
                  <em>"Analyze Wakad trends"</em><br/>
                  <em>"Show me data for Akurdi"</em>
                </div>
              )}
              
              {chatHistory.map((msg, index) => (
                <div key={index} className={`d-flex ${msg.sender === 'user' ? 'justify-content-end' : 'justify-content-start'} mb-3`}>
                  <div className={`chat-bubble shadow-sm ${msg.sender === 'user' ? 'chat-user' : 'chat-bot'}`}>
                    {msg.text}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="text-start mb-3">
                  <div className="chat-bubble chat-bot">
                    <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Analyzing data...
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-3 border-top bg-light" style={{ borderBottomLeftRadius: '12px', borderBottomRightRadius: '12px' }}>
              <div className="input-group">
                <input 
                  type="text" 
                  className="form-control modern-input border-0 shadow-none" 
                  placeholder="Ask a question..." 
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                  style={{ backgroundColor: 'white' }}
                />
                <button 
                  className="btn btn-dark px-4" 
                  style={{ borderRadius: '10px', marginLeft: '8px', backgroundColor: '#2c3e50' }}
                  onClick={handleSend} 
                  disabled={loading}
                >
                  <i className="bi bi-send-fill"></i> Send
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Visualization Dashboard */}
        <div className="col-lg-8">
          {(!currentChartData && !currentTableData) ? (
            <div className="h-100 d-flex align-items-center justify-content-center text-muted modern-card" style={{minHeight: '400px', backgroundColor: '#fcfcfc'}}>
              <div className="text-center">
                <h1 className="display-4 text-secondary opacity-25"><i className="bi bi-bar-chart"></i></h1>
                <p>Data visualization will appear here</p>
              </div>
            </div>
          ) : (
            <div className="fade-in">
              {/* Chart Section */}
              <div className="mb-4">
                <AnalysisChart chartData={currentChartData} />
              </div>
              
              {/* Table Section */}
              <div className="modern-card p-4">
                 <h6 className="text-uppercase text-secondary mb-3" style={{letterSpacing: '1px', fontSize: '0.75rem'}}>Detailed Records</h6>
                <DataTable tableData={currentTableData} />
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}

export default App;