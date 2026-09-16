import sqlite3
import datetime

class ClientReportingAgent:
    def __init__(self, db_path: str = "seo_orchestrator.db"):
        self.db_path = db_path

    def generate_html_report(self, site_name: str) -> str:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Fetch approved logs
        cursor.execute("SELECT action_name, status, timestamp FROM audit_logs WHERE status='APPROVED'")
        approved_records = cursor.fetchall()
        conn.close()

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
                h1 {{ color: #1a365d; }}
                .badge {{ background: #def7ec; color: #03543f; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border: 1px solid #e2e8f0; padding: 12px; text-align: left; }}
                th {{ background-color: #f7fafc; }}
            </style>
        </head>
        <body>
            <h1>AI SEO Orchestrator - Executive Summary</h1>
            <p><strong>Target Site:</strong> {site_name}</p>
            <p><strong>Generated Date:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h2>Applied Fixes & Approved Code Patches</h2>
            <table>
                <tr>
                    <th>Action Item</th>
                    <th>Status</th>
                    <th>Timestamp</th>
                </tr>
        """
        
        for item, status, timestamp in approved_records:
            html_content += f"""
                <tr>
                    <td>{item}</td>
                    <td><span class="badge">{status}</span></td>
                    <td>{timestamp}</td>
                </tr>
            """

        html_content += """
            </table>
        </body>
        </html>
        """
        
        with open("SEO_Audit_Report.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        return "SEO_Audit_Report.html"