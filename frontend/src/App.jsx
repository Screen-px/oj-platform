import { Routes, Route, Navigate } from "react-router-dom";
import ProblemList from "./pages/ProblemList";
import ProblemDetail from "./pages/ProblemDetail";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/problems" replace />} />
      <Route path="/problems" element={<ProblemList />} />
      <Route path="/problems/:id" element={<ProblemDetail />} />
    </Routes>
  );
}
