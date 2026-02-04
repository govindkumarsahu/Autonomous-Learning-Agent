import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../context/AuthContext';
import Sidebar from '../components/Sidebar';
import Card from '../components/Card';
import Button from '../components/Button';

export default function LearnPage() {
    const navigate = useNavigate();
    const [selectedTopic, setSelectedTopic] = useState('');
    const [explanation, setExplanation] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [showQuiz, setShowQuiz] = useState(false);

    const topics = [
        'Artificial Intelligence',
        'Machine Learning',
        'Deep Learning',
        'Neural Networks',
        'Natural Language Processing',
        'Computer Vision',
        'Reinforcement Learning',
        'Generative AI',
        'Transformers',
        'Diffusion Models',
    ];

    const handleStartLearning = async () => {
        if (!selectedTopic) {
            setError('Please select a topic');
            return;
        }

        setError('');
        setLoading(true);
        try {
            const response = await api.post('/explain', { topic: selectedTopic });
            setExplanation(response.data.explanation);
            setShowQuiz(false);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to load explanation');
        } finally {
            setLoading(false);
        }
    };

    const handleStartQuiz = () => {
        navigate('/quiz', { state: { topic: selectedTopic, explanation } });
    };

    return (
        <div className="flex min-h-screen bg-slate-50">
            <Sidebar />

            <div className="flex-1 p-8">
                <div className="max-w-4xl mx-auto">
                    <h1 className="text-3xl font-bold text-slate-900 mb-8">Learn</h1>

                    {/* Topic Selection */}
                    <Card className="mb-6">
                        <h2 className="text-xl font-semibold text-slate-900 mb-4">Select Topic</h2>

                        <select
                            value={selectedTopic}
                            onChange={(e) => setSelectedTopic(e.target.value)}
                            className="w-full px-4 py-3 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
                        >
                            <option value="">Choose a topic...</option>
                            {topics.map((topic) => (
                                <option key={topic} value={topic}>
                                    {topic}
                                </option>
                            ))}
                        </select>

                        <Button
                            onClick={handleStartLearning}
                            disabled={loading || !selectedTopic}
                            variant="primary"
                        >
                            {loading ? 'Loading...' : 'Start Learning'}
                        </Button>
                    </Card>

                    {error && (
                        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
                            {error}
                        </div>
                    )}

                    {/* Explanation */}
                    {explanation && (
                        <Card className="mb-6">
                            <h2 className="text-xl font-semibold text-slate-900 mb-4">{selectedTopic}</h2>
                            <div className="prose max-w-none text-slate-700 whitespace-pre-wrap">
                                {explanation}
                            </div>
                            <div className="mt-6">
                                <Button onClick={handleStartQuiz} variant="primary">
                                    Start Quiz
                                </Button>
                            </div>
                        </Card>
                    )}
                </div>
            </div>
        </div>
    );
}
