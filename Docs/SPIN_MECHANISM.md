# PROOF – Spin & Win Loyalty Engine Specification

> Complete architectural reference for today's frontend slot-machine loyalty reward game, mathematical probabilities, mutually exclusive single-reward logic, and tomorrow's production backend & physical hardware integration.

---

## 🎰 1. Core Philosophy: Loyalty Reward, Not Gambling

The PROOF Spin & Win experience is designed as an interactive **customer loyalty reward program**, not real-money gambling:
1. **100% Win Guarantee:** Every customer who is eligible to spin receives a valuable reward (either a loyalty stamp or a complimentary food/drink gift).
2. **Transparent Odds:** Exact mathematical distribution engineered to protect merchant margins while maximizing customer delight.
3. **Strict Single Reward (Mutually Exclusive):** A customer receives **ONLY ONE REWARD PER SPIN** — either a loyalty stamp OR a complimentary gift. Never both.

---

## 📊 2. Today's Mathematical Probabilities & Reward Matrix

### Probability Tiers

| Tier Name | Probability | Frequency | Winning Symbols | Reward Options (Mutually Exclusive) | Customer Screen Headline |
|---|---|---|---|---|---|
| **SMALL** | **83.0%** (0.83) | ~83 in 100 spins | Low suit pairs/combos (`[♣ ♣ 7]`, `[♦ ♠ ♣]`) | **Option A (50%):** 1 Green Stamp<br/>**Option B (50%):** 1 Small Gift (*Extra Coffee Powder*, *Syrup Shot*, *Dark Chocolate*) | **Congratulations!**<br/>*"You won a Green Stamp!"* or *"You won a complimentary gift!"* |
| **MEDIUM** | **15.0%** (0.15) | ~15 in 100 spins | Matching 7s pair or heart pair (`[7 7 ♣]`, `[♥ ♥ ♦]`) | **Option A (50%):** 1 Blue Stamp<br/>**Option B (50%):** 1 Medium Gift (*Size Upgrade*, *Artisan Oat/Specialty Milk*) | **Great Win!**<br/>*"You won a Blue Stamp!"* or *"You unlocked a special reward!"* |
| **JACKPOT** | **1.5%** (0.015) | ~15 in 1,000 spins | Triple matching suits (`[♥ ♥ ♥]`, `[♠ ♠ ♠]`) | **Single Gift:** Complimentary Pour Over or French Pastry of the Day | **Jackpot!**<br/>*"Fantastic! You won a premium gift!"* |
| **MEGA JACKPOT** | **0.5%** (0.005) | ~5 in 1,000 spins | Triple Lucky Sevens (`[7 7 7]`) | **Single Grand Gift:** Buy One Get One VIP Pass or Deluxe Coffee Gift Hamper | **MEGA JACKPOT!**<br/>*"Unbelievable! You've won our grand reward!"* |

**Total Cumulative Probability:** $0.83 + 0.15 + 0.015 + 0.005 = 1.00$ (**Exactly 100%**).

---

## 🎨 3. Slot Machine Architecture (Horizontal 3-Reel Layout)

### A. Cabinet & Reels Layout (Reference Image 1)
- **Three Reels Side-by-Side:** Positioned horizontally within `.reels-stage` using `display: flex; flex-direction: row; justify-content: center; gap: 8px`.
- **Three Separate Reel Frames (`.slot-reel-frame`):**
  - Dimensions: `width: 76px; height: 102px` (`REEL_WIN_H = 102`).
  - Dark metallic housing with gold borders (`1.5px solid rgba(212, 175, 55, 0.55)`).
  - Cylindrical 3D drum gradient overlay with center payline highlight.
- **Five Authentic Symbols:**
  - `7`: High-gloss gold metallic gradient with drop shadow.
  - `♥`: Crimson ruby heart (`#e74c3c`).
  - `♦`: Amber radiant diamond (`#e67e22`).
  - `♠`: Obsidian black spade with gold glow.
  - `♣`: Champagne gold clover (`#d4af37`).
- **Attract State Initial Display (Reference Image 1):**
  - Reel 1: `7` (top), `♠` (center), `♥` (bottom)
  - Reel 2: `♣` (top), `♥` (center), `♣` (bottom)
  - Reel 3: `♦` (top), `7` (center), `♠` (bottom)
  - Label: `"GOOD LUCK !"` at bottom.

### B. 22-Bulb Clockwise Perimeter Marquee Chase
- Surrounding bulbs follow a clockwise perimeter delay from top row (1-8) $\rightarrow$ right column (9-11) $\rightarrow$ bottom row (12-19) $\rightarrow$ left column (20-22).
- **Idle State:** Soft 2.4s breathing glow.
- **Spinning State:** High-speed 0.35s chase animation with golden radiant halos.
- **Celebration State:** Rhythmic win flare animation when the reels stop.
- **Accessibility:** Fully supports `prefers-reduced-motion: reduce` by replacing animations with static warm gold illumination.

### C. "You Have One Spin!" Availability Badge
- Positioned **directly above** the Spin & Win button.
- Heading: **You Have One Spin!**
- Description: *"Try your luck and discover your reward."*
- Animation: Gentle scale $1.0 \rightarrow 1.06$ pulse (`@keyframes spinAvailPulse`) with zero layout shift. Pauses during active spinning.

---

## 🔒 4. Mutually Exclusive Single-Reward Logic

A spin transaction **strictly awards either ONE stamp OR ONE gift**. Never both.

```
              ┌──────────────────────────┐
              │      Spin Triggered      │
              └─────────────┬────────────┘
                            │
              ┌─────────────▼────────────┐
              │  Tier Selected (e.g. 83%) │
              └─────────────┬────────────┘
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
    [Option A: Stamp (50%)]       [Option B: Gift (50%)]
    - stampColor: "GREEN"         - stampColor: null
    - stampCount: 1               - stampCount: 0
    - gift: null                  - gift: { name: "Coffee Powder" }
             │                             │
             ▼                             ▼
    [Increment Green Stamp]       [Stamp Unchanged!]
    [Face 12: Stamp Card Only]    [Face 12: Gift Card Only]
```

### Exact Customer Screen & Counter Display Parity

| Outcome | Customer Screen (Face 12) | Counter Terminal Display (Panel 2) |
| :--- | :--- | :--- |
| **Green Stamp** | **Congratulations!**<br/>*"You won a Green Stamp!"*<br/>*1 Green Stamp has been added to your loyalty collection.*<br/>3D Green Stamp SVG graphic | **LOYALTY STAMP WON**<br/>*You won 1 Green Stamp!*<br/>*Added to Green Stamp Collection.*<br/>Tag: `STAMP CREDITED` |
| **Blue Stamp** | **Great Win!**<br/>*"You won a Blue Stamp!"*<br/>*1 Blue Stamp has been added to your loyalty collection.*<br/>3D Blue Stamp SVG graphic | **LOYALTY STAMP WON**<br/>*You won 1 Blue Stamp!*<br/>*Added to Blue Stamp Collection.*<br/>Tag: `STAMP CREDITED` |
| **Gift Item** | Headline & Subhead per Tier<br/>Gift Title & Description<br/>*"Show pass at checkout to claim!"* | **COMPLIMENTARY GIFT WON**<br/>Gift Name<br/>*Show Pass at Checkout*<br/>Tag: `CLAIM AT COUNTER` |

---

## 🏁 5. Post-Spin Navigation (Exactly Two Actions)

After the single spin completes, Face 12 displays exactly two actions:

1. **Return to Start (`#resultReturnStartBtn`):**
   - Resets the terminal to idle.
   - Navigates immediately to Face 0 (NFC stage).
   - Finishes visit cleanly without granting another spin.
   - Customer balances and reward history remain intact in `localStorage`.

2. **Check Loyalty Wallet (`#resultCheckWalletBtn`):**
   - Navigates to Face 9 (PROOF Loyalty Pass).
   - Displays 3D Green Stamp progress (toward 10) and 3D Blue Stamp progress (toward 5).
   - Displays Active Google Wallet status card.
   - Bottom button: **ONLY "Return to Start"** (`#walletReturnStartBtn` $\rightarrow$ Face 0).
   - **Zero repeat spin buttons**, ensuring the customer cannot spin again.
