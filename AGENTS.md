\## Task Completion Requirements



\- Environment/configuration health check and static type checking  must pass before considering tasks completed.

&#x20; - run code style/lint checks must also pass.

&#x20; - run python achecker.py must also pass.



\## Project Snapshot



Provider-Evo is a minimal runtime skeleton for running multi-platform AI provider adapters behind a unified aiohttp API.



This repository is a VERY EARLY WIP. Proposing sweeping changes that improve long-term maintainability is encouraged.



\## Core Priorities



1\. Performance first.

2\. Reliability first.

3\. Keep behavior predictable under load and during failures (stability assurance mechanism for long-lived connections and streaming services).



If a tradeoff is required, choose correctness and robustness over short-term convenience.



