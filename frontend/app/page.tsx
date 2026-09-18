'use client';

import { useState, useEffect } from 'react';

// --- INLINE PHASE 1 INTELLIGENCE SECTION ---
function Phase1IntelligenceSection() {
  const [seedInput, setSeedInput] = useState('nextjs seo agency, fastapi developer usa');
  const [targetDomain, setTargetDomain] = useState('https://mohsinshahzad.vercel.app');
  const [competitorDomain, setCompetitorDomain] = useState('https://competitor-seo.com');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const runPhase1Action = async (endpoint: string, payload: any) => {
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch(`http://127.0.0.1:8000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      setResult({ endpoint, status: res.status, data });
    } catch (err) {
      setResult({ endpoint, error: String(err) });
    } finally {
      setLoading(false);
    }
  };

  const parsedSeeds = seedInput.split(',').map((s) => s.trim()).filter(Boolean);

  return (
    <section style={{ background: '#1e293b', padding: '24px', borderRadius: '12px', boxSizing: 'border-box', width: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <h2 style={{ margin: 0, color: '#38bdf8', fontSize: '20px' }}>🧠 Phase 1: Core Intelligence & Keyword Engine</h2>
        {loading && <span style={{ fontSize: '12px', color: '#38bdf8' }}>Processing API call...</span>}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '16px', marginBottom: '16px' }}>
        {/* Card 1: Keyword Fetch */}
        <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#fff' }}>1. Keyword Fetch (GKP / DataForSEO)</h3>
            <input
              type="text"
              value={seedInput}
              onChange={(e) => setSeedInput(e.target.value)}
              style={{ width: '100%', padding: '8px', marginBottom: '12px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '12px', borderRadius: '4px', boxSizing: 'border-box' }}
            />
          </div>
          <button
            onClick={() =>
              runPhase1Action('/api/v1/intelligence/keywords', {
                seed_keywords: parsedSeeds,
              })
            }
            disabled={loading}
            style={{ width: '100%', padding: '8px', background: '#0284c7', color: '#fff', border: 'none', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}
          >
            Fetch Keywords
          </button>
        </div>

        {/* Card 2: Competitor Gap Analysis */}
        <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#fff' }}>2. Competitor Gap Analysis</h3>
            <input
              type="text"
              value={targetDomain}
              onChange={(e) => setTargetDomain(e.target.value)}
              placeholder="Your URL"
              style={{ width: '100%', padding: '6px', marginBottom: '8px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
            />
            <input
              type="text"
              value={competitorDomain}
              onChange={(e) => setCompetitorDomain(e.target.value)}
              placeholder="Competitor URL"
              style={{ width: '100%', padding: '6px', marginBottom: '12px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
            />
          </div>
          <button
            onClick={() =>
              runPhase1Action('/api/v1/intelligence/competitor-gaps', {
                target_url: targetDomain,
                competitor_url: competitorDomain,
                reference_target_keywords: parsedSeeds,
              })
            }
            disabled={loading}
            style={{ width: '100%', padding: '8px', background: '#0284c7', color: '#fff', border: 'none', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}
          >
            Analyze Gaps
          </button>
        </div>

        {/* Card 3: GSC Historical Diff */}
<div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
  <div>
    <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#fff' }}>3. GSC Historical Diff</h3>
    <p style={{ fontSize: '11px', color: '#94a3b8', marginBottom: '12px' }}>
      Calculates Ranked & Deranked terms delta over 30d baseline.
    </p>
  </div>
  <button
    onClick={() =>
      runPhase1Action('/api/v1/intelligence/gsc-diff', {
        baseline_data: parsedSeeds.map((k, idx) => ({ keyword: k, position: 2.1 + idx })),
        current_data: parsedSeeds.map((k, idx) => ({ keyword: k, position: 1.5 + idx })),
        lookback_days: 30,
        position_threshold: 3,
      })
    }
    disabled={loading}
    style={{ width: '100%', padding: '8px', background: '#0284c7', color: '#fff', border: 'none', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}
  >
    Compute Diff
          </button>
        </div>
      </div>
      {result && (
        <div style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', padding: '12px', fontFamily: 'monospace', fontSize: '11px' }}>
          <div style={{ color: '#38bdf8', marginBottom: '6px', fontWeight: 'bold' }}>
            Response from {result.endpoint} (Status: {result.status}):
          </div>
          <pre style={{ margin: 0, color: '#cbd5e1', maxHeight: '200px', overflowY: 'auto', whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>
            {JSON.stringify(result.data || result.error, null, 2)}
          </pre>
        </div>
      )}
    </section>
  );
}

export default function Dashboard() {
  const [status, setStatus] = useState<string>('Checking...');
  const [auditUrl, setAuditUrl] = useState<string>('https://mohsinshahzad.vercel.app');
  const [loading, setLoading] = useState<boolean>(false);
  const [auditResult, setAuditResult] = useState<any>(null);
  const [approvedRecords, setApprovedRecords] = useState<any[]>([]);
  const [errorMsg, setErrorMsg] = useState<string>('');

  // Phase 4 States (Deployment & Rankings)
  const [deployStatus, setDeployStatus] = useState<string>('');
  const [deployLoading, setDeployLoading] = useState<boolean>(false);
  const [rankings, setRankings] = useState<any[]>([]);

  // Phase 2 Direct Push States
  const [wpDirectForm, setWpDirectForm] = useState({
    site_url: 'https://live.wordpress.site',
    api_key: '',
    post_id: '42',
    meta_title: 'Direct Push Meta Title',
    meta_description: 'Direct push description sync.'
  });
  const [wpDirectStatus, setWpDirectStatus] = useState<string>('');

  const [shopifyDirectForm, setShopifyDirectForm] = useState({
    shop_domain: 'mystore.myshopify.com',
    access_token: '',
    resource_id: 'gid://shopify/Product/12345',
    metafield_value: 'Direct metadata sync value'
  });
  const [shopifyDirectStatus, setShopifyDirectStatus] = useState<string>('');

  // Phase 3: Technical SEO & Indexing Acceleration States
  const [indexnowForm, setIndexnowForm] = useState({ host: 'mohsinshahzad.vercel.app', key: 'sample-key-12345', url_list: 'https://mohsinshahzad.vercel.app/' });
  const [indexnowStatus, setIndexnowStatus] = useState<string>('');
  const [psiForm, setPsiForm] = useState({ url: 'https://mohsinshahzad.vercel.app', strategy: 'mobile' });
  const [psiStatus, setPsiStatus] = useState<string>('');
  const [linksForm, setLinksForm] = useState({ target_url: 'https://mohsinshahzad.vercel.app/blog/nextjs-seo', keyword: 'nextjs seo agency' });
  const [linksStatus, setLinksStatus] = useState<string>('');

  // Phase 4 Semantic SEO deep modules States
  const [pseoForm, setPseoForm] = useState({ template_type: 'location-service', seed_keywords: 'fastapi developer usa, python saas' });
  const [pseoStatus, setPseoStatus] = useState<string>('');
  const [schemaForm, setSchemaForm] = useState({ entity_name: 'Mohsin Shahzad', entity_type: 'Person', context_url: 'https://mohsinshahzad.vercel.app' });
  const [schemaStatus, setSchemaStatus] = useState<string>('');
  const [decayForm, setDecayForm] = useState({ target_url: 'https://mohsinshahzad.vercel.app/blog/old-post', focus_keyword: 'seo audit' });
  const [decayStatus, setDecayStatus] = useState<string>('');

  // Phase 5 Off-Page & Authority Automation States
  const [mentionForm, setMentionForm] = useState({ brand_name: 'Mohsin AI Freelancer Assistant', domain: 'mohsinshahzad.vercel.app' });
  const [mentionStatus, setMentionStatus] = useState<string>('');
  const [backlinkForm, setBacklinkForm] = useState({ target_domain: 'mohsinshahzad.vercel.app', competitor_domain: 'competitor-seo.com' });
  const [backlinkStatus, setBacklinkStatus] = useState<string>('');

  // Phase 6 & 7 States
  const [cronInfo, setCronInfo] = useState<any>(null);
  const [kwSeed, setKwSeed] = useState<string>('nextjs seo agency, fastapi developer usa');
  const [kwResult, setKwResult] = useState<any[]>([]);
  const [kwLoading, setKwLoading] = useState<boolean>(false);
  const [dropStatus, setDropStatus] = useState<string>('');
  const [notifStatus, setNotifStatus] = useState<string>('');
  const [wpForm, setWpForm] = useState({
    base_url: 'https://staging.wordpress.site',
    username: 'admin',
    app_password: 'xxxx xxxx xxxx xxxx',
    post_id: '42',
    title: 'Optimized via AI SEO Engine',
    meta_description: 'High-converting technical SEO metadata push.'
  });
  const [wpStatus, setWpStatus] = useState<string>('');

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

  const fetchCronStatus = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/cron/status');
      const data = await res.json();
      setCronInfo(data);
    } catch (e) {}
  };

  useEffect(() => {
    fetch('http://127.0.0.1:8000/health')
      .then((res) => res.json())
      .then((data) => setStatus(data.status === 'ok' ? 'Connected (Online)' : 'Issue'))
      .catch(() => setStatus('Disconnected'));
    
    fetchApprovals();
    fetchRankings();
    fetchCronStatus();
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
          target_url: auditResult?.target_url || auditUrl,
          status: decisionStatus,
          proposed_content: item.proposed || null
        }),
      });
      const data = await res.json();
      alert(`Success: ${data.message}`);
      
      setAuditResult((prev: any) => prev ? ({
        ...prev,
        pending_approvals: prev.pending_approvals.filter((i: any) => i.id !== item.id),
      }) : null);
      fetchApprovals();
    } catch (err) {
      alert('Failed to record decision');
    }
  };

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

  // Phase 2 Direct Push Handlers
  const pushWpDirect = async () => {
    setWpDirectStatus('Pushing WP direct metadata...');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/cms/wordpress/push', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(wpDirectForm),
      });
      const data = await res.json();
      setWpDirectStatus(JSON.stringify(data));
    } catch (e) {
      setWpDirectStatus('WP direct push failed');
    }
  };

  const pushShopifyDirect = async () => {
    setShopifyDirectStatus('Pushing Shopify direct metafield...');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/cms/shopify/push', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(shopifyDirectForm),
      });
      const data = await res.json();
      setShopifyDirectStatus(JSON.stringify(data));
    } catch (e) {
      setShopifyDirectStatus('Shopify direct push failed');
    }
  };

  // Phase 3 Technical SEO Handlers
  const submitIndexNow = async () => {
    setIndexnowStatus('Submitting IndexNow...');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/technical-seo/indexnow/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          host: indexnowForm.host,
          key: indexnowForm.key,
          url_list: indexnowForm.url_list.split(',').map((u) => u.trim()).filter(Boolean),
        }),
      });
      const data = await res.json();
      setIndexnowStatus(JSON.stringify(data));
    } catch (e) {
      setIndexnowStatus('IndexNow submit failed');
    }
  };

  const monitorPsi = async () => {
    setPsiStatus('Monitoring PSI...');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/technical-seo/psi/monitor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(psiForm),
      });
      const data = await res.json();
      setPsiStatus(JSON.stringify(data));
    } catch (e) {
      setPsiStatus('PSI monitor failed');
    }
  };

  const injectLinks = async () => {
    setLinksStatus('Injecting internal links...');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/technical-seo/links/inject', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(linksForm),
      });
      const data = await res.json();
      setLinksStatus(JSON.stringify(data));
    } catch (e) {
      setLinksStatus('Link injection failed');
    }
  };

  // Phase 4 Semantic SEO Handlers
  const generatePseo = async () => {
    setPseoStatus('Generating pSEO bulk batch...');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/semantic-seo/pseo/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          template_type: pseoForm.template_type,
          seed_keywords: pseoForm.seed_keywords.split(',').map((k) => k.trim()).filter(Boolean),
        }),
      });
      const data = await res.json();
      setPseoStatus(JSON.stringify(data));
    } catch (e) {
      setPseoStatus('pSEO generation failed');
    }
  };

  const buildEntityGraph = async () => {
    setSchemaStatus('Building Entity Graph...');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/semantic-seo/schema/entity-graph', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(schemaForm),
      });
      const data = await res.json();
      setSchemaStatus(JSON.stringify(data));
    } catch (e) {
      setSchemaStatus('Entity graph builder failed');
    }
  };

  const injectFaq = async () => {
    setDecayStatus('Injecting FAQ for content decay fix...');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/semantic-seo/decay/inject-faq', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(decayForm),
      });
      const data = await res.json();
      setDecayStatus(JSON.stringify(data));
    } catch (e) {
      setDecayStatus('FAQ injector failed');
    }
  };

  // Phase 5 Off-Page & Authority Handlers
  const scanUnlinkedMentions = async () => {
    setMentionStatus('Scanning unlinked brand mentions...');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/authority-seo/mentions/scan-unlinked', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mentionForm),
      });
      const data = await res.json();
      setMentionStatus(JSON.stringify(data));
    } catch (e) {
      setMentionStatus('Mention scan failed');
    }
  };

  const analyzeBacklinkGap = async () => {
    setBacklinkStatus('Analyzing competitor backlink gap...');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/authority-seo/backlinks/gap-analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(backlinkForm),
      });
      const data = await res.json();
      setBacklinkStatus(JSON.stringify(data));
    } catch (e) {
      setBacklinkStatus('Backlink gap analysis failed');
    }
  };

  const analyzeKeywords = async () => {
    setKwLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/keywords/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          seed_keywords: kwSeed.split(',').map((k) => k.trim()).filter(Boolean),
          target_country: 'US'
        }),
      });
      const data = await res.json();
      setKwResult(data.analysis || []);
    } catch (e) {
      alert('Failed to analyze keywords');
    }
    setKwLoading(false);
  };

  const detectPositionDrops = async () => {
    setDropStatus('Scanning drops...');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/automation/position-drops/detect', { method: 'POST' });
      const data = await res.json();
      setDropStatus(JSON.stringify(data));
    } catch (e) {
      setDropStatus('Scan failed');
    }
  };

  const sendAuditReportNotification = async () => {
    setNotifStatus('Sending report notification...');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/automation/notifications/send-report', { method: 'POST' });
      const data = await res.json();
      setNotifStatus(JSON.stringify(data));
    } catch (e) {
      setNotifStatus('Failed to send notification');
    }
  };

  const deployWpPatch = async () => {
    setWpStatus('Pushing WP patch...');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/v1/adapters/wordpress/deploy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(wpForm),
      });
      const data = await res.json();
      setWpStatus(JSON.stringify(data));
    } catch (e) {
      setWpStatus('WP deploy failed');
    }
  };

  return (
    <div style={{ width: '100%', maxWidth: '1100px', margin: '0 auto', padding: '20px', fontFamily: 'sans-serif', background: '#0f172a', color: '#fff', minHeight: '100vh', boxSizing: 'border-box' }}>
      <header style={{ borderBottom: '1px solid #334155', paddingBottom: '20px', marginBottom: '24px' }}>
        <h1 style={{ margin: 0, color: '#38bdf8', fontSize: '28px' }}>🚀 AI SEO Orchestrator</h1>
        <p style={{ color: '#94a3b8', margin: '6px 0 12px 0' }}>Complete Phase 1–7: HITL Manager, pSEO, Cron, Multi-CMS Direct Push, Technical SEO & Authority Automation</p>
        <span style={{ padding: '4px 12px', borderRadius: '12px', fontSize: '12px', background: status.includes('Connected') ? '#059669' : '#dc2626', display: 'inline-block' }}>
          Backend: {status}
        </span>
      </header>

      <main style={{ display: 'grid', gap: '24px', width: '100%', boxSizing: 'border-box' }}>
        {/* 👉 PHASE 1: CORE INTELLIGENCE & KEYWORD ENGINE */}
        <Phase1IntelligenceSection />

        {/* 👉 PHASE 2: MULTI-CMS DIRECT PUSH */}
        <section style={{ background: '#1e293b', padding: '24px', borderRadius: '12px', boxSizing: 'border-box', width: '100%' }}>
          <div style={{ borderBottom: '1px solid #334155', paddingBottom: '16px', marginBottom: '20px' }}>
            <h2 style={{ margin: '0 0 4px 0', color: '#f59e0b', fontSize: '20px' }}>⚡ Phase 2: Multi-CMS Direct Push (Live Production)</h2>
            <p style={{ margin: 0, color: '#94a3b8', fontSize: '13px' }}>
              Direct API metadata/metafield injection bypassing staging queues.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
            {/* WP Direct Metadata Push */}
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#fff' }}>[ ] WP Direct Metadata Push</h3>
              <p style={{ fontSize: '11px', color: '#64748b', marginBottom: '10px' }}>POST /api/v1/cms/wordpress/push</p>
              <input
                type="text"
                value={wpDirectForm.meta_title}
                onChange={(e) => setWpDirectForm({ ...wpDirectForm, meta_title: e.target.value })}
                placeholder="Direct Push Meta Title"
                style={{ width: '100%', padding: '6px', marginBottom: '6px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <input
                type="text"
                value={wpDirectForm.meta_description}
                onChange={(e) => setWpDirectForm({ ...wpDirectForm, meta_description: e.target.value })}
                placeholder="Direct push description sync."
                style={{ width: '100%', padding: '6px', marginBottom: '10px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <button
                onClick={pushWpDirect}
                style={{ width: '100%', padding: '8px', background: '#f59e0b', color: '#0f172a', border: 'none', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}
              >
                Push WP Direct
              </button>
              {wpDirectStatus && (
                <pre style={{ fontSize: '10px', color: '#fcd34d', marginTop: '8px', overflowX: 'auto', whiteSpace: 'pre-wrap' }}>
                  {wpDirectStatus}
                </pre>
              )}
            </div>

            {/* Shopify Direct Metafield Push */}
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#fff' }}>[ ] Shopify Direct Metafield Push</h3>
              <p style={{ fontSize: '11px', color: '#64748b', marginBottom: '10px' }}>POST /api/v1/cms/shopify/push</p>
              <input
                type="text"
                value={shopifyDirectForm.resource_id}
                onChange={(e) => setShopifyDirectForm({ ...shopifyDirectForm, resource_id: e.target.value })}
                placeholder="gid://shopify/Product/12345"
                style={{ width: '100%', padding: '6px', marginBottom: '6px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <input
                type="text"
                value={shopifyDirectForm.metafield_value}
                onChange={(e) => setShopifyDirectForm({ ...shopifyDirectForm, metafield_value: e.target.value })}
                placeholder="Direct metadata sync value"
                style={{ width: '100%', padding: '6px', marginBottom: '10px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <button
                onClick={pushShopifyDirect}
                style={{ width: '100%', padding: '8px', background: '#f59e0b', color: '#0f172a', border: 'none', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}
              >
                Push Shopify Direct
              </button>
              {shopifyDirectStatus && (
                <pre style={{ fontSize: '10px', color: '#fcd34d', marginTop: '8px', overflowX: 'auto', whiteSpace: 'pre-wrap' }}>
                  {shopifyDirectStatus}
                </pre>
              )}
            </div>
          </div>
        </section>

        {/* 👉 PHASE 3: TECHNICAL SEO & INDEXING ACCELERATION */}
        <section style={{ background: '#1e293b', padding: '24px', borderRadius: '12px', boxSizing: 'border-box', width: '100%' }}>
          <div style={{ borderBottom: '1px solid #334155', paddingBottom: '16px', marginBottom: '20px' }}>
            <h2 style={{ margin: '0 0 4px 0', color: '#38bdf8', fontSize: '20px' }}>⚡ Phase 3: Technical SEO & Indexing Acceleration</h2>
            <p style={{ margin: 0, color: '#94a3b8', fontSize: '13px' }}>
              IndexNow submissions, Core Web Vitals monitoring, and automated internal link graph injection.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
            {/* IndexNow Instant Submit */}
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#fff' }}>[ ] IndexNow Instant Submit</h3>
              <p style={{ fontSize: '11px', color: '#64748b', marginBottom: '10px' }}>POST /api/v1/technical-seo/indexnow/submit</p>
              <input
                type="text"
                value={indexnowForm.host}
                onChange={(e) => setIndexnowForm({ ...indexnowForm, host: e.target.value })}
                placeholder="Host Domain"
                style={{ width: '100%', padding: '6px', marginBottom: '6px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <input
                type="text"
                value={indexnowForm.url_list}
                onChange={(e) => setIndexnowForm({ ...indexnowForm, url_list: e.target.value })}
                placeholder="URLs (comma-separated)"
                style={{ width: '100%', padding: '6px', marginBottom: '10px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <button onClick={submitIndexNow} style={{ width: '100%', padding: '8px', background: '#0284c7', color: '#fff', border: 'none', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}>
                Submit IndexNow
              </button>
              {indexnowStatus && <pre style={{ fontSize: '10px', color: '#38bdf8', marginTop: '8px', overflowX: 'auto', whiteSpace: 'pre-wrap' }}>{indexnowStatus}</pre>}
            </div>

            {/* Core Web Vitals (PSI) Monitor */}
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#fff' }}>[ ] Core Web Vitals (PSI) Monitor</h3>
              <p style={{ fontSize: '11px', color: '#64748b', marginBottom: '10px' }}>POST /api/v1/technical-seo/psi/monitor</p>
              <input
                type="text"
                value={psiForm.url}
                onChange={(e) => setPsiForm({ ...psiForm, url: e.target.value })}
                placeholder="Target URL"
                style={{ width: '100%', padding: '6px', marginBottom: '6px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <select
                value={psiForm.strategy}
                onChange={(e) => setPsiForm({ ...psiForm, strategy: e.target.value })}
                style={{ width: '100%', padding: '6px', marginBottom: '10px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              >
                <option value="mobile">Mobile Strategy</option>
                <option value="desktop">Desktop Strategy</option>
              </select>
              <button onClick={monitorPsi} style={{ width: '100%', padding: '8px', background: '#0284c7', color: '#fff', border: 'none', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}>
                Monitor PSI
              </button>
              {psiStatus && <pre style={{ fontSize: '10px', color: '#38bdf8', marginTop: '8px', overflowX: 'auto', whiteSpace: 'pre-wrap' }}>{psiStatus}</pre>}
            </div>

            {/* Auto Internal Link Injector */}
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#fff' }}>[ ] Auto Internal Link Injector</h3>
              <p style={{ fontSize: '11px', color: '#64748b', marginBottom: '10px' }}>POST /api/v1/technical-seo/links/inject</p>
              <input
                type="text"
                value={linksForm.target_url}
                onChange={(e) => setLinksForm({ ...linksForm, target_url: e.target.value })}
                placeholder="Target URL"
                style={{ width: '100%', padding: '6px', marginBottom: '6px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <input
                type="text"
                value={linksForm.keyword}
                onChange={(e) => setLinksForm({ ...linksForm, keyword: e.target.value })}
                placeholder="Anchor Keyword"
                style={{ width: '100%', padding: '6px', marginBottom: '10px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <button onClick={injectLinks} style={{ width: '100%', padding: '8px', background: '#0284c7', color: '#fff', border: 'none', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}>
                Inject Links
              </button>
              {linksStatus && <pre style={{ fontSize: '10px', color: '#38bdf8', marginTop: '8px', overflowX: 'auto', whiteSpace: 'pre-wrap' }}>{linksStatus}</pre>}
            </div>
          </div>
        </section>

        {/* 👉 PHASE 4 (SEMANTIC SEO DEEP MODULES) */}
        <section style={{ background: '#1e293b', padding: '24px', borderRadius: '12px', boxSizing: 'border-box', width: '100%' }}>
          <div style={{ borderBottom: '1px solid #334155', paddingBottom: '16px', marginBottom: '20px' }}>
            <h2 style={{ margin: '0 0 4px 0', color: '#10b981', fontSize: '20px' }}>🧩 Phase 4: Semantic SEO Deep Modules</h2>
            <p style={{ margin: 0, color: '#94a3b8', fontSize: '13px' }}>
              Programmatic pSEO generation, multi-entity knowledge graph builder, and content decay/FAQ repair.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
            {/* Programmatic pSEO Bulk Generator */}
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#fff' }}>[ ] Programmatic pSEO Bulk Generator</h3>
              <p style={{ fontSize: '11px', color: '#64748b', marginBottom: '10px' }}>POST /api/v1/semantic-seo/pseo/generate</p>
              <input
                type="text"
                value={pseoForm.template_type}
                onChange={(e) => setPseoForm({ ...pseoForm, template_type: e.target.value })}
                placeholder="Template Type"
                style={{ width: '100%', padding: '6px', marginBottom: '6px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <input
                type="text"
                value={pseoForm.seed_keywords}
                onChange={(e) => setPseoForm({ ...pseoForm, seed_keywords: e.target.value })}
                placeholder="Seed Keywords (comma-separated)"
                style={{ width: '100%', padding: '6px', marginBottom: '10px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <button onClick={generatePseo} style={{ width: '100%', padding: '8px', background: '#10b981', color: '#0f172a', border: 'none', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}>
                Generate pSEO
              </button>
              {pseoStatus && <pre style={{ fontSize: '10px', color: '#34d399', marginTop: '8px', overflowX: 'auto', whiteSpace: 'pre-wrap' }}>{pseoStatus}</pre>}
            </div>

            {/* Multi-Entity Schema Graph Builder */}
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#fff' }}>[ ] Multi-Entity Schema Graph Builder</h3>
              <p style={{ fontSize: '11px', color: '#64748b', marginBottom: '10px' }}>POST /api/v1/semantic-seo/schema/entity-graph</p>
              <input
                type="text"
                value={schemaForm.entity_name}
                onChange={(e) => setSchemaForm({ ...schemaForm, entity_name: e.target.value })}
                placeholder="Entity Name"
                style={{ width: '100%', padding: '6px', marginBottom: '6px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <input
                type="text"
                value={schemaForm.entity_type}
                onChange={(e) => setSchemaForm({ ...schemaForm, entity_type: e.target.value })}
                placeholder="Entity Type (Person/Organization)"
                style={{ width: '100%', padding: '6px', marginBottom: '10px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <button onClick={buildEntityGraph} style={{ width: '100%', padding: '8px', background: '#10b981', color: '#0f172a', border: 'none', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}>
                Build Entity Graph
              </button>
              {schemaStatus && <pre style={{ fontSize: '10px', color: '#34d399', marginTop: '8px', overflowX: 'auto', whiteSpace: 'pre-wrap' }}>{schemaStatus}</pre>}
            </div>

            {/* Content Decay & FAQ Injector */}
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#fff' }}>[ ] Content Decay & FAQ Injector</h3>
              <p style={{ fontSize: '11px', color: '#64748b', marginBottom: '10px' }}>POST /api/v1/semantic-seo/decay/inject-faq</p>
              <input
                type="text"
                value={decayForm.target_url}
                onChange={(e) => setDecayForm({ ...decayForm, target_url: e.target.value })}
                placeholder="Target URL"
                style={{ width: '100%', padding: '6px', marginBottom: '6px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <input
                type="text"
                value={decayForm.focus_keyword}
                onChange={(e) => setDecayForm({ ...decayForm, focus_keyword: e.target.value })}
                placeholder="Focus Keyword"
                style={{ width: '100%', padding: '6px', marginBottom: '10px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <button onClick={injectFaq} style={{ width: '100%', padding: '8px', background: '#10b981', color: '#0f172a', border: 'none', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}>
                Inject FAQ / Fix Decay
              </button>
              {decayStatus && <pre style={{ fontSize: '10px', color: '#34d399', marginTop: '8px', overflowX: 'auto', whiteSpace: 'pre-wrap' }}>{decayStatus}</pre>}
            </div>
          </div>
        </section>

        {/* 👉 PHASE 5: OFF-PAGE & AUTHORITY AUTOMATION */}
        <section style={{ background: '#1e293b', padding: '24px', borderRadius: '12px', boxSizing: 'border-box', width: '100%' }}>
          <div style={{ borderBottom: '1px solid #334155', paddingBottom: '16px', marginBottom: '20px' }}>
            <h2 style={{ margin: '0 0 4px 0', color: '#c084fc', fontSize: '20px' }}>🌐 Phase 5: Off-Page & Authority Automation</h2>
            <p style={{ margin: 0, color: '#94a3b8', fontSize: '13px' }}>
              Unlinked brand mention scanner and competitor backlink gap discovery.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
            {/* Unlinked Brand Mention Scanner */}
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#fff' }}>[ ] Unlinked Brand Mention Scanner</h3>
              <p style={{ fontSize: '11px', color: '#64748b', marginBottom: '10px' }}>POST /api/v1/authority-seo/mentions/scan-unlinked</p>
              <input
                type="text"
                value={mentionForm.brand_name}
                onChange={(e) => setMentionForm({ ...mentionForm, brand_name: e.target.value })}
                placeholder="Brand Name"
                style={{ width: '100%', padding: '6px', marginBottom: '6px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <input
                type="text"
                value={mentionForm.domain}
                onChange={(e) => setMentionForm({ ...mentionForm, domain: e.target.value })}
                placeholder="Domain"
                style={{ width: '100%', padding: '6px', marginBottom: '10px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <button onClick={scanUnlinkedMentions} style={{ width: '100%', padding: '8px', background: '#c084fc', color: '#0f172a', border: 'none', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}>
                Scan Unlinked Mentions
              </button>
              {mentionStatus && <pre style={{ fontSize: '10px', color: '#e9d5ff', marginTop: '8px', overflowX: 'auto', whiteSpace: 'pre-wrap' }}>{mentionStatus}</pre>}
            </div>

            {/* Competitor Backlink Gap Analyzer */}
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#fff' }}>[ ] Competitor Backlink Gap Analyzer</h3>
              <p style={{ fontSize: '11px', color: '#64748b', marginBottom: '10px' }}>POST /api/v1/authority-seo/backlinks/gap-analysis</p>
              <input
                type="text"
                value={backlinkForm.target_domain}
                onChange={(e) => setBacklinkForm({ ...backlinkForm, target_domain: e.target.value })}
                placeholder="Target Domain"
                style={{ width: '100%', padding: '6px', marginBottom: '6px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <input
                type="text"
                value={backlinkForm.competitor_domain}
                onChange={(e) => setBacklinkForm({ ...backlinkForm, competitor_domain: e.target.value })}
                placeholder="Competitor Domain"
                style={{ width: '100%', padding: '6px', marginBottom: '10px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <button onClick={analyzeBacklinkGap} style={{ width: '100%', padding: '8px', background: '#c084fc', color: '#0f172a', border: 'none', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}>
                Analyze Backlink Gap
              </button>
              {backlinkStatus && <pre style={{ fontSize: '10px', color: '#e9d5ff', marginTop: '8px', overflowX: 'auto', whiteSpace: 'pre-wrap' }}>{backlinkStatus}</pre>}
            </div>
          </div>
        </section>

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

        {/* PHASE 6 & 7: CRON, pSEO & MULTI-CMS STAGING ADAPTERS */}
        <section style={{ background: '#1e293b', padding: '24px', borderRadius: '12px', boxSizing: 'border-box', width: '100%' }}>
          <div style={{ borderBottom: '1px solid #334155', paddingBottom: '16px', marginBottom: '20px' }}>
            <h2 style={{ margin: '0 0 4px 0', color: '#38bdf8', fontSize: '20px' }}>⚙️ Phase 6 & 7: Autonomous Cron, pSEO & Staging CMS</h2>
            <p style={{ margin: 0, color: '#94a3b8', fontSize: '13px' }}>
              Cron monitoring, programmatic keyword/intent analysis, and headless WP/Shopify staging deployment.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '16px' }}>
            {/* Cron & Notifications Box */}
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '15px' }}>⏰ Cron & Notifications</h3>
              <p style={{ fontSize: '12px', color: '#94a3b8', marginBottom: '12px' }}>
                Status: {cronInfo?.status || 'active'} | Jobs: {cronInfo?.scheduled_jobs_count ?? 2}
              </p>
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                <button onClick={detectPositionDrops} style={{ padding: '8px 12px', background: '#334155', color: '#fff', border: 'none', borderRadius: '4px', fontSize: '12px', cursor: 'pointer' }}>
                  Detect Drops
                </button>
                <button onClick={sendAuditReportNotification} style={{ padding: '8px 12px', background: '#334155', color: '#fff', border: 'none', borderRadius: '4px', fontSize: '12px', cursor: 'pointer' }}>
                  Send Report
                </button>
              </div>
              {(dropStatus || notifStatus) && (
                <pre style={{ fontSize: '11px', color: '#34d399', marginTop: '8px', overflowX: 'auto' }}>
                  {dropStatus} {notifStatus}
                </pre>
              )}
            </div>

            {/* WordPress CMS Adapter Box */}
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '15px' }}>🌐 WordPress Staging Deploy</h3>
              <input
                type="text"
                value={wpForm.base_url}
                onChange={(e) => setWpForm({ ...wpForm, base_url: e.target.value })}
                placeholder="WP URL"
                style={{ width: '100%', padding: '6px', marginBottom: '6px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <input
                type="text"
                value={wpForm.title}
                onChange={(e) => setWpForm({ ...wpForm, title: e.target.value })}
                placeholder="Post Title"
                style={{ width: '100%', padding: '6px', marginBottom: '8px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <button onClick={deployWpPatch} style={{ width: '100%', padding: '8px', background: '#0284c7', color: '#fff', border: 'none', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}>
                Deploy WP Patch
              </button>
              {wpStatus && <p style={{ fontSize: '11px', color: '#34d399', marginTop: '6px', wordBreak: 'break-all' }}>{wpStatus}</p>}
            </div>

            {/* Shopify CMS Adapter Box */}
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '15px' }}>🛍️ Shopify Staging Deploy</h3>
              <input
                type="text"
                defaultValue="mystore.myshopify.com"
                id="shopify-url"
                placeholder="Shopify Store Domain"
                style={{ width: '100%', padding: '6px', marginBottom: '6px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <input
                type="text"
                defaultValue="SEO Metadata Metafield Update"
                id="shopify-title"
                placeholder="Title/Resource"
                style={{ width: '100%', padding: '6px', marginBottom: '8px', background: '#1e293b', border: '1px solid #475569', color: '#fff', fontSize: '11px', borderRadius: '4px', boxSizing: 'border-box' }}
              />
              <button 
                onClick={async () => {
                  const shopUrl = (document.getElementById('shopify-url') as HTMLInputElement)?.value;
                  const title = (document.getElementById('shopify-title') as HTMLInputElement)?.value;
                  const res = await fetch('http://127.0.0.1:8000/api/v1/adapters/shopify/deploy', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ shop_url: shopUrl, title })
                  });
                  const d = await res.json();
                  alert(JSON.stringify(d));
                }} 
                style={{ width: '100%', padding: '8px', background: '#059669', color: '#fff', border: 'none', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold', cursor: 'pointer' }}
              >
                Deploy Shopify Patch
              </button>
            </div>
          </div>

          {/* pSEO Keyword Analyzer */}
          <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155', marginTop: '16px' }}>
            <h3 style={{ margin: '0 0 8px 0', fontSize: '15px' }}>🔍 pSEO Keyword & Intent Analyzer (/api/v1/keywords/analyze)</h3>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              <input
                type="text"
                value={kwSeed}
                onChange={(e) => setKwSeed(e.target.value)}
                style={{ flex: '1 1 250px', padding: '8px', background: '#1e293b', border: '1px solid #475569', color: '#fff', borderRadius: '4px', fontSize: '12px' }}
              />
              <button onClick={analyzeKeywords} disabled={kwLoading} style={{ padding: '8px 16px', background: '#059669', color: '#fff', border: 'none', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer', fontSize: '12px' }}>
                {kwLoading ? 'Analyzing...' : 'Analyze'}
              </button>
            </div>
            {kwResult.length > 0 && (
              <div style={{ display: 'grid', gap: '6px', marginTop: '12px' }}>
                {kwResult.map((item: any, idx: number) => (
                  <div key={idx} style={{ background: '#1e293b', padding: '8px 12px', borderRadius: '4px', fontSize: '12px', display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '6px' }}>
                    <span style={{ fontWeight: 'bold', color: '#fff' }}>{item.keyword}</span>
                    <span style={{ color: '#38bdf8' }}>{item.intent} | {item.difficulty}</span>
                    <span style={{ color: '#94a3b8' }}>{item.recommended_action}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
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
                      <div style={{ flex: 'none', display: 'flex', gap: '8px' }}>
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