import React, { useState } from "react";
import axios from "axios";

function QABox({ context }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question) return;
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5001/ask", {
        question,
        snippet: context,
      });
      setAnswer(res.data.answer);
    } catch {
      alert("Failed to get answer");
    }
    setLoading(false);
  };

  return (
    <div>
      <input
        type="text"
        value={question}
        onChange={e => setQuestion(e.target.value)}
        placeholder="Ask a question"
        style={{ width: "70%", marginRight: "1em" }}
      />
      <button onClick={handleAsk} disabled={loading}>
        {loading ? "Asking..." : "Ask"}
      </button>
      {answer && (
        <div>
          <h4>AI Answer</h4>
          <pre>{answer}</pre>
        </div>
      )}
    </div>
  );
}
export default QABox;
