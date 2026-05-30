/** @type {import('next').NextConfig} */
const DJANGO_ORIGIN = process.env.DJANGO_ORIGIN || "http://127.0.0.1:8000";

const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    // Proxy API calls to the Django backend so cookies stay same-origin.
    return [
      {
        source: "/api/:path*",
        destination: `${DJANGO_ORIGIN}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
