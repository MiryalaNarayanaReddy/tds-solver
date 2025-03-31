import httpx  # Use httpx for async requests
import base64

# Fetch file SHA (required for updates)
async def get_file_sha(FILE_PATH, REPO_OWNER, REPO_NAME, GITHUB_TOKEN=None):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("sha")
    return None


async def update_github_file(content, FILE_PATH, REPO_OWNER, REPO_NAME, BRANCH, GITHUB_TOKEN):
    try:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Content-Type": "application/json",
        }
        payload = {
            "message": "Updating index.html via GitHub API",
            "content": base64.b64encode(content.encode()).decode(),
            "branch": BRANCH,
        }

        sha = await get_file_sha(FILE_PATH, REPO_OWNER, REPO_NAME, GITHUB_TOKEN)

        if sha:
            payload["sha"] = sha  # Required for updating an existing file

        async with httpx.AsyncClient() as client:
            response = await client.put(url, headers=headers, json=payload)

        if response.status_code in [200, 201]:
            return True  # Successfully updated

        return {"error": f"GitHub API error: {response.status_code}, {response.text}"}

    except Exception as e:
        return {"error": f"Error updating GitHub file: {e}"}


async def trigger_github_workflow(REPO_OWNER, REPO_NAME, WORKFLOW_FILENAME, GITHUB_TOKEN, REF="main"):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILENAME}/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    payload = {"ref": REF}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)

    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    if response.status_code == 204:
        return {"success": "Workflow triggered successfully"}
    return {"error": f"GitHub API error: {response.status_code}, {response.text}"}