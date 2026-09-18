'use client';
import { useState } from 'react';

export default function KeywordControl() {
  const [keywords, setKeywords] = useState('nextjs seo agency, fastapi developer usa');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const analyzeKeywords = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/keywords/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          seed_keywords: keywords.split(',').map(k => k.trim()),
          target_country: 'US'
        })
      });
      const data = await res.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg">
      <h2 className="text-xl font-bold text-white mb-4">🔍 pSEO Keyword & Intent Analyzer</h2>
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
          className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-sky-500"
          placeholder="Enter comma-separated keywords..."
        />
        <button
          onClick={analyzeKeywords}
          disabled={loading}
          className="bg-sky-600 hover:bg-sky-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition"
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>

      {result && (
        <div className="space-y-2 mt-4">
          {result.analysis.map((item: any, idx: number) => (
            <div key={idx} className="bg-slate-950 border border-slate-800 p-3 rounded-lg text-xs space-y-1">
              <div className="flex justify-between font-semibold text-white">
                <span>{item.keyword}</span>
                <span className="text-sky-400">{item.intent}</span>
              </div>
              <p className="text-slate-400">{item.recommended_action}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}