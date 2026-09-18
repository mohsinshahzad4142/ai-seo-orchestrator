'use client';
import React, { useState, useEffect } from 'react';

interface ApprovalItem {
  id: number;
  target_url: string;
  action: string;
  status: string;
  code_patch?: string;
  created_at?: string;
  proposed_payload?: any;
}

interface ApprovalQueueProps {
  websiteId?: number;
  apiBaseUrl?: string;
}

export const ApprovalQueue: React.FC<ApprovalQueueProps> = ({ 
  websiteId, 
  apiBaseUrl = 'http://127.0.0.1:8000' 
}) => {
  const [approvals, setApprovals] = useState<ApprovalItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [filter, setFilter] = useState<'PENDING' | 'ALL'>('PENDING');

  const fetchApprovals = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${apiBaseUrl}/api/v1/approvals`);
      if (res.ok) {
        const data = await res.json();
        setApprovals(data);
      }
    } catch (error) {
      console.error('Failed to fetch approval queue:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApprovals();
  }, [websiteId, apiBaseUrl]);

  const handleReview = async (item: ApprovalItem, reviewAction: 'APPROVE' | 'REJECT') => {
    const targetStatus = reviewAction === 'APPROVE' ? 'APPROVED' : 'REJECTED';
    try {
      const res = await fetch(`${apiBaseUrl}/api/v1/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          item_id: item.id,
          action: item.action,
          target_url: item.target_url,
          status: targetStatus,
          proposed_content: item.proposed_payload || {}
        }),
      });

      if (res.ok) {
        setApprovals((prev) =>
          prev.map((i) => (i.id === item.id ? { ...i, status: targetStatus } : i))
        );
      }
    } catch (error) {
      console.error('Failed to submit review:', error);
    }
  };

  const filteredApprovals = filter === 'PENDING'
    ? approvals.filter((item) => !item.status || item.status === 'PENDING')
    : approvals;

  return (
    <div className="p-6 bg-slate-900 text-white rounded-xl shadow-lg border border-slate-800 space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-xl font-bold flex items-center gap-2">
            🛡️ HITL Approval & Code Patch Queue
            {websiteId && <span className="text-xs bg-slate-800 text-slate-400 px-2 py-0.5 rounded">Site #{websiteId}</span>}
          </h2>
          <p className="text-xs text-slate-400 mt-1">Human-in-the-Loop governance for AI-generated SEO patches</p>
        </div>
        <div className="flex bg-slate-950 p-1 rounded-lg border border-slate-800">
          <button
            onClick={() => setFilter('PENDING')}
            className={`px-3 py-1 rounded-md text-xs font-medium transition ${
              filter === 'PENDING' ? 'bg-sky-600 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            Pending
          </button>
          <button
            onClick={() => setFilter('ALL')}
            className={`px-3 py-1 rounded-md text-xs font-medium transition ${
              filter === 'ALL' ? 'bg-sky-600 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            All History
          </button>
        </div>
      </div>

      {loading ? (
        <div className="space-y-3">
          {[1, 2].map((n) => (
            <div key={n} className="h-24 bg-slate-800/50 animate-pulse rounded-lg border border-slate-800" />
          ))}
        </div>
      ) : filteredApprovals.length === 0 ? (
        <div className="text-center py-10 bg-slate-950/50 rounded-lg border border-dashed border-slate-800">
          <p className="text-slate-400 text-sm">No {filter.toLowerCase()} approval requests found.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredApprovals.map((item) => (
            <div 
              key={item.id} 
              className="p-5 bg-slate-950 rounded-xl border border-slate-800 hover:border-slate-700 transition flex flex-col gap-3"
            >
              <div className="flex flex-wrap justify-between items-start gap-2">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-xs bg-sky-500/20 text-sky-400 border border-sky-500/30 px-2.5 py-0.5 rounded-full font-mono font-medium">
                    #{item.id}
                  </span>
                  <span className="text-sm font-bold text-white">{item.action}</span>
                </div>
                <span className={`text-xs px-2.5 py-1 rounded-full font-semibold border ${
                  item.status === 'APPROVED' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' :
                  item.status === 'REJECTED' ? 'bg-rose-500/10 text-rose-400 border-rose-500/30' :
                  'bg-amber-500/10 text-amber-400 border-amber-500/30'
                }`}>
                  {item.status || 'PENDING'}
                </span>
              </div>

              <div className="text-xs text-slate-300">
                <span className="text-slate-500">Target URL:</span>{' '}
                <code className="text-sky-300 break-all">{item.target_url}</code>
              </div>

              {item.code_patch && (
                <div className="space-y-1">
                  <span className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">Generated Code Patch</span>
                  <pre className="bg-slate-900 p-3 rounded-lg text-xs text-slate-200 overflow-x-auto border border-slate-800 font-mono">
                    {item.code_patch}
                  </pre>
                </div>
              )}

              {(item.status === 'PENDING' || !item.status) && (
                <div className="flex justify-end gap-2 pt-2 border-t border-slate-900">
                  <button
                    onClick={() => handleReview(item, 'REJECT')}
                    className="px-3.5 py-1.5 bg-rose-600/20 hover:bg-rose-600 text-rose-400 hover:text-white border border-rose-500/30 text-xs rounded-lg font-medium transition"
                  >
                    Reject
                  </button>
                  <button
                    onClick={() => handleReview(item, 'APPROVE')}
                    className="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs rounded-lg font-medium transition shadow-sm"
                  >
                    Approve & Apply
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};