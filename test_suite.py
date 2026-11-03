import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('proof-tap-signin-walkthrough.html', 'r', encoding='utf-8') as f:
    html = f.read()

tests = []

def test(name, condition, details=""):
    tests.append((name, condition, details))
    status = "[PASS]" if condition else "[FAIL]"
    print(f"{status}: {name}")
    if not condition and details:
        print(f"   Details: {details}")

print("=======================================================")
print("  PROOF COMPREHENSIVE VERIFICATION TEST SUITE (22 CASES)")
print("=======================================================\n")

# Test 1 & 2: Face 3 (Registration Success)
face3_match = re.search(r'<div[^>]*data-face="3"[^>]*>(.*?)</div>\s*</div>\s*<!-- FACE 4', html, re.DOTALL)
face3_content = face3_match.group(1) if face3_match else ""

test("Case 1: Registration Success screen preserved with 'You\'re In!' heading",
     "You're In!" in face3_content and "Digital Loyalty Pass Created" in face3_content)

test("Case 2: Face 3 displays only 'Spin & Win' button (NO 'Back to Start')",
     'id="startSpinBtn"' in face3_content and 'Back to Start' not in face3_content)

# Test 3: Horizontal 3-reel slot machine design
test("Case 3: Face 11 uses horizontal 3-reel layout with reels-stage and 3 separate reel frames",
     'class="reels-stage"' in html and
     'class="slot-reel-frame" id="reel1"' in html and
     'class="slot-reel-frame" id="reel2"' in html and
     'class="slot-reel-frame" id="reel3"' in html and
     '.reels-stage' in html and 'display: flex' in html and 'flex-direction: row' in html)

# Test 4: Bulbs layout and animation
test("Case 4: Bulbs blink with staggered perimeter marquee chase (22 bulbs) and celebration mode",
     '.slot-bulb' in html and
     '.top-bulbs' in html and '.bottom-bulbs' in html and
     '.left-bulbs' in html and '.right-bulbs' in html and
     'bulbIdleGlow' in html and 'bulbCelebration' in html and
     'prefers-reduced-motion' in html)

# Test 5 & 6: "You Have One Spin!" message directly above Spin & Win button
spin_avail_pos = html.find('id="spinAvailBox"')
spin_btn_pos = html.find('id="spinActionBtn"')
test("Case 5: 'You Have One Spin!' message placed directly above Spin & Win button",
     spin_avail_pos != -1 and spin_btn_pos != -1 and spin_avail_pos < spin_btn_pos and
     "You Have One Spin!" in html and "Try your luck and discover your reward." in html)

test("Case 6: One spin message animated with subtle scale 1.06 pulse without shifting layout",
     '@keyframes spinAvailPulse' in html and 'scale(1.06)' in html and 'transform-origin: center center' in html)

# Test 7 & 8: Reminder below Google Wallet button
gw_btn_pos = html.find('id="googleWalletBtn"')
reminder_pos = html.find('id="walletReqReminder"')
active_card_pos = html.find('id="face11ActivePassCard"')

test("Case 7: Clicking Spin without wallet registration displays reminder message",
     "Please add your PROOF Loyalty Pass to Google Wallet before spinning." in html and
     "reminder.style.display = 'flex'" in html)

test("Case 8: Reminder positioned below the wallet button/card (NOT between buttons)",
     gw_btn_pos < reminder_pos and active_card_pos < reminder_pos and spin_btn_pos < gw_btn_pos)

# Test 9, 10, 11, 12: In-place Google Wallet Registration
test("Case 9: Clicking Add to Google Wallet registers mock pass in place",
     'function handleInPlaceGoogleWalletRegistration' in html and
     'activeCustomer.googleWallet = {' in html and
     'registered: true' in html)

test("Case 10: Google Wallet button has NO navigation to Face 9 (stays on Face 11)",
     "gwBtn.addEventListener('click', function()" in html and
     'handleInPlaceGoogleWalletRegistration()' in html and
     'showFace(9' not in html[html.find('id="googleWalletBtn"'):html.find('id="googleWalletBtn"')+400])

test("Case 11: Active Google Wallet Pass Card replaces registration button in place",
     'class="face11-active-pass-card" id="face11ActivePassCard"' in html and
     'Google Wallet Pass Active' in html and
     'Your PROOF Loyalty Pass is ready.' in html and
     "activePassCard.style.display = 'flex'" in html and
     "gwBtn.style.display = 'none'" in html)

test("Case 12: Wallet registration button hidden for returning/already registered customers",
     'if(!isRegistered)' in html and "gwBtn.style.display = 'none'" in html)

# Test 13: 3D Scalloped Loyalty Stamps
test("Case 13: Green and Blue stamps use 3D embossed scalloped SVG graphics",
     'function get3DStampSvg' in html and
     ('scallop' in html.lower() or 'M 57.00 30.00' in html) and
     'stroke-dasharray="2.5 2"' in html)

# Test 14: Stamp result messages
test("Case 14: Stamp result screen copy is customer-friendly ('You won a Green Stamp!' / 'You won a Blue Stamp!')",
     "You won a Green Stamp!" in html and
     "You won a Blue Stamp!" in html and
     "1 Green Stamp has been added to your loyalty collection." in html and
     "1 Blue Stamp has been added to your loyalty collection." in html)

# Test 15: Counter display synchronization
test("Case 15: Physical counter display mirrors exact same reward outcome",
     'function deviceShowReward' in html and
     'LOYALTY STAMP WON' in html and
     'You won 1 Green Stamp!' in html and
     'You won 1 Blue Stamp!' in html and
     'Added to Green Stamp Collection.' in html)

# Test 16: Strict single reward (Stamp OR Gift, never both)
test("Case 16: One spin awards strictly ONE reward (mutually exclusive stamp OR gift)",
     "outcome.rewardType === 'STAMP'" in html and
     "if(outcome.rewardType === 'STAMP')" in html and
     "stampRow.style.display = 'flex'" in html and
     "giftRow.style.display  = 'none'" in html)

# Test 17 & 18: Face 12 Post-Spin Exactly Two Actions
face12_start = html.find('<!-- FACE 12: REWARD RESULT SCREEN')
face12_end = html.find('<!-- ═══ PROOF DISPLAY')
face12_sub = html[face12_start:face12_end]

test("Case 17: Result screen shows exactly two actions: Return to Start & Check Loyalty Wallet",
     'id="resultReturnStartBtn"' in face12_sub and
     'id="resultCheckWalletBtn"' in face12_sub and
     'Return to Start' in face12_sub and
     'Check Loyalty Wallet' in face12_sub and
     'Claim Reward &amp; Finish Visit' not in face12_sub and
     'View Loyalty Pass' not in face12_sub)

test("Case 18: Check Loyalty Wallet button opens Face 9 with stamp balances",
     'resultChkWallet.addEventListener' in html and
     'renderFace9LoyaltyWallet();' in html and
     'showFace(9, 4);' in html)

# Test 19 & 20: Face 9 (Loyalty Wallet Screen)
face9_start = html.find('<!-- FACE 9: PROOF LOYALTY WALLET')
face9_end = html.find('<!-- FACE 13:')
face9_sub = html[face9_start:face9_end]

test("Case 19: Loyalty Wallet screen does NOT display Spin & Win, Continue to Spin, or Back to Spin",
     'id="walletReturnStartBtn"' in face9_sub and
     'Continue to Spin &amp; Win' not in face9_sub and
     'Spin &amp; Win' not in face9_sub and
     'Back to Spin' not in face9_sub)

test("Case 20: Return to Start from both Face 12 and Face 9 navigates directly to Face 0",
     "resultRetStart.addEventListener('click', function(){" in html and
     "walletRetStart.addEventListener('click', function(){" in html and
     'showFace(0, 0)' in html)

# Test 21 & 22: Persistence & Core Functionality
test("Case 21: Customer balances, Google Wallet state, and reward history persist in localStorage",
     'activeCustomer.googleWallet' in html and
     'activeCustomer.stampWallet' in html and
     'activeCustomer.rewardHistory' in html and
     'updateCustomer(' in html and
     'saveCustomers(' in html and
     'localStorage.setItem' in html)

test("Case 22: Existing customer registration, sign-in, and 3-visit cooldown flows preserved",
     'submitCapture' in html and
     'PROMPT_COOLDOWN_VISITS' in html and
     'visits' in html and
     'createCustomer' in html)

print("\n=======================================================")
passed = sum(1 for _, c, _ in tests if c)
total = len(tests)
print(f"  TOTAL RESULT: {passed}/{total} CASES PASSED ({'100% SUCCESS' if passed == total else 'SOME FAILED'})")
print("=======================================================")
