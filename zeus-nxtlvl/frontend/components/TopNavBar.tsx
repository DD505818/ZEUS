import Link from 'next/link';

export default function TopNavBar() {
  return (
    <nav className="flex items-center justify-between p-4 bg-gray-200">
      <div className="font-bold">ZEUS Dashboard</div>
      <Link href="/login" className="text-blue-600">
        Login
      </Link>
    </nav>
  );
}
