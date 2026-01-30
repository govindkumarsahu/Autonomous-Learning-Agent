import React, { useMemo } from 'react'

export default function TopicSelector({
  topics,
  selectedTopic,
  searchQuery,
  onSelectTopic,
  onSearchQuery,
  onStart,
  disabled,
}) {
  const effectiveTopic = useMemo(() => {
    const trimmed = (searchQuery || '').trim()
    return trimmed.length > 0 ? trimmed : selectedTopic
  }, [searchQuery, selectedTopic])

  const canStart = !disabled && Boolean(effectiveTopic && effectiveTopic.trim().length > 0)

  return (
    <div className="bg-white shadow-lg rounded-2xl p-6 space-y-5 transition-all duration-200">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold text-slate-900">Topic Section</h2>
          <p className="text-slate-600 mt-1">
            Pick from the dropdown or search a topic. Then start learning.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <label className="text-sm font-medium text-slate-700">Dropdown topic</label>
          <select
            className="w-full border border-slate-200 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-600 transition-all duration-200"
            value={selectedTopic}
            onChange={(e) => {
              onSelectTopic(e.target.value)
              if (e.target.value) onSearchQuery('')
            }}
            disabled={disabled}
          >
            <option value="">Select a topic...</option>
            {topics.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
          <p className="text-xs text-slate-500">No preselected topic.</p>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium text-slate-700">Search topic</label>
          <input
            className="w-full border border-slate-200 rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-600 transition-all duration-200"
            placeholder="e.g., Artificical Intelligence, Deep Learning, ML"
            value={searchQuery}
            onChange={(e) => {
              onSearchQuery(e.target.value)
              if (e.target.value.trim().length > 0) onSelectTopic('')
            }}
            disabled={disabled}
          />
          <p className="text-xs text-slate-500">Typing here clears the dropdown selection.</p>
        </div>
      </div>

      <div className="flex items-center justify-end">
        <button
          className={
            canStart
              ? 'bg-blue-600 text-white px-5 py-2.5 rounded-xl font-semibold shadow-sm hover:bg-blue-700 hover:scale-[1.02] transition-all duration-200'
              : 'bg-slate-200 text-slate-500 px-5 py-2.5 rounded-xl font-semibold cursor-not-allowed'
          }
          onClick={onStart}
          disabled={!canStart}
        >
          Start Learning
        </button>
      </div>
    </div>
  )
}
