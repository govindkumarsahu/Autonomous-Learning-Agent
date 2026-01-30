import React from 'react'

export default function QuizCard({ questions, answers, onChangeAnswer, onSubmit, relevanceScore, disabled }) {
  const allAnswered = answers.every((a) => a >= 0)

  return (
    <div className="bg-white shadow-lg rounded-2xl p-6 space-y-5 transition-all duration-200">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold text-slate-900">Quiz Section</h2>
          <p className="text-slate-600 mt-1">10 MCQs derived from the explanation.</p>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200 px-3 py-1 rounded-full">
            Relevance: {relevanceScore}/100
          </span>
          <button
            className={
              !disabled && allAnswered
                ? 'bg-blue-600 text-white px-4 py-2 rounded-xl font-semibold shadow-sm hover:bg-blue-700 hover:scale-[1.02] transition-all duration-200'
                : 'bg-slate-200 text-slate-500 px-4 py-2 rounded-xl font-semibold cursor-not-allowed'
            }
            onClick={onSubmit}
            disabled={disabled || !allAnswered}
          >
            Submit Answers
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {questions.map((q, idx) => (
          <div
            key={idx}
            className="border border-slate-200 rounded-2xl p-4 space-y-3 hover:shadow-sm transition-all duration-200"
          >
            <div className="font-semibold text-slate-900">Q{idx + 1}. {q.question}</div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {q.options.map((opt, optIdx) => {
                const checked = answers[idx] === optIdx
                return (
                  <label
                    key={optIdx}
                    className={
                      checked
                        ? 'border border-blue-600 bg-blue-50 rounded-lg p-3 cursor-pointer'
                        : 'border border-slate-200 rounded-lg p-3 cursor-pointer hover:border-slate-300'
                    }
                  >
                    <div className="flex items-start gap-2">
                      <input
                        type="radio"
                        name={`q-${idx}`}
                        value={optIdx}
                        checked={checked}
                        onChange={() => onChangeAnswer(idx, optIdx)}
                        disabled={disabled}
                        className="mt-1"
                      />
                      <div className="text-sm text-slate-700">{opt}</div>
                    </div>
                  </label>
                )
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
