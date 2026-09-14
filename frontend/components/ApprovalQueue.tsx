import React, { useState, useEffect } from 'react';

interface ApprovalItem {
  id: number;
  agent_name: string;
  action_type: string;
  target_url: string;
  payload: any;
  status: string;
}

export const ApprovalQueue: React.FC<{ websiteId: number }> = ({ websiteId }) => {
  const [approvals, setApprovals] = useState<ApprovalItem[]>([]);

  useEffect(() => {
    fetch(`/api/v1/approvals/pending?website_id=${websiteId}`)
      .then((res) => res.json())
      .then((data) => setApprovals(data));
  }, [websiteId]);

  const handleReview = async (id: number, action: 'APPROVE' | 'REJECT') => {
    await fetch(`/api/v1/approvals/${id}/review`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action }),
    });
    setApprovals(approvals.filter((item) => item.id !== id));
  };

  return (
    <div className="p-6 bg-slate-900 text-white rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4">HITL Pending Approvals</h2>
      {approvals.length === 0 ? (
        <p className="text-gray-400">No pending approval requests.</p>
      ) : (
        <div className="space-y-4">
          {approvals.map((item) => (
            <div key={item.id} className="p-4 bg-slate-800 rounded border border-slate-700 flex justify-between items-center">
              <div>
                <span className="text-xs bg-indigo-600 px-2 py-1 rounded font-mono mr-2">{item.agent_name}</span>
                <span className="font-semibold">{item.action_type}</span>
                <p className="text-sm text-gray-300 mt-1">{item.target_url}</p>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => handleReview(item.id, 'APPROVE')}
                  className="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white text-sm rounded font-medium"
                >
                  Approve
                </button>
                <button
                  onClick={() => handleReview(item.id, 'REJECT')}
                  className="px-3 py-1 bg-rose-600 hover:bg-rose-500 text-white text-sm rounded font-medium"
                >
                  Reject
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
