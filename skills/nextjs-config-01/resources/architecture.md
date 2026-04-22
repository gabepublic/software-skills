# Next.js Project Specific Architecture

Apply these rules when generating stories, implementing, reviewing or improving code for the project.


## Additional Next.js rules (summary)

These reinforce the stack in **Project Constraints**. Use [Next.js Best Practices](@.agents/skills/next-best-practices/) for routing, data fetching, caching, and Server Actions.

### Service Provider Architecture

- **Goal:** Provider-agnostic domain types and interfaces; swap implementations via factories.

- **Example:** **Prisma** as the Database service provider. The Prisma service implementation is in `services/user_crud_prisma.ts`, wired through `providers/user_crud_providers.ts` with `getUserCRUD()` returning the `createPrismaUserCRUD()`.

- For adding additional alternate providers, like Supabase, see the appendix, "Appendix: Supabase alternate provider" 

- **Example Codes:**

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

  - Prisma implementation: `services/user_crud_prisma.ts` — satisfies `UserCRUD` using the shared Prisma client (e.g. `@/lib/prisma`), consistent with [convention](./convention.md) (prefer functional style over classes).
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

  - Prisma Provider factory: `providers/user_crud_providers.ts` — no Supabase import; safe default for a Prisma-only repo.
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

### Metadata (SEO)

- Prefer concrete **title** (~50–60 characters) and **description** (~150–160 characters) where they are user-facing SERP fields.
- Set **Open Graph** (and Twitter when needed) and a **canonical URL** (`alternates.canonical`) when duplicate or parameterized URLs exist.
- Use `generateMetadata` (or the static `metadata` export) for all SEO — never hardcode `<title>` or `<meta>` tags in JSX. (See also `metadata.md` in the Next.js skill.)
- See the Next.js Best Practices, [metadata.md](@.agents/skills/next-best-practices/metadata.md), for additional details.

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
- Shared types and Zod schemas: locations and naming per [convention](./convention.md) (`*.types.ts`, `/lib/validation/`).

---

## Appendix: Supabase alternate provider

Use this only when the product intentionally uses **`@supabase/supabase-js`** for `UserCRUD` (e.g. bounded subsystem, migration, or external Supabase project). Add the dependency, env vars (`SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`), and `services/user_crud_supabase.ts`, then extend the factory with a `USER_DB_PROVIDER` switch.

- **Typing / wire shape:** PostgREST returns JSON keys that match **database column names** (often **snake_case** per [convention](./convention.md)). Do **not** treat the raw `data` object as `User`—map rows into the domain type. Adjust `UsersRow` keys to match your table; the mapper below assumes columns `id`, `email`, `name` in SQL (add `@map` or rename fields if yours differ).

- **Adapter:** `services/user_crud_supabase.ts`
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

- **Factory with switch** (replace the Prisma-only `getUserCRUD` when you add Supabase):
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
