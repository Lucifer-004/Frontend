# PROOF – Premium 3D NFC Customer Experience & Loyalty Platform

> An interactive, next-generation digital customer onboarding and loyalty rewards platform built for physical retail, luxury hospitality, and specialty cafes. Designed for high-speed smartphone NFC tap interactions, progressive profile collection, Google Wallet passes, and a 3D slot-machine loyalty reward experience.

---

## 📋 Table of Contents
1. [Project Overview](#1-project-overview)
2. [Screen & Journey Architecture](#2-screen--journey-architecture)
3. [Key Modules & Final UI/UX Corrections](#3-key-modules--final-uiux-corrections)
   - [Horizontal 3-Reel Slot Machine (Reference Image 1)](#a-horizontal-3-reel-slot-machine-reference-image-1)
   - [In-Place Google Wallet Pass Activation](#b-in-place-google-wallet-pass-activation)
   - [Animated "You Have One Spin!" Message](#c-animated-you-have-one-spin-message)
   - [3D Scalloped Loyalty Stamps](#d-3d-scalloped-loyalty-stamps)
   - [Customer-Friendly Reward Result Copy & Counter Mirroring](#e-customer-friendly-reward-result-copy--counter-mirroring)
   - [Post-Spin Navigation: Exactly Two Actions](#f-post-spin-navigation-exactly-two-actions)
   - [Loyalty Wallet Final Behavior (Face 9)](#g-loyalty-wallet-final-behavior-face-9)
4. [File Structure & Documentation Index](#4-file-structure--documentation-index)
5. [Data Model & LocalStorage Persistence](#5-data-model--localstorage-persistence)
6. [Automated Verification Test Results](#6-automated-verification-test-results)

---

## 1. Project Overview

The PROOF NFC Customer Experience transforms physical retail counters into an interactive, digital customer touchpoint:
- **Left Panel — Customer Smartphone View:** Simulates the customer's phone display upon tapping the counter NFC tag (responsive 410px mobile viewport with high-end glassmorphism, champagne gold metallic accents, and realistic 3D depth).
- **Right Panel — PROOF Counter Display (Kiosk Screen):** Simulates the commercial 4K terminal facing the customer and cashier, showing verified Google ratings, real-time NFC sensing pulses, and immediate live synchronization of customer visits, profile updates, and spin reward victories.
- **Bottom Panel — Live Kiosk Audit Log:** Chronological, tamper-evident event log tracking all sign-ups, sign-ins, Google Wallet pass issuances, spin outcomes, and stamp redemptions with localStorage persistence.

---

## 2. Screen & Journey Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MAIN CUSTOMER JOURNEYS                          │
└────────────────────────────────────────────────────────────────────────┘

[Face 0: 3D NFC Tap Stage]
          │
          ▼
[Face 1: NFC Gate Selection] 
       ├── First-Time Here? ──────► [Face 2: Phone-Only Registration]
       │                                       │
       │                                       ▼
       │                            [Face 3: You're In! Pass Created]
       │                            (Single Action: 'Spin & Win →')
       │                                       │
       │                                       ▼
       └── Signed In Before? ─────► [Face 4: Returning Member Sign-In]
                                               │
                                 ┌─────────────┴─────────────┐
                                 ▼                           ▼
                     [Face 6: Profile Prompt]    [Face 13: Birthday Prompt]
                     (If Visit >= Cooldown)      (If Profile Done & Cooldown)
                                 │                           │
                                 └─────────────┬─────────────┘
                                               ▼
                                 [Face 5: VIP Welcome Back]
                                               │ (Click 'Play Spin & Win 🎰')
                                               ▼
                                 [Face 11: Spin & Win 3D Slot Machine]
                                 - Horizontal 3 reels side-by-side
                                 - 22-bulb perimeter marquee chase
                                 - "You Have One Spin!" (1.06 pulse)
                                 - In-place Google Wallet activation
                                               │ (Click 'SPIN & WIN →')
                                               ▼
                                 [Face 12: Reward Result Screen]
                                 - Strictly Mutually Exclusive Reward:
                                   * Option A: 3D Stamp (+1 Green or Blue)
                                   * Option B: Complimentary Gift Item
                                 - Mirrored onto Physical Counter Display
                                 - EXACTLY TWO ACTIONS:
                                   [1] Return to Start (Face 0)
                                   [2] Check Loyalty Wallet (Face 9)
                                               │
                                               ▼
                                 [Face 9: PROOF Loyalty Wallet]
                                 - Active Google Wallet card
                                 - 3D Green Stamp progress (toward 10)
                                 - 3D Blue Stamp progress (toward 5)
                                 - ONLY ACTION: Return to Start (Face 0)
                                 - (Zero repeat spin buttons)
```

---

## 3. Key Modules & Final UI/UX Corrections

### A. Horizontal 3-Reel Slot Machine (Reference Image 1)
- **Three Reels Side-by-Side:** Restored via `.reels-stage` flexbox row (`gap: 8px`).
- **Three Distinct Frames (`.slot-reel-frame`):** Width 76px, height 102px (`REEL_WIN_H = 102`), metallic gold borders (`1.5px solid rgba(212, 175, 55, 0.55)`), dark interior gradient, cylindrical drum shadow overlay (`.reel-overlay`) and center payline highlight.
- **Five Authentic Symbols:** High-gloss gradient `7`, crimson ruby `♥`, amber `♦`, obsidian `♠`, champagne gold `♣`.
- **Attract State Initial Alignment (Reference Image 1):**
  - Reel 1: `7` (top), `♠` (center), `♥` (bottom)
  - Reel 2: `♣` (top), `♥` (center), `♣` (bottom)
  - Reel 3: `♦` (top), `7` (center), `♠` (bottom)
  - Footer: `"GOOD LUCK !"` centered.
- **22-Bulb Clockwise Marquee:** Staggered delays sequentially tracing the perimeter: top (1-8) $\rightarrow$ right (9-11) $\rightarrow$ bottom (12-19) $\rightarrow$ left (20-22). Transitions smoothly between idle breathing glow, high-energy spin chase, and celebratory win flare.

### B. In-Place Google Wallet Pass Activation
- Clicking `Add to Google Wallet` on Face 11 **remains on Face 11** (zero navigation to another face).
- Performs immediate in-place simulation, sets `activeCustomer.googleWallet.registered = true`, saves in `localStorage`, and logs to the audit log.
- Replaces registration button in place with `.face11-active-pass-card`:
  - Glowing Google Wallet badge.
  - Heading: **Google Wallet Pass Active**
  - Subhead: *"Your PROOF Loyalty Pass is ready."*
  - Monospace pass identifier (`PASS: GW-PROOF-XXXX`).
  - Pulsing green active dot and shimmer effect.
- Unlocks the `Spin & Win` button immediately (`SPIN & WIN →`).
- If a customer clicks the locked spin button before registering, an attractive reminder appears **below** the Google Wallet button:
  *"⚠️ Please add your PROOF Loyalty Pass to Google Wallet before spinning."* (never inserted between buttons).

### C. Animated "You Have One Spin!" Message
- Positioned **directly above** the Spin & Win button.
- Heading: **You Have One Spin!**
- Description: *"Try your luck and discover your reward."*
- Animation: Gentle scale $1.0 \rightarrow 1.06$ pulse (`@keyframes spinAvailPulse`) with gold glow and `transform-origin: center center`. Does not shift layout flow.

### D. 3D Scalloped Loyalty Stamps
- Replaced flat colored dots with 3D embossed vector scalloped stamp graphics generated via `get3DStampSvg(color, size, animClass)`.
- Features 16-lobed scalloped outer rim, metallic gradient fill, dashed gold stitch line, embossed center core, raised metallic star/diamond emblem, specular glass crescent highlight, and soft colored ambient drop shadow.
- Plays a 3D rotate-Y and scale-up entrance pop (`stampAwardPop`) on award.

### E. Customer-Friendly Reward Result Copy & Counter Mirroring
- **Green Stamp Won:**
  - Customer Screen: **Congratulations!** / **You won a Green Stamp!** / *"1 Green Stamp has been added to your loyalty collection."*
  - Counter Display: **LOYALTY STAMP WON** / **You won 1 Green Stamp!** / *"Added to Green Stamp Collection."* / Tag: `STAMP CREDITED`.
- **Blue Stamp Won:**
  - Customer Screen: **Great Win!** / **You won a Blue Stamp!** / *"1 Blue Stamp has been added to your loyalty collection."*
  - Counter Display: **LOYALTY STAMP WON** / **You won 1 Blue Stamp!** / *"Added to Blue Stamp Collection."* / Tag: `STAMP CREDITED`.
- **Complimentary Gift Won:**
  - Mirrors identical gift item across both customer screen and counter display.
  - Zero stamp increase for gift-only wins; zero gifts issued for stamp-only wins.

### F. Post-Spin Navigation: Exactly Two Actions
Face 12 displays exactly two actions at the bottom:
1. **Return to Start (`#resultReturnStartBtn`):** Resets terminal and returns directly to Face 0 without granting another spin.
2. **Check Loyalty Wallet (`#resultCheckWalletBtn`):** Opens Face 9 to view stamp balances and Google Wallet pass status.

### G. Loyalty Wallet Final Behavior (Face 9)
- Header: **PROOF LOYALTY PASS** / *"Your rewards, all in one place."*
- Shows Active Google Wallet Pass Card (no duplicate registration button).
- Displays 3D Green Stamp Card (progress toward 10) with text: *"Collect 10 Green Stamps to redeem your reward."*
- Displays 3D Blue Stamp Card (progress toward 5) with text: *"Collect 5 Blue Stamps to redeem your reward."*
- Strictly displays **zero gift names or product descriptions** inside stamp cards.
- Bottom action: **ONLY "Return to Start"** (`#walletReturnStartBtn` $\rightarrow$ Face 0).
- Zero repeat spin buttons, ensuring single-spin compliance.

---

## 4. File Structure & Documentation Index

```
Frontend/
├── proof-tap-signin-walkthrough.html    # Single-file production prototype
├── test_suite.py                       # 22-case automated test verification harness
├── Docs/
│   ├── README.md                       # Master system guide & test results
│   ├── SPIN_MECHANISM.md               # Mathematical odds, slot machine architecture & MQTT spec
│   └── GOOGLE_WALLET.md                # Google Wallet flow, in-place pass activation & production plan
```

---

## 5. Data Model & LocalStorage Persistence

Customer state is preserved in browser `localStorage.proof_customers` under normalized E.164 phone numbers:

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
  "stamps": {
    "green": 1,
    "blue": 0
  },
  "spin": {
    "available": false,
    "completed": true
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

## 6. Automated Verification Test Results

```
=======================================================
  PROOF COMPREHENSIVE VERIFICATION TEST SUITE (22 CASES)
=======================================================

[PASS]: Case 1: Registration Success screen preserved with 'You're In!' heading
[PASS]: Case 2: Face 3 displays only 'Spin & Win' button (NO 'Back to Start')
[PASS]: Case 3: Face 11 uses horizontal 3-reel layout with reels-stage and 3 separate reel frames
[PASS]: Case 4: Bulbs blink with staggered perimeter marquee chase (22 bulbs) and celebration mode
[PASS]: Case 5: 'You Have One Spin!' message placed directly above Spin & Win button
[PASS]: Case 6: One spin message animated with subtle scale 1.06 pulse without shifting layout
[PASS]: Case 7: Clicking Spin without wallet registration displays reminder message
[PASS]: Case 8: Reminder positioned below the wallet button/card (NOT between buttons)
[PASS]: Case 9: Clicking Add to Google Wallet registers mock pass in place
[PASS]: Case 10: Google Wallet button has NO navigation to Face 9 (stays on Face 11)
[PASS]: Case 11: Active Google Wallet Pass Card replaces registration button in place
[PASS]: Case 12: Wallet registration button hidden for returning/already registered customers
[PASS]: Case 13: Green and Blue stamps use 3D embossed scalloped SVG graphics
[PASS]: Case 14: Stamp result screen copy is customer-friendly ('You won a Green Stamp!' / 'You won a Blue Stamp!')
[PASS]: Case 15: Physical counter display mirrors exact same reward outcome
[PASS]: Case 16: One spin awards strictly ONE reward (mutually exclusive stamp OR gift)
[PASS]: Case 17: Result screen shows exactly two actions: Return to Start & Check Loyalty Wallet
[PASS]: Case 18: Check Loyalty Wallet button opens Face 9 with stamp balances
[PASS]: Case 19: Loyalty Wallet screen does NOT display Spin & Win, Continue to Spin, or Back to Spin
[PASS]: Case 20: Return to Start from both Face 12 and Face 9 navigates directly to Face 0
[PASS]: Case 21: Customer balances, Google Wallet state, and reward history persist in localStorage
[PASS]: Case 22: Existing customer registration, sign-in, and 3-visit cooldown flows preserved

=======================================================
  TOTAL RESULT: 22/22 CASES PASSED (100% SUCCESS)
=======================================================
```
