import { useState } from "react";
import FileUpload from "./components/FileUpload";
import TextDisplay from "./components/TextDisplay";
import TableDisplay from "./components/TableDisplay";
import ChartDisplay from "./components/ChartDisplay";
import QABox from "./components/QBX";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div style={{ padding: 40 }}>
      <h1>AI Document Analyzer</h1>
      <FileUpload onResult={setResult} />
      {result && (
        <>
          <TextDisplay text={result.text} />
          <TableDisplay tables={result.tables} />
          <ChartDisplay charts={result.charts} />
          <QABox context={result.text} />
        </>
      )}
    </div>
  );
}
export default App;
