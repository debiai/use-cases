# Welding Quality Detection - Confiance.AI Challenge - Metadata DebiAI analysis

<div style="text-align: center;">
    <img src="images/MetadataAnalysis.png" alt="Metadata AnalysisPartners" width="800" style="border-radius: 15px; border: 1px solid;"/>
</div>

## [The challenge](https://confianceai.github.io/Welding-Quality-Detection-Challenge/)

The Welding Quality Detection challenge is organized by the Confiance.ai community and IRT SystemX, with the support of Renault Group.

<div style="text-align: center;">
    <img src="images/partners.png" alt="Partners" width="600" style="border-radius: 15px;"/>
</div>

It is part of the European Trustworthy AI Foundation of the Confiance.ai community, positioned as the driving force behind an ambitious European strategy for industrial and responsible AI. Its aim is to propel Europe to the forefront of innovation in trustworthy AI by establishing Confiance.ai's methodologies and tools as an international benchmark.

<div style="text-align: center;">
    <a href="https://confianceai.github.io/Welding-Quality-Detection-Challenge/">
        Welding Quality Detection Challenge website
    </a>
    /
    <a href="https://confianceai.github.io/Welding-Quality-Detection-Challenge/docs/dataset/">
        The dataset page
    </a>
</div>

## [DebiAI](https://debiai.irt-systemx.fr/)

DebiAI is an open-source web app designed to simplify machine learning development through data analysis, bias/error identification, model performance comparison, and fast visualization creation / live exploration.

<div style="text-align: center;">
    <a href="https://debiai.irt-systemx.fr/">
        DebiAI website, documentation and tutorials
    </a>
</div>

## Analyzing the Welding Quality Detection dataset with DebiAI

This repository contains a Data-provider ([learn more about DebiAI Data-providers](https://debiai.irt-systemx.fr/dataInsertion/dataProviders/)) for the Welding Detection Challenge Dataset Metadata: [data_provider.py](data_provider.py).

The Data-provider is used to provide the dataset to DebiAI, allowing you to analyze the dataset and identify biases and errors.

### DebiAI Data-provider python module

This Data-provider uses the `debiai_data_provider` python module to provide the dataset. Learn more about the Python module [here](https://github.com/debiai/easy-data-provider).

### Setup

Run the Data-provider:

```bash
pip install -r requirements.txt
python data_provider.py
```

Expect the following output:

```bash
% python data_provider.py

Loading data from parquet file
╭──────────────────────── DebiAI Data Provider v1.0.2 ─────────────────────────╮
│ The Data Provider is being started...                                        │
│                                                                              │
│ API Server: http://0.0.0.0:8000                                              │
│ Number of Projects: 1                                                        │
╰──────────────────────────────────────────────────────────────────────────────╯
Loading data from parquet file
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Welding quality… ┃ Created: 2025-03-20                                       ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│       Structure: │                                                           │
│            class │ auto context                                              │
│        timestamp │ auto context                                              │
│    welding-seams │ auto context                                              │
│   labelling_type │ auto context                                              │
│       resolution │ auto context                                              │
│             path │ auto context                                              │
│           sha256 │ auto context                                              │
│     storage_type │ auto context                                              │
│      data_origin │ auto context                                              │
│       blur_level │ auto context                                              │
│       blur_class │ auto context                                              │
│ luminosity_level │ auto context                                              │
│    external_path │ auto context                                              │
│                  │                                                           │
│      NB samples: │ 22753                                                     │
│                  │                                                           │
└──────────────────┴───────────────────────────────────────────────────────────┘
INFO:     Started server process [22314]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

In a new process, start DebiAI with the the url of the Data-provider:

```bash
debiai-gui start -dp http://localhost:8000
```

DebiAI will start and open a new tab in your browser with the DebiAI home page. The project will be available to be analyzed.

<div style="text-align: center;">
    <img src="images/parallel_coordinates.png" alt="Parallel Coordinates" style="border-radius: 15px; border: 1px solid;"/>
</div>

Check our [DebiAI Dashboard Guide](https://debiai.irt-systemx.fr/dashboard/), the [Woodscape tutorial](../woodscape/README.md) is also a good way to learn how to use DebiAI.

## Support

[Contact](https://debiai.irt-systemx.fr/meta/contact.html#contact)
