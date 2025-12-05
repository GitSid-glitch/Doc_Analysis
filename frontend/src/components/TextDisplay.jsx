function TextDisplay({ text }) {
    if (!text) return null;
    return (
      <div>
        <h3>Extracted Text</h3>
        <pre>{text}</pre>
      </div>
    );
  }
  export default TextDisplay;
  