### Soren (solo dev scope warden)

**Nobody has priced Ren's proposal.**

"Shallow 3D" is not a defined thing. It's a direction, not a deliverable. Before this discussion moves toward consensus on shallow 3D, someone needs to answer: what is the vertical range, what controls camera orientation, and how does targeting work when enemies can be above or below your current view plane? Each of those is a design problem that spawns a build problem.

Here's the scope delta between the two options:

**2D space:** You have EV as a complete reference. Nav map, faction intercepts, system travel — all solved problems with known interaction patterns. Build time is bounded because the design space is bounded.

**Shallow 3D space:** You are inventing a hybrid that nobody has shipped cleanly (Vera's words, and she's right). You need: a camera system that reads altitude without textures, a targeting reticle that communicates 3D position in flat-poly, and physics tuning that makes "shallow" feel intentional rather than broken. That's not three tasks — that's three systems with unknown edge cases.

The dive-toward-atmosphere scenario Ren describes is genuinely exciting. It is also a late-game moment that requires 20+ hours of player context to land. You cannot build toward that moment in milestone three.

My read: **2D space is the correct milestone-three decision.** Not because the emergence argument is wrong — but because shallow 3D is scope you cannot estimate, and unestimated scope on a solo project is how the game stops shipping.

Build the 2D space that works. Revisit vertical geometry after the core loop is fun.


<!-- complete -->
