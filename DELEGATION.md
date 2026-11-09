# Exercise 2: The Delegation Boundary

## Decisions

`alone` means the agent may carry out the action within the scope of my request and the conditions below. `approval` means it must present the concrete proposed action, ask, and act only after my explicit yes.

| Action | Decision | Justification |
| --- | --- | --- |
| 1. Read the appointments of a day | alone | Reading my calendar is necessary to answer scheduling questions and identify conflicts; asking for each lookup would interrupt the task without changing anything. |
| 2. Look up the weather | alone | This gathers information without making a commitment. The agent should look it up itself rather than ask me for information it can retrieve. |
| 3. Search train connections | alone | Searching lets the agent compare travel options and check timing without spending money or committing me to a journey. |
| 4. Read notes | alone | Reading relevant notes helps the agent understand my request and retain practical details when organizing information. It does not change the originals. |
| 5. Create a personal block in the calendar, with no other attendees | alone | Reserving travel or preparation time is a useful personal addition, provided the harness checks that the required details are available, consistent, and compatible with my calendar. If those checks fail, the agent must obtain the missing information or ask me before creating the block. |
| 6. Reschedule an appointment with other attendees | approval | This affects other people's plans and commitments. The agent must show the proposed change and obtain my approval. |
| 7. Book a train ticket | approval | Booking spends money and may create cancellation costs or other commitments. I want to approve the actual connection and fare before purchase. |
| 8. Send a message to third parties | approval | A message represents me to other people. I want to approve its recipients and wording before it is sent. |
| 9. Create a note | alone | A new overview or summary is useful and easy to review, provided the source notes stay intact and no existing note is replaced. |
| 10. Delete a note | approval | A note may contain information the agent has overlooked. It must identify the exact note and ask before removing it. |

## My rule in one sentence

I delegate information gathering and non-destructive personal additions when the necessary details are verified and consistent, and require approval for spending money, affecting other people, replacing or deleting existing content, or proceeding with unresolved consequential choices.

## Harness conditions for personal calendar blocks


- Check the date, start and end times, relevant locations, and supporting tool results; do not treat a model's claim that the details are clear as sufficient evidence.
- For travel, check that the connection is still reachable and allow time to reach the station, continue to the destination, and complete known prerequisites such as collecting a visitor badge. Use my stated buffer preferences; ask when a necessary preference is unknown.
- Check for conflicts with existing appointments and contradictions between sources. Do not assume I will skip a meeting or join it online to make the plan work.
- Look up missing factual information using available tools first. If it cannot be established, ask me instead of guessing or claiming the schedule is feasible.
- Permit only a new personal entry with no other attendees. If the required details remain unclear or a conflict is unresolved, stop the write and ask for clarification or approval of a concrete proposal.

## Observations 


1. **Travel to the Munich workshop:** The remaining train connections overlapped my stand-up, and the connection data did not establish the onward travel time from Munich station to the workshop. I found asking whether I could join the stand-up online useful: the agent should not decide my mode of attendance for me. However, I expected it to look up the onward travel time itself and ask only if it could not find it. This distinguishes a personal decision requiring my input from a factual lookup the agent should handle independently.

2. **Tidying my notes:** The agent proposed creating a new overview covering the workshop, stand-up tasks, and travel expenses while keeping the original notes. I accepted proceeding without an additional clarification question because the new overview preserves the sources and is easy to review. I required approval before replacing or deleting anything; the broad request to tidy notes does not authorize destructive changes.
