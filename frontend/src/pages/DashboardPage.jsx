import React, { useEffect, useState } from 'react';
import { Target, TrendingUp, XCircle, Award } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../context/AuthContext';
import Sidebar from '../components/Sidebar';
import Card from '../components/Card';

export default function DashboardPage() {
    const { user } = useAuth();
    const [progress, setProgress] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchProgress();
    }, []);

    const fetchProgress = async () => {
        try {
            const response = await api.get('/progress');
            setProgress(response.data.progress);
        } catch (error) {
            console.error('Failed to fetch progress:', error);
        } finally {
            setLoading(false);
        }
    };

    const stats = {
        total: progress.length,
        passed: progress.filter(p => p.score >= 70).length,
        failed: progress.filter(p => p.score < 70).length,
        avgScore: progress.length > 0
            ? Math.round(progress.reduce((sum, p) => sum + p.score, 0) / progress.length)
            : 0
    };

    // Utility function to convert UTC date to IST display
    const formatDateToIST = (utcDate) => {
        const date = new Date(utcDate);
        // Add 5 hours 30 minutes for IST (UTC+5:30)
        const istDate = new Date(date.getTime() + (5.5 * 60 * 60 * 1000));

        return istDate.toLocaleString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        });
    };

    return (
        <div className="flex min-h-screen bg-slate-50">
            <Sidebar />

            <div className="flex-1 p-8">
                <div className="max-w-6xl mx-auto">
                    <h1 className="text-3xl font-bold text-slate-900 mb-2">Dashboard</h1>
                    <p className="text-slate-600 mb-8">Welcome, {user?.email}</p>

                    {/* Stats Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                        <Card>
                            <div className="flex items-center gap-3">
                                <div className="bg-blue-100 p-3 rounded-lg">
                                    <Target size={24} className="text-blue-600" />
                                </div>
                                <div>
                                    <div className="text-2xl font-bold text-slate-900">{stats.total}</div>
                                    <div className="text-sm text-slate-600">Total Attempts</div>
                                </div>
                            </div>
                        </Card>

                        <Card>
                            <div className="flex items-center gap-3">
                                <div className="bg-green-100 p-3 rounded-lg">
                                    <Award size={24} className="text-green-600" />
                                </div>
                                <div>
                                    <div className="text-2xl font-bold text-slate-900">{stats.passed}</div>
                                    <div className="text-sm text-slate-600">Passed (≥70%)</div>
                                </div>
                            </div>
                        </Card>

                        <Card>
                            <div className="flex items-center gap-3">
                                <div className="bg-red-100 p-3 rounded-lg">
                                    <XCircle size={24} className="text-red-600" />
                                </div>
                                <div>
                                    <div className="text-2xl font-bold text-slate-900">{stats.failed}</div>
                                    <div className="text-sm text-slate-600">Failed</div>
                                </div>
                            </div>
                        </Card>

                        <Card>
                            <div className="flex items-center gap-3">
                                <div className="bg-purple-100 p-3 rounded-lg">
                                    <TrendingUp size={24} className="text-purple-600" />
                                </div>
                                <div>
                                    <div className="text-2xl font-bold text-slate-900">{stats.avgScore}%</div>
                                    <div className="text-sm text-slate-600">Avg Score</div>
                                </div>
                            </div>
                        </Card>
                    </div>

                    {/* Latest Activity */}
                    <Card>
                        <h2 className="text-xl font-bold text-slate-900 mb-4">Latest Activity</h2>

                        {loading ? (
                            <div className="text-slate-600">Loading...</div>
                        ) : progress.length === 0 ? (
                            <div className="text-slate-600">No activity yet. Start learning!</div>
                        ) : (
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead>
                                        <tr className="border-b border-slate-200">
                                            <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Topic</th>
                                            <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Attempt</th>
                                            <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Score</th>
                                            <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Date</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {progress.slice(0, 10).map((record, index) => (
                                            <tr key={index} className="border-b border-slate-100 hover:bg-slate-50">
                                                <td className="py-3 px-4 text-sm text-slate-900">{record.topic}</td>
                                                <td className="py-3 px-4 text-sm text-slate-600">{record.attempt_number}/3</td>
                                                <td className="py-3 px-4">
                                                    <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${record.score >= 70
                                                        ? 'bg-green-100 text-green-700'
                                                        : 'bg-red-100 text-red-700'
                                                        }`}>
                                                        {record.score}%
                                                    </span>
                                                </td>
                                                <td className="py-3 px-4 text-sm text-slate-600">
                                                    {formatDateToIST(record.date)}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </Card>
                </div>
            </div>
        </div>
    );
}
