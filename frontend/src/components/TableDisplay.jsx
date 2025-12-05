function TableDisplay({ tables }) {
    if (!tables || !tables.length) return null;
    return (
      <div>
        <h3>Table Summaries</h3>
        {tables.map((table, i) => (
          <pre key={i}>{JSON.stringify(table, null, 2)}</pre>
        ))}
      </div>
    );
  }
  export default TableDisplay;
  