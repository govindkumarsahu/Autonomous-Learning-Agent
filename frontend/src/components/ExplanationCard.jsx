import React from 'react'

export default function ExplanationCard({ topic, explanation, onStartQuiz, disabled, showStartQuiz }) {
  return (
    <div className="bg-white shadow-lg rounded-2xl p-6 space-y-4 transition-all duration-200">
      <div>
        <h2 className="text-xl font-semibold text-slate-900">Explanation Section</h2>
        <p className="text-slate-600 mt-1">
          Topic: <span className="font-medium text-slate-900">{topic}</span>
        </p>
      </div>

      <div className="border border-slate-200 rounded-2xl p-4 max-h-[420px] overflow-y-auto bg-white">
        <div className="whitespace-pre-wrap leading-relaxed text-slate-700 text-sm">{explanation}</div>
      </div>

      {showStartQuiz ? (
        <div className="flex items-center justify-end pt-2">
          <button
            className={
              disabled
                ? 'bg-slate-200 text-slate-500 px-5 py-2 rounded-xl font-semibold cursor-not-allowed'
                : 'bg-blue-600 text-white px-5 py-2 rounded-xl font-semibold shadow-sm hover:bg-blue-700 hover:scale-[1.02] transition-all duration-200'
            }
            onClick={onStartQuiz}
            disabled={disabled}
          >
            Start Quiz
          </button>
        </div>
      ) : null}
    </div>
  )
}
