'use client';

import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [status, setStatus] = useState<string>('Checking...');
  const [auditUrl, setAuditUrl] = useState<string>('https://mohsinshahzad.vercel.app');
  const [loading, setLoading] = useState<boolean>(false);
  const [auditResult, setAuditResult] = useState<any>(null);
  const [approvedRecords, setApprovedRecords] = useState<any[]>([]);
  const [errorMsg, setErrorMsg] = useState<string>('');

  // Phase 4 States
  const [deployStatus, setDeployStatus] = useState<string>('');
  const [deployLoading, setDeployLoading] = useState<boolean>(false);
  const [rankings, setRankings] = useState<any[]>([]);

  const fetchApprovals = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/approvals');
      const data = await res.json();
      setApprovedRecords(data);
    } catch (e) {}
  };

  const fetchRankings = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/phase4/rankings');
      const result = await res.json();
      setRankings(result.data || []);
    } catch (e) {}
  };

  useEffect(() => {
    fetch('http://127.0.0.1:8000/health')
      .then((res) => res.json())
      .then((data) => setStatus(data.status === 'ok' ? 'Connected (Online)' : 'Issue'))
      .catch(() => setStatus('Disconnected'));
    
    fetchApprovals();
    fetchRankings();
  }, []);

  const runAudit = async () => {
    setLoading(true);
    setAuditResult(null);
    setErrorMsg('');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/audit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: auditUrl }),
      });
      const data = await res.json();
      if (!res.ok || data.detail) setErrorMsg(data.detail || 'Audit failed');
      else setAuditResult(data);
    } catch (err: any) {
      setErrorMsg('Backend connection failed');
    }
    setLoading(false);
  };

  const handleDecision = async (item: any, decisionStatus: 'APPROVED' | 'REJECTED') => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/approve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          item_id: item.id,
          action: item.action,
          target_url: auditResult.target_url,
          status: decisionStatus,
          proposed_content: item.proposed || null
        }),
      });
      const data = await res.json();
      alert(`Success: ${data.message}`);
      
      setAuditResult((prev: any) => ({
        ...prev,
        pending_approvals: prev.pending_approvals.filter((i: any) => i.id !== item.id),
      }));
      fetchApprovals();
    } catch (err) {
      alert('Failed to record decision');
    }
  };

  // Phase 4: Handle Trigger Deployment
  const handleDeploy = async () => {
    setDeployLoading(true);
    setDeployStatus('');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/phase4/deploy', {
        method: 'POST',
      });
      const data = await res.json();
      setDeployStatus(data.message || 'Deployment triggered successfully!');
    } catch (err) {
      setDeployStatus('Failed to trigger deployment.');
    }
    setDeployLoading(false);
  };

  return (
    <div style={{ width: '100%', maxWidth: '1100px', margin: '0 auto', padding: '20px', fontFamily: 'sans-serif', background: '#0f172a', color: '#fff', minHeight: '100vh', boxSizing: 'border-box' }}>
      <header style={{ borderBottom: '1px solid #334155', paddingBottom: '20px', marginBottom: '24px' }}>
        <h1 style={{ margin: 0, color: '#38bdf8', fontSize: '28px' }}>🚀 AI SEO Orchestrator</h1>
        <p style={{ color: '#94a3b8', margin: '6px 0 12px 0' }}>Phase 3 & 4: HITL Manager, Code Patch, Auto-Deploy & Rank Tracker</p>
        <span style={{ padding: '4px 12px', borderRadius: '12px', fontSize: '12px', background: status.includes('Connected') ? '#059669' : '#dc2626', display: 'inline-block' }}>
          Backend: {status}
        </span>
      </header>

      <main style={{ display: 'grid', gap: '24px', width: '100%', boxSizing: 'border-box' }}>
        {/* TARGET SITE AUDIT */}
        <section style={{ background: '#1e293b', padding: '24px', borderRadius: '12px', boxSizing: 'border-box', width: '100%' }}>
          <h2 style={{ marginTop: 0 }}>Target Site Audit</h2>
          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', width: '100%', boxSizing: 'border-box' }}>
            <input
              type="text"
              value={auditUrl}
              onChange={(e) => setAuditUrl(e.target.value)}
              style={{ flex: '1 1 300px', minWidth: '0', padding: '12px', borderRadius: '6px', border: '1px solid #475569', background: '#0f172a', color: '#fff', boxSizing: 'border-box' }}
            />
            <button 
              onClick={runAudit} 
              disabled={loading} 
              style={{ flexShrink: 0, padding: '12px 24px', background: '#0284c7', color: '#fff', border: 'none', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer', whiteSpace: 'nowrap' }}
            >
              {loading ? 'Processing Phase 3...' : 'Run Phase 3 Audit'}
            </button>
          </div>

          {errorMsg && <div style={{ marginTop: '16px', background: '#7f1d1d', padding: '12px', borderRadius: '6px', color: '#fca5a5' }}>{errorMsg}</div>}
        </section>

        {/* HITL APPROVAL QUEUE */}
        <section style={{ background: '#1e293b', padding: '24px', borderRadius: '12px', boxSizing: 'border-box', width: '100%' }}>
          <h2 style={{ marginTop: 0 }}>HITL (Human-In-The-Loop) Approval Queue</h2>
          {!auditResult?.pending_approvals?.length ? (
            <p style={{ color: '#64748b' }}>No pending approvals. Run audit to generate tasks.</p>
          ) : (
            <div style={{ display: 'grid', gap: '12px', width: '100%' }}>
              {auditResult.pending_approvals.map((item: any) => (
                <div key={item.id} style={{ padding: '16px', background: '#0f172a', borderLeft: '4px solid #f59e0b', borderRadius: '6px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
                  <div style={{ flex: '1 1 250px', marginRight: '16px' }}>
                    <span style={{ fontSize: '12px', color: '#f59e0b', fontWeight: 'bold' }}>[{item.type}]</span>
                    <p style={{ margin: '4px 0', fontWeight: 'bold' }}>{item.issue}</p>
                  </div>
                  <div style={{ display: 'flex', gap: '8px', flexShrink: 0 }}>
                    <button onClick={() => handleDecision(item, 'APPROVED')} style={{ padding: '10px 16px', background: '#10b981', color: '#fff', border: 'none', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer' }}>
                      Approve & Patch
                    </button>
                    <button onClick={() => handleDecision(item, 'REJECTED')} style={{ padding: '10px 16px', background: '#ef4444', color: '#fff', border: 'none', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer' }}>
                      Reject
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* AGENT 6 & 7: DB RECORDS & CODE PATCHES */}
        <section style={{ background: '#1e293b', padding: '24px', borderRadius: '12px', boxSizing: 'border-box', width: '100%' }}>
          <h2 style={{ marginTop: 0 }}>📁 Agent 6 & 7: Saved DB Records & Generated Code Patches</h2>
          {!approvedRecords.length ? (
            <p style={{ color: '#64748b' }}>No database records found yet.</p>
          ) : (
            <div style={{ display: 'grid', gap: '16px', width: '100%' }}>
              {approvedRecords.map((rec) => (
                <div key={rec.id} style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', borderLeft: rec.status === 'APPROVED' ? '4px solid #10b981' : '4px solid #ef4444', boxSizing: 'border-box', width: '100%' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', flexWrap: 'wrap', gap: '8px' }}>
                    <strong>#{rec.id} {rec.action}</strong>
                    <span style={{ fontSize: '12px', padding: '2px 8px', borderRadius: '4px', background: rec.status === 'APPROVED' ? '#065f46' : '#991b1b' }}>{rec.status}</span>
                  </div>
                  <p style={{ fontSize: '12px', color: '#64748b', margin: '4px 0' }}>Time: {rec.created_at}</p>
                  {rec.status === 'APPROVED' && (
                    <pre style={{ background: '#1e293b', padding: '12px', borderRadius: '6px', color: '#38bdf8', overflowX: 'auto', fontSize: '12px', marginTop: '8px', whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                      {rec.code_patch}
                    </pre>
                  )}
                </div>
              ))}
            </div>
          )}
        </section>

        {/* PHASE 4: DEPLOYMENT, TRACKING & REPORTING */}
        <section style={{ background: '#1e293b', padding: '24px', borderRadius: '12px', boxSizing: 'border-box', width: '100%' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', borderBottom: '1px solid #334155', paddingBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
            <div>
              <h2 style={{ margin: 0, color: '#34d399', fontSize: '20px' }}>🚀 Phase 4: Deployment, Tracking & Reporting</h2>
              <p style={{ margin: '4px 0 0 0', color: '#94a3b8', fontSize: '14px' }}>
                Automated deployment triggers, live rank tracking, and executive client reports.
              </p>
            </div>
            <a
              href={`http://127.0.0.1:8000/api/v1/phase4/generate-report?target_url=${encodeURIComponent(auditUrl)}`}
              target="_blank"
              rel="noopener noreferrer"
              style={{ flexShrink: 0, padding: '10px 18px', background: '#059669', color: '#fff', textDecoration: 'none', borderRadius: '6px', fontWeight: 'bold', fontSize: '14px', whiteSpace: 'nowrap' }}
            >
              📄 Download Executive Report
            </a>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px', width: '100%' }}>
            {/* Agent 8: Auto-Deployer */}
            <div style={{ background: '#0f172a', padding: '20px', borderRadius: '8px', border: '1px solid #334155', boxSizing: 'border-box' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '16px', color: '#38bdf8' }}>🤖 Agent 8: Auto-Deployer</h3>
              <p style={{ fontSize: '13px', color: '#94a3b8', marginBottom: '16px' }}>
                Trigger direct live deployment via Vercel / GitHub integration.
              </p>
              <button
                onClick={handleDeploy}
                disabled={deployLoading}
                style={{ width: '100%', padding: '10px', background: '#0284c7', color: '#fff', border: 'none', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer', opacity: deployLoading ? 0.6 : 1 }}
              >
                {deployLoading ? 'Deploying...' : 'Trigger Live Deployment'}
              </button>
              {deployStatus && (
                <p style={{ fontSize: '12px', color: '#34d399', marginTop: '10px', fontFamily: 'monospace', wordBreak: 'break-word' }}>
                  {deployStatus}
                </p>
              )}
            </div>

            {/* Agent 9: Rank Tracker */}
            <div style={{ background: '#0f172a', padding: '20px', borderRadius: '8px', border: '1px solid #334155', boxSizing: 'border-box' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '16px', color: '#38bdf8' }}>📈 Agent 9: Rank Tracker</h3>
              <p style={{ fontSize: '13px', color: '#94a3b8', marginBottom: '12px' }}>
                Live GSC keyword metrics & search visibility.
              </p>
              {!rankings.length ? (
                <p style={{ fontSize: '12px', color: '#64748b' }}>No ranking data available.</p>
              ) : (
                <div style={{ display: 'grid', gap: '8px' }}>
                  {rankings.map((r: any, i: number) => (
                    <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#1e293b', padding: '8px 12px', borderRadius: '4px', fontSize: '12px', flexWrap: 'wrap', gap: '4px' }}>
                      <span style={{ color: '#cbd5e1', fontWeight: 'bold' }}>{r.keyword}</span>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <span style={{ color: '#34d399' }}>Pos: #{r.position}</span>
                        <span style={{ color: '#94a3b8' }}>{r.clicks} clicks</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}