import ProtectedRoute from "../../../src/components/ProtectedRoute.jsx";
import ImportantTopicUpload from "../../../src/features/upload/ImportantTopicUpload.jsx";

export default function Page() {
  return (
    <ProtectedRoute>
      <ImportantTopicUpload />
    </ProtectedRoute>
  );
}
