# Next.js Project Specific Architecture

Apply these rules when generating stories, implementing, reviewing or improving code for the project.

## Project Constraints

| Category                 | Technology             | Scope                      |
| ------------------------ | ---------------------- | -------------------------- |
| Language                 | TypeScript             | Entire stack               |
| Framework                | Next.js (App Router)   | Frontend + server          |
| UI                       | React                  | Component layer            |
| UI components            | shadcn/ui              | Component-based UI library |
| Styling                  | Tailwind CSS           | Styling system             |
| Validation               | Zod                    | Single source of truth     |
| Form Management          | React Hook Form        | Form state management      |
| State Management         | React Context + Hook   | Local state mgmt for UI    |
| Session                  | iron-session           | Authentication state       |
| Cryptography             | bcrypt.js              | Password hashing           |
| Database ORM             | Prisma ORM             | Database ORM               |
| Server state Management  | @tanstack/react-query  | Server state               |
| Testing                  | Vitest, Playwright     | Unit + E2E                 |

**Prisma / database runtime:** Prisma Client targets the **Node.js** runtime. Use it from **Server Components**, **Server Actions**, and **`route.ts`** handlers that run on **Node** (the default). Do **not** rely on Prisma in **Edge** `proxy` / `middleware` or in routes that set **`runtime = 'edge'`** unless you adopt an explicitly edge-compatible data client. See [runtime selection](@.agents/skills/next-best-practices/runtime-selection.md) in Next.js Best Practices.

---

## Additional Next.js rules (summary)

These reinforce the stack in **Project Constraints**. Use [Next.js Best Practices](@.agents/skills/next-best-practices/) for routing, data fetching, caching, and Server Actions.

- **Server vs client:** Prefer Server Components; use `'use client'` only where hooks, events, or browser APIs require it; prefer **server parent + client child** for mixed routes.
- **Data and mutations:** Database reads in server code; HTTP with explicit cache/revalidate; mutations via Server Actions with Zod validation (see convention for shared schema location).
- **Hooks:** Logic-only, composable, under `hooks/` per [convention](@convention.md); do not return JSX, import UI components, or mix unrelated concerns in one hook.
- **Anti-patterns:** Avoid `'use client'` on large trees, client-fetching for core reads where RSC suffices, and missing `loading.tsx` / `error.tsx` where UX needs them—aligned with the skill’s RSC and UX guidance.

- **Service Provider Architecture**

  - **Goal:**
    - Provider-agnostic service access
    - Enable easy swapping of services

  - **Stack alignment:** **Prisma** (see **Project Constraints**) is the default way to access the application database. Use a **Prisma-backed** adapter for `UserCRUD` in normal product code—only from **Node** server contexts (see **Prisma / database runtime** above), not from Edge `proxy` / `middleware` unless you use a different data client there. The **factory below is Prisma-only** so it compiles without `@supabase/supabase-js`. For an optional **Supabase client** adapter and a multi-provider factory, see [Appendix: Supabase alternate provider](#appendix-supabase-alternate-provider).

  - **Example:**

    - Domain Model (Provider-Agnostic): `services/user.ts`
    ```ts
    // `services/user.ts`
    export interface User {
      id: string
      email: string
      name?: string
    }
    ```

    - Service Interface: `services/user_crud_interface.ts`
    ```ts
    import type { User } from "@/services/user"

    export interface UserCRUD {
      getById(id: string): Promise<User | null>
      create(user: User): Promise<void>
    }
    ```

    - Primary implementation (Prisma): `services/user_crud_prisma.ts` — satisfies `UserCRUD` using the shared Prisma client (e.g. `@/lib/prisma`), consistent with [convention](@convention.md) (prefer functional style over classes).
    ```ts
    import type { UserCRUD } from "@/services/user_crud_interface"
    import type { User } from "@/services/user"
    import { prisma } from "@/lib/prisma"

    export function createPrismaUserCRUD(): UserCRUD {
      return {
        async getById(id: string): Promise<User | null> {
          const row = await prisma.user.findUnique({ where: { id } })
          if (!row) return null
          return {
            id: row.id,
            email: row.email,
            name: row.name ?? undefined,
          }
        },

        async create(user: User): Promise<void> {
          await prisma.user.create({
            data: {
              id: user.id,
              email: user.email,
              name: user.name,
            },
          })
        },
      }
    }
    ```

    - Provider factory (Prisma only): `providers/user_crud_providers.ts` — no Supabase import; safe default for a Prisma-only repo.
    ```ts
    import type { UserCRUD } from "@/services/user_crud_interface"
    import { createPrismaUserCRUD } from "@/services/user_crud_prisma"

    export function getUserCRUD(): UserCRUD {
      return createPrismaUserCRUD()
    }
    ```

    - Usage in Server Components or Server Actions
    ```ts
    import { getUserCRUD } from "@/providers/user_crud_providers"

    export default async function UserPage() {
      const userCRUD = getUserCRUD()
      const user = await userCRUD.getById("123")

      return <pre>{JSON.stringify(user, null, 2)}</pre>
    }
    ```


- **Metadata (SEO)**

  - Prefer concrete **title** (~50–60 characters) and **description** (~150–160 characters) where they are user-facing SERP fields.
  - Set **Open Graph** (and Twitter when needed) and a **canonical URL** (`alternates.canonical`) when duplicate or parameterized URLs exist.
  - Use `generateMetadata` (or the static `metadata` export) for all SEO — never hardcode `<title>` or `<meta>` tags in JSX. (See also `metadata.md` in the Next.js skill.)

---

## Non-functional Requirements

### Performance (Primary)

- Core Web Vitals (primary thresholds):
  - LCP < 2.5s
  - INP < 200ms (good)
  - CLS < 0.1

- System Targets (Secondary):
  - Initial page load < 2s (product-level; align with LCP where measured)
  - **Lab:** Total Blocking Time (TBT) < 200ms (Lighthouse mobile profile); complements field **INP**
  - Client-side navigation < 500ms

### Security Requirements

- HTTPS enforced in production
- Secure cookies (`HttpOnly`, `Secure`, `SameSite=Lax`)
- No sensitive data logged

### Browser Support
- Modern evergreen browsers only
- Latest 2 versions of Chrome, Firefox, Safari, Edge

### Accessibility (Global)

- WCAG 2.1 Level A baseline
- Keyboard navigation
- Semantic HTML
- Visible focus indicators
- Proper form label associations

Accessibility requirements apply globally to all UI unless explicitly stated.

All subsequent references to accessibility across this document inherit from this section and must not redefine or dilute these requirements.

### Privacy & Compliance

- GDPR / CCPA compliant architecture
- Consent-aware data handling
- Data deletion and export supported in later phases

### Graceful Degradation

- Fault-tolerant integration boundaries
- One external dependency failure must not break UX

---

## Monitoring & Observability

- **Monitoring Stack:**
	- **Frontend:** Vercel Analytics (RUM, Core Web Vitals)
	- **Backend:** Vercel Logs (API routes, serverless functions)
	- **Error Tracking:** Console logging + Error boundaries (baseline), Sentry or LogRocket (Optional)
	- **Performance:** Lighthouse CI in GitHub Actions
	- **Profiling:** Chrome DevTools
	- **Latency Monitoring:** Custom instrumentation to be implemented by product

- **Analytics vs other scripts:** **Vercel Analytics** (`@vercel/analytics`) is the primary product analytics choice—integrate it as in the example below. Any additional third-party scripts must follow script-loading guidance in [Next.js Best Practices](@.agents/skills/next-best-practices/) (`scripts.md`: `next/script`, loading strategies)—do not add raw `<script>` tags where the skill prescribes otherwise.

- **Key Metrics:**
	- **Frontend:**
		- Core Web Vitals
		- JavaScript errors
		- API response times
		- User interactions
	- **Backend:**
		- Request rate and error rate
		- Response time (P95)
		- Authentication success rate

- **Analytics example:**

```typescript
// app/layout.tsx
import type { ReactNode } from 'react';
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({
  children,
}: Readonly<{ children: ReactNode }>) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

- **Custom Event Tracking:**

```typescript
import { track } from '@vercel/analytics';

track('todo_created', { descriptionLength: description.length });
track('user_signin', { provider: 'google' });
```

- **Logging:**
	- **Development:** Verbose console logging
	- **Production:** Minimal structured logs, no PII
	- **Phase 2:** Winston for structured logging, Sentry for error tracking

---

## Release

- Do not ship without a clean next build (and, in TS projects, no type errors), check `NEXT_PUBLIC_*` and server-only env vars are set, run Lighthouse/PageSpeed to confirm Core Web Vitals requirements.

---

## TypeScript

- Strict TypeScript across the stack; no `any` for public APIs without justification.
- Shared types and Zod schemas: locations and naming per [convention](@convention.md) (`*.types.ts`, `/lib/validation/`).

---

## Appendix: Supabase alternate provider

Use this only when the product intentionally uses **`@supabase/supabase-js`** for `UserCRUD` (e.g. bounded subsystem, migration, or external Supabase project). Add the dependency, env vars (`SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`), and `services/user_crud_supabase.ts`, then extend the factory with a `USER_DB_PROVIDER` switch.

**Typing / wire shape:** PostgREST returns JSON keys that match **database column names** (often **snake_case** per [convention](@convention.md)). Do **not** treat the raw `data` object as `User`—map rows into the domain type. Adjust `UsersRow` keys to match your table; the mapper below assumes columns `id`, `email`, `name` in SQL (add `@map` or rename fields if yours differ).

**Adapter:** `services/user_crud_supabase.ts`

```ts
import type { UserCRUD } from "@/services/user_crud_interface"
import type { User } from "@/services/user"
import { createClient } from "@supabase/supabase-js"

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

/** Row as returned by Supabase — keys follow physical column names */
type UsersRow = {
  id: string
  email: string
  name: string | null
}

function mapRowToUser(row: UsersRow): User {
  return {
    id: row.id,
    email: row.email,
    name: row.name ?? undefined,
  }
}

export function createSupabaseUserCRUD(): UserCRUD {
  return {
    async getById(id: string): Promise<User | null> {
      const { data, error } = await supabase
        .from("users")
        .select("*")
        .eq("id", id)
        .single()

      if (error || !data) return null
      return mapRowToUser(data as UsersRow)
    },

    async create(user: User): Promise<void> {
      await supabase.from("users").insert({
        id: user.id,
        email: user.email,
        name: user.name ?? null,
      })
    },
  }
}
```

**Factory with switch** (replace the Prisma-only `getUserCRUD` when you add Supabase):

```ts
import type { UserCRUD } from "@/services/user_crud_interface"
import { createPrismaUserCRUD } from "@/services/user_crud_prisma"
import { createSupabaseUserCRUD } from "@/services/user_crud_supabase"

export function getUserCRUD(): UserCRUD {
  const provider = process.env.USER_DB_PROVIDER ?? "prisma"
  switch (provider) {
    case "prisma":
      return createPrismaUserCRUD()
    case "supabase":
      return createSupabaseUserCRUD()
    default:
      throw new Error(`Unknown USER_DB_PROVIDER: ${provider}`)
  }
}
```
