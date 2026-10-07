---
name: research-company
description: >
  Research a target company by navigating and reviewing the
  company's website, extract key business information, and use an LLM to produce
  a structured summary in templates/summary.md. Use when the user asks to
  research, profile, summarize, or analyze a company from its website.
---

# Research Company

## When To Use

Use this skill when the user provides a company name, domain, or website URL and asks for a company summary, company research, business profile, or structured findings.

## Inputs

- Target company name or website URL.
- Any user-provided focus areas, such as products, market, customers, pricing, leadership, or positioning.

If the user gives only a company name, identify the official website before scraping. If there are multiple plausible companies, ask a brief clarifying question.

## Workflow

1. Open the official company website. Prefer the homepage, then inspect likely high-signal pages such as About, Products, Services, Solutions, Customers, Pricing, Blog, Careers, Contact, and Terms/Privacy when available.

2. Extract relevant page text and metadata. Capture concise evidence for:
   - What the company does.
   - Primary products or services.
   - Target customers, industries, or use cases.
   - Differentiators, positioning, or claims.
   - Company location, leadership, funding, or team details if present on the site.
   - Notable calls to action, pricing signals, or contact channels.

3. Use an LLM to synthesize the gathered material into neutral, factual language. Prioritize information directly supported by the website and do not invent missing facts.

4. Read `templates/summary.md` and produce the final response in that exact structure:
   - Replace every placeholder with concise, website-supported content.
   - Use `Not found on the website` for fields that cannot be supported by available website content.
   - Keep `<EXECUTIVE_SUMMARY>` to 2-4 sentences.
   - Keep `<COMPANY_SUMMARY>` to one concise paragraph explaining what the company does and the most important supporting details from the website.
   - Use the caveats section for ambiguity, sparse evidence, inaccessible pages, or analyst inference.

## Quality Bar

- Cite the company website URL in the summary text when useful.
- Keep the summary concise and avoid raw scraped dumps.
- Separate observed facts from inference.
- Mention uncertainty when the website is sparse, inaccessible, or ambiguous.
- Do not use unrelated sources unless the user asks for broader research.

## Edge Cases

- If the website is inaccessible or blocks retrieval, explain the limitation and summarize only accessible content.
- If the site is not in English, translate only enough to produce the requested summary and state that the source site was in another language.
- If the website has no clear company description, report that clearly rather than guessing.
