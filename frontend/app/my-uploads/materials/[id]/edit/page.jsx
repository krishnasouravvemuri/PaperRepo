import ProtectedRoute from "../../../../../src/components/ProtectedRoute.jsx";
import EditMaterial from "../../../../../src/features/myUploads/EditMaterial.jsx";

export default function Page() {
  return (
    <ProtectedRoute>
      <EditMaterial />
    </ProtectedRoute>
  );
}
