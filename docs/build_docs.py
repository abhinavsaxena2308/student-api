"""Builds Docker_Documentation.md and Docker_Documentation.docx from one content list.

Flow: DevOps and CI/CD -> Git and GitHub -> CI/CD with GitHub Actions
      -> Containerization (Docker) and Orchestration (Kubernetes)

Run from anywhere:  python docs/build_docs.py
"""
import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

DOCS = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(DOCS, "screenshots")
ROOT = os.path.dirname(DOCS)
REPO = "https://github.com/abhinavsaxena2308/student-api"
IMAGE = "ghcr.io/abhinavsaxena2308/student-api"


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read().rstrip()


# ---------------------------------------------------------------------------
# Content. Item types:
#   ("title"|"subtitle"|"part"|"h1"|"h2"|"h3", text)  ("p", text)  ("bullets", [..])
#   ("code", text, lang)
#   ("cmd", screenshot_key, command, explanation)   -> terminal screenshot
#   ("img", file, caption)                          -> app / browser screenshot
#   ("table", [header], [[row], ...])
# "part" starts a new page and is a top-level (Heading 1) entry in the contents list.
# ---------------------------------------------------------------------------
C = []
add = C.append

add(("title", "DevOps Practical Documentation"))
add(("subtitle", "Student Management API: Git & GitHub, CI/CD with GitHub Actions, "
                 "Docker and Kubernetes"))
add(("p", f"Project repository: {REPO}"))

# ===========================================================================
add(("part", "DevOps and CI/CD"))
# ===========================================================================
add(("h1", "What is DevOps"))
add(("p", "DevOps is a set of practices that brings software development (Dev) and IT operations "
          "(Ops) together. Instead of developers handing code over to a separate team to deploy, "
          "the whole path from writing code to running it in production is automated, repeatable "
          "and owned by one team. The goals are faster releases, fewer failures and quicker recovery."))
add(("h3", "The DevOps lifecycle"))
add(("table", ["Stage", "What happens", "Tool used in this project"], [
    ["Plan", "Decide features and fixes", "GitHub repository"],
    ["Code", "Write code and track every change", "Git, GitHub"],
    ["Build", "Turn source code into a runnable artifact", "Docker (image build)"],
    ["Test", "Run automated tests on every change", "Jest + Supertest in GitHub Actions"],
    ["Release", "Publish a versioned artifact", "GitHub Container Registry (GHCR)"],
    ["Deploy", "Run the artifact on servers", "Kubernetes"],
    ["Operate", "Keep it running, scale, self-heal", "Kubernetes Deployments"],
    ["Monitor", "Watch logs, health and resources", "kubectl logs, docker stats, /health"],
]))
add(("h1", "What is CI/CD"))
add(("table", ["Term", "Meaning"], [
    ["Continuous Integration (CI)", "Every push is automatically built and tested, so broken code is "
                                    "caught within minutes instead of at release time."],
    ["Continuous Delivery", "Every change that passes CI produces a release-ready artifact "
                            "(here: a Docker image)."],
    ["Continuous Deployment", "The release is deployed automatically without manual steps."],
    ["Pipeline", "The ordered set of automated stages a change goes through (test → build → publish)."],
]))
add(("h1", "Tools used"))
add(("table", ["Category", "Tool", "Role in this project"], [
    ["Version control", "Git", "Track changes, branches, merges"],
    ["Code hosting", "GitHub", "Remote repository, pull requests, Actions, packages"],
    ["CI/CD", "GitHub Actions", "Test, build and publish on every push"],
    ["Containerization", "Docker, Docker Compose", "Package the API and MongoDB as containers"],
    ["Registry", "GHCR (ghcr.io)", "Stores the published images"],
    ["Orchestration", "Kubernetes (Docker Desktop)", "Deploy, scale and self-heal the containers"],
]))
add(("h1", "The project: Student Management API"))
add(("p", "A REST API built with Node.js, Express and MongoDB (Mongoose) that performs CRUD "
          "operations on student records."))
add(("table", ["Method", "Endpoint", "Description"], [
    ["GET", "/api/students", "List all students"],
    ["GET", "/api/students/:id", "Get a single student"],
    ["POST", "/api/students", "Create a student"],
    ["PUT", "/api/students/:id", "Update a student"],
    ["DELETE", "/api/students/:id", "Delete a student"],
    ["GET", "/health", "API and database health check"],
]))
add(("h3", "Folder structure"))
add(("code", """student-management-api/
├── .github/workflows/ci-cd.yml   GitHub Actions pipeline
├── src/
│   ├── app.js                    Express app (routes, middleware)
│   ├── server.js                 Connects to MongoDB and starts the server
│   ├── controllers/studentController.js
│   ├── models/Student.js
│   └── routes/studentRoutes.js
├── tests/api.test.js             Jest + Supertest API tests
├── k8s/                          Kubernetes manifests
│   ├── namespace.yaml
│   ├── mongo.yaml
│   └── api.yaml
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
└── package.json""", "text"))
add(("cmd", "a1_tree", "tree /F /A src", "Source code layout in the terminal."))
add(("h3", "Student model (src/models/Student.js)"))
add(("code", read("src/models/Student.js"), "javascript"))
add(("h1", "End-to-end flow"))
add(("code", """Developer ──git push──► GitHub ──triggers──► GitHub Actions pipeline
                                                │
                     ┌──────────────────────────┼───────────────────────────┐
                     ▼                          ▼                           ▼
              1. Test job                2. Docker job               3. Publish job (main only)
           Jest + MongoDB         docker compose up + curl       build & push image to GHCR
                                                                            │
                                                                            ▼
                                             Kubernetes pulls ghcr.io/.../student-api:latest
                                             and runs it as a scalable, self-healing Deployment""",
     "text"))

# ===========================================================================
add(("part", "Version Control using Git and GitHub"))
# ===========================================================================
add(("h1", "Git and GitHub concepts"))
add(("p", "Git is a distributed version control system: it records every change to the code as a "
          "commit, so you can see history, compare versions, work on branches and undo mistakes. "
          "GitHub hosts Git repositories online and adds collaboration features such as pull "
          "requests, Actions (CI/CD) and Packages (container registry)."))
add(("table", ["Term", "Meaning"], [
    ["Repository", "The project folder plus its full history (.git)."],
    ["Working directory / staging area", "Files you edit / changes selected for the next commit (git add)."],
    ["Commit", "A saved snapshot with a message, author and unique hash."],
    ["Branch", "An independent line of work; main is the default branch."],
    ["Merge", "Combines the commits of one branch into another."],
    ["Remote (origin)", "The copy of the repository on GitHub."],
    ["Push / Pull", "Upload local commits to / download new commits from the remote."],
]))
add(("h1", "Basic Git workflow"))
add(("cmd", "g01_git_version", "git --version", "Confirms Git is installed."))
add(("cmd", "g02_git_config", "git config user.name",
     "Shows the author name recorded in commits (set once with git config --global user.name)."))
add(("cmd", "c08_git_remote", "git remote -v", "The local repository is linked to the GitHub repository as origin."))
add(("h2", "git status: see what changed"))
add(("cmd", "g03_git_status", "git status",
     "The new k8s/ folder is untracked, meaning Git sees it but it is not part of any commit yet."))
add(("h2", "git add: stage changes"))
add(("cmd", "g04_git_add", "git add k8s/", "Moves the new files into the staging area. It prints nothing on success."))
add(("cmd", "g05_git_status_staged", "git status --short",
     "A = added to the staging area, ?? = still untracked."))
add(("h2", "git commit: save a snapshot"))
add(("cmd", "g06_git_commit", "git commit -m \"...\"",
     "Creates a commit containing the staged files. a6e4d30 is its short hash."))
add(("h2", "git push: upload to GitHub"))
add(("cmd", "g07_git_push", "git push origin main",
     "Sends the new commit to GitHub. This push also triggers the CI/CD pipeline."))
add(("h2", "git log and git branch: history"))
add(("cmd", "g08_git_log_graph", "git log --oneline --graph -8",
     "Shows commit history as a graph, including the feature branch that was merged into main."))
add(("cmd", "g09_git_branch", "git branch -a", "Lists local branches and remote-tracking branches (remotes/origin/...)."))
add(("h1", "Branching and merging workflow"))
add(("p", "New work is done on a feature branch, so main always stays working. In this project a "
          "feature branch was used to show how CI protects main:"))
add(("bullets", [
    "git switch -c feature/status-code-change: create and switch to a new branch",
    "Commit a change (the create endpoint now returns 200 instead of 201) and push the branch",
    "GitHub Actions runs the tests on the branch; they fail, so the problem is caught before main",
    "Commit a fix on the same branch and push; the pipeline passes",
    "git switch main and git merge --no-ff feature/status-code-change, then git push",
]))
add(("cmd", "g10_git_show_bug", "git show --stat 0bf911f", "The commit that introduced the bug."))
add(("cmd", "g11_git_diff_fix", "git diff 0bf911f 2ec99ee -- src/controllers/studentController.js",
     "The difference between the buggy commit and the fix: status 200 goes back to 201."))
add(("h1", "The repository on GitHub"))
add(("img", "gh_repo.png", "GitHub repository page with the project files"))
add(("img", "gh_commits.png", "Commit history on GitHub"))
add(("h3", "Git command reference"))
add(("table", ["Command", "What it does"], [
    ["git init", "Create a new repository"],
    ["git clone <url>", "Copy a remote repository"],
    ["git status", "Show changed, staged and untracked files"],
    ["git add <files> / git add .", "Stage changes"],
    ["git commit -m \"msg\"", "Commit staged changes"],
    ["git push / git pull", "Upload / download commits"],
    ["git log --oneline --graph", "Show history"],
    ["git switch -c <branch>", "Create and switch to a branch"],
    ["git merge <branch>", "Merge a branch into the current one"],
    ["git diff", "Show line-by-line changes"],
    ["git remote -v", "Show linked remotes"],
]))

# ===========================================================================
add(("part", "CI/CD using GitHub Actions"))
# ===========================================================================
add(("h1", "GitHub Actions concepts"))
add(("table", ["Term", "Meaning"], [
    ["Workflow", "A YAML file in .github/workflows/ that defines the automation."],
    ["Event (on)", "What starts the workflow: push, pull_request, manual run (workflow_dispatch)."],
    ["Job", "A group of steps that runs on one machine. Jobs can depend on each other (needs)."],
    ["Step", "A single command (run) or a reusable action (uses)."],
    ["Runner", "The virtual machine GitHub provides to run a job (ubuntu-latest)."],
    ["Action", "A reusable step, e.g. actions/checkout or docker/build-push-action."],
    ["Service container", "An extra container for a job, e.g. MongoDB for the tests."],
    ["GITHUB_TOKEN", "A temporary token GitHub creates for each run; used here to push to GHCR."],
]))
add(("h1", "Automated tests"))
add(("p", "The pipeline is only useful if it can tell good code from bad code, so the project has "
          "API tests written with Jest and Supertest. They call every endpoint against a real "
          "MongoDB database."))
add(("cmd", "c03_cat_test_head", "cat tests/api.test.js | Select-Object -First 30", "The first part of the test file."))
add(("p", "Running the tests locally against a temporary MongoDB container:"))
add(("cmd", "c04_mongo_for_tests", "docker run -d --rm --name test-mongo -p 27017:27017 mongo:7",
     "Starts a throwaway MongoDB for the tests (--rm deletes it when stopped)."))
add(("cmd", "c05_npm_test", "npm test", "All 6 tests pass."))
add(("cmd", "c06_stop_mongo", "docker stop test-mongo", "Stops (and removes) the test database."))
add(("h1", "The CI/CD workflow file"))
add(("cmd", "c01_tree_github", "tree /F /A .github", "Workflows live in .github/workflows/."))
add(("cmd", "c02_cat_workflow", "cat .github/workflows/ci-cd.yml", "The complete pipeline definition."))
add(("table", ["Section", "Purpose"], [
    ["on: push (all branches), pull_request, workflow_dispatch",
     "Run on every push to any branch, on pull requests to main, and manually."],
    ["env: REGISTRY, IMAGE_NAME", "Image is published as ghcr.io/<owner>/<repo>."],
    ["job test", "Starts a MongoDB service container, installs dependencies with npm ci and runs npm test."],
    ["job docker-build (needs: test)", "Runs only if tests pass. Builds the image and starts the whole "
                                       "stack with docker compose, waits for /health, then calls the API with curl."],
    ["if: always() steps", "Container logs are printed and the stack is stopped even if a step failed."],
    ["job publish (needs: docker-build)", "Runs only for pushes to main. Logs in to GHCR with GITHUB_TOKEN, "
                                          "generates tags and builds and pushes the image."],
    ["permissions: packages: write", "Allows this job (and only this job) to publish packages."],
    ["tags: latest and sha-<commit>", "latest always points to the newest main build; the sha tag "
                                      "identifies exactly which commit an image came from."],
]))
add(("img", "gh_workflow_file.png", "The workflow file on GitHub"))
add(("h1", "The pipeline in action"))
add(("p", "Every git push starts the pipeline automatically. The Actions tab lists all runs, with "
          "the branch and the result of each:"))
add(("img", "gh_actions_list.png", "Actions tab: runs on main and on the feature branch (one failed, the rest passed)"))
add(("h2", "A successful run on main"))
add(("img", "gh_run_success.png",
     "Run summary: Test → Docker build & smoke test → Publish image to GHCR, all passed"))
add(("img", "gh_job_test_log.png", "Test job log: the 6 Jest tests passing on the GitHub runner"))
add(("h2", "Continuous Delivery: the published image"))
add(("p", "The publish job pushed the image to GitHub Container Registry. The package is public, "
          "so anyone, including Kubernetes, can pull it:"))
add(("img", "gh_package.png", "GHCR package page with the latest and sha-<commit> tags"))
add(("code", f"docker pull {IMAGE}:latest", "powershell"))
add(("h2", "When the pipeline catches a bug"))
add(("p", "On the feature branch the create endpoint was changed to return 200 instead of 201. The "
          "push triggered the pipeline and the test job failed. Because the later jobs depend on it "
          "(needs: test), the Docker build and publish jobs were skipped, so no broken image was published."))
add(("img", "gh_run_failed.png", "Failed run: Test failed, Docker build and Publish were skipped"))
add(("img", "gh_job_failed_log.png", "Failed test log: expected status 201 but received 200"))
add(("p", "After the fix was pushed the branch went green, and once it was merged the pipeline on "
          "main ran all three jobs and published a new image (see the Actions list above)."))

# ===========================================================================
add(("part", "Containerization and Orchestration"))
# ===========================================================================
add(("h1", "Docker"))
add(("p", "Docker packages an application together with everything it needs (runtime, libraries, "
          "configuration) into an image. A running image is a container. Containers run the same "
          "way on a laptop, on a GitHub Actions runner and in a Kubernetes cluster."))
add(("table", ["Term", "Meaning"], [
    ["Image", "A read-only template built from a Dockerfile. Example: student-api:1.0"],
    ["Container", "A running instance of an image. Many containers can run from one image."],
    ["Dockerfile", "Step-by-step instructions to build an image."],
    ["Registry", "A store for images: Docker Hub, GHCR."],
    ["Volume", "Persistent storage; data survives container removal."],
    ["Network", "A virtual network that lets containers reach each other by name."],
    ["Docker Compose", "Defines and runs multi-container apps from one YAML file."],
]))
add(("h2", "Setup"))
add(("cmd", "01_version", "docker --version", "Confirms the Docker CLI is installed."))
add(("cmd", "02_info", "docker info",
     "Engine details: containers, images, storage driver, kernel, CPUs and memory. (Server section shown.)"))
add(("h2", "The Dockerfile"))
add(("cmd", "a2_cat_dockerfile", "cat Dockerfile", "The Dockerfile used to build the API image."))
add(("table", ["Instruction", "Purpose"], [
    ["FROM node:22-alpine", "Base image: Node.js 22 on lightweight Alpine Linux."],
    ["WORKDIR /app", "Working directory inside the image."],
    ["COPY package*.json ./", "Copy dependency manifests first so the install layer is cached."],
    ["RUN npm ci --omit=dev", "Clean install of production dependencies from package-lock.json."],
    ["COPY src ./src", "Copy the application source code."],
    ["ENV PORT=5000 / EXPOSE 5000", "Default port and documentation of the listening port."],
    ["CMD [\"npm\", \"start\"]", "Command executed when a container starts."],
]))
add(("cmd", "a3_cat_dockerignore", "cat .dockerignore",
     "Files kept out of the build context (faster builds, smaller images)."))
add(("h2", "Image commands"))
add(("cmd", "03_pull", "docker pull node:22-alpine", "Downloads the base image from Docker Hub."))
add(("cmd", "04_build", "docker build -t student-api:1.0 .",
     "-t names the image; . is the build context. Each Dockerfile instruction is a build step."))
add(("cmd", "05_images", "docker images", "Lists local images with tag, ID and size."))
add(("cmd", "06_tag", "docker tag student-api:1.0 student-api:latest", "Adds a second tag to the same image."))
add(("cmd", "07_images_filtered", "docker images student-api", "Filters the list by repository name."))
add(("cmd", "08_history", "docker history student-api:1.0",
     "The layer created by each instruction. The top 7 rows come from our Dockerfile, the rest from the base image."))
add(("cmd", "09_inspect", 'docker inspect student-api:1.0 --format "..."', "Low-level image metadata."))
add(("img", "dd_images.png", "Docker Desktop: Images view"))
add(("h2", "Networks and volumes"))
add(("cmd", "10_network_create", "docker network create student-net", "A user-defined network; containers on it resolve each other by name."))
add(("cmd", "11_network_ls", "docker network ls", "Lists networks."))
add(("cmd", "12_volume_create", "docker volume create student-data", "A named volume for MongoDB data."))
add(("cmd", "13_volume_ls", "docker volume ls", "Lists volumes."))
add(("h2", "Container commands"))
add(("cmd", "14_run_mongo", "docker run -d --name student-mongo --network student-net -v student-data:/data/db mongo:7",
     "-d detached, --name container name, --network attach to network, -v mount volume. The image is pulled automatically."))
add(("cmd", "15_run_api", "docker run -d --name student-api --network student-net -p 5000:5000 "
                          "-e MONGO_URI=mongodb://student-mongo:27017/studentdb student-api:1.0",
     "-p maps host port to container port, -e sets an environment variable."))
add(("cmd", "16_ps", "docker ps", "Running containers with status and ports."))
add(("cmd", "17_logs", "docker logs student-api", "Container output (add -f to follow)."))
add(("cmd", "18_curl_post", "curl -s -X POST http://localhost:5000/api/students ...", "Create a student through the containerised API."))
add(("cmd", "20_curl_get", "curl -s http://localhost:5000/api/students", "Read all students back."))
add(("cmd", "21_exec", "docker exec student-api sh -c \"...\"", "Run commands inside a running container."))
add(("cmd", "22_exec_mongo", "docker exec student-mongo mongosh studentdb --eval \"...\"", "Query MongoDB inside its container."))
add(("cmd", "23_top", "docker top student-api", "Processes inside the container."))
add(("cmd", "24_stats", "docker stats --no-stream", "CPU, memory, network and disk usage."))
add(("cmd", "25_stop", "docker stop student-api", "Gracefully stop a container."))
add(("cmd", "26_ps_a", "docker ps -a", "All containers including stopped ones."))
add(("cmd", "27_start", "docker start student-api", "Start it again."))
add(("cmd", "28_restart", "docker restart student-api", "Stop and start in one step."))
add(("cmd", "29_network_inspect", 'docker network inspect student-net --format "..."', "Containers attached to the network and their IPs."))
add(("cmd", "30_volume_inspect", "docker volume inspect student-data", "Volume details and mount point."))
add(("cmd", "31_rm", "docker rm -f student-api student-mongo", "Remove containers (data stays in the volume)."))
add(("cmd", "32_network_rm", "docker network rm student-net", "Remove the network."))
add(("h2", "Docker Compose"))
add(("p", "Compose describes the API, database, network and volume in one YAML file and starts "
          "everything with one command. The same file is used by the GitHub Actions smoke test."))
add(("cmd", "a4_cat_compose", "cat docker-compose.yml", "The project's compose file."))
add(("table", ["Key", "Purpose"], [
    ["services", "The containers: mongo (database) and api (backend)."],
    ["image / build", "mongo uses a ready image; api is built from the local Dockerfile."],
    ["ports", "Publishes container port 5000 on host port 5000."],
    ["environment", "MONGO_URI uses the service name mongo as the hostname."],
    ["depends_on", "Starts mongo before api."],
    ["volumes / networks", "Persistent database storage and a private network."],
]))
add(("cmd", "33_compose_up", "docker compose up -d --build", "Build and start the whole stack in the background."))
add(("cmd", "34_compose_ps", "docker compose ps", "Containers of this compose project."))
add(("cmd", "35_compose_logs", "docker compose logs api", "Logs of the api service."))
add(("cmd", "37_health", "curl -s http://localhost:5000/health", "The API is connected to MongoDB."))
add(("img", "dd_containers.png", "Docker Desktop: the compose stack with student-mongo and student-api"))
add(("img", "dd_container_logs.png", "Docker Desktop: logs of the student-api container"))
add(("img", "dd_container_stats.png", "Docker Desktop: live CPU, memory, disk and network stats"))
add(("img", "dd_volumes.png", "Docker Desktop: volumes"))
add(("img", "dd_builds.png", "Docker Desktop: build history"))
add(("cmd", "38_compose_down", "docker compose down", "Stop and remove the stack (add -v to delete volumes)."))
add(("h2", "Docker cleanup"))
add(("cmd", "39_rmi", "docker rmi student-api:latest", "Remove an image tag."))
add(("cmd", "40_system_df", "docker system df", "Disk used by images, containers, volumes and cache."))
add(("cmd", "41_image_prune", "docker image prune -f", "Delete dangling images."))
add(("cmd", "42_volume_rm", "docker volume rm student-data", "Delete a volume and its data."))

add(("h1", "Kubernetes"))
add(("p", "Docker runs containers on one machine. Kubernetes runs containers across a cluster of "
          "machines and keeps them in the state you declare: if you ask for 4 copies of the API, "
          "it starts 4, restarts any that crash, replaces any that are deleted and balances "
          "traffic between them."))
add(("table", ["Object", "Meaning"], [
    ["Cluster / Node", "A set of machines (nodes) managed by Kubernetes. Here: one node in Docker Desktop."],
    ["Pod", "The smallest unit: one or more containers running together."],
    ["Deployment", "Declares which image to run and how many replicas; handles rollouts and self-healing."],
    ["ReplicaSet", "Created by a Deployment to keep the requested number of pods running."],
    ["Service", "A stable name and IP that load-balances traffic to matching pods."],
    ["ConfigMap", "Configuration (environment variables) kept outside the image."],
    ["PersistentVolumeClaim", "A request for persistent storage (used by MongoDB)."],
    ["Namespace", "A logical group that isolates this app's objects (student-app)."],
    ["kubectl", "The command-line tool used to talk to the cluster."],
]))
add(("h2", "Enabling Kubernetes in Docker Desktop"))
add(("p", "Settings → Kubernetes → Enable Kubernetes → Apply → Install. Docker Desktop created a "
          "single-node cluster (kind provisioner, Kubernetes v1.36.1)."))
add(("img", "dd_k8s_settings.png", "Docker Desktop Kubernetes settings"))
add(("cmd", "k01_kubectl_version", "kubectl version", "kubectl client and cluster server versions."))
add(("cmd", "k02_cluster_info", "kubectl cluster-info", "Address of the cluster's control plane."))
add(("cmd", "k03_get_nodes", "kubectl get nodes -o wide", "The cluster has one Ready node."))
add(("h2", "Kubernetes manifests"))
add(("p", "The desired state is written as YAML in the k8s/ folder. The API Deployment uses the "
          "image that GitHub Actions published to GHCR, which connects the CI/CD pipeline to the "
          "deployment."))
add(("cmd", "k00b_cat_mongo_yaml", "cat k8s/mongo.yaml",
     "MongoDB: a PersistentVolumeClaim for data, a Deployment with 1 replica and a ClusterIP Service named mongo."))
add(("cmd", "k00a_cat_api_yaml", "cat k8s/api.yaml",
     "API: a ConfigMap with MONGO_URI, a Deployment with 2 replicas of the GHCR image, health probes "
     "and resource limits, and a NodePort Service."))
add(("table", ["Setting", "Purpose"], [
    ["replicas: 2", "Run two identical API pods."],
    ["image: ghcr.io/.../student-api:latest", "The image built and published by the CI/CD pipeline."],
    ["envFrom: configMapRef", "Injects MONGO_URI and PORT from the ConfigMap."],
    ["readinessProbe /health", "A pod only receives traffic once /health responds."],
    ["livenessProbe /health", "Kubernetes restarts the container if /health stops responding."],
    ["resources requests / limits", "Guaranteed and maximum CPU/memory per pod."],
    ["Service selector app: student-api", "Sends traffic to all pods with that label."],
]))
add(("h2", "Deploying the application"))
add(("cmd", "k04_apply_ns", "kubectl apply -f k8s/namespace.yaml", "Create the student-app namespace."))
add(("cmd", "k05_apply_all", "kubectl apply -f k8s/", "Create every object defined in the folder."))
add(("cmd", "k06_rollout_status", "kubectl rollout status deployment/student-api -n student-app",
     "Waits until all replicas are available."))
add(("cmd", "k07_get_all", "kubectl get all -n student-app", "Pods, services, deployments and replicasets of the app."))
add(("cmd", "k08_get_pods_wide", "kubectl get pods -n student-app -o wide", "Pods with their internal IP and node."))
add(("cmd", "k09_describe", "kubectl describe deployment student-api -n student-app",
     "Full details of the deployment: image, probes, limits, rollout strategy and events."))
add(("cmd", "k10_logs", "kubectl logs deployment/student-api -n student-app", "Logs from an API pod: connected to MongoDB."))
add(("h2", "Accessing the application"))
add(("cmd", "k11_port_forward", "kubectl port-forward svc/student-api 8080:80 -n student-app",
     "Forwards localhost:8080 to the service inside the cluster (left running in its own terminal)."))
add(("cmd", "k12_curl_health", "curl -s http://localhost:8080/health", "The API running in Kubernetes is healthy."))
add(("cmd", "k13_curl_post", "curl -s -X POST http://localhost:8080/api/students ...", "Create a student in the Kubernetes deployment."))
add(("cmd", "k14_curl_get", "curl -s http://localhost:8080/api/students", "Read it back from MongoDB running in the cluster."))
add(("h2", "Scaling"))
add(("cmd", "k15_scale", "kubectl scale deployment student-api --replicas=4 -n student-app", "Scale the API from 2 to 4 pods."))
add(("cmd", "k16_pods_scaled", "kubectl get pods -n student-app -l app=student-api", "Two new pods were started."))
add(("h2", "Self-healing"))
add(("cmd", "k17_delete_pod", "kubectl delete pod <pod-name> -n student-app", "Delete one pod on purpose."))
add(("cmd", "k18_pods_healed", "kubectl get pods -n student-app -l app=student-api",
     "Kubernetes immediately created a replacement pod (age a few seconds) to keep 4 replicas."))
add(("cmd", "k19_rollout_history", "kubectl rollout history deployment/student-api -n student-app",
     "Revision history; kubectl rollout undo can return to an earlier revision."))
add(("cmd", "k20_get_cm_pvc", "kubectl get configmap,pvc -n student-app", "The ConfigMap and the bound storage claim."))
add(("img", "dd_k8s_view.png", "Docker Desktop: Kubernetes view of the student-app namespace"))
add(("h2", "Kubernetes cleanup"))
add(("cmd", "k21_delete", "kubectl delete -f k8s/", "Deletes everything that was created from the manifests."))
add(("cmd", "k22_get_ns", "kubectl get namespaces", "The student-app namespace is gone."))

# ===========================================================================
add(("part", "Summary"))
# ===========================================================================
add(("h1", "Command cheat sheet"))
add(("table", ["Area", "Command", "What it does"], [
    ["Git", "git add / commit / push", "Stage, commit and upload changes"],
    ["Git", "git switch -c / merge", "Create a branch / merge it"],
    ["Git", "git log --oneline --graph", "View history"],
    ["Actions", ".github/workflows/*.yml", "Define the pipeline"],
    ["Actions", "on: push / pull_request", "Run on every push / PR"],
    ["Actions", "needs: <job>", "Run a job only after another succeeds"],
    ["Docker", "docker build -t name:tag .", "Build an image"],
    ["Docker", "docker run -d -p h:c --name n img", "Run a container"],
    ["Docker", "docker ps / logs / exec / stop / rm", "Manage containers"],
    ["Docker", "docker compose up -d / down", "Start / stop a multi-container stack"],
    ["Kubernetes", "kubectl apply -f <dir>", "Create or update objects from YAML"],
    ["Kubernetes", "kubectl get pods / all", "List resources"],
    ["Kubernetes", "kubectl describe / logs", "Inspect a resource / read logs"],
    ["Kubernetes", "kubectl scale --replicas=N", "Scale a deployment"],
    ["Kubernetes", "kubectl port-forward svc/x 8080:80", "Reach a service locally"],
    ["Kubernetes", "kubectl delete -f <dir>", "Remove the app"],
]))
add(("h1", "Conclusion"))
add(("p", "The Student Management API went through a complete DevOps workflow. Its code is "
          "versioned with Git and hosted on GitHub, using feature branches and merges. Every push "
          "runs a GitHub Actions pipeline that tests the code, builds and smoke-tests the Docker "
          "stack, and publishes a versioned image to GitHub Container Registry. A deliberate bug "
          "showed the pipeline blocking a broken change. The published image was then deployed to "
          "Kubernetes, where it was scaled, accessed, and automatically healed after a pod was "
          "deleted."))


# ---------------------------------------------------------------------------
# Markdown writer
# ---------------------------------------------------------------------------
def to_markdown():
    out = []
    for it in C:
        t = it[0]
        if t == "title":
            out.append(f"# {it[1]}\n")
        elif t == "subtitle":
            out.append(f"*{it[1]}*\n")
        elif t == "part":
            out.append(f"---\n\n# {it[1]}\n")
        elif t == "h1":
            out.append(f"## {it[1]}\n")
        elif t == "h2":
            out.append(f"### {it[1]}\n")
        elif t == "h3":
            out.append(f"#### {it[1]}\n")
        elif t == "p":
            out.append(it[1] + "\n")
        elif t == "bullets":
            out.append("\n".join(f"- {b}" for b in it[1]) + "\n")
        elif t == "code":
            out.append(f"```{it[2]}\n{it[1]}\n```\n")
        elif t == "cmd":
            _, key, cmd, expl = it
            out.append(f"```powershell\n{cmd}\n```\n\n{expl}\n\n![{key}](screenshots/{key}.png)\n")
        elif t == "img":
            out.append(f"![{it[2]}](screenshots/{it[1]})\n\n*{it[2]}*\n")
        elif t == "table":
            hdr, rows = it[1], it[2]
            esc = lambda s: s.replace("|", "\\|")
            lines = ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
            lines += ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows]
            out.append("\n".join(lines) + "\n")
    with open(os.path.join(DOCS, "Docker_Documentation.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))


# ---------------------------------------------------------------------------
# DOCX writer
# ---------------------------------------------------------------------------
BLUE = RGBColor(0x1D, 0x63, 0xED)


def shade(cell_or_par, hex_fill):
    el = cell_or_par._tc if hasattr(cell_or_par, "_tc") else cell_or_par._p
    pr = el.get_or_add_tcPr() if hasattr(cell_or_par, "_tc") else el.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hex_fill)
    pr.append(shd)


def code_par(doc, text, fill="F3F4F6", color=None, size=9.5):
    p = doc.add_paragraph()
    shade(p, fill)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.font.name = "Consolas"; r._element.rPr.rFonts.set(qn("w:eastAsia"), "Consolas")
    r.font.size = Pt(size)
    if color:
        r.font.color.rgb = color
    return p


def to_docx():
    doc = Document()
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Inches(0.8)
    sec.top_margin = sec.bottom_margin = Inches(0.8)
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"; normal.font.size = Pt(11)
    for name, size in (("Heading 1", 20), ("Heading 2", 15), ("Heading 3", 13), ("Heading 4", 12)):
        st = doc.styles[name]; st.font.color.rgb = BLUE; st.font.size = Pt(size)
    width = Inches(6.9)
    toc_done = False
    for it in C:
        t = it[0]
        if t == "title":
            doc.add_heading(it[1], 0)
        elif t == "subtitle":
            p = doc.add_paragraph(); r = p.add_run(it[1]); r.italic = True; r.font.size = Pt(13)
        elif t == "part":
            if not toc_done:
                doc.add_heading("Contents", 2)
                for x in C:
                    if x[0] == "part":
                        p = doc.add_paragraph(style="List Number"); p.add_run(x[1]).bold = True
                    elif x[0] == "h1":
                        doc.add_paragraph(x[1], style="List Bullet 2")
                toc_done = True
            doc.add_page_break()
            doc.add_heading(it[1], 1)
        elif t in ("h1", "h2", "h3"):
            doc.add_heading(it[1], {"h1": 2, "h2": 3, "h3": 4}[t])
        elif t == "p":
            doc.add_paragraph(it[1])
        elif t == "bullets":
            for b in it[1]:
                doc.add_paragraph(b, style="List Bullet")
        elif t == "code":
            code_par(doc, it[1], size=8.5 if it[2] == "text" else 9.5)
        elif t == "cmd":
            _, key, cmd, expl = it
            code_par(doc, "> " + cmd, fill="1E1E1E",
                     color=RGBColor(0xF9, 0xF1, 0xA5)).paragraph_format.keep_with_next = True
            doc.add_paragraph(expl).paragraph_format.keep_with_next = True
            doc.add_picture(os.path.join(SHOTS, key + ".png"), width=width)
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif t == "img":
            doc.add_picture(os.path.join(SHOTS, it[1]), width=width)
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            doc.paragraphs[-1].paragraph_format.keep_with_next = True
            cap = doc.add_paragraph(); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = cap.add_run(it[2]); r.italic = True; r.font.size = Pt(9.5)
        elif t == "table":
            hdr, rows = it[1], it[2]
            tb = doc.add_table(rows=1, cols=len(hdr)); tb.style = "Table Grid"
            for i, h in enumerate(hdr):
                c = tb.rows[0].cells[i]; c.text = ""
                r = c.paragraphs[0].add_run(h); r.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)
                shade(c, "1D63ED")
            for row in rows:
                cells = tb.add_row().cells
                for i, v in enumerate(row):
                    cells[i].text = v
            doc.add_paragraph()
    doc.save(os.path.join(DOCS, "Docker_Documentation.docx"))


if __name__ == "__main__":
    missing = [x[1] for x in C if x[0] == "cmd" and not os.path.exists(os.path.join(SHOTS, x[1] + ".png"))]
    missing += [x[1] for x in C if x[0] == "img" and not os.path.exists(os.path.join(SHOTS, x[1]))]
    if missing:
        raise SystemExit(f"Missing screenshots: {missing}")
    to_markdown()
    to_docx()
    print("Wrote Docker_Documentation.md and Docker_Documentation.docx")
