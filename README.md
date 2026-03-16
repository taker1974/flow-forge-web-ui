# Flow Forge Web UI · Stage 1 Prototype

This is a minimal standalone prototype of an n8n/make-style canvas:

- **Top toolbar**: 10 “Lorem ipsum” style buttons; each shows a simple `alert` when clicked.
- **Left library**: 10 colorful rectangular blocks with arbitrary labels (different categories).
- **Right canvas**: Bounded 1200×700 grid canvas where blocks can be:
  - **Dragged from the library** onto the canvas (copy behaviour, the original stays in the library).
  - **Freely moved around** inside the canvas after they have been added.

No build step is required: everything is in a single `index.html` file.

## Run locally

From the project root:

```bash
npm install
npm run start
```

Then open the printed URL (for example `http://localhost:3000` or `http://localhost:5000`, depending on `serve`) in your browser.
