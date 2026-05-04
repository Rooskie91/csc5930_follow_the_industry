# Follow the Industry

A Project by:  Christopher Getzie
For class:     CSC 5930 - 002: Network Science
Professor:     Dr. Maurício Gruppi

Lobbying-contribution network analysis:
    A bipartite Industry <-> Legislator graph built from PAC-to-candidate contribution data

## Project Descritpion

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

## Create Vitrual Envionment

    python -m venv .venv

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