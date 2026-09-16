import os
from dotenv import load_dotenv

# Force load .env file at module startup
load_dotenv()

class AutoDeploymentAgent:
    def __init__(self):
        self.branch = os.getenv("GITHUB_BRANCH", "main")

    def push_patch_to_github(
        self, 
        file_path: str = "app/layout.tsx", 
        patch_code: str = "", 
        commit_msg: str = "SEO & UI Fix: Preserved global CSS and updated metadata"
    ):
        github_token = os.getenv("GITHUB_TOKEN")
        repo_name = os.getenv("GITHUB_REPO")

        if not github_token or not repo_name:
            return {
                "status": "mock_success",
                "message": "Pushed to GitHub successfully! (Mock Mode: Set GITHUB_TOKEN and GITHUB_REPO in .env)"
            }

        try:
            from github import Github
        except ImportError:
            return {
                "status": "error",
                "message": "Missing 'PyGithub' library. Run 'pip install PyGithub' in terminal."
            }

        try:
            g = Github(github_token)
            repo = g.get_repo(repo_name)
            contents = repo.get_contents(file_path, ref=self.branch)
            
            # Restores Global CSS import + Metadata
            if not patch_code:
                patch_code = """import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Web Development Services | Full-Stack & Next.js Developer",
  description: "Professional website development services for modern web apps, SaaS, and custom platforms. Fast, SEO-ready & scalable.",
  keywords: ["web development services", "website development service", "website development services near me"],
  metadataBase: new URL("https://mohsinshahzad.vercel.app"),
  alternates: {
    canonical: "/",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
"""

            repo.update_file(
                path=contents.path,
                message=commit_msg,
                content=patch_code,
                sha=contents.sha,
                branch=self.branch
            )

            return {
                "status": "success",
                "message": f"Successfully updated '{file_path}' on GitHub! Vercel is deploying styling + metadata."
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"GitHub Commit Error: {str(e)}"
            }

    def trigger_vercel_deployment(self):
        return self.push_patch_to_github()