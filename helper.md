# Tasks That Can Run on FastAPI in Vercel
## GA1 - 4,5 (Excel/GSheets formulas in Python)

You can compute Excel-like formulas using pandas, numpy, or openpyxl in a FastAPI endpoint.
Since no GUI automation is needed, this should work fine on Vercel.
GA1 - 6 (Scraping HTML with hidden inputs using LLM or parser)

If the HTML is passed in the request, you can parse it with BeautifulSoup or an LLM (like OpenAI API).
Since Vercel allows external API calls, LLM integration should work.
## GA1 - 13, 2 - 7 (Using GitHub API / GH CLI in container)

✅ GitHub API can run on Vercel using httpx or requests.
❌ GitHub CLI (gh command) won’t run directly on Vercel, as it requires a persistent environment.
Workaround: Deploy a microservice elsewhere (e.g., Render, Fly.io) to handle GitHub CLI.
## GA2 - 2 (Image responses as base64 data URIs)

Convert images to base64 in Python (PIL, base64 module) and return it in a JSON response.
This is lightweight and should work well on Vercel.
## GA2 - 3 (GitHub API if CLI isn't available)

This is similar to GA1 - 13, and it can be done using the GitHub API.
## GA2 - 6 (Deploying FastAPI apps on Vercel using LLM and API)

You can automate deployment via the Vercel API.
LLM (e.g., OpenAI, local models) can help generate FastAPI code dynamically.
#  Tasks That Need Workarounds
## GA2 - 8 (Uploading to DockerHub using the Docker API)

Problem: Vercel doesn’t support running Docker Daemon (required for docker push).
Workaround:
Use a GitHub Action to push images to DockerHub.
Use another service like Fly.io, Render, or a VPS to build and push Docker images.
## GA2 - 10 (Running Llamafile elsewhere if not on Vercel)

Vercel doesn’t support running binaries like Llamafile natively.
Solution:
Run Llamafile on another server (e.g., Fly.io, local server, or ngrok tunnel).
Make a FastAPI endpoint that forwards requests to the Llamafile server.
## GA3 - 4, 3 - 5 (Faking Google Colab response)

Colab API calls won’t work on Vercel because it requires an interactive session.
If you just need to return mocked responses, you can do this in a FastAPI route.