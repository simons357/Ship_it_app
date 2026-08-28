# AI Surgeon — Adaptive Systems, Progression, and What "Teach One" Actually Is

**Simons Medical Innovations, LLC** · August 2026
Companion to `AI-Surgeon-Scoped-Concept.md` and `AI-Surgeon-Curriculum.md`.
All of this is now built and running in `ai-surgeon-systems.js`, wired into the appendectomy module and verified by a headless playtest.

---

## The part you were right to question

You asked how anyone is expected to *teach* inside a game, and the honest answer is that what is in the prototype right now is not teaching. It is a multiple-choice question with the word "teach" written above it. It was a placeholder and you caught it.

Here is what Teach One should be, and it costs almost nothing to build because it is the engine you already have, running backwards.

**You supervise a junior doing the operation.** An AI resident has the knife. The camera is over their shoulder instead of over yours. They work through the same eleven steps, and they are *deliberately imperfect* — they hesitate at the mesoappendix, they reach for a Mayo when they need a Metzenbaum, they put traction on a retrocecal appendix they cannot see. Your job is four things and they are the four things an attending actually does:

You **call the step** before they start it, in your own words, from a short list of phrasings — and getting the sequence right is the part that proves you know the operation, because nobody can prompt you.

You **stop them** before the error, not after. There is a window, roughly two seconds wide, between the junior committing to a wrong move and the wrong move happening. Stopping them inside that window is worth the most points in the game. Stopping them when they were about to do it correctly costs you a little, because an attending who interrupts constantly is not teaching either.

You **answer their questions.** They ask you what you ask the player during Do One — why this instrument, where is the artery, what happens if I am wrong here — and now it is free text and it is your answer being scored, not a choice you picked off a list.

You **decide when to take the knife.** This is the same handover mechanic in the other direction, and it is the whole point. Letting the junior struggle a little is how they learn. Letting them struggle past the point where the patient is paying for it is the error. The scoring makes taking over at the right moment worth more than either taking over early or letting them push on and get away with it.

Teach One built that way is the most valuable forty points in the product, and it is the only phase that could not be replaced by a textbook.

---

## Then you graduate

Completing a module's four phases clears the module. Clearing the year clears the year. When the residency ladder is finished you become an **attending**, and three things change permanently.

You operate alone. No demonstration phase, no hint floor, no "identify first" prompt — the identify-before-you-cut rule still applies but nothing tells you it is time. The full tray, every time.

You start getting handed the cases that were locked. Attending-level cases are not just harder anatomy; they are cases where the right answer is sometimes not to operate.

And you become the person in Teach One for somebody else. In the co-op mode, a real player in residency can be assigned to your room. Your score becomes partly *their* outcome. That is the honest version of what being an attending feels like and no other surgical training product does it.

**Super-specialty** is optional and it is above attending. Cardiac, neuro, transplant, paediatric. Highest multipliers, steepest penalties, and the entry requirement is a competency percentage in the relevant domains rather than a total score — you cannot buy your way in with volume.

---

## Every sensor the phone will actually give a web page

You said use all that apply. These all apply, they are all reachable from a browser today, and they are all now in `AISS.Sensors`:

| Signal | API | What it is worth |
|---|---|---|
| Accelerometer + gyroscope | `DeviceMotionEvent` | Hand tremor and stillness, measured directly at 60 Hz. This is the good one. A steady hand on a phone is measurably different from an unsteady one, and it is free. |
| Device attitude | `DeviceOrientationEvent` | Where the phone is aimed. Feeds the gaze system. |
| Touch force | `Touch.force` / `PointerEvent.pressure` | Grip pressure on hardware that reports it. Tightening grip is a real stress tell. |
| Attention | `visibilitychange` | You left the case. Free, no permission, and it is a genuine signal. |
| Ambient light | `AmbientLightSensor` | Room conditions. Chrome only, behind a flag, harmless when absent. |
| Voice | `SpeechRecognition` | You say "ten blade" out loud instead of tapping it. Already wired into the scrub mechanic. |
| Heart rate | Web Bluetooth GATT `0x180D` | The cheap wearable. Any standard chest strap or armband, $30–60, no custom hardware. |

iOS requires a user tap before granting motion access, so it is a button on the opening screen, not something that happens silently. There is no eye tracker on a phone, so gaze is the honest proxy: a ray from the centre of the screen. In a headset that same line of code becomes real head gaze with no change to the module.

**What the strap adds** is a baseline you cannot fake. Heart rate is compared against *your own* rolling baseline, not a population number, so it works on a 22-year-old athlete and a 55-year-old attending equally.

---

## Coherence, defined — because you said you need to pin this down

Here is a concrete definition to argue with.

Coherence as it exists now measures **how right you are and how long you take**. That is one axis. It is not enough, because it cannot tell the difference between a player who is cruising and a player who is holding on by their fingernails and about to fail.

So the system now runs **two axes**: performance (coherence) and **load** (arousal, from the sensors above). The intervention is different in each corner, and that is the part worth defending in a patent:

| | Settled | Overloaded |
|---|---|---|
| **Accurate** | Push. Remove hints, tighten gesture tolerance, run the clock 15% faster. | Hold. Do not add load. This player is performing well at a cost they cannot sustain, and adding difficulty here produces a failure that teaches nothing. |
| **Struggling** | Push. This is boredom, not overwhelm. The correct response to a disengaged learner is more, not less. |Back off. Restore hints, widen tolerance, slow the deterioration to 78%. |

The single most important cell is *accurate and overloaded*. Every adaptive-difficulty system in every game reads "performing well" and makes it harder. That is the wrong call here, and being able to distinguish it is what a biometric input is actually for.

**Regulatory reality, said plainly.** Biometric identifiers are a regulated data class — Illinois BIPA, GDPR Article 9, Texas CUBI. The design position is enforced in the code, not just asserted: derive on device, keep the band, discard the signal. Heart rate is never stored, never transmitted, and only the word — settled, engaged, loaded, overloaded — survives into the debrief. That position is worth stating before this claim goes into any public document, because a school district's counsel will ask, and "we do not retain it" is a much shorter conversation than the alternative.

---

## Patient safety, and the handover mechanic

You said it and the scoring now says it: **patient safety is number one, and knowing when to turn it over beats FAFO.**

The way that is enforced is that **the ceiling on gambling sits below the floor on the right call.**

| Decision | Points |
|---|---|
| Handed over inside the window | **+40** — the highest single decision in the module |
| Pushed on past the envelope and got away with it | +22 |
| Handed over early, before it was needed | +8 |
| Handed over after harm was already done | −6 |
| Pushed on past the envelope and the patient paid | **−55** |

A player who stays and wins scores less than a player who handed over. That is not a bug and the debrief says so out loud: *"You were outside the envelope; the outcome was availability, not skill. The version of this where it does not work is the same decision."*

There is a **Hand it over** button visible during every Do One phase, in every module, with no penalty hidden inside it. The button being always available is the point. And the headline number on a player's profile is not points and it is not speed — it is the **harm-free streak**, consecutive cases with no patient morbidity. That is the only streak that counts toward institutional awards.

---

## Measuring progress exactly

Not one score. Seven competencies, tracked separately, persisted between sessions, reported to the percent, with the weakest one named and a specific remediation attached:

Anatomy identification · Instrument naming · Technique and maneuver · Judgement at forks · Monitor vigilance · Safety and handover · Teaching.

The debrief shows this run and lifetime side by side, and then says one sentence like: *"Instrument naming is your weakest at 61% (14 of 23). Run skills-lab module 00.4, the tray. It is fifteen minutes and it fixes this outright."*

That is the difference between a game telling you that you lost and a training tool telling you what to do on Tuesday.

---

## Decision forks

Three are live in the appendectomy. **Nothing is marked correct.** Every option carries the rationale a real surgeon would give for it, every option has a consequence that applies to the rest of the case, and once you choose it locks and the button says *"I own that."*

The incision length fork is the clearest one. Three centimetres for the scar on a nineteen-year-old, five for exposure, or palpate under anaesthesia first and site it over what you actually feel. The third answer is what experienced surgeons do and it is why their incisions look lucky — but it costs thirty seconds and the module does not tell you it was the good one until the debrief.

The retrocecal fork is the one that teaches. Pull harder, mobilise the cecum along the white line of Toldt, extend the incision, or go retrograde. Pulling harder works — and it is how a retained appendiceal tip happens, which you will not find out until later.

---

## Hooks, honestly

You want it addictive. It should be. But a training product's retention mechanics have an obligation an ordinary game does not, because the behaviour the hooks reinforce is the behaviour the player carries into a real room. So every hook is hung off safety rather than speed:

The **harm-free streak** is the front-of-profile number. Unlocks are content, not power — anatomical variants (retrocecal, pelvic, subhepatic, situs inversus), a cadaveric-detail model at full fascial density, night float with 3 a.m. lighting and one instrument missing from the tray, a paediatric case with a parent asking you questions. **Real prizes** — merch, scholarships — are funded by schools, hospital systems and STEM grants, gated behind a verified institutional account, and awarded on the safety streak and competency percentages rather than on volume or spend.

---

## Humor

It belongs in there for exactly the reason you gave: people in operating rooms are funny because they have to be, and it is how the pressure gets discharged. It is in, with hard fences that are enforced in code:

Never while the patient is unstable. Never after a patient has been harmed, in that case or in the debrief. Never from the head of the bed — the monks do not participate, which is the only reason the blame-anaesthesia joke lands at all. Never at the patient's expense. And never at the player's expense while they are behind.

The scrub tech gets the best lines. *"That is a Mayo. You asked for a Mayo. You wanted a Metzenbaum. Those are three different sentences."*

---

## What is built and what is next

Built and playtested: profile selection, two-axis adaptive difficulty, phone sensor fusion, voice instrument calls, gaze and attention tracking, free-text ask-the-attending over a 66-document index of the module's own content, three decision forks, the handover mechanic, seven-domain competency tracking, unlocks, and the fenced humor system.

Next, in order: the real Teach One described at the top of this document, because the current one is a placeholder and you know it. Then Module 01, the finger. Then the anaesthesia monks. Laparoscopic technique gets its own skills-lab strand before Module 13, because the fulcrum effect and working off a screen are motor skills that have to be taught separately from the anatomy — you cannot learn lap surgery by doing open surgery faster.
