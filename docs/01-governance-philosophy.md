# Governance Philosophy

## Why This Framework Exists

Claude Code agents can read, write, execute, and network. In a production environment, those capabilities are exactly what makes them useful. They are also exactly what makes them dangerous without a control layer. The governance framework is not a patch on top of an unsafe system; it is a principled architecture for deploying that system in environments where mistakes have real costs.

This document explains the principles that shaped the design. Understanding the reasoning matters because the framework will need to be extended over time. New controls should fit the existing philosophy, not contradict it.

## Principle 1: Defense in Depth

No single control is sufficient. The framework layers multiple independent controls so that a failure in one does not create an open path for harm.

**In practice:**
- The file guard (PreToolUse) blocks writes to protected paths.
- The bash guard (PreToolUse) blocks dangerous commands.
- The post-tool verifier (PostToolUse) confirms that writes actually succeeded as expected.
- The stop auditor records everything for retrospective review.
- The release scanner checks the output tree before publication.

Each of these controls can fail independently. If the file guard's config is misconfigured, the post-tool verifier still logs anomalies. If the bash guard misses a pattern, the audit trail still records what ran. If the audit trail is corrupted, the release scanner still catches secrets before they ship.

Defense in depth means that an attacker (or an errant agent) must defeat multiple independent controls to cause undetected harm. It also means that a bug in one control does not create a catastrophic gap.

## Principle 2: Verification Before Assertion

Agents frequently make claims about system state: "the file was written," "the tests pass," "the API returned success." These claims feel authoritative but are often based on memory or inference rather than observed evidence.

The framework treats unverified claims as hypotheses. Before any claim about system state can be presented as fact — to the user, to a downstream process, or in an audit record — it must be backed by tool output.

**In practice:**
- The post-tool verify hook checks that files exist after writes. It does not trust the Write tool's success response alone.
- The verification-before-completion skill requires an explicit evidence checklist before any task is declared done.
- The systematic-debugging skill requires reproduction of the bug before hypothesizing a cause.

This principle traces to a deeper problem: language models are trained to produce fluent, confident text. They will assert that a task is complete when it is not, because asserting completion is the fluent thing to do. Structural verification requirements counteract this tendency.

## Principle 3: Minimal Blast Radius

When the framework errs, it should err toward doing less, not more. A blocked operation that the user wanted is recoverable. An unblocked operation that corrupts data may not be.

**In practice:**
- PROTECTED paths are blocked absolutely, with no override mechanism in the hook itself.
- GOVERNANCE paths require explicit user approval, not model approval.
- New patterns added to the bash blocklist default to blocking, not warning.
- The audit trail records blocks so a human can review and override deliberately.

The framework is not trying to be maximally permissive. It is trying to be maximally safe at the cost of occasionally requiring a human to explicitly authorize something the model could have done automatically.

## Principle 4: Separation of Public and Private Trees

The framework itself — its documentation, its hook scripts, its skill definitions, its example configurations — is designed to be publishable. Organizations that adopt this framework should be able to share it, fork it, and contribute to it without exposing their secrets or their organizational context.

This requires a hard structural boundary between what is generic (public tree) and what is personal or organizational (private tree).

**In practice:**
- Framework code lives in the public tree: `docs/`, `hooks/`, `skills/`, `scripts/`, `examples/`.
- Personal configuration lives in the private tree: `~/.claude/`, `.env`, the real `settings.json`.
- The examples directory contains `.example.` files — templates that illustrate the structure without containing real secrets.
- The release scanner (`scripts/scan_public_template.py`) enforces this boundary before any release.

The boundary is not just a social convention. It is enforced by path guards (the GOVERNANCE tier covers private config files) and by the release scanner (which detects credentials and personal data in the public tree).

## Principle 5: Named Processes Over Inline Improvisation

Multi-step processes executed inline by the model are unreliable because there is no contract. The model may skip steps, reorder them, or invent new ones depending on the context window, the phrasing of the prompt, or random sampling.

Named skills solve this by encoding the process in a `SKILL.md` file that the model reads before executing. The contract specifies the trigger conditions, the steps in order, the evidence requirements at each step, and the output format. The model is not improvising; it is following a defined process.

**In practice:**
- The systematic-debugging skill requires reproduction before hypothesis. A model executing inline might skip directly to a fix.
- The TDD skill requires the failing test to exist before any implementation code is written.
- The verification-before-completion skill requires an explicit evidence checklist before done is declared.

The skill routing design (doc 06) covers when to use a named skill versus inline execution.

## Principle 6: Transparency Over Opacity

The framework must be auditable by the humans who depend on it. Controls that block silently are more dangerous than controls that explain themselves, because silent blocks lead users to believe that operations succeeded when they were blocked.

**In practice:**
- The file guard emits a JSON response that Claude can read, explaining what was blocked and why.
- The bash guard logs blocked commands with the matched pattern.
- The stop auditor writes structured JSONL that can be queried with standard tools.
- The release scanner produces file:line findings, not a pass/fail binary.

Transparency also means the framework documentation is thorough. A control that is not documented is a control that will be bypassed accidentally by the next person who configures the system.

## Principle 7: Prefer Explicit over Implicit

Configuration should be explicit. Behavior should not be inferred from absence. If a path is not listed in the path guard config, the framework should take the safer default (warn) rather than assume it is safe to write.

**In practice:**
- Unlisted paths default to IMPORTANT tier (warning) rather than unrestricted.
- Skills are invoked by explicit routing, not by pattern-matching on the prompt alone.
- Environment variables for secrets must be explicitly declared in settings; they are not read from the shell environment implicitly.
- The audit record explicitly lists tools used, files written, and blocks triggered — not a summary derived from inference.

## What These Principles Rule Out

These principles collectively rule out some design choices that might otherwise seem appealing:

- **"Smart" blocklists that learn from usage.** Learning systems can be fooled, gamed, or drifted. The blocklist is static and reviewed by humans.
- **Auto-approving GOVERNANCE tier writes after a delay.** The point of GOVERNANCE tier is human review, not timeout.
- **Trusting model self-reports of task completion.** The post-tool verify hook and the verification skill exist precisely because self-reports are unreliable.
- **Storing secrets in environment variables set in the CLAUDE.md.** CLAUDE.md is read into context and can appear in transcripts. Secrets go in OS secure stores.

## The Goal Is Not Restriction; It Is Trust

A governance framework that makes Claude Code agents trustworthy in production is not a restriction on their power. It is the infrastructure that makes it safe to give them more power. An agent that can write to any file without review is an agent that cannot be trusted in a production environment. An agent that writes only to verified paths, with an audit trail, and with evidence of completion, is an agent that can be given access to real systems.

The governance framework is an investment in trust. It pays off when the agent encounters an edge case, makes a mistake, or is given a task with ambiguous scope — and the controls catch the problem before it becomes a crisis.
