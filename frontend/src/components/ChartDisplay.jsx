function ChartDisplay({ charts }) {
    if (!charts || !charts.length) return null;
    return (
      <div>
        <h3>Extracted Charts</h3>
        {charts.map((c, i) => (
          <img
            key={i}
            src={`http://localhost:5001/static/${c.split('/').pop()}`}
            alt={`chart${i + 1}`}
            style={{ maxWidth: "250px", margin: "10px" }}
          />
        ))}
      </div>
    );
  }
  export default ChartDisplay;
  