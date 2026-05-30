import ProtectedRoute from "../../src/components/ProtectedRoute.jsx";
import MyUploads from "../../src/features/myUploads/MyUploads.jsx";

export default function Page() {
  return (
    <ProtectedRoute>
      <MyUploads />
    </ProtectedRoute>
  );
}
