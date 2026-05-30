import ProtectedRoute from "../../../src/components/ProtectedRoute.jsx";
import MaterialUpload from "../../../src/features/upload/MaterialUpload.jsx";

export default function Page() {
  return (
    <ProtectedRoute>
      <MaterialUpload />
    </ProtectedRoute>
  );
}
