# Follow the Industry

A Project by:  Christopher Getzie
For class:     CSC 5930 - 002: Network Science
Professor:     Dr. Maurício Gruppi

Lobbying-contribution network analysis:
    A bipartite Industry <-> Legislator graph built from PAC-to-candidate contribution data

## Project Descritpion

### NOTE: OpenSecrets ToS restricts me from republishing their data. Data is available upon request. 

A network science analysis of U.S. campaign-finance flows for CSC 5930 - 002 
(Network Science). Industries are linked to federal legislators via
PAC contributions from the 2022 cycle (117th Congress), and the
resulting bipartite network is analyzed for scale-free structure,
centrality, community structure, assortativity, and influence-spreading
dynamics.

## Data Sources:
    OpenSecrets [https://www.opensecrets.org/bulk-data/downloads]
    Members of the United States Congress [https://github.com/unitedstates/congress-legislators]
    Vote View UCLA [https://voteview.com/data]

## Contents

FOLLOW_THE_INDUSTRY/
    analysis.ipynb                           -> Where the magic (i.e. netowrk analysis) happens
    data_prep.ipynb                          -> First, we massage the data until it is relxed enough to cooperat
    helpers.py                               -> Shared utilites from class labs, modified for this project
    README.md                                -> You're looking at it (so meta)!
    data/
        cands20.txt                          -> OpenSecrets: Campaign Finance Data, 2020 Cycle Tables
        cands22.txt                          -> OpenSecrets: Campaign Finance Data, 2022 Cycle Tables
        cmtes20.txt                          -> OpenSecrets: Campaign Finance Data, 2020 Cycle Tables
        cmtes22.txt                          -> OpenSecrets: Campaign Finance Data, 2022 Cycle Tables
        committee-membership-current.yaml    -> Members of the United States Congress: Committee assignments
        committees-current.yaml              -> Members of the United States Congress: Committee assignments
        CRP_Categories.txt                   -> Open Secrets: Reference Data (a tab-delimited text file of Industry codes)
        CRP_IDs.xls                          -> Open Secrets: Reference Data (an Excel spreadsheet containing pages for candidate IDs, industry codes, expenditure codes and Congressional Cmtes)
        HS117_members.csv                    -> Vote View UCLA: Numerical ideology scores (-1 = most liberal, +1 = most conservative) for every legislator
        legislators-current.yaml             -> Members of the United States Congress: for sitting members during the 117th Congress
        legislators-historical.yaml          -> Members of the United States Congress: for sitting members during the 117th Congress who may have left office
        pacs20.txt                           -> OpenSecrets: Campaign Finance Data, 2020 Cycle Tables
        pacs22.txt                           -> OpenSecrets: Campaign Finance Data, 2022 Cycle Tables

## Get Dependencies

    pip install jupyter notebook ipykernel networkx pandas matplotlib numpy scipy pyyaml powerlaw openpyxl

## Real-data benchmarks (2022 cycle)

- **Raw**: 758,125 PAC-to-candidate transactions
- **After OpenSecrets filters** (drop Z9*/Z4*, keep DI=D, drop refunds):
  227,605 valid contributions worth **$496.5M**
- **Bipartite graph**: 390 industries × 1,485 legislators, 54,991 edges
- **Power-law fit** on the legislator projection: γ ≈ 2.89
- **Communities**: 2 large communities at 98% party purity — textbook
  polarization signature
- **Party assortativity**: r = 0.23
- **Ideology assortativity (DW-NOMINATE)**: r = 0.23
- **Degree assortativity**: r = -0.28

## AI Usage Disclosure (Course: CSC 5930 — Network Science)

**Tool(s) used:** Claude (Anthropic)

**Purpose:**
- Translating the OpenSecrets bulk-data schema into a working pandas loader (column names, quoting conventions, filter rules from the User's Guide)
- Debugging Python errors during development (missing return statement, scipy.stats.moment central-vs-raw second moment bug, pandas KeyError on a renamed column)
- Drafting the synthetic-data generator used for end-to-end pipeline testing before real OpenSecrets data was downloaded.
- Writing setup instructions (VS Code + Jupyter without virtualenv, GitHub publishing workflow)

**Sample prompts:**
- "Give me specific instructions on how to get the required data for the 117th congress from OpenSecrets."
- "I get this error: TypeError: cannot unpack non-iterable NoneType object — what's wrong? Give me step by step indsturciton on how to fix it and explain the process to me."
- "Is there anything wrong with this part of my helper code? I'm getting weird results when I run this..."
- "Can you debug the code that will generate centrality.png?"
- "The little white box that displays gamma shows up behind the legend. Give me specific instructions on how to make that show up in the middle? Don't write code, only explain how to fix this problem."

**Verification:**
- Every code block produced by the AI was run end-to-end in my own VS Code/Jupyter environment against the real OpenSecrets data; only code that produced sensible, replicable outputs was kept.
- Numerical claims (power-law exponent γ ≈ 2.89, party assortativity r = 0.23, $496.5M total contribution dollars, 98% community-party purity) were verified by inspecting the notebook outputs directly rather than trusting figures cited in conversation.
- The OpenSecrets User's Guide filter rules (drop `Z9*`/`Z4*` `RealCode` values, keep only `DI = 'D'`) were independently confirmed against the official OpenSecrets data documentation before being added to the pipeline.
- One AI-suggested implementation was identified as incorrect and rewritten: the `scipy.stats.moment(degrees, 2)` call returned the *central* second moment (variance) rather than the raw `<k²>` needed by the epidemic-threshold formula `λ_c = <k>/<k²>`. Replaced with `np.mean(degrees**2)` after verifying the issue numerically.
- All interpretive claims about the network (e.g., that party-aligned community structure mirrors the donor-class echo chamber observed in political-science literature) are my own.

**Authorship:** I confirm the submitted work reflects my own understanding and writing.