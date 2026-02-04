import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Brain, Target, TrendingUp, BookOpen } from 'lucide-react';
import Button from '../components/Button';

export default function LandingPage() {
    const navigate = useNavigate();

    const features = [
        {
            icon: Brain,
            title: 'Adaptive Quizzes',
            description: 'AI-generated quizzes tailored to your learning topic'
        },
        {
            icon: Target,
            title: '70% Mastery Rule',
            description: 'Achieve 70% to master a topic and move forward'
        },
        {
            icon: TrendingUp,
            title: 'Progress Tracking',
            description: 'Monitor your learning journey and improvements'
        },
        {
            icon: BookOpen,
            title: 'Smart Reteaching',
            description: 'Feynman technique-based re-explanations for better understanding'
        }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100">
            {/* Hero Section */}
            <div className="max-w-6xl mx-auto px-8 py-20">
                <div className="text-center mb-16">
                    <div className="flex justify-center mb-6">
                        <div className="bg-blue-100 p-4 rounded-2xl">
                            <Brain size={64} className="text-blue-600" />
                        </div>
                    </div>

                    <h1 className="text-5xl font-bold text-slate-900 mb-4">
                        Autonomous Learning Agent
                    </h1>

                    <p className="text-xl text-slate-600 max-w-2xl mx-auto mb-8">
                        AI-powered adaptive learning platform for engineering students.
                        Master topics with intelligent quizzes and personalized feedback.
                    </p>

                    <div className="flex gap-4 justify-center">
                        <Button onClick={() => navigate('/login')} variant="primary">
                            Login
                        </Button>
                        <Button onClick={() => navigate('/register')} variant="secondary">
                            Register
                        </Button>
                    </div>
                </div>

                {/* Features */}
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mt-16">
                    {features.map((feature) => {
                        const Icon = feature.icon;
                        return (
                            <div
                                key={feature.title}
                                className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow"
                            >
                                <div className="bg-blue-50 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                                    <Icon size={24} className="text-blue-600" />
                                </div>
                                <h3 className="font-semibold text-slate-900 mb-2">{feature.title}</h3>
                                <p className="text-sm text-slate-600">{feature.description}</p>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
