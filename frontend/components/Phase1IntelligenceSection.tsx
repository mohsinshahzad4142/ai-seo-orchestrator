"use client";
import React, { useState } from "react";

export default function Phase1IntelligenceSection() {
  const [seedInput, setSeedInput] = useState("nextjs seo agency, fastapi developer usa");
  const [targetDomain, setTargetDomain] = useState("mohsinshahzad.vercel.app");
  const [competitorDomain, setCompetitorDomain] = useState("competitor-seo.com");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const runPhase1Action = async (endpoint: string, payload: any) => {
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch(`http://127.0.0.1:8000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      setResult({ endpoint, data });
    } catch (err) {
      setResult({ endpoint, error: String(err) });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          🧠 Phase 1: Core Intelligence & Keyword Engine
        </h2>
        {loading && <span className="text-xs text-indigo-400 animate-pulse">Processing API call...</span>}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        {/* Card 1: DataForSEO / GKP Fetch */}
        <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-semibold text-slate-200 mb-2">1. Keyword Fetch (GKP / DataForSEO)</h3>
            <input
              type="text"
              value={seedInput}
              onChange={(e) => setSeedInput(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 mb-3"
              placeholder="comma, separated, seeds"
            />
          </div>
          <button
            onClick={() =>
              runPhase1Action("/api/v1/intelligence/keywords", {
                seeds: seedInput.split(",").map((s) => s.trim()),
              })
            }
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium py-1.5 rounded transition"
          >
            Fetch Keywords
          </button>
        </div>

        {/* Card 2: Competitor Gap Analysis */}
        <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-semibold text-slate-200 mb-2">2. Competitor Gap Analysis</h3>
            <input
              type="text"
              value={targetDomain}
              onChange={(e) => setTargetDomain(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1 text-xs text-slate-200 mb-2"
              placeholder="Your domain"
            />
            <input
              type="text"
              value={competitorDomain}
              onChange={(e) => setCompetitorDomain(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1 text-xs text-slate-200 mb-3"
              placeholder="Competitor domain"
            />
          </div>
          <button
            onClick={() =>
              runPhase1Action("/api/v1/intelligence/competitor-gaps", {
                target_domain: targetDomain,
                competitor_domain: competitorDomain,
              })
            }
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium py-1.5 rounded transition"
          >
            Analyze Gaps
          </button>
        </div>

        {/* Card 3: GSC Historical Metrics Diff */}
        <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-semibold text-slate-200 mb-2">3. GSC Historical Diff</h3>
            <p className="text-xs text-slate-400 mb-3">
              Calculates Ranked ($\uparrow$) & Deranked ($\downarrow$) terms delta over 30d baseline.
            </p>
          </div>
          <button
            onClick={() =>
              runPhase1Action("/api/v1/intelligence/gsc-diff", {
                lookback_days: 30,
                position_threshold: 3,
              })
            }
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium py-1.5 rounded transition"
          >
            Compute Diff
          </button>
        </div>
      </div>

      {/* Response Inspector */}
      {result && (
        <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 font-mono text-xs overflow-x-auto">
          <div className="text-indigo-400 mb-1 font-semibold">Response from {result.endpoint}:</div>
          <pre className="text-slate-300 max-h-60 overflow-y-auto">
            {JSON.stringify(result.data || result.error, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}