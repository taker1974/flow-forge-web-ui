# Flow Forge Web UI · Stage 1 Prototype

This is a minimal standalone prototype of an n8n/make-style canvas:

- **Top toolbar**: 10 “Lorem ipsum” style buttons; each shows a simple `alert` when clicked.
- **Left library**: 10 colorful rectangular blocks with arbitrary labels (different categories).
- **Right canvas**: Bounded 1200×700 grid canvas where blocks can be:
  - **Dragged from the library** onto the canvas (copy behaviour, the original stays in the library).
  - **Freely moved around** inside the canvas after they have been added.

No build step is required: static HTML, CSS, and JavaScript only. Shared assets (`font/`, `images/`) live in the project root; each app entry point references them with relative paths.

## Project layout

- **`index.html`** (root) — landing page with links to the apps below.
- **`developer/index.html`** — **FlowForge Developer Studio**: editing workflow templates (blocks, connections, defaults).
- **`runner/index.html`** — **FlowForge Runner**: placeholder aligned with the future “run template instance” experience (currently a copy of the developer UI).

## Run locally

From the project root:

```bash
npm install
npm run start
```

Then open the printed URL (for example `http://localhost:3000` or `http://localhost:5000`, depending on `serve`) in your browser. Use **`/`** for the hub, **`/developer/`** for the studio, or **`/runner/`** for the runner.
