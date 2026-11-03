# PROOF – Google Wallet Loyalty Pass Integration & Architecture

> Complete reference for today's simulated frontend Google Wallet pass registration, in-place pass activation, 3D loyalty stamp wallet, and tomorrow's production Google Wallet REST API integration.

---

## 📱 1. Architecture Overview

Google Wallet is the digital home for customer loyalty cards on Android smartphones. Integrating PROOF with Google Wallet provides:
1. **NFC Tap Synergy:** Customers hold their phone to the counter NFC reader; the digital pass identifies them instantly.
2. **Lock Screen Push Notifications:** When a customer approaches the cafe or earns a stamp, Google Wallet can push geofenced and real-time point balance notifications directly to their smartphone lock screen.
3. **Zero App Download:** Customers do not need to install a proprietary cafe mobile app; the pass lives directly inside native Google Wallet.

---

## 🔒 2. Final In-Place Registration Flow (Same Screen, No Navigation)

### A. Customer Journey & Screen Flow

```
[Registration Success (Face 3)]
             │
             ▼
[Spin & Win Screen (Face 11)]
             │
   Is Wallet Registered?
     ├── NO ──► Spin & Win button is LOCKED (🔒 SPIN & WIN (WALLET REQUIRED))
     │          If customer clicks locked spin:
     │            Display inline reminder below the wallet button:
     │            "⚠️ Please add your PROOF Loyalty Pass to Google Wallet before spinning."
     │          Customer clicks "#googleWalletBtn" ("Add to Google Wallet"):
     │            1. Registration executes IMMEDIATELY IN PLACE (no screen navigation).
     │            2. State set: activeCustomer.googleWallet.registered = true, passId = "GW-PROOF-XXXX".
     │            3. Persisted in localStorage.
     │            4. Button is replaced in place by Active Status Card:
     │               "✓ Google Wallet Pass Active – Your PROOF Loyalty Pass is ready."
     │            5. Spin & Win button unlocks immediately: "SPIN & WIN →"
     │                    │
     │                    ▼
     └── YES ─► Unlocked immediately:
                - Active Google Wallet Pass Card displayed in place.
                - Spin & Win button ready to spin.
```

### B. In-Place Active Status Card vs. Registration Button

| State | Google Wallet Element | Spin & Win Button | Reminder Notice |
| :--- | :--- | :--- | :--- |
| **Unregistered (First Spin)** | Black Google Wallet Button (`Add to Google Wallet`) | Locked: `🔒 SPIN & WIN (WALLET REQUIRED)` | Shown below wallet button if locked spin clicked |
| **Registered (In Place)** | Replaced by `.face11-active-pass-card` with glowing green badge, pass ID & live sync | Unlocked: `SPIN & WIN →` | Hidden |
| **Returning Customer** | Displays `.face11-active-pass-card` immediately | Unlocked: `SPIN & WIN →` | Hidden |

---

## 🏆 3. Face 9: PROOF Loyalty Wallet & 3D Stamp Cards

Face 9 is accessed post-spin by clicking **"Check Loyalty Wallet"** on Face 12:
- **Header:** **PROOF LOYALTY PASS** / *"Your rewards, all in one place."*
- **Google Wallet Status Card:** Displays active pass card: *"Google Wallet Pass Active"* / *"Your PROOF Loyalty Pass is ready."* (Zero duplicate registration buttons).
- **3D Embossed Scalloped Stamps:**
  - **Green Stamp Card:** 3D Green Stamp badge with progress toward 10. Strict instruction: *"Collect 10 Green Stamps to redeem your reward."*
  - **Blue Stamp Card:** 3D Blue Stamp badge with progress toward 5. Strict instruction: *"Collect 5 Blue Stamps to redeem your reward."*
  - **Strict Display Rule:** Zero gift names or product descriptions on the stamp collection cards.
- **Bottom Action:** ONLY **"Return to Start"** (`#walletReturnStartBtn` $\rightarrow$ Face 0).
  - **Zero Spin & Win, Continue to Spin, or Back to Spin buttons**, preventing repeat spins.

---

## 💾 4. Frontend State Model (`localStorage.proof_customers`)

```json
{
  "id": "cust_1741000000000_abc12",
  "phoneNumber": "+919876543210",
  "name": "Priya Sharma",
  "visits": 1,
  "googleWallet": {
    "registered": true,
    "passId": "GW-PROOF-3210",
    "addedAt": "2026-11-03T08:30:00.000Z"
  },
  "stampWallet": {
    "green": 1,
    "blue": 0
  },
  "rewardHistory": [
    {
      "spinId": "spin-1741000000000-xyz1",
      "rewardCategory": "SMALL",
      "rewardType": "STAMP",
      "stampColor": "GREEN",
      "stampCount": 1,
      "gift": null,
      "symbols": ["7", "♦", "♦"],
      "createdAt": "2026-11-03T08:31:00.000Z"
    }
  ]
}
```

---

## 🚀 5. Production Google Wallet Integration Plan

When the backend (Node.js/Express) and MongoDB are connected:

1. **Google Wallet API Issuer Account:**
   - Register Issuer ID in Google Pay & Wallet Console.
   - Generate Service Account Private Key (`credentials.json`).

2. **Loyalty Class Creation (`POST /loyaltyClass`):**
   - Class ID: `issuerId.proof_loyalty_club`
   - Program Name: "PROOF Coffee Co. Loyalty"
   - Hex Colors: Background `#0c0f17`, Gold Accent `#d4af37`.

3. **Pass Object JWT Signing (`POST /loyaltyObject`):**
   - Object ID: `issuerId.proof_cust_<phone>`
   - Link to customer record in MongoDB.
   - Real-time balance updates pushed via Google Wallet REST API patch calls.
