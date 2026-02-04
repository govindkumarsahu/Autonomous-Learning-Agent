import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { CheckCircle, XCircle, RefreshCw, ArrowRight } from 'lucide-react';
import { api } from '../context/AuthContext';
import Sidebar from '../components/Sidebar';
import Card from '../components/Card';
import Button from '../components/Button';

export default function ResultPage() {
    const location = useLocation();
    const navigate = useNavigate();
    const { score, attemptNumber, maxAttemptsReached, topic } = location.state || {};

    const [reteachExplanation, setReteachExplanation] = useState('');
    const [loading, setLoading] = useState(false);

    const passed = score >= 70;

    useEffect(() => {
        if (!passed && !maxAttemptsReached) {
            fetchReteach();
        }
    }, []);

    const fetchReteach = async () => {
        setLoading(true);
        try {
            const response = await api.post('/reteach', { topic });
            setReteachExplanation(response.data.simplified_explanation);
        } catch (err) {
            console.error('Failed to fetch reteach:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleRetry = async () => {
        // Get the explanation again for the same topic
        setLoading(true);
        try {
            const response = await api.post('/explain', { topic });
            const explanation = response.data.explanation;

            // Navigate directly to quiz with topic and explanation
            navigate('/quiz', { state: { topic, explanation } });
        } catch (err) {
            console.error('Failed to load explanation for retry:', err);
            // Fallback: go to learn page
            navigate('/learn');
        } finally {
            setLoading(false);
        }
    };

    const handleNextTopic = () => {
        navigate('/learn');
    };

    if (!topic) {
        navigate('/dashboard');
        return null;
    }

    return (
        <div className="flex min-h-screen bg-slate-50">
            <Sidebar />

            <div className="flex-1 p-8">
                <div className="max-w-4xl mx-auto">
                    <h1 className="text-3xl font-bold text-slate-900 mb-8">Quiz Result</h1>

                    {/* Result Card */}
                    <Card className={`mb-6 ${passed ? 'border-2 border-green-500' : 'border-2 border-red-500'}`}>
                        <div className="flex items-center gap-4 mb-4">
                            {passed ? (
                                <CheckCircle size={48} className="text-green-600" />
                            ) : (
                                <XCircle size={48} className="text-red-600" />
                            )}
                            <div>
                                <h2 className="text-3xl font-bold text-slate-900">{score}% Score</h2>
                                <p className="text-slate-600">Attempt {attemptNumber} of 3</p>
                            </div>
                        </div>

                        {passed ? (
                            <div className="bg-green-50 p-4 rounded-lg">
                                <h3 className="text-xl font-semibold text-green-900 mb-2">
                                    🎉 Mastery Achieved!
                                </h3>
                                <p className="text-green-800">
                                    Congratulations! You've demonstrated a strong understanding of {topic}.
                                </p>
                            </div>
                        ) : (
                            <div className="bg-red-50 p-4 rounded-lg">
                                <h3 className="text-xl font-semibold text-red-900 mb-2">
                                    Below 70% Mastery
                                </h3>
                                <p className="text-red-800">
                                    {maxAttemptsReached
                                        ? 'Maximum attempts reached. Please review the material before retrying later.'
                                        : 'Don\'t worry! Review the simplified explanation below and try again.'}
                                </p>
                            </div>
                        )}
                    </Card>

                    {/* Reteach Explanation */}
                    {!passed && !maxAttemptsReached && (
                        <Card className="mb-6">
                            <h3 className="text-xl font-semibold text-slate-900 mb-4">
                                📚 Simplified Explanation (Feynman Technique)
                            </h3>

                            {loading ? (
                                <div className="text-slate-600">Loading simplified explanation...</div>
                            ) : (
                                <div className="prose max-w-none text-slate-700 whitespace-pre-wrap bg-blue-50 p-4 rounded-lg">
                                    {reteachExplanation}
                                </div>
                            )}
                        </Card>
                    )}

                    {/* Action Buttons */}
                    <div className="flex gap-4">
                        {passed ? (
                            <Button onClick={handleNextTopic} variant="primary">
                                Learn Next Topic <ArrowRight size={20} className="ml-2 inline" />
                            </Button>
                        ) : !maxAttemptsReached ? (
                            <Button onClick={handleRetry} variant="primary">
                                <RefreshCw size={20} className="mr-2 inline" /> Retry Quiz
                            </Button>
                        ) : null}

                        <Button onClick={() => navigate('/dashboard')} variant="secondary">
                            Back to Dashboard
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
}
