# 💡 Local Gov Hack: Inspiration Pack

## ✨ Quick summary
The UK's emerging **PlanTech** stack already shows how open data + AI can upgrade local‑government planning: machine‑learning models sharpen housing‑demand forecasts, OCR and computer‑vision pipelines turn PDFs into structured planning data, NLP dashboards surface the signal in thousands of consultation comments, digital twins test the "how‑many‑homes‑before‑the‑pipes‑break?" question, and open‑source transport tools help design 15‑minute neighbourhoods. The resources below merge previous lists with new transportation & sustainability examples, deduplicated and grouped so teams can grab code, data or design patterns in seconds.

---

## 🏗️ Planning & Housing

### 🔮 Housing‑Demand Forecasting
| Resource | Link | Why it matters |
|---|---|---|
| **ONS ML House‑Price & Demand Prototype (XGBoost)** | [ONS Machine Learning House Price Model](https://www.ons.gov.uk/news/statementsandletters/machinelearninghousepricemodel) | Shows feature‑engineering & evaluation pipeline on UK transaction data—perfect template for LPA‑level demand models |
| **Predicting UK Housing Prices using ML** | [Article](https://www.researchgate.net/publication/379621960_Predicting_UK_Housing_Price_using_Machine_Learning_Algorithms/fulltext/661155082034097c54f9dbce/Predicting-UK-Housing-Price-using-Machine-Learning-Algorithms.pdf) | Benchmarks multiple regressors & discusses overfitting with UK economic covariates |
| **Street2Vec change‑detection (London, 15 M images)** | [arXiv Paper](https://arxiv.org/abs/2309.11354) | Self‑supervised model spots new housing supply from Street View—idea: plug into planning‑photo archives ([arxiv.org](https://arxiv.org/abs/2309.11354)) |
| **ONS Floor‑Area Admin Pilot** | [ONS Geography Methodology](https://www.ons.gov.uk/methodology/geography) | Adds missing floor‑area attributes that improve dwelling‑stock estimates |
| **Short‑Term UK Water‑Demand ML Forecast (2024)** | [ResearchGate Publication](https://www.researchgate.net/publication/350559345_Short-Term_Forecasting_of_Household_Water_Demand_in_the_UK_Using_an_Interpretable_Machine_Learning_Approach) | Example of interpretable tree model that links demand to infrastructure capacity ([ResearchGate](https://www.researchgate.net/publication/350559345_Short-Term_Forecasting_of_Household_Water_Demand_in_the_UK_Using_an_Interpretable_Machine_Learning_Approach)) |
| **Parliamentary POST note – Housing: demographic and environmental trends** | [Parliament Research Briefing](https://post.parliament.uk/housing-demographic-and-environmental-trends/) | How can the housing be adapted to an ageing population and to meet the challenge of climate change? |

### ⚙️ Planning‑Process Automation
| Resource | Link | Why it matters |
|---|---|---|
| **Extract - AI pipeline (DSIT/MHCLG)** | [Extract Project](https://ai.gov.uk/projects/extract/) | OCR + computer‑vision turns PDF plans into JSON in <40 s |
| **Turing DSG Mask‑RCNN for Planning Drawings** | [Turing Data Study Group](https://www.turing.ac.uk/collaborate-turing/data-study-groups/can-we-automate-uks-planning-system-using-ai) | Open dataset & code identify north arrows, floorplans etc. |
| **PlanX Planning Applications** | [PlanX](https://opendigitalplanning.org/planx) | Automating processes for submitting planning applications |
| **PlanTech market‑scan blog** | [Medium Article](https://medium.com/capital-enterprise/plantech-a-new-market-for-digital-planning-products-and-services-885678f9de89) | Maps commercial + open‑source APIs you can mash together ([Medium](https://medium.com/capital-enterprise/plantech-a-new-market-for-digital-planning-products-and-services-885678f9de89)) |

---

## 🗣️ Public & Citizen Engagement
| Resource | Link | Why it matters |
|---|---|---|
| **Commonplace "TrendsAI"** | [Commonplace Guide](https://www.commonplace.is/product-roadmap/commonplace-2.0-guide) | Map‑based consultation hub; NLP clusters sentiment & topics, exports via webhooks ([Commonplace](https://www.commonplace.is/product-roadmap/commonplace-2.0-guide)) |
| **Consult** | [Consult Project](https://ai.gov.uk/projects/consult/) | AI-powered tool to analyze and extract themes from public consultation responses |
| **ThemeFinder** | [GitHub Repository](https://github.com/i-dot-ai/themefinder) | Topic modelling Python package for analyzing survey responses and public consultations with LLM-powered theme identification |
| **Minute** | [Minute Project](https://ai.gov.uk/projects/minute/) | AI tool for automatically creating summaries of meeting minutes and highlighting action items |
| **MHCLG PropTech Innovation Fund (Prospectus + Case Studies)** | [PropTech Innovation Fund PDF](https://media.localdigital.gov.uk/uploads/2023/10/16171343/PropTech-Innovation-Fund-Prospectus-Round-4-.pdf) | User‑research findings, open schemas & funding for LPA pilots ([Local Digital](https://media.localdigital.gov.uk/uploads/2023/10/16171343/PropTech-Innovation-Fund-Prospectus-Round-4-.pdf)) |
| **Digital Planning Programme overview** | [Local Digital Planning Overview](https://www.localdigital.gov.uk/digital-planning/digital-planning-programme-overview/) | Summaries of real council pilots—"what worked / what bombed" insights ([Local Digital](https://www.localdigital.gov.uk/digital-planning/digital-planning-programme-overview/)) |

---

## 🏛️ Infrastructure & Capacity
| Resource | Link | Why it matters |
|---|---|---|
| **National Infrastructure Commission Progress Review 2024** | [NIC Assessment](https://nic.org.uk/studies-reports/national-infrastructure-assessment/) | Latest capacity gaps & target metrics across water, energy, digital |
| **Anglian Water Safe Smart Systems Digital Twin** | [Anglian Water Innovation](https://www.iotinsider.com/industries/industrial/lessons-from-anglian-waters-large-scale-digital-twin-deployment) | County‑scale twin streaming pipe‑flow data; open architecture diagram |
| **UKRI Environmental‑Science Digital‑Twin Programme** | [UKRI Digital Twins](https://www.ukri.org/news/digital-twin-projects-to-transform-environmental-science/) | Grants + open Python tooling for scenario testing floods/droughts |

---

## 🚍 Transport & Active Travel
| Tool / Project | Link | Notes |
|---|---|---|
| **Network Planning Tool (Scotland)** | [NPT Scotland Manual](https://nptscot.github.io/manual/) | Web‑based planner estimates cycling potential street‑level; easy to fork ([NPT Scotland](https://nptscot.github.io/manual/)) |
| **ACTON / ActDev (CyIPT)** | [CyIPT Acton](https://cyipt.github.io/acton/) | R‑package + web UI assessing active‑travel options for new housing developments ([CyIPT](https://cyipt.github.io/acton/)) |
| **Active‑Travel Infrastructure Platform (ATIP)** | [ATIP GitHub](https://github.com/acteng/atip) | Open‑source map‑based sketcher & browser for walking/cycling schemes ([GitHub](https://github.com/acteng/atip)) |
| **A/B Street toolkit** | [A/B Street Documentation](https://a-b-street.github.io/docs/software/ungap_the_map/tech_details.html) | Rust‑based interactive transport digital‑twin; includes 15‑minute‑city analyser ([A/B Street](https://a-b-street.github.io/docs/software/ungap_the_map/tech_details.html)) |
| **15‑Minute Neighbourhood explorer** | [15-Minute Explorer](https://a-b-street.github.io/15m/#1/0/0) | Quick visual demo built on A/B Street engine (policy storytelling) ([A/B Street](https://a-b-street.github.io/docs/software/ungap_the_map/tech_details.html)) |

---

## 🌱 Sustainability & Carbon
| Tool | Link | Why it matters |
|---|---|---|
| **Place‑Based Carbon Calculator** | [Carbon Place](https://www.carbon.place) | Maps per‑person emissions—including housing & transport—down to LSOA; open data licence ([Carbon Place](https://www.carbon.place/legacy/data/)) |

---
