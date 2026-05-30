# Projects

A **Project** is a bounded piece of work — something with a **start** and, usually, an **end**. "Relaunch the website." "Plan the trip." "Write the book." You open it, you work on it, you finish it, you archive it.

A Project does **not** hold your files itself. It **points at** the things the work touches:

- one or more **Codespaces** (repos / sites)
- **Docs** pages
- **Drive** folders
- **Tasks** lists
- the **people** working on it

Think of a Project as a folder of *links*, not a folder of *files*. The real stuff stays where it already lives in your pod; the Project just gathers references to it.

Where it lives: a shared `/projects/` space in your pod, one document per project — so other apps (like Flow) and your agents can read it without extra sharing steps.

## A Project can have many Codespaces

A real project often spans several repos — a website, a blog, some infrastructure — plus non-code things like a brief and a task list. So one Project can reference **many** Codespaces, and a Codespace can be used by **more than one** Project. Because the Project only links to them, nothing has to move when work is reorganized.

## Project vs. Codespace — the key difference

| | **Project** | **Codespace** |
|---|---|---|
| Lifespan | Has a start and an end | Lives on indefinitely |
| Nature | An *initiative* you pursue | An *asset* you keep |
| State | active → done → archived | maintained or dormant — never "finished" |
| When a project ends | it archives; its links stay as history | unaffected — it outlives the project |

This is *why* a Project must only **link** to its Codespaces, never own them: when the project ends, the repos and docs stay in your pod and can be picked up by the next project.

---

## Why we don't have a "Workspace"

"Workspace" sounds useful, but every time we tried to pin it on something, a clearer word already did the job:

- **The front door** — where you sign in, launch apps, edit your profile, manage your account — is **Home**.
- **A place to write notes and pages** is **Docs**.
- **A bounded piece of work** is a **Project**.
- **The long-lived place that holds everything you own** is your **Pod**. (Need to separate work from personal life? You make a second pod — not a second "workspace".)

So "workspace" has no job left that isn't already covered:

- The thing you *work in* → that's a **Project**.
- The lasting space that *holds many projects* → that's your **Pod**.

Adding "Workspace" on top would just be a third word competing with **Pod** and **Project**, and we'd spend forever explaining the difference. So we leave it out.

**One exception, for later:** if people ever want separate areas *inside a single pod* — a "Work" side and a "Personal" side, each with its own projects and members — "Workspace" would be the right name for that. We're keeping the word on the shelf for that case only, and not using it before then.
