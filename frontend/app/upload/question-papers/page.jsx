import ProtectedRoute from "../../../src/components/ProtectedRoute.jsx";
import QuestionPaperUpload from "../../../src/features/upload/QuestionPaperUpload.jsx";

export default function Page() {
  return (
    <ProtectedRoute>
      <QuestionPaperUpload />
    </ProtectedRoute>
  );
}
