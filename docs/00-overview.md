# Claude Code Governance Framework — Overview

## What This Framework Is

This governance framework is a control layer that sits between Claude Code agents and the systems they operate on. It is not a restriction on Claude's capabilities; it is a disciplined structure that makes those capabilities safe to use in real environments with real consequences.

The framework is built on the premise that AI coding agents are powerful tools that can cause irreversible harm when they operate without appropriate constraints. A single misrouted file write can corrupt configuration. A bash command executed without review can delete data. A secret logged to a transcript can be exposed. The governance framework adds verification, boundaries, and audit trails at every point where those risks arise.

## Goals

1. **Prevent catastrophic, irreversible actions.** Block writes to protected system files, block dangerous bash patterns, and require evidence before declaring success.

2. **Maintain a clear audit trail.** Every session produces structured audit records: what tools were used, what files were written, what was blocked, and why.

3. **Enforce secret hygiene.** API keys and credentials must never appear in logs, transcripts, public files, or any output visible outside the controlled environment.

4. **Separate public and private concerns.** Framework code, documentation, and reusable components can be published. Personal configuration, credentials, and organization-specific data must not leave the private tree.

5. **Enable consistent, reusable processes.** Common multi-step operations (debugging, brainstorming, TDD, verification) are encoded as named skills that can be invoked reliably.

## Layers of Control

The framework has four primary control layers. They operate independently and provide defense in depth — a failure in one layer does not defeat the others.

### Layer 1: Hooks

Claude Code hooks are shell commands or scripts that run at defined lifecycle points in the agent's execution. This framework uses four hook types:

- **PreToolUse / file guard** (`hooks/pre_tool_guard_files.py`): Intercepts every file-writing tool call before it executes. Classifies the target path into PROTECTED, GOVERNANCE, or IMPORTANT tier and either blocks the call, challenges it for approval, or emits a warning.

- **PreToolUse / bash guard** (`hooks/pre_tool_guard_bash.py`): Intercepts every Bash tool call. Checks the command string against a blocklist of dangerous patterns. Blocks commands that match.

- **PostToolUse / verification** (`hooks/post_tool_verify.py`): Runs after every Write, Edit, and Bash call. Confirms that files actually exist after writes, logs non-zero bash exit codes, and produces structured records for the audit trail.

- **Stop / audit** (`hooks/stop_audit.py`): Runs when Claude ends a turn. Writes a structured audit entry to `~/.claude/audit.jsonl` summarizing the turn: session, timestamp, tools used, files touched, blocks triggered.

### Layer 2: Skills

Skills are named, reusable multi-step processes defined by a `SKILL.md` contract file. Instead of executing complex workflows inline and inconsistently, the agent routes to a named skill. The skill contract specifies the trigger, the process steps, the evidence requirements at each step, and the output format.

Current skills:
- **brainstorming** — Structured ideation with divergent/convergent phases.
- **systematic-debugging** — Reproduce → isolate → hypothesize → fix → verify.
- **tdd** — Red-green-refactor cycle with explicit test-first discipline.
- **verification-before-completion** — Evidence checklist before declaring any task done.

### Layer 3: Path Guards

Path guards classify filesystem paths into protection tiers. The tiers are defined in a configuration file (`examples/pre_tool_guard_files.config.example.json`) and enforced by the file guard hook:

- **PROTECTED**: Absolute block. No writes permitted under any circumstances.
- **GOVERNANCE**: Model-initiated writes blocked; user-approved writes may proceed.
- **IMPORTANT**: Warning emitted, write allowed. Used for files where accidental writes would be costly but recoverable.

### Layer 4: Secret Management

The framework enforces strict rules about how API keys and credentials are handled. Secrets are never logged, never written to the public tree, never embedded in scripts as literals. They are injected via environment variables from secure stores (OS keychain, secrets manager) and rotated on suspected exposure. The PowerShell wrapper (`examples/claude-wrapper.example.ps1`) shows the canonical injection pattern for Windows environments.

## How the Pieces Fit Together

```
User invokes claude
       |
       v
  [Pre-session]
  claude-wrapper injects ANTHROPIC_API_KEY from secure store
       |
       v
  [Claude Code session begins]
       |
  +----|------------------------------------------------------------+
  |    v                                                            |
  |  Claude proposes a tool call                                    |
  |    |                                                            |
  |    +---> PreToolUse hook fires                                  |
  |           |                                                     |
  |           +-- File write? --> pre_tool_guard_files.py           |
  |           |                   (PROTECTED → block, GOVERNANCE    |
  |           |                    → challenge, IMPORTANT → warn)   |
  |           |                                                     |
  |           +-- Bash call? --> pre_tool_guard_bash.py             |
  |                               (pattern match → block or allow)  |
  |    |                                                            |
  |    v                                                            |
  |  Tool executes (if not blocked)                                 |
  |    |                                                            |
  |    +---> PostToolUse hook fires                                 |
  |           |                                                     |
  |           +-- post_tool_verify.py: verify file exists,          |
  |               log bash failures, write audit record             |
  |                                                                 |
  |  Claude ends turn                                               |
  |    |                                                            |
  |    +---> Stop hook fires                                        |
  |           |                                                     |
  |           +-- stop_audit.py: write audit.jsonl entry            |
  +-----------|----------------------------------------------------|
              v
        Audit trail in ~/.claude/audit.jsonl
```

Alongside this runtime control, the `scripts/scan_public_template.py` script runs as a pre-release gate to catch secrets or private data before any version of the framework is published.

## Where to Go from Here

- **docs/01-governance-philosophy.md** — The reasoning behind the design choices.
- **docs/02-failure-modes-and-controls.md** — The failure matrix.
- **docs/03-control-surface-map.md** — What each control file guards and how.
- **docs/04-directory-tree-and-file-placement.md** — Where files go and why.
- **docs/05-path-guard-design.md** — Path tier definitions and membership.
- **docs/06-skill-routing-design.md** — How skills work and when to use them.
- **docs/07-secret-management.md** — Token discipline rules.
- **docs/08-private-vs-public-boundary.md** — What can be published.
- **docs/09-verification-discipline.md** — Evidence before assertions.
- **docs/10-release-redaction-checklist.md** — Pre-publish safety checklist.
