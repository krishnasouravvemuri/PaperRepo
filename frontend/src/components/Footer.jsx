export default function Footer() {
  const links = [
    { href: "https://23sou.xyz", label: "Portfolio" },
    {
      href: "https://www.linkedin.com/in/vemuri-krishna-sourav-ba8403252/",
      label: "LinkedIn",
    },
    { href: "https://github.com/krishnasouravvemuri/", label: "GitHub" },
  ];

  return (
    <footer className="bg-gradient-to-r from-[#221c35] to-[#1c1530] border-t border-teal-500/30 shadow-inner shadow-black/40 py-8 mt-auto">
      <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
        <p className="text-gray-400 text-sm">
          Made with <span className="text-red-400">❤️</span> by Sourav
        </p>
        <div className="flex space-x-6 text-sm">
          {links.map((l) => (
            <a
              key={l.label}
              href={l.href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-300 hover:text-teal-300 transition-transform transform hover:scale-110 duration-300"
            >
              {l.label}
            </a>
          ))}
        </div>
      </div>
    </footer>
  );
}
