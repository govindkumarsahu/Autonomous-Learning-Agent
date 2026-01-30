import React from 'react'

export default function ResultCard({
  score,
  passed,
  simplifiedExplanation,
  onRetry,
  onNextTopic,
  onBackToTopics,
  disabled,
}) {
  return (
    <div className="bg-white shadow-lg rounded-2xl p-6 space-y-5 transition-all duration-200">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold text-slate-900">Result Section</h2>
          <p className="text-slate-600 mt-1">Your score: <span className="font-semibold">{score}%</span></p>
        </div>

        {passed ? (
          <span className="text-xs font-semibold bg-green-50 text-green-700 border border-green-200 px-3 py-1 rounded-full">
            PASS
          </span>
        ) : (
          <span className="text-xs font-semibold bg-red-50 text-red-700 border border-red-200 px-3 py-1 rounded-full">
            RETEACH
          </span>
        )}
      </div>

      {passed ? (
        <div className="border border-green-200 bg-green-50 rounded-2xl p-4 text-green-800">
          <div className="font-semibold">Congratulations! You understood the topic.</div>
          <div className="text-sm mt-1">You can move to the next topic and continue learning.</div>
        </div>
      ) : (
        <div className="border border-red-200 bg-red-50 rounded-2xl p-4 text-red-800">
          <div className="font-semibold">Your score is below 70%.</div>
          <div className="text-sm mt-1">Read the simplified Feynman re-explanation, then retry the quiz.</div>
        </div>
      )}

      {!passed && simplifiedExplanation ? (
        <div className="border border-slate-200 rounded-2xl p-4 bg-white">
          <div className="text-sm font-semibold text-slate-900">Feynman Re-Explanation</div>
          <div className="whitespace-pre-wrap leading-relaxed text-slate-700 text-sm mt-2 max-h-[320px] overflow-y-auto">
            {simplifiedExplanation}
          </div>
        </div>
      ) : null}

      <div className="flex items-center justify-between gap-3">
        <button
          className={
            disabled
              ? 'text-slate-400 px-4 py-2 rounded-xl font-semibold cursor-not-allowed'
              : 'text-slate-600 px-4 py-2 rounded-xl font-semibold hover:bg-white hover:shadow-sm transition-all duration-200'
          }
          onClick={onBackToTopics}
          disabled={disabled || !onBackToTopics}
        >
          Choose Topic
        </button>

        {passed ? (
          <button
            className={
              disabled
                ? 'bg-slate-200 text-slate-500 px-5 py-2.5 rounded-xl font-semibold cursor-not-allowed'
                : 'bg-emerald-500 text-white px-5 py-2.5 rounded-xl font-semibold shadow-sm hover:bg-emerald-600 hover:scale-[1.02] transition-all duration-200'
            }
            onClick={onNextTopic}
            disabled={disabled}
          >
            Learn Next Topic
          </button>
        ) : (
          <button
            className={
              disabled
                ? 'bg-slate-200 text-slate-500 px-5 py-2.5 rounded-xl font-semibold cursor-not-allowed'
                : 'bg-red-500 text-white px-5 py-2.5 rounded-xl font-semibold shadow-sm hover:bg-red-600 hover:scale-[1.02] transition-all duration-200'
            }
            onClick={onRetry}
            disabled={disabled}
          >
            Retry Quiz
          </button>
        )}
      </div>
    </div>
  )
}
