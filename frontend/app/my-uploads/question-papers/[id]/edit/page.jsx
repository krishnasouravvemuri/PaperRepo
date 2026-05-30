import ProtectedRoute from "../../../../../src/components/ProtectedRoute.jsx";
import EditQuestionPaper from "../../../../../src/features/myUploads/EditQuestionPaper.jsx";

export default function Page() {
  return (
    <ProtectedRoute>
      <EditQuestionPaper />
    </ProtectedRoute>
  );
}
