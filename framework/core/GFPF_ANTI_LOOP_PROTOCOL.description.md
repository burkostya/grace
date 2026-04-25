### GFPF_ANTI_LOOP_PROTOCOL

The Anti-Loop Protocol is a mechanism for strictly controlling the state of an implementer agent during the testing and debugging phase, aimed at preventing infinite cycles of logic degradation ("error -> failed fix -> error again").

When an autonomous agent (LLM) encounters a recurring error, its context overflows with a history of failures, causing the probability of finding the correct solution to drop sharply. The Anti-Loop Protocol solves this problem by forcibly tracking attempts and escalating the level of intervention. In the early stages, the protocol provides the agent with "cheat sheets" (checklists); in the middle stages, it forces the use of external search tools; and in the late stages, it forcibly stops work (Fallback), delegating the task to a human or triggering a reflection process (Superposition).

