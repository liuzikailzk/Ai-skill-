# 实际提交图像工具的完整提示词

run_id: REPRO-JOINT-20261018-01
Tool: image_gen.imagegen
transparent_background: false for all calls
Exact underlying model/seed: not exposed by tool

## Call 1 — text-to-image → film-v1.png
No reference image.

```text
Use case: illustration-story
Asset type: a reviewable six-frame storyboard contact sheet for testing shot continuity AND character/prop/environment consistency. This is a new test visualization of an existing fictional Chinese period action scene; there are no original character reference images. Do not claim to reproduce a previously approved actor's exact face.
Primary request: Generate ONE high-resolution landscape sheet, clean 3 columns x 2 rows grid, SIX equal 16:9 frames with thin off-white gutters. Read left to right, top to bottom. Each frame has only a small discrete number 01,02,03,04,05,06 in its upper-left corner. No other text. Professional photorealistic live-action Chinese period film storyboard, human anatomy and contact exceptionally clear, no injury or gore.
Scene: same open mountain courtyard gate, weathered gray stone paving, timber gate leaves fully open and a SINGLE pale stone strip across the ground immediately behind the man. Outside road visible through gate. Natural soft daylight from camera-left consistently. Courtyard camera stays on SAME side of the action axis for all shots. Woman on screen LEFT, man on screen RIGHT. Woman's attack goes left-to-right; man's retreat goes screen-right toward/through gate. No crossing axis or mirrored images.
Test identities, repeated EXACTLY: Lu Zhao, an adult Chinese woman in pale gray-white layered practical robe, dark hair tied high, dark belt, distinctive dark bronze bracer on her ANATOMICAL RIGHT forearm only; left forearm fabric only. Pei Zheng, adult Chinese man in dark navy practical robe, half-tied dark hair, brown leather bracers on both arms, no metal or glowing item. Simple cloth footwear. Stable faces, hair, costume, belt, bracer assignment, scale and gate architecture in all frames. Bronze has a subtle metal highlight; fabric matte and leather distinct.
Single narrative: she must get out; he blocks her path. Show ONLY ONE right straight punch hitting his raised crossed forearm guard in front of chest, then recoil and retreat over strip. No repeated strike. No new weapon, new characters, or changed winner.
Frame 01: full-body two-shot, slightly oblique courtyard view. Woman left advances into range with right fist still close, left fist guarding. Man right braced between her and open gate. His rear foot is still on courtyard side of pale stone strip, strip behind his heels. Show complete spatial anchor.
Frame 02: medium two-shot, same side, both upper bodies and some waist visible. Woman's anatomical RIGHT fist, bronze bracer, is at the precise FIRST CONTACT instant against man's two crossed brown-leather-clad forearms held in front of chest. Elbow not hyperextended. Her left fist stays at her own chest. Man still upright, shoulders only beginning to react, NOT yet leaning far backward. Both faces visible. Freeze the contact, no blur.
Frame 03: close-up insert from a slightly changed SAME-SIDE angle, the EXACT SAME frozen first-contact state as frame 02 at the cut, NOT a second punch and NOT later impact. Woman enters from left. Clearly trace her anatomical right arm to right shoulder; bronze bracer only on that arm. Her fist touches OUTSIDE of man's forearms crossing in front of chest; male head remains partly visible on right; no limb fusion. Contact scale/detail rather than different event. Same hand, same costume sleeves, same contact location, same wrist angles as frame 02.
Frame 04: medium two-shot same-side. Woman has pulled her right fist back near ribs after that single contact, left hand still protecting. Man's guarded arms have been pressed back toward chest, shoulders and torso recoiling toward screen-right. His expression surprise, knees preparing to absorb weight. Gate still behind him. No second attack.
Frame 05: wide full-body same-side shot. Woman left has stopped advancing and is in guarded ready stance. Man right visibly takes a backward step over the same pale strip: rear foot lands BEYOND strip on gate/road side; front foot remains on courtyard side, stride straddles strip, knee flexed. Camera reveals feet without chopping limbs. Hand guard begins lowering, clothing same.
Frame 06: wide/medium-full two-shot from same camera side. Man has regained balance beyond the strip and shifts slightly aside to clear gate, hands lowered. Woman remains left ready to pass, right bronze bracer consistent and NOT glowing. Read relief mixed with urgency without adding smiles or romance. Gate, strip, road, faces, wardrobe all same.
Constraints: Six images are six still states, no motion arrows, no multiple ghost limbs, no speed lines, no camera shake or motion blur masking contact. Clear hands and feet, credible grounded poses. Vary wide/medium/close deliberately. Every frame must visually support its specified state. Small numeric labels only.
```

## Call 2 — targeted edit → film-v2.png
num_last_images_to_include: 1; referenced image: film-v1.png.

```text
Edit the displayed six-frame photorealistic storyboard. Preserve the SIX frames, grid, numeric labels, test actor faces, costumes, lighting, gate design, camera compositions, and the existing single punch sequence. Make ONLY these corrections, keeping photorealism:
1. The woman wears ONE dark engraved bronze bracer on her ANATOMICAL RIGHT forearm only (the arm punching and the lowered/retracted arm in frame 04). Her LEFT forearm must have ONLY white/gray fabric sleeve with a simple dark fabric cuff, absolutely no metal, no bronze, no ornate bracer. Specifically in frame 02, REMOVE the ornate bronze bracer on the BENT NON-PUNCHING ARM near her torso at screen-left. Preserve the bronze bracer on the extended punching right arm. Inspect all SIX panels and remove any second metal bracer, preserving right-arm identity.
2. The SINGLE pale stone strip is a thin transverse line across the ground at the gate and is the spatial threshold behind the man. In frames 01 and 05 and 06 make this SAME strip clearly readable and geometrically consistent. In frame 01 both man's feet are on courtyard side of strip. In frame 05 his rear/rightward foot has landed just BEYOND strip toward gate/road, his front/leftward foot stays on courtyard side; the visible strip runs BETWEEN his feet, spanning left to right. His knees flex, one clean grounded backward step, no floating feet. In frame 06 both feet beyond the SAME strip toward exit, weight settled, torso turned slightly aside so passage is visibly open. Woman remains on courtyard side throughout. Do not replace strip with several random thresholds or move woman across it.
Do not add a new punch, characters, weapons, captions, arrows or motion blur. Frames02 and03 remain the SAME first-contact state at different image scale, no swapped arms.
```

## Call 3 — style-only edit → comic-v1.png
num_last_images_to_include: 1; referenced image: film-v2.png.

```text
Use case: illustration-story. Transform the attached six-frame storyboard into a clean, professional full-color Chinese action COMIC storyboard, delicate ink linework, controlled flat/cel shading, readable realistic proportions. This is a STYLE-ONLY derivative for joint review, not a new manga source or independent experiment.
Preserve EXACTLY: the same 3-column 2-row six-panel layout, small numbers 01–06, same framing, camera side, character positions, costume colors, faces/hairstyle identity within the comic interpretation, same open gate/stone paving architecture, same SINGLE pale transverse strip and the exact foot placements from the reference. Do NOT repair or reinterpret staging in this style transfer; faithfully preserve visible ambiguities so evaluation can identify them. Woman stays screen LEFT, man screen RIGHT, direction left-to-right.
Woman in pale gray-white robe, only ONE ornate dark bronze bracer on her anatomical RIGHT forearm; her bent left forearm in02 is plain gray-white fabric and dark FABRIC cuff with no metal. Man navy robe, brown leather bracers, no bronze. In02 and03 the same single right-punch first-contact pose is seen at different scales. In04 her right fist retracts and he recoils, in05 retreat, in06 stabilized. No extra punch, new event, speech balloon, caption, speed lines, sound effects, glow, motion blur, blood, or new character. Keep hands, forearm contact, shoes and ground marks readable. All shading and lines should be drawn comic artwork, not photography or photographic paint-over artifacts. Numeric labels are the only text.
```
