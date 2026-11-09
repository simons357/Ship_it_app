# ChatVault Testing - Quick Summary

> Lab notes only. Canonical decision and rejected overclaims: [`../MASTER-AUDIT.md`](../MASTER-AUDIT.md).

## ✅ What Works
- **Full conversation vault** with 15 demo conversations (SaaS product topics)
- **Ingest:** Paste text, bulk import (=== separator), media upload
- **Search:** Plain keyword + Semantic AI search
- **Organization:** Tags (90), Books (4), Subjects, Second-order tags
- **Edit:** Add/remove tags in real-time
- **Export:** JSON per conversation
- **Dashboard:** Metrics, charts, readiness tracking
- **Disclaimer:** Comprehensive legal language about data retention, no professional advice
- **Data persistence:** Survives page refresh

## ❌ What's Missing
- **No research schema:** No theorems, claims, open_gaps, CLAIM_LEDGER statuses
- **No bulk export:** Only per-conversation JSON
- **No Markdown/CSV export**
- **No search highlighting**
- **No AND/OR operators in search**

## 🔍 Key Findings

### Conversation Fields Present:
- Title, Status (PASTED/HIGH/MEDIUM/LOW), Readiness %
- Summary (AI-generated), Conversation (raw text preserved)
- Tags, Books, Subjects, Second-order tags
- Metadata (Project, Location, Importance, Date)

### Conversation Fields NOT Present:
- ❌ Claims section
- ❌ Theorems section  
- ❌ Open Gaps section
- ❌ Action Items section
- ❌ CLAIM_LEDGER (PROVED/CONDITIONAL/NUMERICAL/CONJECTURAL/OPEN/WITHDRAWN)

### Data Type:
- **Demo data:** 14 SaaS product development conversations (rate limiters, CRM, investor decks, refactoring)
- **Test data:** 1 ingested Euler identity note (100% readiness)
- **NOT research notes:** No personal research, theorems, or formal claims

## 🌐 Additional URLs Tested

### C2 Drive (/drive)
- **Purpose:** Google Drive integration for document import
- **Status:** Requires OAuth sign-in
- **Type:** Feature extension, not standalone product

### Paper Vault (different preview URL)
- **Purpose:** Academic paper management
- **Type:** Separate product with versioning, drafts
- **Status:** Empty state (0 papers)

## 🐛 Minor Issues
1. Console error: API 401 on `/api/apps/.../entities/user.json` (expected auth check)
2. Manifest deprecation warning (P4 - future maintenance)
3. BuilderBridge parent window warnings (P4 - non-blocking)

## 📊 Product Classification

**ChatVault IS:**
- AI conversation organizer
- Personal knowledge base for AI chats
- Semantic search tool
- Tagging/categorization system

**ChatVault IS NOT:**
- Research claim tracker
- Theorem management system
- Gap analysis tool
- Formal proof assistant
- Truth verification engine

## 🎯 Verdict

**FULLY FUNCTIONAL** general-purpose AI conversation vault. Excellent for organizing ChatGPT/Claude conversations. Does NOT implement research-oriented schema (claims, theorems, gaps, CLAIM_LEDGER). For formal research use, additional schema layer needed.

---

**Screenshots:** 16 total (see CHATVAULT_TEST_REPORT.md for manifest)  
**Test Duration:** ~15 minutes  
**Test Date:** Aug 24, 2026, 3:12 AM UTC
