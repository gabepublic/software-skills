---
name: nextjs-config-01
description: >-
  Defines this repository's Next.js App Router stack, boundaries, and conventions:
  strict TypeScript, shadcn/ui, Tailwind, Zod definitions only under lib/validation,
  React Hook Form, iron-session, bcrypt.js, Prisma (Node runtime only), TanStack Query,
  Vitest and Playwright, service-provider pattern with interfaces and factories,
  kebab-case routes and _private folders, @/ imports, Prisma snake_case DB mapping,
  REST and JSON naming, metadata/SEO, Vercel Analytics, Core Web Vitals and security
  baselines, and release gates. Use when implementing, reviewing, refactoring, planning
  stories, or generating project code; when the user mentions architecture, conventions,
  folder layout, business-layer, providers, validation schemas, Prisma, proxy vs
  middleware, or aligning with this project's standards—even if they do not name this skill.
user-invocable: false
---

# Next.js project config (nextjs-config-01)

Apply this skill together with [Next.js Best Practices](@.agents/skills/next-best-practices/SKILL.md) for App Router mechanics (routing, RSC, caching, Server Actions, `next/script`, etc.).

**Additional detail** for *this* skill lives in:

| Document | Contents |
|----------|----------|
| [resources/architecture.md](./resources/architecture.md) | Service provider architecture, metadata (SEO) , monitoring & observability, release, and TypeScript |
| [resources/convention.md](./resources/convention.md) | Naming, folder tree, imports, Zod, formats, anti-patterns, enforcement, testing, docs |

When instructions conflict, follow the **guidances** in this skill and the referenced resources; use this file as a compressed checklist.

---

## Stack (fixed choices)

| Category | Technology |
|----------|------------|
| Language | TypeScript (strict; no `any` on public APIs without justification) |
| Framework | Next.js (App Router) — frontend + server |
| UI | React |
| UI components | shadcn/ui |
| Styling | Tailwind CSS |
| Validation | Zod — **definitions only** under `/lib/validation/` |
| Forms | React Hook Form |
| Local UI state | React Context + hooks |
| Session | iron-session |
| Password hashing | bcrypt.js |
| Database ORM | Prisma |
| Server/async client state | @tanstack/react-query |
| Testing | Vitest (unit/integration); Playwright (E2E) |

---

## Runtime and data boundaries

- **Prisma targets Node.** Use Prisma from Server Components, Server Actions, and `route.ts` on the **default Node** runtime. Do **not** rely on Prisma in **Edge** (`proxy` / `middleware` or `runtime = 'edge'`) unless you adopt an edge-compatible data client. See [runtime-selection.md](@.agents/skills/next-best-practices/runtime-selection.md).

- **Server vs client:** Prefer Server Components; use `'use client'` only where hooks, events, or browser APIs require it; prefer **server parent + client child** for mixed routes.

- **Data:** Database reads in server code; HTTP with explicit cache/revalidate where applicable; mutations via Server Actions (and/or route handlers) with Zod validation from `/lib/validation/`.

- **Hooks:** Logic-only, composable, under `hooks/` per convention; do **not** return JSX, import UI for unrelated concerns, or mix unrelated responsibilities in one hook.

- **Anti-patterns (align with Next.js skill):** Avoid `'use client'` on large trees, client-fetching for core reads where RSC suffices, and missing `loading.tsx` / `error.tsx` where UX needs them.

---

## Folder layout (high level)

Follow [resources/convention.md](@./resources/convention.md) for the full tree. Important roots:

- `app/` — routes, layouts, pages, loading/error/not-found, `route.ts` APIs
- `components/` — reusable UI (`ui/`, `forms/`, `layout/`, `ui-mobile/`, …)
- `lib/` — utilities, `prisma.ts`, shared logic; **`lib/validation/*.schemas.ts`** for Zod
- `services/` — domain types, `*_interface.ts`, `*_prisma.ts` implementations
- `providers/` — factories (e.g. `user_crud_providers.ts`)
- `business-layer/` — app `config/`, `types/`, `queries/`, `mutations/`, `utils/`
- `hooks/` — `browser/` vs `mobile/` as needed
- `tests/` — unit area; E2E under `tests/e2e/`
- Root: `proxy.ts` (**Next.js 16+**) *or* `middleware.ts` (**14–15**) for edge auth/redirects — **one** pattern matching the installed version, not both active. See [file-conventions.md](@.agents/skills/next-best-practices/file-conventions.md).

**Reserved App Router filenames** (exact names, lowercase): `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`, `global-error.tsx`, `route.ts`, `template.tsx`, `default.tsx`. Do **not** rename to PascalCase. Do **not** put `route.ts` and `page.tsx` in the **same** segment.

**Private route folders:** leading `_` (e.g. `_components/`, `_tests/`) — excluded from the URL.

---

## Naming (quick reference)

| Area | Rule |
|------|------|
| Route segments (public) | `kebab-case` |
| Private folders | `_name/` |
| Your React component modules | `PascalCase.tsx` matching the primary export |
| Lib / hooks / utilities | `camelCase.ts` |
| Type-only modules | `camelCase.types.ts` |
| Prisma | PascalCase models; plural **snake_case** tables `@@map`; DB columns **snake_case** with `@map` on camelCase fields |
| REST API paths | Lowercase, hyphenated segments, no trailing slash |
| JSON / TS objects | **camelCase** keys |
| DB | **snake_case**; transform at boundary |

---

## Imports and validation

- **`@/`** for project imports; **relative** only for same-directory (`./`).

- **Order:** external packages → `next/*` → internal `@/` → `import type` for types-only.

- **Zod:** **Single source of truth** in `/lib/validation/` (e.g. `auth.schemas.ts`). **Never** duplicate schema definitions in components; optional barrels may **re-export** only. Same schema on client (forms) and server (actions/routes).

- **Components:** Co-locate component-only types/helpers; import schemas from `@/lib/validation/...`.

---

## Monitoring and analytics

- **Primary product analytics:** **Vercel Analytics** (`@vercel/analytics`) — `<Analytics />` in root layout; `track()` for custom events.

- **Other scripts:** Use `next/script` and loading strategies per [scripts.md](@.agents/skills/next-best-practices/scripts.md); avoid raw `<script>` where the skill prescribes otherwise.

- **Observability baseline:** Frontend RUM/CWV (e.g. Vercel Analytics), server logs for API routes, error boundaries + optional Sentry/LogRocket; Lighthouse CI in GitHub Actions per architecture.

- For additional details and examples, see [resources/architecture.md](@resources/architecture.md) - Monitoring & Observability.

---

## Non-functional requirements (baseline)

**Performance (primary):** LCP under 2.5s, INP under 200ms, CLS under 0.1. Secondary: initial load under 2s where measured; lab TBT under 200ms; client navigations under 500ms.

**Security:** HTTPS in production; cookies **HttpOnly**, **Secure**, **SameSite=Lax**; no sensitive data in logs.

**Browsers:** Modern evergreen; latest two of Chrome, Firefox, Safari, Edge.

**Accessibility:** WCAG 2.1 Level A baseline — keyboard, semantic HTML, visible focus, form labels — global unless explicitly scoped otherwise.

**Privacy / compliance:** GDPR/CCPA-oriented architecture; consent-aware handling; deletion/export in later phases per product.

**Graceful degradation:** Fault-tolerant integration boundaries; one external dependency failure must not break overall UX.

**Release:** Clean `next build`, no TypeScript errors; verify `NEXT_PUBLIC_*` vs server-only secrets; Lighthouse/PageSpeed as needed for CWV goals.

---

## Testing

- Unit: `*.test.ts` / `*.test.tsx`; components: `ComponentName.test.tsx`.
- Page tests: co-located `app/.../_tests/PageName.test.tsx`.
- E2E: `tests/e2e/*.spec.ts`.

---

## Documentation

- JSDoc on **public** APIs; explain *why*, not *what*.
- Session and shared types: ISO 8601 strings where convention shows `loginTimestamp`, etc.

---

## Anti-patterns (reject in review)

- Duplicate Zod outside `/lib/validation/`.
- Cross-directory relative imports instead of `@/`.
- camelCase physical DB columns without `@map` to snake_case.
- Mismatched component filename vs export (except reserved App Router files).
- Prisma or Node-only APIs on Edge without an explicit compatible approach.
- Inconsistent REST paths (wrong casing, trailing slashes).

---

## Mandatory agent behaviors (enforcement)

1. Follow **naming** and **folder** conventions (including reserved `app/` filenames).
2. **Import** validation schemas — never duplicate Zod definitions.
3. Follow **project structure** (components, lib, app, services, providers, business-layer).
4. Use **`@/`** for internal imports.
5. **Co-locate** page tests in `_tests/` beside the route.
6. Match **component** file names to exports (`SignupForm` → `SignupForm.tsx`).

---

## Agent checklist

1. Stack matches the fixed table; Prisma used only on **Node** server contexts unless otherwise designed.
2. Files live where **convention.md** specifies; `proxy.ts` vs `middleware.ts` matches Next version.
3. Zod only under `/lib/validation/`; JSON camelCase; DB snake_case with Prisma mapping.
4. Imports use `@/` and prescribed order; `import type` for type-only imports.
5. Services use interfaces + factories; default CRUD factory Prisma-only unless Supabase appendix applies.
6. Metadata via `generateMetadata` / `metadata` export; Vercel Analytics pattern when adding analytics.
7. For large features or refactors, read **generate-skills-artifacts/architecture.md** and **convention.md** in full first.

---

## Resources

- [Architecture & NFRs](./resources/architecture.md)
- [Convention](./resources/convention.md)
- [Next.js Best Practices](@.agents/skills/next-best-practices/SKILL.md)
