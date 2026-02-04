import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { api } from '../context/AuthContext';
import Sidebar from '../components/Sidebar';
import Card from '../components/Card';
import Button from '../components/Button';

export default function QuizPage() {
    const location = useLocation();
    const navigate = useNavigate();
    const { topic, explanation } = location.state || {};

    const [quiz, setQuiz] = useState(null);
    const [currentQuestion, setCurrentQuestion] = useState(0);
    const [answers, setAnswers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        if (!topic) {
            navigate('/learn');
            return;
        }
        fetchQuiz();
    }, []);

    const fetchQuiz = async () => {
        try {
            const response = await api.post('/generate-quiz', { topic });
            setQuiz(response.data);
            setAnswers(new Array(response.data.questions.length).fill(-1));
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to generate quiz');
        } finally {
            setLoading(false);
        }
    };

    const handleAnswerChange = (optionIndex) => {
        const newAnswers = [...answers];
        newAnswers[currentQuestion] = optionIndex;
        setAnswers(newAnswers);
    };

    const handleNext = () => {
        if (currentQuestion < quiz.questions.length - 1) {
            setCurrentQuestion(currentQuestion + 1);
        }
    };

    const handlePrevious = () => {
        if (currentQuestion > 0) {
            setCurrentQuestion(currentQuestion - 1);
        }
    };

    const handleSubmit = async () => {
        if (answers.includes(-1)) {
            setError('Please answer all questions before submitting');
            return;
        }

        setLoading(true);
        try {
            const correctAnswers = quiz.questions.map(q => q.answer_index);
            const response = await api.post('/evaluate', {
                topic,
                answers,
                correct_answers: correctAnswers
            });

            navigate('/result', {
                state: {
                    score: response.data.score,
                    attemptNumber: response.data.attempt_number,
                    maxAttemptsReached: response.data.max_attempts_reached,
                    topic
                }
            });
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to submit quiz');
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex min-h-screen bg-slate-50">
                <Sidebar />
                <div className="flex-1 flex items-center justify-center">
                    <div className="text-slate-600">Loading quiz...</div>
                </div>
            </div>
        );
    }

    if (!quiz) {
        return (
            <div className="flex min-h-screen bg-slate-50">
                <Sidebar />
                <div className="flex-1 flex items-center justify-center">
                    <div className="text-slate-600">Failed to load quiz</div>
                </div>
            </div>
        );
    }

    const question = quiz.questions[currentQuestion];

    return (
        <div className="flex min-h-screen bg-slate-50">
            <Sidebar />

            <div className="flex-1 p-8">
                <div className="max-w-4xl mx-auto">
                    <h1 className="text-3xl font-bold text-slate-900 mb-8">Quiz: {topic}</h1>

                    {/* Explanation (visible during quiz) */}
                    {explanation && (
                        <Card className="mb-6 max-h-48 overflow-y-auto">
                            <h3 className="text-sm font-semibold text-slate-700 mb-2">Reference Explanation</h3>
                            <div className="text-sm text-slate-600 whitespace-pre-wrap line-clamp-6">
                                {explanation}
                            </div>
                        </Card>
                    )}

                    {error && (
                        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
                            {error}
                        </div>
                    )}

                    {/* Question Card */}
                    <Card className="mb-6">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-xl font-semibold text-slate-900">
                                Question {currentQuestion + 1} of {quiz.questions.length}
                            </h2>
                            <span className="text-sm bg-blue-100 text-blue-700 px-3 py-1 rounded-full font-semibold">
                                Relevance: {quiz.relevance_score}/100
                            </span>
                        </div>

                        <p className="text-lg text-slate-900 mb-6 font-medium">{question.question}</p>

                        <div className="space-y-3">
                            {question.options.map((option, index) => (
                                <label
                                    key={index}
                                    className={`flex items-center p-4 rounded-lg border-2 cursor-pointer transition-all ${answers[currentQuestion] === index
                                            ? 'border-blue-600 bg-blue-50'
                                            : 'border-slate-200 hover:border-blue-300'
                                        }`}
                                >
                                    <input
                                        type="radio"
                                        name={`question-${currentQuestion}`}
                                        checked={answers[currentQuestion] === index}
                                        onChange={() => handleAnswerChange(index)}
                                        className="mr-3"
                                    />
                                    <span className="text-slate-900">{option}</span>
                                </label>
                            ))}
                        </div>
                    </Card>

                    {/* Navigation */}
                    <div className="flex justify-between items-center">
                        <Button
                            onClick={handlePrevious}
                            disabled={currentQuestion === 0}
                            variant="secondary"
                        >
                            Previous
                        </Button>

                        <div className="flex gap-2">
                            {quiz.questions.map((_, index) => (
                                <div
                                    key={index}
                                    className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${answers[index] !== -1
                                            ? 'bg-blue-600 text-white'
                                            : 'bg-slate-200 text-slate-600'
                                        }`}
                                >
                                    {index + 1}
                                </div>
                            ))}
                        </div>

                        {currentQuestion === quiz.questions.length - 1 ? (
                            <Button onClick={handleSubmit} variant="success" disabled={loading}>
                                Submit Quiz
                            </Button>
                        ) : (
                            <Button onClick={handleNext} variant="primary">
                                Next
                            </Button>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
