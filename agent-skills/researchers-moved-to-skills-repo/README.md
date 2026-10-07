# researchers

for research skills, yet to be collected and compiled.

See example outputs: `research-company-output`

## research-website

A simple agent skill to research a topic from the provided website(s) and create a summary 
using the pre-created template.

**dependency:** none

NOTE: based on testings, the "agent-browser" skill is not very useful here
because the agent (i.e., cursor, antigravity, etc.) has their own browsing capability now.
So, the "agent-browser" dependency was dropped.

## research-company

A simple agent skill to research a company website and create a summary 
using the pre-created template.

**dependency:** none

NOTE: based on testings, the "agent-browser" skill is not very useful here
because the agent (i.e., cursor, antigravity, etc.) has their own browsing capability now.
So, the "agent-browser" dependency was dropped.

*DEPRACATED:* Utilize the agent-browser to programmatically scrape the target company website, extract pertinent information, and process the data using an LLM to produce a structured summary aligned with the defined template format.

### Test findings

- Cursor - the "agent-browser" has NOT been installed; the entire process ran smoothly
  generating the summary report; see `research-company-output/cursor_lumentum.md`

- Cursor - the "agent-browser" has been installed globally; the entire process ran smoothly
  generating the summary report; see `research-company-output/

- **Antigravity - Open Editor**, 
  - can't install "agent-browser" if it's not there; the reason is because
    it uses PowerShell as the default shell on Windows, and PowerShell's default execution policy
    on Windows is set to Restricted, which prevents the execution of PowerShell scripts (like npm.ps1).
  - NO resolution, other than pre-install "agent-browser" globally. 

- **Antigravity - Agent Manager**, "agent-browser" was not installed; same behavior as "Antigravity - Open Editor".

- Antigravity - Agent Manager with "agent-browser" installed.
  - Ran very slow with many user approval.

- LOOKS LIKE without "agent-browser" BUT use the agent built-in browser 
  wrked better; both for cursor and antigravity. 