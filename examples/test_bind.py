from octopus.sequence.runtime import *
from octopus.sequence.control import Bind

from twisted.internet import defer
defer.Deferred.debug = True

v = variable(0, "i", "i")
d = variable(False, "b", "b")

d_ctrl = Bind(d, v, lambda x: x > 5)

s = sequence(
<<<<<<< HEAD
	log("Running"),
	loop_while(v < 10, [
		increment(v),
		log("v = " + v + "; d = " + d),
		wait(1),
	]),
	log("Stopping experiment")
=======
    log("Running"),
    loop_while(v < 10, [
        increment(v),
        log("v = " + v + "; d = " + d),
        wait(1),
    ]),
    log("Stopping experiment")
>>>>>>> bad-master
)
s.dependents.add(d_ctrl)

run(s)


