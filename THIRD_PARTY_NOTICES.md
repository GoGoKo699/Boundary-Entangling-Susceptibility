# Third-party material

The [repository license scope](LICENSE_STATUS.md) concerns original project material. It does not change the terms of dependencies, font software or cited works.

## Embedded fonts

The 19 tracked PDFs inspected during release preparation contain embedded STIXGeneral Regular/Italic subsets. This includes the six accepted numerical panels and historical, audit and repair redraws. No standalone font files are tracked.

Matplotlib distributes these STIX fonts with the [STIX notice and SIL Open Font License 1.1](https://github.com/matplotlib/matplotlib/blob/v3.10.8/lib/matplotlib/mpl-data/fonts/ttf/LICENSE_STIX). That source identifies the STI Pub Companies and portions attributed to MicroPress and Elsevier. The requirement to keep font software under the OFL does not require documents created using those fonts to use the OFL. The CC BY 4.0 scope covers original figure content and does not relicense embedded font software. The linked version is the upstream notice checked for this preparation, not a claim that every historical PDF used that Matplotlib version.

## Runtime dependencies

The Python packages declared in [package metadata](pyproject.toml), [requirements](requirements.txt) and the [reproduction environment](requirements-reproducible.txt) are installed separately. Their licenses and notices remain with their distributions. This checkout does not vendor their source. A future release that bundles dependencies or font files must retain the applicable notices with those components.

## Research attribution and external assets

[Related work](docs/RELATED_WORK.md) is the authoritative home for primary scientific attribution. The selected review is linked as background; its PDF, pages and figures are not distributed here. Citation establishes intellectual attribution, not permission to reproduce an external asset.

The stored records have a [source-member manifest](data/record_bundle_manifest.json). It records origins and byte identities, not copyright ownership. The owner confirmed authority to license the included original study records, software, prose and artwork when approving the [adopted scope](LICENSE_STATUS.md). Actual editable external composite-schematic sources remain unavailable and have not been cleared for distribution. See [availability limits](docs/REPRODUCIBILITY_LIMITS.md).

[Next: public-release preparation](docs/PUBLIC_RELEASE.md) · [Return to README](README.md)
