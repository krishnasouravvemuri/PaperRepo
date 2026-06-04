// Fetches a file from a signed URL as a blob and triggers a browser download.
// Returns a promise so callers can show a loading state while it runs.
export async function downloadFromUrl(url, filename) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Download failed (${res.status})`);
  const blob = await res.blob();

  // Prefer the server-provided filename; fall back to the URL basename.
  let name = filename;
  if (!name) {
    const path = url.split("?")[0];
    name = decodeURIComponent(path.substring(path.lastIndexOf("/") + 1)) || "download";
  }

  const objectUrl = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = objectUrl;
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(objectUrl);
}
