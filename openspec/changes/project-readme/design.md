# Design

## Context

See [proposal.md](proposal.md) for the motivation and scope. The repository contains a Reflex application connected to Xano, documentation for authentication and the employee, manager, technician, and administrator areas, and an `.env.example` with the Xano URL variable. The general project overview still describes the frontend choice as undecided, while the current application and dependency files use Reflex. The administrator change also records implementation details alongside validations that remain incomplete.

## Goals / Non-Goals

**Goals:**
- Make the root README a concise starting point for an evaluator, with links to authoritative details.
- Make it clear which statements describe the current application and which describe planned MVP scope or pending validation.
- Keep setup guidance short and sourced from versioned files.

**Non-Goals:**
- Rewrite or reconcile the existing project documentation as part of this change.
- Claim production deployment, completed MVP, integrated AI features, or fully validated backend behavior without evidence.
- Document every API contract, database field, or contributor workflow.

## Decisions

- **Use one root `README.md` as the evaluator entry point.** A single discoverable file fits the requested audience; a separate presentation document would split the overview without adding value.
- **Prefer current implementation and operational records over stale planning statements when describing the present.** The current Python application, Reflex dependency, portal documentation, and OpenSpec task records are stronger evidence of current state than the older overview's unresolved Streamlit/Reflex choice. Where implementation and validation differ, label the validation as pending rather than treating code presence as proof of end-to-end behavior.
- **Organize the overview around purpose, user profiles, current capabilities, project status, technology, brief startup configuration, and further reading.** This keeps the evaluator's path focused while linking to detailed portal and session documents instead of copying their contracts.
- **Use only the versioned environment example for configuration guidance.** Refer to `.env.example` and the documented `XANO_API_BASE_URL` setup; never include local environment values, tokens, or deployment claims.

Alternatives considered: retain the older overview's undecided frontend statement (contradicts the current code); present all MVP goals as completed (overstates delivery); or duplicate portal-level details in the README (creates multiple sources of truth). The chosen approach avoids these inaccuracies and duplication.

## Risks / Trade-offs

- [Existing documentation may remain inconsistent with the README] -> State current facts based on implementation and operational evidence, link detailed documents, and keep updating the README's status when implementation changes.
- [A short evaluator-focused README may omit developer details] -> Link to the existing login/session and portal documentation rather than expanding the root document.
- [Setup guidance could expose environment-specific configuration] -> Show only a placeholder and instructions from `.env.example`; do not read or copy `.env`.

## Migration Plan

Create the root README without changing application behavior. Review every link and command against repository files, check that configuration examples contain no secrets, and confirm the README distinguishes current implementation from pending validation. Rollback, if needed, is limited to removing the new README.
