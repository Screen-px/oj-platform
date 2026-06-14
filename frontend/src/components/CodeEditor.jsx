import MonacoEditor from "@monaco-editor/react";

export default function CodeEditor({ value, onChange }) {
  return (
    <MonacoEditor
      height="100%"
      language="python"
      theme="vs-dark"
      value={value}
      onChange={(v) => onChange(v || "")}
      options={{
        fontSize: 14,
        lineNumbers: "on",
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        padding: { top: 10 },
        automaticLayout: true,
        tabSize: 4,
        insertSpaces: true,
      }}
    />
  );
}
