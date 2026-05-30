import ProtectedRoute from "../../src/components/ProtectedRoute.jsx";
import UploadHome from "../../src/features/upload/UploadHome.jsx";

export default function Page() {
  return (
    <ProtectedRoute>
      <UploadHome />
    </ProtectedRoute>
  );
}
