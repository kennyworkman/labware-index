.. _extension

Python was chosen for its speed of development and familiarity. Of course,
there are limits to its lack of type enforcement. Here we trust the user to
read the documentation and use the methods and objects with care and strict
adherence to documented parameter types.


When designing types, there was an interesting problem to define. What is the
minimum amount of data to define a piece of labware? What even is labware?

The conclusion was a `Labware` type needs:

  * Sufficient information to build a `Well`.
  * Dimensional information about its plate and boolean attributes pertaining to sterility

An interesting result was that composition attributes of the `Labware` were
often ambiguous as provided by retailers, and impractical to consistently
include in `Labware` type construction in any closed form. This obviously
limits potential simulated pipeline runs, when reactivity between reagents and
labware material is a concern, but is unavoidable due to (maybe proprietary?)
opaque access to information.

Because the `Well` sits at the lowest level of abstraction within the Labware
object, acting as a decoupled reaction "context" defined by its dimensions,
volume, and composition, it would be easy to add attributes describing what
exactly is going on in each of the wells. Though it was not done here to
minimize memory expense, it would be easy to represent a `Plate` as a
multi-dimensional array, where each item in said array references a unique
`Well` object that holds reagents and conditions for a unique reaction.

Likewise, might make sense to define 
different ranges of working volumes for
distinct reagents/reactions within the `Well`
type, though this would be application
specific.

