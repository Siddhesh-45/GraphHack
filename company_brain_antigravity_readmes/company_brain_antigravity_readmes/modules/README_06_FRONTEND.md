# Module 06 — Frontend and Graph Explorer

## Goal
Build a polished, accessible React application that exposes real Company Brain capabilities.

## Stack
- React + TypeScript + Vite
- Tailwind CSS
- shadcn/ui where useful
- `@xyflow/react` for graph visualization
- Typed API client based on the backend contract

## Pages and components
1. **Chat**
   - Message composer and conversation display.
   - Loading, retry, empty, and error states.
   - Render citations inline or in a side panel.
   - “Why this answer?” evidence panel.
   - Display uncertainty and conflicts visibly.
2. **Graph Explorer**
   - Render nodes and edges returned by the backend.
   - Support zoom, pan, fit-to-view, selection, and readable node labels.
   - Click a node to view details and related evidence.
   - Provide filters for people, projects, teams, decisions, incidents, and services.
   - Do not fabricate graph nodes on the client.
3. **Sources**
   - Upload supported files.
   - Show ingestion status, source type, timestamp, and errors.
   - Open source/chunk details.
4. **People and ownership**
   - Show explicit owners separately from inferred experts.
   - Explain why a person is suggested and link evidence.
5. **Decision history**
   - Timeline of decisions, current/superseded status, sources, and conflicts.
6. **Impact view**
   - Display direct and indirect dependencies and their graph paths.

## UX and design requirements
- Professional, modern, clean enterprise interface.
- Light and dark mode only if it can be completed without delaying core functionality.
- Use accessible labels, keyboard navigation, sensible contrast, responsive layout, and consistent spacing.
- Include empty states with next-step guidance.
- Do not show hard-coded demo answers in production UI.
- Use synthetic sample data only in clearly labelled demo mode.
- Avoid excessive animation and unnecessary dashboard widgets.
- Never show fake “100% confidence” badges or fabricated source counts.

## API integration
- Create a single typed API client.
- Configure API base URL via environment variable.
- Handle HTTP errors and timeouts.
- Keep server state and UI state separate.
- Validate response data where useful.
- Avoid direct database access from the browser.

## Acceptance criteria
- Every visible action works or is explicitly disabled with a reason.
- Chat answer citations can be opened.
- Graph Explorer renders actual API graph data.
- Source upload status refreshes correctly.
- Layout works at desktop and mobile widths.
- Loading, error, empty, and no-evidence states are implemented.
