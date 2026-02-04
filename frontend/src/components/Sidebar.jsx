import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, BookOpen, BarChart3, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Sidebar() {
    const location = useLocation();
    const { logout } = useAuth();

    const menuItems = [
        { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
        { path: '/learn', label: 'Learn', icon: BookOpen },
        { path: '/progress', label: 'Progress', icon: BarChart3 },
    ];

    return (
        <div className="w-64 bg-white border-r border-slate-200 min-h-screen p-4">
            <div className="flex items-center gap-2 mb-8 px-2">
                <div className="text-2xl">🧠</div>
                <div className="font-bold text-slate-900">AI Learning</div>
            </div>

            <nav className="space-y-2">
                {menuItems.map((item) => {
                    const Icon = item.icon;
                    const isActive = location.pathname === item.path;

                    return (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${isActive
                                    ? 'bg-blue-50 text-blue-600 font-semibold'
                                    : 'text-slate-600 hover:bg-slate-50'
                                }`}
                        >
                            <Icon size={20} />
                            <span>{item.label}</span>
                        </Link>
                    );
                })}

                <button
                    onClick={logout}
                    className="flex items-center gap-3 px-4 py-3 rounded-lg transition-all text-red-600 hover:bg-red-50 w-full"
                >
                    <LogOut size={20} />
                    <span>Logout</span>
                </button>
            </nav>
        </div>
    );
}
