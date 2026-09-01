# Luma Foundry — Modern IP Protection Roadmap Beyond Digital Watermarking

**Prepared by:** Operator A  
**Date:** 2026-08-28  
**Status:** Working implementation analysis; not formal legal advice. A qualified IP lawyer should review the final licence, registration strategy, contributor agreements, and enforcement process before commercial release.

> **Recommended principle:** Protect Luma Foundry with a layered evidence-and-delivery system. Do not rely on right-click blocking, JavaScript obfuscation, or any single watermark. The objective is to prove authorship, control commercial delivery, trace legitimate releases, and respond quickly when misuse occurs.

## Recommended safeguards

| Priority | Safeguard | Practical Luma Foundry implementation | Main value | Important limit |
|---|---|---|---|---|
| P0 | **Signed source and release history** | Give every product a release ID; create a Git tag tied to the live commit; sign the tag or release; generate `SHA256SUMS`; store the commit, artifact hash, build time, and operator in the release ledger. GitHub supports verified GPG, SSH, and S/MIME commit/tag signatures, while Sigstore can sign and verify software artifacts.[1] [2] | Creates a verifiable chain from source to delivered package. | Integrity evidence does not by itself establish legal ownership. |
| P0 | **Asset-rights register** | For every image, font, icon, illustration, video, texture, and audio file, record creator, source URL, licence, commercial/resale scope, attribution, purchase receipt or permission, checksum, and affected Product IDs. | Prevents accidental resale of an asset without sufficient rights. | A licence register is only as reliable as the underlying evidence. |
| P0 | **Contributor-rights records** | Require signed assignment, work-for-hire, or clearly scoped licence terms from designers, developers, photographers, and contractors before their work enters a commercial release. | Reduces ambiguity over who may commercialize each contribution. | The correct agreement depends on jurisdiction and working relationship. |
| P0 | **Buyer-specific licence manifest** | Each sale should create a non-personal `licence_id`, buyer or named-client reference, Product ID, release version/hash, permitted end-use, restrictions, included-assets list, issue date, and support boundary. Put a copy inside the download package. | Connects a legitimate buyer to an exact licensed release. | It does not prevent redistribution; it strengthens traceability and enforcement evidence. |
| P0 | **Controlled digital delivery** | Keep commercial packages private. After payment and order validation are eventually enabled, issue short-lived S3 presigned download URLs and retain a delivery log. AWS confirms presigned URLs give time-limited object access but behave as bearer tokens and must be protected.[3] | Avoids leaving permanent public ZIP links available for scraping. | Anyone who receives a valid URL during its lifetime may be able to use it. |
| P1 | **Per-buyer package fingerprint** | Insert the `licence_id`, Product ID, release hash, and issue timestamp into `LUMA-LICENCE.json`, package metadata, and documentation. Optionally vary harmless build metadata per delivery. Do not embed hidden personal data. | Helps identify which authorized package a leaked archive originated from. | Fingerprints can be removed; they are supporting evidence, not surveillance. |
| P1 | **Private-source access and least privilege** | Keep unreleased source, master assets, pricing logic, automation, and customer records private. Give collaborators role-based access only to the repositories and folders they need; revoke access after the engagement. WIPO notes that trade-secret treatment generally requires secrecy, limited access, and reasonable confidentiality measures.[4] | Protects valuable pre-release know-how and original master files. | Publicly disclosed information normally cannot remain a trade secret. |
| P1 | **NDA and confidentiality workflow** | Use confidentiality clauses before sharing unreleased designs, factory workflows, customer lists, source archives, or commercial strategy with contractors and partners. Maintain an access register and off-boarding checklist. | Supports the “reasonable measures” needed for confidential information. | An NDA cannot stop independent creation or every lawful form of reverse engineering. |
| P1 | **SPDX dependency and licence inventory** | Generate an SPDX Software Bill of Materials for each release and review package licences, copyrights, notices, and redistribution obligations. SPDX is an open ISO/IEC standard for representing software components and related licence information.[5] | Identifies third-party obligations before selling a template package. | An automated SBOM may miss copied snippets, fonts, or untracked media. |
| P1 | **Public-preview minimization** | Publish optimized preview renders rather than original master images. Keep editable design files, RAW media, source illustrations, and high-resolution masters behind restricted access. WIPO identifies lower-quality public versions and access controls as possible digital-work safeguards.[6] | Reduces the commercial usefulness of copied public assets while preserving browsing quality. | Screenshots and page-source inspection remain possible. |
| P1 | **Production source-map discipline** | Do not publish production source maps unless debugging needs justify them. Keep secrets, private endpoints, purchase logic, and internal comments out of client bundles entirely. | Reduces accidental leakage of internal implementation detail. | Minification and unavailable source maps are not copyright protection. Browser-delivered code remains observable. |
| P2 | **Trademark and domain protection** | Search the relevant trademark registers, then consider registering `Luma Foundry` and distinctive brand marks in the jurisdictions and classes that match the business. Monitor confusingly similar domains and marketplace seller names. WIPO explains that trademark registration can reinforce exclusive brand rights within its applicable territory and classes.[7] | Protects the brand identity customers use to identify the seller. | Trademark does not grant ownership over generic layout ideas or all template code. |
| P2 | **Evidence-led monitoring** | Schedule periodic reverse-image checks, marketplace searches, code-search queries for distinctive non-secret strings, and domain/brand monitoring. Preserve URLs, timestamps, screenshots, downloads, hashes, and comparison notes before contacting a platform or suspected copier. | Shortens discovery and creates a reliable incident record. | Similarity alone does not prove infringement; legal assessment may be required. |
| P2 | **Abuse controls for automated scraping** | Use rate limiting, CDN/WAF bot controls, anomaly alerts, and caching rules against abusive automated collection while allowing normal visitors and accessibility tools. | Limits high-volume extraction and infrastructure abuse. | `robots.txt` is voluntary, and bot controls do not create IP rights. |
| P2 | **Enforcement playbook** | Define a review sequence: preserve evidence, verify ownership and licence scope, assess substantial similarity and permitted use, send a proportionate notice, use platform takedown processes where appropriate, and escalate to counsel for contested cases. | Makes responses faster, consistent, and less emotional. | Incorrect notices can create legal and reputational risk. |

## The strongest Luma Foundry package architecture

Each commercial download should eventually contain the following release files:

| File | Purpose |
|---|---|
| `README.md` | Setup, customization, support boundary, and update instructions. |
| `LICENCE.pdf` or `LICENCE.md` | Human-readable commercial terms reviewed for the target jurisdiction. |
| `LUMA-LICENCE.json` | Buyer licence ID, Product ID, release version, issue time, and non-personal delivery fingerprint. |
| `RELEASE-MANIFEST.json` | Commit SHA, build ID, artifact checksums, included-file inventory, and toolchain version. |
| `SHA256SUMS` | Integrity hashes for the released files. |
| `SBOM.spdx.json` | Dependency, copyright, and licence inventory in SPDX format. |
| `THIRD_PARTY_NOTICES.md` | Required third-party attributions and licence notices. |
| `ASSET-REGISTER.csv` | Asset sources, creators, permissions, resale scope, and attribution rules. |

The public Google Sheet may hold **product-level release fields**, but buyer identity, order history, download access, and enforcement evidence should remain in the protected database or restricted storage rather than the collaboration sheet.

## Recommended release data model

| Field | Storage | Purpose |
|---|---|---|
| `product_id` | Master Sheet + database | Stable product identity. |
| `release_version` | Master Sheet + database | Human-readable release version. |
| `git_commit_sha` | Master Sheet + release manifest | Immutable source reference. |
| `signed_release_status` | Master Sheet | Whether signature verification actually passed. |
| `artifact_sha256` | Release manifest + database | Delivered-package integrity. |
| `asset_register_url` | Restricted evidence workspace | Source and licence evidence. |
| `sbom_url` | Restricted evidence workspace | Dependency and licence inventory. |
| `commercial_clearance_status` | Master Sheet | `pending`, `reviewed`, or owner-approved final state; never inferred from a live preview. |
| `licence_id` | Protected order database | Buyer-specific entitlement reference. |
| `delivery_expires_at` | Protected order database | Expiring download authorization. |
| `evidence_bundle_key` | Restricted storage | Incident evidence and enforcement history. |

## Practical 30-day order

| Window | Work | Completion gate |
|---|---|---|
| Days 1–3 | Define Product IDs, release versions, commit/hash fields, and one standard release manifest. | One pilot template can be mapped from live route to source commit and checksum. |
| Days 4–10 | Complete the asset register, contributor-rights record, dependency inventory, and third-party notices for the pilot. | Every included file has a documented origin and redistribution status. |
| Days 11–17 | Draft the buyer licence, delivery manifest, support boundary, and incident-response process. | Qualified legal review identifies no unresolved release blockers. |
| Days 18–24 | Build private package storage, short-lived downloads, delivery logs, and non-personal licence fingerprints after commerce is formally approved. | Test buyer can purchase or receive, download, verify, and reinstall the exact package. |
| Days 25–30 | Add signed release verification, SPDX generation, monitoring queries, and an evidence-preservation workflow. | A release can be verified and a simulated misuse case produces a complete evidence bundle. |

## Avoid these false protections

| Avoid | Reason |
|---|---|
| Right-click, text-selection, or keyboard-copy blocking | Easily bypassed and harmful to accessibility and legitimate use. |
| Treating minification or obfuscation as ownership protection | It may slow casual inspection but does not create or prove rights. |
| Publishing permanent download links | They can be copied, indexed, and redistributed without access expiry. |
| Hidden collection of buyer personal data inside template files | Creates privacy and trust risk; use a non-personal licence identifier instead. |
| Assuming a copyright notice or hash proves all asset rights | It identifies a claim or file state, but underlying third-party permissions still require evidence. |
| Blockchain/NFT registration without source and licence evidence | A timestamped record does not cure missing ownership, contributor, or asset rights. |

## Recommended next decision

Do **not** roll this system across all 50 products immediately. First complete a single pilot release—recommended: **Axiom Grid**—and prove the full chain from source commit to asset evidence, signed package, buyer licence, controlled download, and verification. After the pilot passes legal and operational review, reuse the same release schema for the other 49 products.

## References

[1]: [GitHub Docs — Managing commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification)

[2]: [Sigstore — Sign, verify, protect software artifacts](https://www.sigstore.dev/)

[3]: [Amazon S3 — Download and upload objects with presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html)

[4]: [WIPO — Trade Secrets](https://www.wipo.int/en/web/trade-secrets)

[5]: [SPDX — System Package Data Exchange](https://spdx.dev/)

[6]: [WIPO — How to Obtain Copyright Protection](https://www.wipo.int/en/web/copyright/protection)

[7]: [WIPO — Trademarks](https://www.wipo.int/en/web/trademarks)
