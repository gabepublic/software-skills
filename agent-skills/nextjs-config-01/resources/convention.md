# Next.js Project Specific Convention

Apply these rules when generating stories, implementing, reviewing or improving code for the project.

## Code Style and Structure

- Write concise, technical TypeScript code with accurate examples
- Employ functional and declarative programming patterns; **avoid classes** for application logic—use functions and object literals (or factories) that satisfy interfaces for service providers and adapters, as in [architecture](./architecture.md) § Service Provider Architecture
- Prioritize iteration and modularization over code duplication
- Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError)
- Organize files: exported component, subcomponents, helpers, static content, types

---

## Naming Conventions

### Folders and Files

- **Route segment folders** (under `app/`, not private): `kebab-case` for multi-word paths
  - Examples: `user-profile/`, `sign-in/`

- **Private folders** (excluded from the URL): leading `_`, then typically `kebab-case`
  - Examples: `_components/`, `_tests/`

- **Folder Structure:**
```
/
├── .github/workflows/          # CI/CD pipelines
├── app/                        # Pages, layouts, route handlers
│   ├── api/                    # API route layer (URL mirrors folder path)
│   │   └── auth/
│   │       └── signup/
│   │           └── route.ts    # e.g. POST /api/auth/signup
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Root page (redirect logic)
│   └── globals.css             # Global styles
├── business-layer/             # Application specific artifacts and business logic 
│   ├── config/                 # Application specific configuration
│   ├── mutations/              # React Query mutation hook
│   ├── types/                  # Application specific Domain types
│   ├── queries/                # React Query integration
│   │   └── user.ts           
│   └── utils/                  # Application specific utilities
├── components/                 # Reusable React components
│   ├── layout/                 # Layout components (Header, Footer)
│   ├── forms/                  # Form-specific components
│   ├── ui/                     # UI base components
│   └── ui-mobile/              # Mobile UI base components
├── data/                       # Data files (gitignored - users.json)
├── docs/                       # Documentation
├── hooks/                      # Hooks
│   ├── browser/                # Hooks for web browser desktop or mobile
│   └── mobile/                 # Hooks for mobile
├── lib/                        # Utilities, helpers, shared logic
│   ├── prisma.ts               # Prisma client singleton (server-only)
│   └── img_processor_sdk.ts    # Image processor sdk
├── providers/                  # Service provider switch
│   └── user_crud_providers.ts  # User CRUD provider factory (see architecture doc)
├── public/                     # Static assets
├── services/                   # Services implementation
│   ├── user.ts                 # User domain type
│   ├── user_crud_interface.ts  # User service interface
│   └── user_crud_prisma.ts     # UserCRUD via Prisma (see architecture; Supabase adapter is appendix-only)
├── scripts/                    # Scripts file
├── styles/                     # Global styles (if needed)
├── tests/                      # Unit and integration tests
├── .gitignore                  # Git ignore file
├── .env.example                # Environment template
├── .env.local                  # Local environment (gitignored)
├── eslint.config.mjs           # ESLint config file
├── proxy.ts                    # Edge auth / redirects (Next.js 16+); 14–15: use middleware.ts instead (see below)
├── next.config.ts              # Next.js config
├── package.json                # Dependencies
├── playwright.config.ts        # Playwright config file
├── postcss.config.mjs          # CSS transformation
├── tailwind.config.ts          # Tailwind config
└── tsconfig.json               # TypeScript config
```

**Proxy vs middleware (project root):** Next.js **16+** uses `proxy.ts` with `export function proxy` and `export const proxyConfig` for edge auth, redirects, and rewrites. On **Next.js 14–15** the same role is `middleware.ts` with `export function middleware` and `export const config`. Use the file that matches your installed Next version—do not keep both active. See the **Middleware / Proxy** section in [Next.js Best Practices · file-conventions](@.agents/skills/next-best-practices/file-conventions.md).

### App Router reserved filenames

Next.js requires **exact** filenames for route entry points. They are **not** PascalCase component files—even though you export React components from some of them.

| File | Role |
|------|------|
| `page.tsx` | UI for the segment |
| `layout.tsx` | Shared layout |
| `loading.tsx` | Loading / Suspense UI |
| `error.tsx` | Error boundary UI |
| `not-found.tsx` | 404 UI |
| `global-error.tsx` | Root error UI |
| `route.ts` | HTTP API handlers (`GET`, `POST`, …) |
| `template.tsx` | Layout that re-renders on navigation |
| `default.tsx` | Parallel route fallback |

**Rules:**

- Do **not** rename these to match a component (e.g. never `Error.tsx` instead of `error.tsx`).
- **`route.ts`:** implement API endpoints here; **do not** put `route.ts` and `page.tsx` in the **same** folder (same segment).

Reference: [Next.js file conventions](https://nextjs.org/docs/app/api-reference/file-conventions).

### Your React component modules

- **Files:** `PascalCase.tsx` matching the primary export (`SignupForm` → `SignupForm.tsx`).
- **Where:** e.g. `components/`, `app/.../_components/`—not by renaming reserved files above.

### Other TypeScript files

- **Libraries, hooks, utilities** (e.g. `lib/`): `camelCase.ts` — `authUtils.ts`, `sessionHelpers.ts`
- **Type definition files:** `camelCase` + `.types.ts` — `auth.types.ts`, `user.types.ts`

### Database Naming Conventions (Prisma schema)

**Physical SQL stays snake_case; Prisma models use PascalCase (singular) and camelCase fields mapped with `@@map` / `@map`.**

This block teaches **SQL/Prisma naming only**. It uses an **`Account`** model (typical **credentials / login** fields). That is **not** the same shape as the **`User`** domain type in [architecture — Service Provider](./architecture.md) (`id`, `email`, `name` for `UserCRUD`). Define a separate **`User`** model in `schema.prisma` that matches your product API (e.g. `String` `@id` if you use UUIDs).

```prisma
// CORRECT: singular model, plural snake_case table, snake_case columns in the database
model Account {
  id           Int       @id @default(autoincrement())
  userId       String    @unique @map("user_id")
  passwordHash String    @map("password_hash")
  createdAt    DateTime  @default(now()) @map("created_at")
  updatedAt    DateTime? @updatedAt @map("updated_at")

  @@map("accounts")
}

// INCORRECT: plural/PascalCase table name; camelCase column names in the database (no @map)
model Accounts {
  id           Int    @id @default(autoincrement())
  userId       String
  passwordHash String
}
```

**Rules:**
- **Tables (database):** lowercase, plural (`accounts`, `users`, `sessions`); avoid PascalCase SQL table names (`Accounts`) or singular names for shared tables (`user`); use `@@map("accounts")` on a singular Prisma model (e.g. `Account`).
- **Columns (database):** snake_case (`user_id`, `password_hash`); express them with `@map("...")` on camelCase Prisma fields so the generated client stays idiomatic TypeScript.
- **Timestamps:** `created_at`, `updated_at` columns mapped from `DateTime` fields as above; if you standardize on Unix integers in SQL, use `Int` with `@map` and the appropriate `@db.*` scalar (provider-specific).
- **Foreign keys:** column name `user_id` style, not `userId` in SQL and not Hungarian prefixes like `fk_user`.
- **Rationale:** SQL identifiers stay conventional; Prisma schema stays aligned with TypeScript and Prisma client ergonomics.

### API Naming Conventions

```typescript
// CORRECT: REST conventions
POST /api/auth/signup
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/session

// INCORRECT: Inconsistent casing/format
POST /api/Auth/signUp
POST /api/auth/log_in
```

**Rules:**
- **Endpoints:** All lowercase, hyphen-separated for multi-word (`/signup`, `/sign-up`)
- **Resource naming:** Plural for collections, singular for auth actions
- **Route parameters:** Use descriptive names (`:userId` not `:id` when ambiguous)
- **Query parameters:** camelCase in TypeScript, sent as-is (`?userId=123`)
- **No trailing slashes:** `/api/auth/login` not `/api/auth/login/`
- **Implementation:** Map URL segments under `app/api/.../` to **`route.ts`** files (one `route.ts` per leaf segment)

### TypeScript/React Code Naming Conventions

```typescript
// CORRECT: TypeScript/React conventions

// Components: PascalCase
export function SignupForm() { }
export function DashboardHeader() { }

// Files: Match component/export name
SignupForm.tsx
DashboardHeader.tsx
authUtils.ts
sessionHelpers.ts

// Functions: camelCase
function validatePassword(password: string) { }
function hashPassword(password: string) { }

// Variables: camelCase
const userId = session.userId;
const loginTimestamp = new Date().toISOString();

// Constants: UPPER_SNAKE_CASE
const MAX_LOGIN_ATTEMPTS = 5;
const SESSION_TIMEOUT = 1800;

// Types/Interfaces: PascalCase
interface SessionData { }
type AuthResponse = { };

// Enums: PascalCase (keys UPPER_SNAKE_CASE)
enum AuthStatus {
  AUTHENTICATED = 'authenticated',
  UNAUTHENTICATED = 'unauthenticated',
}
```

**Rules:**
- Component **modules:** name and file match: `SignupForm` → `SignupForm.tsx` (does not apply to `page.tsx`, `error.tsx`, etc.)
- Library / utility files: `camelCase.ts` (`authUtils.ts`, `sessionHelpers.ts`)
- Type definition files: camelCase with `.types.ts` suffix (`auth.types.ts`)
- No abbreviations unless universally understood (`auth` OK, `usr` NOT OK)

---

## Import & Dependency Rules

### Import Rules

```typescript
// CORRECT: Clear, organized imports (Next.js 15+: await cookies() in async server code)
// /lib/auth/session.ts
import { getIronSession } from 'iron-session';
import { cookies } from 'next/headers';
import type { SessionData } from '@/lib/types';

export async function getSession() {
  const cookieStore = await cookies();
  return await getIronSession<SessionData>(cookieStore, sessionOptions);
}
// sessionOptions: IronSessionOptions — define once per iron-session docs

// INCORRECT: Messy imports
import type { SessionData } from '../types';
import { cookies } from 'next/headers';
import { getIronSession } from 'iron-session';
```

**Import Rules:**
- **Absolute imports:** Use `@/` alias for project imports (`@/lib/auth/session`)
- **Relative imports:** Only for files in same directory (`./utils`)
- **Import order:** External packages → Next.js packages → Internal packages → Types
- **Type imports:** Use `import type` for types only

### Import Order Example

```typescript
// 1. External packages
import { z } from 'zod';
import bcrypt from 'bcryptjs';

// 2. Next.js packages
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

// 3. Internal packages
import { getSession } from '@/lib/auth/session';
import { hashPassword } from '@/lib/auth/password';

// 4. Types
import type { SessionData } from '@/lib/types';
import type { ApiResponse } from '@/lib/types';
```

---

## Code Organization Conventions

### Component Structure

**Co-locate component-only types and helpers; import Zod schemas from `/lib/validation/`.**

Canonical `z.object(...)` (and other Zod schema **definitions**) live **only** under `/lib/validation/`. UI modules never own a second copy of the same rules.

```typescript
// CORRECT: Schema from shared validation; types/helpers may live beside the component
// components/forms/SignupForm.tsx
import { signupSchema } from '@/lib/validation/auth.schemas';

export function SignupForm() {
  // Component implementation (e.g. useForm + zodResolver(signupSchema))
}
```

```typescript
// OPTIONAL: Thin barrel next to a feature — re-export only, no new Zod definitions
// components/forms/signup.schema.ts
export { signupSchema } from '@/lib/validation/auth.schemas';
```

If you use a barrel, keep it to **re-exports** so there is still a single definition in `/lib/validation/`. Prefer importing `@/lib/validation/...` directly unless a barrel noticeably simplifies a dense feature folder.

### Validation Schema Sharing

**Single source of truth for validation schemas:**

```typescript
// /lib/validation/auth.schemas.ts - SINGLE SOURCE OF TRUTH (definitions only here)
import { z } from 'zod';

export const signupSchema = z.object({
  username: z.string()
    .min(3, "Username must be at least 3 characters")
    .max(20, "Username must be at most 20 characters")
    .regex(/^[a-zA-Z0-9_]+$/, "Username can only contain letters, numbers, and underscores"),
  password: z.string()
    .min(8, "Password must be at least 8 characters"),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

// CORRECT: Import and reuse schemas
// In React Hook Form (client)
import { signupSchema } from '@/lib/validation/auth.schemas';
const form = useForm({ resolver: zodResolver(signupSchema) });

// In API route (server)
import { signupSchema } from '@/lib/validation/auth.schemas';
const validated = signupSchema.parse(await request.json());
```

**Rules:**
- **Single source of truth:** All Zod **definitions** live in `/lib/validation/` (files such as `auth.schemas.ts`, grouped by domain).
- **Never duplicate:** Do not redefine the same shape in a component-local file; use imports (or a re-export barrel that points at `/lib/validation/` only).
- **Client + Server:** Use the same exported schemas on both sides.
- **Error messages:** User-friendly, embedded in schema.

---

## Format Patterns

### JSON Field Naming

**camelCase in TypeScript/JSON:**

```typescript
// CORRECT: camelCase in TypeScript/JSON
{
  userId: "gabe",
  loginTimestamp: "2026-01-17T10:30:00.000Z",
  isLoggedIn: true
}

// INCORRECT: snake_case in JSON (only use in database)
{
  user_id: "gabe",
  login_timestamp: "2026-01-17T10:30:00.000Z"
}
```

**Rule:** JSON field names use camelCase (JavaScript/TypeScript convention), even though database uses snake_case. Transform at the boundary.

### Date/Time Formats

**Different formats for different layers:**

```typescript
// Database layer (Prisma): e.g. createdAt DateTime @default(now()) @map("created_at")
// SQL column is snake_case; type is DateTime (or Int + @db.Integer for Unix time if you standardize on that)

// API layer (JSON responses): ISO 8601 strings
{
  success: true,
  data: {
    userId: "gabe",
    loginTimestamp: "2026-01-17T10:30:00.000Z"  // ISO string
  }
}

// UI layer (React components): Formatted for display
<p>Logged in: {new Date(loginTimestamp).toLocaleString()}</p>
// Displays: "1/17/2026, 10:30:00 AM"
```

**Rules:**
- **Database:** Integer Unix timestamps (or native SQL `timestamp` types) per schema—normalize at the boundary.
- **API/JSON, session payloads (e.g. iron-session), and client state:** **ISO 8601 strings** (`"2026-01-17T10:30:00.000Z"`)—this is the default for JSON and the most common choice in TypeScript web apps.
- **UI:** Parse ISO strings with `new Date(isoString)` then format with `toLocaleString()` or a date library.
- **Never mix formats within a layer:** Transform only at boundaries (DB ↔ app ↔ wire).

---

## Anti-Patterns to Avoid

```prisma
// DON'T: camelCase column names in the database (omit @map to snake_case)
model Account {
  id     Int    @id @default(autoincrement())
  userId String // Wrong: physical column should be user_id
  @@map("accounts")
}
```

```typescript
// DON'T: Duplicate validation schemas
const schema = z.object({...});  // Should import from schemas file

// DON'T: Use relative imports across directories
import { getSession } from '../../lib/auth/session';  // Use @/ alias

// DON'T: Inconsistent file naming
export function SignupForm() { }  // Component
// File: signup-form.tsx  // Wrong! Should be SignupForm.tsx

// DON'T: Rename Next.js reserved files
// error.tsx → Error.tsx  // Wrong — breaks the App Router convention

// DON'T: Mix naming conventions
const USER_ID = "gabe";  // Wrong: should be camelCase for variables
const userId = "gabe";  // Correct
```

---

## Enforcement Guidelines

**All AI Agents MUST:**

1. **Follow naming conventions** - snake_case (DB); reserved `app/` filenames per Next.js; PascalCase for your component modules; camelCase for `lib/` utilities
2. **Import validation schemas** - Never duplicate Zod schemas
3. **Follow project structure** - Components, lib, app directories as specified
4. **Use absolute imports** - `@/` prefix for all project imports
5. **Co-locate tests** - Page tests in a `_tests/` private folder beside the route (not a URL segment)
6. **Match file names to exports** - For your components, `SignupForm` → `SignupForm.tsx` (not for `page.tsx`, `error.tsx`, `route.ts`, etc.)

**Pattern Enforcement:**

- **Type checking:** TypeScript will catch type mismatches
- **Code review:** Verify naming conventions and structure during implementation
- **Testing:** Ensure conventions are followed
- **Linting:** ESLint enforces import order and naming patterns

---

## Testing Conventions

### Test File Naming

- Unit tests: `*.test.ts` or `*.test.tsx`
- Component tests: `ComponentName.test.tsx`
- Page tests: Co-located in `app/[route]/_tests/PageName.test.tsx` (leading `_` excludes the folder from routing, same pattern as `_components/`)
- E2E tests: `tests/e2e/*.spec.ts`

### Test Organization

```
app/
  profile/
    page.tsx
    _tests/
      ProfilePage.test.tsx  # Private folder (excluded from routing)

tests/
  e2e/
    login.spec.ts  # E2E user flow tests
  unit/
    utils.test.ts  # Unit tests for utilities
```

---

## Documentation Conventions

### Code Comments

- Use JSDoc for public APIs
- Explain "why" not "what" in comments
- Keep comments up-to-date with code changes

### Type Documentation

```typescript
/**
 * Session data structure for iron-session.
 *
 * @property userId - Unique user identifier
 * @property loginTimestamp - Login time as ISO 8601 string (e.g. `new Date().toISOString()`)
 * @property isLoggedIn - Authentication status
 */
export interface SessionData {
  userId: string;
  loginTimestamp: string;
  isLoggedIn: boolean;
}
```

---

## Resources

- [Architecture & NFRs](./architecture.md) — stack, skills compliance, performance and release gates
- [Next.js Best Practices](@.agents/skills/next-best-practices/) — agent skill for App Router implementation
- [TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
- [React Naming Conventions](https://react.dev/learn/describing-the-ui#naming-components)
- [Next.js File Conventions](https://nextjs.org/docs/app/building-your-application/routing)
