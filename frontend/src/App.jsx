import React, { useMemo, useState } from 'react'
import TopicSelector from './components/TopicSelector.jsx'
import ExplanationCard from './components/ExplanationCard.jsx'
import QuizCard from './components/QuizCard.jsx'
import ResultCard from './components/ResultCard.jsx'

const API_BASE_URL = 'http://localhost:8000'

function buildInitialAnswers() {
  return Array.from({ length: 10 }, () => -1)
}

async function fetchJson(path, options) {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `Request failed: ${res.status}`)
  }

  return res.json()
}

export default function App() {
  const topics = useMemo(
    () => [
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
    ],
    []
  )

  const [selectedTopic, setSelectedTopic] = useState('')
  const [searchQuery, setSearchQuery] = useState('')

  const topic = useMemo(() => {
    const trimmed = (searchQuery || '').trim()
    return trimmed.length > 0 ? trimmed : selectedTopic
  }, [searchQuery, selectedTopic])

  const [step, setStep] = useState('topic')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const [explanation, setExplanation] = useState('')

  const [quiz, setQuiz] = useState(null)
  const [answers, setAnswers] = useState(buildInitialAnswers())
  const [correctAnswers, setCorrectAnswers] = useState([])

  const [score, setScore] = useState(null)
  const [simplifiedExplanation, setSimplifiedExplanation] = useState('')

  async function startLearning() {
    setError('')
    setLoading(true)
    try {
      setQuiz(null)
      setScore(null)
      setSimplifiedExplanation('')
      const data = await fetchJson('/explain', {
        method: 'POST',
        body: JSON.stringify({ topic }),
      })
      setExplanation(data.explanation)
      setStep('explanation')
      window.scrollTo({ top: 0, behavior: 'smooth' })
    } catch (e) {
      setError(e.message || 'Failed to explain topic')
    } finally {
      setLoading(false)
    }
  }

  async function startQuiz() {
    setError('')
    setLoading(true)
    try {
      const data = await fetchJson('/generate-quiz', {
        method: 'POST',
        body: JSON.stringify({ topic }),
      })

      setQuiz({ questions: data.questions, relevance_score: data.relevance_score })
      setCorrectAnswers(data.questions.map((q) => q.answer_index))
      setAnswers(buildInitialAnswers())
      setScore(null)
      setSimplifiedExplanation('')
      setStep('quiz')
      window.scrollTo({ top: 0, behavior: 'smooth' })
    } catch (e) {
      setError(e.message || 'Failed to generate quiz')
    } finally {
      setLoading(false)
    }
  }

  function onChangeAnswer(questionIndex, optionIndex) {
    setAnswers((prev) => {
      const next = [...prev]
      next[questionIndex] = optionIndex
      return next
    })
  }

  async function submitQuiz() {
    setError('')
    setLoading(true)
    try {
      const data = await fetchJson('/evaluate', {
        method: 'POST',
        body: JSON.stringify({ topic, answers, correct_answers: correctAnswers }),
      })

      setScore(data.score)

      if (data.score < 70) {
        const reteach = await fetchJson('/reteach', {
          method: 'POST',
          body: JSON.stringify({ topic }),
        })
        setSimplifiedExplanation(reteach.simplified_explanation)
      }

      setStep('result')
      window.scrollTo({ top: 0, behavior: 'smooth' })
    } catch (e) {
      setError(e.message || 'Failed to evaluate answers')
    } finally {
      setLoading(false)
    }
  }

  async function retryQuiz() {
    await startQuiz()
  }

  async function learnNextTopic() {
    const currentIndex = topics.indexOf(topic)
    const nextIndex = currentIndex >= 0 ? (currentIndex + 1) % topics.length : 0
    const nextTopic = topics[nextIndex]

    setSelectedTopic(nextTopic)
    setSearchQuery('')
    setExplanation('')
    setQuiz(null)
    setAnswers(buildInitialAnswers())
    setCorrectAnswers([])
    setScore(null)
    setSimplifiedExplanation('')
    setError('')
    setStep('explanation')

    window.scrollTo({ top: 0, behavior: 'smooth' })

    setLoading(true)
    try {
      const data = await fetchJson('/explain', {
        method: 'POST',
        body: JSON.stringify({ topic: nextTopic }),
      })
      setExplanation(data.explanation)
    } catch (e) {
      setError(e.message || 'Failed to explain next topic')
    } finally {
      setLoading(false)
    }
  }

  function resetToTopicSelection() {
    setSelectedTopic('')
    setSearchQuery('')
    setExplanation('')
    setQuiz(null)
    setAnswers(buildInitialAnswers())
    setCorrectAnswers([])
    setScore(null)
    setSimplifiedExplanation('')
    setError('')
    setStep('topic')
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const passed = score !== null ? score >= 70 : false

  return (
    <div className="min-h-screen bg-gradient-to-br from-white to-blue-50">
      <div className="bg-white/80 backdrop-blur border-b border-slate-200">
        <div className="max-w-5xl mx-auto px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="text-xl">🧠</div>
            <div className="font-semibold text-slate-900">Autonomous Learning Agent</div>
          </div>

          <div className="flex items-center gap-2">
            {topic ? (
              <span className="text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200 px-3 py-1 rounded-full">
                {topic}
              </span>
            ) : null}
            {score !== null ? (
              <span
                className={
                  passed
                    ? 'text-xs font-semibold bg-green-50 text-green-700 border border-green-200 px-3 py-1 rounded-full'
                    : 'text-xs font-semibold bg-red-50 text-red-700 border border-red-200 px-3 py-1 rounded-full'
                }
              >
                Score: {score}%
              </span>
            ) : null}
          </div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto p-8 space-y-8">
        {error ? (
          <div className="bg-white shadow-lg rounded-2xl p-4 border border-red-200 transition-all duration-200">
            <div className="text-sm font-semibold text-red-700">Error</div>
            <div className="text-sm text-red-700 mt-1 whitespace-pre-wrap">{error}</div>
          </div>
        ) : null}

        {loading ? (
          <div className="bg-white shadow-lg rounded-2xl p-4 border border-slate-200 transition-all duration-200">
            <div className="text-sm text-slate-700">Loading...</div>
          </div>
        ) : null}

        {step === 'topic' ? (
          <TopicSelector
            topics={topics}
            selectedTopic={selectedTopic}
            searchQuery={searchQuery}
            onSelectTopic={setSelectedTopic}
            onSearchQuery={setSearchQuery}
            onStart={startLearning}
            disabled={loading}
          />
        ) : null}

        {step !== 'topic' ? (
          <ExplanationCard
            topic={topic}
            explanation={explanation}
            onStartQuiz={startQuiz}
            disabled={loading}
            showStartQuiz={step === 'explanation'}
          />
        ) : null}

        {step === 'quiz' && quiz ? (
          <QuizCard
            questions={quiz.questions}
            answers={answers}
            onChangeAnswer={onChangeAnswer}
            onSubmit={submitQuiz}
            relevanceScore={quiz.relevance_score}
            disabled={loading}
          />
        ) : null}

        {step === 'result' && score !== null ? (
          <ResultCard
            score={score}
            passed={passed}
            simplifiedExplanation={simplifiedExplanation}
            onRetry={retryQuiz}
            onNextTopic={learnNextTopic}
            onBackToTopics={resetToTopicSelection}
            disabled={loading}
          />
        ) : null}
      </div>
    </div>
  )
}
