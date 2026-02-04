import React, { useEffect, useState } from 'react';
import { api } from '../context/AuthContext';
import Sidebar from '../components/Sidebar';
import Card from '../components/Card';

export default function ProgressPage() {
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
                    <h1 className="text-3xl font-bold text-slate-900 mb-8">Progress History</h1>

                    <Card>
                        {loading ? (
                            <div className="text-slate-600">Loading progress...</div>
                        ) : progress.length === 0 ? (
                            <div className="text-slate-600">No progress records yet. Start learning to build your history!</div>
                        ) : (
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead>
                                        <tr className="border-b-2 border-slate-200">
                                            <th className="text-left py-3 px-4 font-semibold text-slate-700">Topic</th>
                                            <th className="text-left py-3 px-4 font-semibold text-slate-700">Attempt</th>
                                            <th className="text-left py-3 px-4 font-semibold text-slate-700">Score</th>
                                            <th className="text-left py-3 px-4 font-semibold text-slate-700">Status</th>
                                            <th className="text-left py-3 px-4 font-semibold text-slate-700">Date</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {progress.map((record, index) => (
                                            <tr key={index} className="border-b border-slate-100 hover:bg-slate-50">
                                                <td className="py-3 px-4 font-medium text-slate-900">{record.topic}</td>
                                                <td className="py-3 px-4 text-slate-600">{record.attempt_number}/3</td>
                                                <td className="py-3 px-4">
                                                    <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${record.score >= 70
                                                        ? 'bg-green-100 text-green-700'
                                                        : 'bg-red-100 text-red-700'
                                                        }`}>
                                                        {record.score}%
                                                    </span>
                                                </td>
                                                <td className="py-3 px-4">
                                                    <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${record.score >= 70
                                                        ? 'bg-green-100 text-green-700'
                                                        : 'bg-orange-100 text-orange-700'
                                                        }`}>
                                                        {record.score >= 70 ? '✓ Passed' : '✗ Failed'}
                                                    </span>
                                                </td>
                                                <td className="py-3 px-4 text-slate-600">
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
