# Luma Foundry — Master Sheet Synchronization Status

**Verification time:** 2026-08-27 03:56 UTC  
**Authoritative sheet:** [Luma Foundry — Operator Sync](https://docs.google.com/spreadsheets/d/1mM6HtzS14FRygndjIDYfzl8LGxF7jq0-ISfpniijaTU/edit)  
**Verification scope:** `Products!A1:I60`, `Sync Log!A1:H80`, and the official public-route registry in `client/src/App.tsx`.

> **Result: route logging is complete.** The 50 official product routes registered in the application reconcile exactly to 50 unique Product rows in the shared Google Sheet. Every Product row has the canonical Luma Foundry hosted-preview URL, `live` status, and `Operator A` ownership. No official route is missing and no unexpected product route is present.

| Control | Verified result | Status |
|---|---:|---|
| Official product routes in application registry | 50 | Pass |
| Product rows in `Products` | 50 | Pass |
| Unique hosted-preview paths in `Products` | 50 | Pass |
| Rows with canonical `https://lumafoundry-jx4veohg.manus.space/<route>` URL | 50 | Pass |
| Rows marked `live` | 50 | Pass |
| Rows owned by `Operator A` | 50 | Pass |
| Missing official routes | 0 | Pass |
| Unexpected sheet routes | 0 | Pass |

## Batch-level reconciliation

| Batch | Products reconciled | Products ledger evidence | Sync-log evidence |
|---|---|---|---|
| 01 | Axiom Grid; Selene Agents; Kinetic Mesh; Lattice Labs; Orbital Ledger | 5 `goal-batch-01` product rows | `sync-0001` initial import |
| 02 | Stilla Care Systems; Morrow Compute; Vanta Proof; Helio Relay; Folio Forms | 5 `goal-factory-50` product rows | `sync-0007` batch publication |
| 03 | Noor Vale; Aster & Alder; Élan Method; Vela Maison; Sardis Parfums | 5 `goal-factory-50` product rows | `sync-0008` batch publication |
| 04 | Ruth Ibarra Botanics; Tempo Atelier; Peregrine Editions; Caldera Optical; Maré House | 5 `goal-factory-50` product rows | `sync-0009` batch publication |
| 05 | Monolith Works; Nocturne Estates; Alder House; Formwell Interiors; Studio Lumen | 5 `goal-factory-50` product rows | `sync-0010` batch publication |
| 06 | Maison Rook; Terra Forma; Veloce District; Hinge & Hearth; Fieldnote Cabins | 5 `goal-factory-50` product rows | `sync-0011` batch publication |
| 07 | Kansa Objects; Ora Roasters; Corella Run; Solace Audio; Basil & Bone | 5 `goal-factory-50` product rows | `sync-0012` batch publication |
| 08 | Vesper Pantry; Arq Supply; Perrin Carry; Wildercare; Havenlark | 5 `goal-factory-50` product rows | `sync-0013` batch publication |
| 09 | Sable & Type; Civic Assembly; Masonry Films; Northline Counsel; Pattern School | 5 `goal-factory-50` product rows | `sync-0014` batch publication |
| 10 | Oriel Advisory; Hinterland Sound; Quorum House; Adjacent Talent; Lumen & Co. | 5 `goal-factory-50` product rows | `sync-0015` batch publication |

The `Sync Log` further records `full_qc_completed` for all 50 official routes and `qc_remediation_verified` for the Batch 05 accessibility correction. These entries confirm the operational record is present; the Product table remains the row-level source of truth for route, category, URL, status, operator, provenance label, and update time.

## Data-quality note

The 23-row `Sync Log` contains three duplicate **event-ID labels**: `sync-0007`, `sync-0016`, and `sync-0017`. The corresponding entries differ by timestamp, operator, and action, so this does **not** create missing or duplicated Product rows and does not affect the 50/50 route reconciliation. It should nevertheless be corrected in a future, explicitly approved audit to make event identifiers unique and preserve unambiguous traceability.

## Scope boundary

This reconciliation verifies **Google Sheet logging completeness** for the live public-route catalogue. It does not constitute commercial/IP clearance, legal review, checkout readiness, webhook activation, or perpetual deployment certification.
