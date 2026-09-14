# Contributing

For a scientific question, start with the [question index](docs/DIALOGUE_QUESTION_MAP.md). For a reproducibility problem, follow the [reproduction guide](docs/REPRODUCTION.md) and report the commit, command, Python environment, expected result and observed result. Keep credentials and personal information out of reports and logs.

Submit a focused pull request for a correction. Explain its reason, affected claim or file, and the checks you ran. Follow the [editorial policy](docs/EDITORIAL_POLICY.md). A documentation correction should preserve scientific qualifications and attribution. Changes to numerical data, methods, accepted figures or scientific conclusions require explicit author review and their own evidence; do not overwrite archived records as part of a prose edit.

Use the checks appropriate to the change from the [reproduction guide](docs/REPRODUCTION.md#integrity). For reader documentation, also run `python scripts/check_reader_docs.py --self-test` and `python scripts/check_markdown_math.py --self-test`. These check links, anchors and portable math source conventions; they do not certify live GitHub rendering. A report does not require rerunning a large simulation campaign.

Submit original contributions under the [license applicable to the material](LICENSE_STATUS.md): MIT for software and executable examples, CC BY 4.0 for research documentation, data and figures. Include only material you have permission to contribute and identify any third-party source and its terms. Discuss any different terms before inclusion. This page does not introduce a copyright assignment or contributor license agreement.

[Next: reproduction guide](docs/REPRODUCTION.md) · [Return to README](README.md)
