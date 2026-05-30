import ProtectedRoute from "../../../../../src/components/ProtectedRoute.jsx";
import EditImportantTopic from "../../../../../src/features/myUploads/EditImportantTopic.jsx";

export default function Page() {
  return (
    <ProtectedRoute>
      <EditImportantTopic />
    </ProtectedRoute>
  );
}
