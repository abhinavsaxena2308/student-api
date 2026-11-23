"""Builds Docker_Documentation.md and Docker_Documentation.docx from one content list.

Run from anywhere:  python docs/build_docs.py
"""
import os
import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

DOCS = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(DOCS, "screenshots")
ROOT = os.path.dirname(DOCS)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read().rstrip()


# ---------------------------------------------------------------------------
# Content. Item types:
#   ("h1"|"h2"|"h3", text)  ("p", text)  ("bullets", [..])  ("code", text, lang)
#   ("cmd", screenshot_key, command, explanation)   -> terminal screenshot
#   ("img", file, caption)                          -> Docker Desktop screenshot
#   ("table", [header], [[row], ...])
# ---------------------------------------------------------------------------
C = []
add = C.append

add(("title", "Docker Basics: Hands-on Documentation"))
add(("subtitle", "Containerising a Student Management Backend (Node.js + Express + MongoDB)"))

# 1 -------------------------------------------------------------------------
add(("h1", "1. Introduction"))
add(("p", "Docker is a platform that packages an application together with everything it needs "
          "(runtime, libraries, configuration) into a portable unit called a container. A container "
          "runs the same way on any machine that has Docker installed, which removes the classic "
          "\"it works on my machine\" problem."))
add(("h3", "Core concepts"))
add(("table", ["Term", "Meaning"], [
    ["Image", "A read-only template (blueprint) built from a Dockerfile. Example: student-api:1.0"],
    ["Container", "A running instance of an image. Many containers can run from one image."],
    ["Dockerfile", "A text file with step-by-step instructions to build an image."],
    ["Registry", "A store for images. Docker Hub is the default public registry."],
    ["Volume", "Persistent storage managed by Docker; data survives container removal."],
    ["Network", "A virtual network that lets containers talk to each other by name."],
    ["Docker Compose", "A tool to define and run multi-container apps from one YAML file."],
]))

# 2 -------------------------------------------------------------------------
add(("h1", "2. Prerequisites and Setup"))
add(("bullets", ["Windows 11 with Docker Desktop installed (WSL 2 backend)",
                 "PowerShell terminal",
                 "Docker Engine 29.9.3, Docker Compose v5.7.1, Docker Desktop 4.100.1"]))
add(("cmd", "01_version", "docker --version",
     "Confirms the Docker CLI is installed and prints its version."))
add(("cmd", "02_info", "docker info",
     "Shows system-wide information about the Docker engine: number of containers and images, "
     "storage driver, kernel, CPUs and memory available to Docker. (Server section shown.)"))

# 3 -------------------------------------------------------------------------
add(("h1", "3. Project Overview: Student Management API"))
add(("p", "A small REST API that performs CRUD operations on student records. It is written in "
          "Node.js with Express, and stores data in MongoDB through Mongoose."))
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
├── src/
│   ├── app.js
│   ├── controllers/studentController.js
│   ├── models/Student.js
│   └── routes/studentRoutes.js
├── package.json
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
└── docs/  (this documentation + screenshots)""", "text"))
add(("cmd", "a1_tree", "tree /F /A src", "Source code layout as seen in the terminal."))
add(("h3", "Student model (src/models/Student.js)"))
add(("code", read("src/models/Student.js"), "javascript"))

# 4 -------------------------------------------------------------------------
add(("h1", "4. Writing the Dockerfile"))
add(("cmd", "a2_cat_dockerfile", "cat Dockerfile", "The Dockerfile used to build the API image."))
add(("table", ["Instruction", "Purpose"], [
    ["FROM node:22-alpine", "Base image: Node.js 22 on lightweight Alpine Linux."],
    ["WORKDIR /app", "Sets /app as the working directory inside the image."],
    ["COPY package*.json ./", "Copies dependency manifests first so the npm install layer is cached."],
    ["RUN npm install --omit=dev", "Installs production dependencies."],
    ["COPY src ./src", "Copies the application source code."],
    ["ENV PORT=5000", "Default environment variable read by the app."],
    ["EXPOSE 5000", "Documents the port the app listens on."],
    ["CMD [\"npm\", \"start\"]", "Command executed when a container starts."],
]))
add(("p", "The .dockerignore file keeps unnecessary files out of the build context, which makes "
          "builds faster and images smaller:"))
add(("cmd", "a3_cat_dockerignore", "cat .dockerignore", "Files excluded from the build context."))

# 5 -------------------------------------------------------------------------
add(("h1", "5. Image Commands"))
add(("h2", "5.1 docker pull: download an image"))
add(("cmd", "03_pull", "docker pull node:22-alpine",
     "Downloads the base image from Docker Hub. Each image is made of layers, which are downloaded "
     "separately and reused across images."))
add(("h2", "5.2 docker build: build an image from a Dockerfile"))
add(("cmd", "04_build", "docker build -t student-api:1.0 .",
     "-t gives the image a name:tag, and . is the build context (current folder). "
     "Each Dockerfile instruction becomes a build step [n/5]."))
add(("h2", "5.3 docker images: list local images"))
add(("cmd", "05_images", "docker images", "Lists every image stored locally with its tag, ID and size."))
add(("h2", "5.4 docker tag: add another name to an image"))
add(("cmd", "06_tag", "docker tag student-api:1.0 student-api:latest",
     "Creates a second tag pointing to the same image. It prints nothing on success."))
add(("cmd", "07_images_filtered", "docker images student-api",
     "Filters the list by repository name. Both tags share the same IMAGE ID."))
add(("h2", "5.5 docker history: view image layers"))
add(("cmd", "08_history", "docker history student-api:1.0",
     "Shows the layer created by each Dockerfile instruction and its size. The top seven rows come "
     "from our Dockerfile; the rest come from the node:22-alpine base image."))
add(("h2", "5.6 docker inspect: low-level image details"))
add(("cmd", "09_inspect", 'docker inspect student-api:1.0 --format "..."',
     "Returns the image metadata as JSON. --format with a Go template picks out specific fields."))
add(("img", "dd_images.png", "Docker Desktop: Images view showing student-api, mongo and node images"))

# 6 -------------------------------------------------------------------------
add(("h1", "6. Networks and Volumes"))
add(("h2", "6.1 Create a network"))
add(("cmd", "10_network_create", "docker network create student-net",
     "Creates a user-defined bridge network. Containers on it can reach each other by container name."))
add(("cmd", "11_network_ls", "docker network ls", "Lists networks (bridge, host and none are built in)."))
add(("h2", "6.2 Create a volume"))
add(("cmd", "12_volume_create", "docker volume create student-data",
     "Creates a named volume used to persist MongoDB data."))
add(("cmd", "13_volume_ls", "docker volume ls", "Lists volumes."))

# 7 -------------------------------------------------------------------------
add(("h1", "7. Container Commands"))
add(("h2", "7.1 docker run: start the MongoDB container"))
add(("cmd", "14_run_mongo",
     "docker run -d --name student-mongo --network student-net -v student-data:/data/db mongo:7",
     "-d runs in the background (detached), --name sets the container name, --network attaches it to "
     "student-net and -v mounts the volume. The image is pulled automatically because it is not "
     "present locally. The long string printed last is the container ID."))
add(("h2", "7.2 docker run: start the API container"))
add(("cmd", "15_run_api",
     "docker run -d --name student-api --network student-net -p 5000:5000 "
     "-e MONGO_URI=mongodb://student-mongo:27017/studentdb student-api:1.0",
     "-p 5000:5000 maps host port to container port and -e sets an environment variable. The API "
     "reaches MongoDB using the hostname student-mongo, which is the container name on the shared network."))
add(("h2", "7.3 docker ps: list running containers"))
add(("cmd", "16_ps", "docker ps", "Shows running containers, their status and port mappings."))
add(("h2", "7.4 docker logs: view container output"))
add(("cmd", "17_logs", "docker logs student-api",
     "Prints what the container wrote to stdout/stderr. Add -f to follow live."))
add(("h2", "7.5 Testing the API running in the container"))
add(("cmd", "18_curl_post", "curl -s -X POST http://localhost:5000/api/students ...",
     "Creates a student through the containerised API."))
add(("cmd", "19_curl_post2", "curl -s -X POST http://localhost:5000/api/students ...",
     "Creates a second student."))
add(("cmd", "20_curl_get", "curl -s http://localhost:5000/api/students",
     "Fetches all students. The data is stored in the MongoDB container."))
add(("h2", "7.6 docker exec: run a command inside a container"))
add(("cmd", "21_exec", "docker exec student-api sh -c \"...\"",
     "Runs commands inside the running API container: Node version, app files and OS (Alpine). "
     "Use docker exec -it student-api sh for an interactive shell."))
add(("cmd", "22_exec_mongo", "docker exec student-mongo mongosh studentdb --eval \"...\"",
     "Queries MongoDB directly inside its container to confirm the records were saved."))
add(("h2", "7.7 docker top and docker stats: monitor containers"))
add(("cmd", "23_top", "docker top student-api", "Lists the processes running inside the container."))
add(("cmd", "24_stats", "docker stats --no-stream",
     "Shows live CPU, memory, network and disk usage. --no-stream prints one snapshot."))
add(("h2", "7.8 docker stop, start, restart"))
add(("cmd", "25_stop", "docker stop student-api", "Gracefully stops a running container."))
add(("cmd", "26_ps_a", "docker ps -a",
     "-a lists all containers including stopped ones; student-api now shows Exited."))
add(("cmd", "27_start", "docker start student-api", "Starts the stopped container again."))
add(("cmd", "28_restart", "docker restart student-api", "Stops and starts the container in one step."))
add(("h2", "7.9 Inspecting the network and volume"))
add(("cmd", "29_network_inspect", 'docker network inspect student-net --format "..."',
     "Shows which containers are attached to the network and their internal IP addresses."))
add(("cmd", "30_volume_inspect", "docker volume inspect student-data",
     "Shows volume details, including where Docker stores the data (Mountpoint)."))
add(("h2", "7.10 docker rm and docker network rm"))
add(("cmd", "31_rm", "docker rm -f student-api student-mongo",
     "Removes containers; -f stops them first if they are running. The data stays in the volume."))
add(("cmd", "32_network_rm", "docker network rm student-net", "Removes the network."))

# 8 -------------------------------------------------------------------------
add(("h1", "8. Docker Compose"))
add(("p", "Running each container by hand needs many flags. Docker Compose describes the whole stack "
          "(API, database, network and volume) in one YAML file and starts it with a single command."))
add(("h2", "8.1 The project's docker-compose.yml"))
add(("cmd", "a4_cat_compose", "cat docker-compose.yml", "The compose file of the project."))
add(("table", ["Key", "Purpose"], [
    ["services", "Defines the containers: mongo (database) and api (our backend)."],
    ["image / build", "mongo uses a ready image; api is built from the local Dockerfile (build: .)."],
    ["container_name", "Fixed container names (student-mongo, student-api)."],
    ["ports", "Publishes container port 5000 on host port 5000."],
    ["environment", "MONGO_URI uses the service name mongo as the hostname."],
    ["depends_on", "Starts mongo before api."],
    ["volumes", "Named volume student-data persists the database files."],
    ["networks", "Both services join student-net so they can talk to each other."],
]))
add(("h2", "8.2 docker compose up"))
add(("cmd", "33_compose_up", "docker compose up -d --build",
     "Builds the API image, creates the network and volume, and starts both containers in the "
     "background. Build log lines are trimmed in the screenshot."))
add(("h2", "8.3 docker compose ps and logs"))
add(("cmd", "34_compose_ps", "docker compose ps", "Lists the containers of this compose project."))
add(("cmd", "35_compose_logs", "docker compose logs api", "Shows logs of the api service."))
add(("cmd", "36_compose_curl", "curl -s -X POST http://localhost:5000/api/students ...",
     "The API works the same way when started through Compose."))
add(("cmd", "37_health", "curl -s http://localhost:5000/health",
     "Health endpoint confirms the API is connected to MongoDB."))

# 9 -------------------------------------------------------------------------
add(("h1", "9. Docker Desktop"))
add(("p", "Docker Desktop is the graphical interface for everything done above. The screenshots "
          "below were taken while the compose stack was running."))
add(("img", "dd_containers.png",
     "Containers view: the student-management-api compose stack with student-mongo and student-api"))
add(("img", "dd_container_logs.png", "Container details: logs of student-api"))
add(("img", "dd_container_stats.png", "Container details: live CPU, memory, disk and network stats"))
add(("img", "dd_volumes.png", "Volumes view: student-data and the compose-managed volume"))
add(("img", "dd_builds.png", "Builds view: build history for student-management-api"))

# 10 ------------------------------------------------------------------------
add(("h1", "10. Pushing to Docker Hub (optional)"))
add(("p", "To share the image, tag it with your Docker Hub username and push it. These commands are "
          "listed for reference and need your own Docker Hub account:"))
add(("code", "docker login\n"
             "docker tag student-api:1.0 <your-dockerhub-username>/student-api:1.0\n"
             "docker push <your-dockerhub-username>/student-api:1.0", "powershell"))

# 11 ------------------------------------------------------------------------
add(("h1", "11. Cleanup"))
add(("cmd", "38_compose_down", "docker compose down",
     "Stops and removes the compose containers and network. Add -v to also delete volumes."))
add(("cmd", "39_rmi", "docker rmi student-api:latest", "Removes an image tag."))
add(("cmd", "40_system_df", "docker system df", "Shows disk space used by images, containers, volumes and cache."))
add(("cmd", "41_image_prune", "docker image prune -f", "Deletes dangling (untagged) images."))
add(("cmd", "42_volume_rm", "docker volume rm student-data", "Deletes a volume and its data."))
add(("p", "docker system prune removes all stopped containers, unused networks, dangling images and "
          "build cache in one go. Use it carefully, because it also affects other projects."))

# 12 ------------------------------------------------------------------------
add(("h1", "12. Command Cheat Sheet"))
add(("table", ["Command", "What it does"], [
    ["docker --version / docker info", "Check installation and engine details"],
    ["docker pull <image>", "Download an image"],
    ["docker build -t name:tag .", "Build an image from a Dockerfile"],
    ["docker images", "List images"],
    ["docker tag src dst", "Add a new tag to an image"],
    ["docker history / inspect", "Show image layers / metadata"],
    ["docker rmi <image>", "Remove an image"],
    ["docker run -d -p h:c --name n img", "Create and start a container"],
    ["docker ps / docker ps -a", "List running / all containers"],
    ["docker logs [-f] <container>", "Show container output"],
    ["docker exec -it <container> sh", "Open a shell inside a container"],
    ["docker top / docker stats", "Processes / resource usage"],
    ["docker stop | start | restart", "Control container lifecycle"],
    ["docker rm [-f] <container>", "Remove a container"],
    ["docker network create | ls | inspect | rm", "Manage networks"],
    ["docker volume create | ls | inspect | rm", "Manage volumes"],
    ["docker compose up -d --build", "Build and start all services"],
    ["docker compose ps | logs | down", "Inspect and stop a compose project"],
    ["docker system df / prune", "Disk usage / cleanup"],
    ["docker login / push", "Publish an image to a registry"],
]))

# 13 ------------------------------------------------------------------------
add(("h1", "13. Conclusion"))
add(("p", "The Student Management API was containerised with a Dockerfile, run as two connected "
          "containers (API and MongoDB) using a custom network and a persistent volume, and then "
          "started as a single stack with Docker Compose. Every basic Docker command for images, "
          "containers, networks, volumes, Compose and cleanup was executed and verified, both from "
          "the terminal and in Docker Desktop."))


# ---------------------------------------------------------------------------
# Markdown writer
# ---------------------------------------------------------------------------
# Strip section numbers such as "1. " or "5.1 " from headings.
C = [(t, re.sub(r"^\d+(\.\d+)*\.?\s+", "", x[0]), *x[1:]) if t in ("h1", "h2", "h3") else (t, *x)
     for t, *x in C]

def to_markdown():
    out = []
    for it in C:
        t = it[0]
        if t == "title":
            out.append(f"# {it[1]}\n")
        elif t == "subtitle":
            out.append(f"*{it[1]}*\n")
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
            out.append(f"```powershell\n{cmd}\n```\n\n{expl}\n\n![{cmd}](screenshots/{key}.png)\n")
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


def code_par(doc, text, fill="F3F4F6", color=None):
    p = doc.add_paragraph()
    shade(p, fill)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.font.name = "Consolas"; r._element.rPr.rFonts.set(qn("w:eastAsia"), "Consolas")
    r.font.size = Pt(9.5)
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
    for name, size in (("Heading 1", 16), ("Heading 2", 13), ("Heading 3", 12)):
        st = doc.styles[name]; st.font.color.rgb = BLUE; st.font.size = Pt(size)
    width = Inches(6.9)
    toc_done = False
    for it in C:
        t = it[0]
        if t == "title":
            doc.add_heading(it[1], 0)
        elif t == "subtitle":
            p = doc.add_paragraph(); r = p.add_run(it[1]); r.italic = True; r.font.size = Pt(13)
        elif t in ("h1", "h2", "h3"):
            if t == "h1" and not toc_done:
                doc.add_heading("Contents", 1)
                for h in [x[1] for x in C if x[0] == "h1"]:
                    doc.add_paragraph(h, style="List Bullet")
                doc.add_page_break(); toc_done = True
            doc.add_heading(it[1], {"h1": 1, "h2": 2, "h3": 3}[t])
        elif t == "p":
            doc.add_paragraph(it[1])
        elif t == "bullets":
            for b in it[1]:
                doc.add_paragraph(b, style="List Bullet")
        elif t == "code":
            code_par(doc, it[1])
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
    to_markdown()
    to_docx()
    print("Wrote Docker_Documentation.md and Docker_Documentation.docx")
