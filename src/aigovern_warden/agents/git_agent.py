import os
from github import Github
from aigovern_warden.agents.scout import WardenState

def run_github_agent(state: WardenState) -> dict:
    """
    Agent 4: Pushes the Terraform fix to a new branch and opens a PR.
    """
    print("--- [AGENT] GitHub: Creating Remediation Pull Request ---")
    
    gh = Github(os.getenv("GITHUB_TOKEN"))
    repo = gh.get_repo(os.getenv("GITHUB_REPO"))
    
    # Extract the Terraform code from the findings
    # (We assume the last finding contains the Terraform block)
    tf_content = state["findings"][-1]
    
    branch_name = "fix/shadow-ai-remediation"
    base_branch = repo.default_branch

    try:
        # 1. Create a new branch
        sb = repo.get_branch(base_branch)
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=sb.commit.sha)

        # 2. Create the file in the new branch
        repo.create_file(
            path="remediation_fix.tf",
            message="feat: autonomous AI compliance remediation",
            content=tf_content,
            branch=branch_name
        )

        # 3. Open the Pull Request
        pr = repo.create_pull(
            title="[WARDEN] Automated AI Compliance Fix",
            body="The AIGovern Warden has detected non-compliant resources. This PR migrates them to the sovereign 'westus' region.",
            head=branch_name,
            base=base_branch
        )
        
        return {"findings": state["findings"] + [f"SUCCESS: Pull Request opened at {pr.html_url}"]}

    except Exception as e:
        return {"findings": state["findings"] + [f"GITHUB_ERROR: {str(e)}"]}