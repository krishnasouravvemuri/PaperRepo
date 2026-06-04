/** @type {import('next').NextConfig} */
const DJANGO_ORIGIN = process.env.DJANGO_ORIGIN || "http://127.0.0.1:8000";

const nextConfig = {
  reactStrictMode: true,
  // Preserve trailing slashes when proxying to Django. Without this, Next's
  // default trailing-slash redirect strips the slash before the rewrite,
  // and Django's APPEND_SLASH can't redirect a POST body -> 500.
  skipTrailingSlashRedirect: true,
  async rewrites() {
    // Proxy API calls to the Django backend so cookies stay same-origin.
    return [
      // Slash-terminated paths first, forwarding the trailing slash intact.
      // The :path* rewrite otherwise drops it, breaking Django APPEND_SLASH on POST.
      {
        source: "/api/:path*/",
        destination: `${DJANGO_ORIGIN}/api/:path*/`,
      },
      {
        source: "/api/:path*",
        destination: `${DJANGO_ORIGIN}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
