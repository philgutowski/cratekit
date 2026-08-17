"""Outbound service writes: playlist export and add-only hearts.

The only two operations that mutate a third-party account live here so they
share one discipline: confirm-gated, idempotent, recorded, and add-only.
Deletion never reaches this package. Empty of imports so importing the
package does not pull the engines (KTD7).
"""
