# 🛠️ Local Gov Planning: Tools

## 🤖 Large Language Models

Large Language Models (LLMs) can provide valuable capabilities for local government planning applications. Some common providers include:

| Provider | Links | Notes |
|------|-------|-------|
| **Azure OpenAI** | • [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/) | Requires Azure subscription and access approval |
| **AWS Bedrock** | • [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/) | Provides access to multiple models through AWS |
| **Anthropic Claude** | • [Anthropic API Documentation](https://docs.anthropic.com/en/api/getting-started) | Offers various Claude models through API access |

> **Note:** The LLM examples and access instructions in this repository were specific to a past hackathon event. You will need to set up your own access credentials to use these services.

## ✨ Large Language Model Capabilities

Large Language Models (LLMs) offer a variety of capabilities that can enhance planning applications:

| Capability | Description | Potential Planning Applications |
|------------|-------------|--------------------------------|
| **📄 Document Processing** | LLMs can extract information from PDFs, forms, and scanned documents, converting unstructured data to structured formats | • Digitizing historical planning records<br>• Automating planning application intake<br>• Extracting key metrics from lengthy policy documents |
| **🎙️ Transcription & Analysis** | Models can transcribe audio from meetings and consultations, then analyze the content for key themes | • Making public planning meetings more accessible<br>• Identifying common concerns in community consultations<br>• Creating searchable archives of planning discussions |
| **✅ Document Verification & Assessment** | LLMs can cross-reference information across multiple sources to verify accuracy and consistency, and evaluate documents against predefined criteria, standards, or checklists to ensure compliance | • Validating planning applications against local policies<br>• Checking infrastructure capacity reports<br>• Ensuring housing forecasts align with demographic data<br>• Screening planning applications for completeness<br>• Assessing development proposals against sustainability criteria<br>• Checking housing designs against accessibility standards |
| **💬 Document Chat & Search** | LLMs can allow natural language conversations with document collections, enabling intuitive information retrieval | • Creating searchable planning policy assistants<br>• Enabling planners to query historical application databases<br>• Helping citizens navigate complex planning documentation |
| **📊 Consultation Analysis** | LLMs can process large volumes of public consultation responses to identify themes, sentiment, and key issues as well as redacting sensitive information | • Summarizing feedback from community engagement events<br>• Identifying recurring concerns across multiple consultations<br>• Categorizing stakeholder priorities for planning decisions<br>• Tracking sentiment changes over multiple consultation phases |
| **🔄 Multimodal Reasoning** | Advanced models can go beyond just across text to use images and data to solve complex problems | • Balancing housing needs with infrastructure constraints<br>• Visualizing planning scenarios for public engagement<br>• Predicting impacts of development on local communities |
| **👁️ Visual Understanding** | Modern LLMs like Claude and Gemini can analyze images, identify objects, and understand spatial relationships such as where items are within images | • Automated review of planning application drawings<br>• Identifying non-compliant elements in building designs<br>• Analyzing satellite imagery for land use changes |
| **💻 Code Generation** | LLMs can write code to automate workflows, analyze data, and create interactive tools | • Building custom planning process automation tools<br>• Creating data pipelines for housing demand forecasting<br>• Developing interactive public engagement platforms |
| **🧩 Reasoning & Planning** | LLMs can break down complex problems into logical steps, identify dependencies, and create structured plans | • Developing phased implementation strategies for housing projects<br>• Identifying critical path dependencies in infrastructure planning<br>• Creating decision trees for planning application assessment |
| **🔧 Tool Use** | LLMs can interact with external tools like calculators, databases, and APIs to extend their capabilities beyond text generation | • Querying planning databases to retrieve relevant precedents<br>• Performing complex calculations for infrastructure capacity assessments<br>• Accessing GIS systems to analyze spatial data for development proposals |
| **🔍 Research & Information Retrieval** | Models can use search through documents, websites, and databases to find relevant information and synthesize findings | • Gathering precedents from similar planning cases<br>• Researching best practices in sustainable urban development<br>• Compiling evidence for policy recommendations |

## 🧠 Other AI Tools

| Tool               | Links                                                                 | Notes                                      |
|--------------------|-----------------------------------------------------------------------|--------------------------------------------|
| **Model Context Protocol** | [Documentation](https://www.anthropic.com/news/model-context-protocol) | Framework for allowing LLMs to use data and tools |
| **Segment Anything** | [Website](https://segment-anything.com/)<br>[GitHub](https://github.com/facebookresearch/segment-anything) | Meta AI model for image segmentation tasks |
| **Whisper**        | [GitHub](https://github.com/openai/whisper)                             | OpenAI model for speech-to-text transcription |
| **YOLO**           | [Website](https://pjreddie.com/darknet/yolo/)<br>[GitHub (v8)](https://github.com/ultralytics/ultralytics) | Real-time object detection models         |
| **spaCy**          | [Website](https://spacy.io/)                                            | Library for advanced Natural Language Processing (NLP) |
| **Raster Vision**  | [Website](https://rastervision.io/)<br>[GitHub](https://github.com/raster-vision/raster-vision) | Framework for deep learning on satellite/aerial imagery |
| **Fairlearn**      | [Website](https://fairlearn.org/)<br>[GitHub](https://github.com/fairlearn/fairlearn)       | Toolkit to assess and improve AI fairness |

## 🧰 Other Tools

| Tool                                              | Links                                                               | Notes                                                                    |
|---------------------------------------------------|---------------------------------------------------------------------|--------------------------------------------------------------------------|
| **Prophet**                                       | [GitHub](https://github.com/facebook/prophet)                               | Fast time‑series forecasting with seasonality & holiday effects          |
| **LightGBM**                                      | [Documentation](https://lightgbm.readthedocs.io/)                                | Gradient‑boosted decision trees ‑ handles sparse geo‑demographic features |
| **docTR**                                         | [Documentation](https://mindee.github.io/doctr/)                                 | Deep‑learning OCR for scanned PDFs; returns token coordinates            |
| **LlamaIndex**                                    | [GitHub](https://github.com/run-llama/llama_index)                          | Drop‑in vector‑database + retrieval for RAG pipelines                    |
| **LangChain**                                     | [Documentation](https://python.langchain.com/)                                   | Orchestration of multi‑step LLM workflows, agents & tools                |
| **TfL Unified API**                               | [API Documentation](https://api.tfl.gov.uk/)                                         | Live transport capacity, routes, disruptions for London                  |
| **Environment Agency Hydrology & Flood Monitoring API** | [API Reference](https://environment.data.gov.uk/flood-monitoring/doc/reference)    | River flow, rainfall, flood alerts & groundwater levels                  |
| **OpenStreetMap (OSM)**                           | [Website](https://www.openstreetmap.org/)                                  | Free, editable map data (roads, buildings, land use) used by many tools  |
| **OSRM**                                          | [Project Website](http://project-osrm.org/)                                        | Open Source Routing Machine using OpenStreetMap data                     |
| **Nominatim**                                     | [Website](https://nominatim.org/)                                          | Geocoding and reverse geocoding service for OpenStreetMap data           |
| **Open Infrastructure Map**                       | [Website](https://openinframap.org/)                                       | Visualisation of power lines, telecoms & pipelines using OSM data        |
| **Overpass Turbo**                                | [Website](https://overpass-turbo.eu/)                                      | Web-based data mining tool for OpenStreetMap                             |
| **UrbanSim**                                      | [GitHub](https://github.com/UDST/urbansim)                                | Open‑source land‑use & transport interaction simulation                  |
| **CitizenLab (Open‑source core)**                 | [GitHub](https://github.com/CitizenLabDotCo/citizenlab-oss)                                          | Survey & idea‑board platform with GraphQL/REST API for engagement        |
| **OR‑Tools**                                      | [Documentation](https://developers.google.com/optimization)                      | Google's open-source optimisation toolkit (routing, assignment, scheduling) |

