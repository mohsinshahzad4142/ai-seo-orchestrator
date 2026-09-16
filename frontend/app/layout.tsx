import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'AI SEO Orchestrator Dashboard',
  description: 'Multi-Agent SEO Management & HITL Approval Queue',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{ margin: 0, padding: 0, fontFamily: 'system-ui, sans-serif', backgroundColor: '#0f172a', color: '#f8fafc' }}>
        {children}
      </body>
    </html>
  );
}