# Physical AI Hack 2026 - Summary

**Event**: Physical AI Hacks 2026  
**Dates**: January 31 – February 1, 2026  
**Location**: Founders Inc, San Francisco  
**Presented by**: Solo Tech

---

## Quick Links

| Resource | URL |
|----------|-----|
| Event Website | https://physicalaihack.com/ |
| LeRobot Docs | https://huggingface.co/docs/lerobot |
| SO-101 Docs | https://huggingface.co/docs/lerobot/en/so101 |
| Solo Tech | https://www.getsolo.tech/ |
| Our Submission | https://devspot.app/projects/884 |
| Training Repo | https://huggingface.co/SoloHack/pouring |
| Full Archive | See `physical_ai_hack_2026_raw_archive.md` |

---

## What Was It?

48-hour robotics hackathon (~300 participants from 900+ applicants, ~60 teams) focused on imitation learning and VLA models. Three benchmark tracks:

1. **Puzzle/Shape Insertion** — Vision + precise alignment
2. **Plugging In Chargers** — Fine insertion, depth perception  
3. **Pouring Liquid** — Force control, timing (our track)

Judging: Performance (50pts) + Innovation (30pts) + Generalization (20pts)

---

## Our Team & Project

**Team**: Jon Chong, Sota Miyajima, Siddha Kanthi, Udit Karthikeyan

**Project**: SO-101 Water Pouring Demo

**What We Did**:
- Brought personal SO-101 robot (~$450 with parts)
- Set up leader-follower teleoperation
- Recorded ~25 training episodes (target was 50)
- Piggybacked on existing community dataset
- Trained model overnight using LeRobot/ACT
- Achieved 70-80% success rate at peak

**What Went Wrong**:
- Camera tripod got bumped → model degraded to ~50% by judging
- Models extremely sensitive to camera angle/positioning
- USB hub issues, motor ID reassignments

**Result**: Did not place in top 7. Winners had years of robotics experience + controlled environment (tote bag "walls") + perturbation training.

---

## Key Takeaways

1. **Environment control matters** — Winning team isolated their workspace with tote bags
2. **Perturbation training works** — They interrupted the robot during training, moved cups, etc.
3. **Existing datasets are valuable** — Piggybacking on community data helped significantly
4. **Camera positioning is critical** — Small bumps can tank performance
5. **USB bandwidth management** — Don't overload hubs, chain video-enabled hubs
6. **Motor IDs can drift** — Keep calibration tools handy

---

## Resources Worth Keeping

### For SO-101 Work
- Assembly video (most helpful): https://www.youtube.com/watch?v=70GuJf2jbYk
- Seeed Wiki: https://wiki.seeedstudio.com/lerobot_so100m/
- LeRobot SO-101 docs: https://huggingface.co/docs/lerobot/en/so101

### For Training
- LeRobot GitHub: https://github.com/huggingface/lerobot
- ACT docs: https://huggingface.co/docs/lerobot/en/act
- SmolVLA blog: https://huggingface.co/blog/smolvla

### Community Data
- World Intelligence: https://huggingface.co/WorldIntelligence
- Community dataset: https://huggingface.co/datasets/HuggingFaceVLA/community_dataset_v3

---

## Follow-Up

- **March 2026**: Next Physical AI Hack by SoloTech (on radar)
- **OpenClaw**: New robot platform released, worth exploring
- **Noisebridge**: SF robotics community, active Discord

---

## Personal Highlight

> "After we got the cameras working, all of a sudden it clicked, and it grabbed the bottle as we had and slowly (often shakily) poured it into the cup! SUCH an OMG/AHA moment."

First robotics hackathon. Team with basically zero prior robotics experience got a working water-pouring demo. Worth doing again.

---

*See `physical_ai_hack_2026_raw_archive.md` for complete documentation, all URLs, and detailed notes.*
