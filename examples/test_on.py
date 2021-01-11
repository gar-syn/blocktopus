from octopus.sequence.runtime import *
from octopus.sequence.util import Trigger
from twisted.internet import reactor


def fn ():
<<<<<<< HEAD
	print ("fn called")
	return sequence(
		log("fn called"),
		set(v, False)
	)
=======
    print ("fn called")
    return sequence(
        log("fn called"),
        set(v, False)
    )
>>>>>>> bad-master

v = variable(False, "v", "v")
v2 = variable(False, "v", "v")

o1 = Trigger(v == True, fn)
o2 = Trigger(v2 == True, log("o2 triggered"), max_calls = 1)

s = sequence(
<<<<<<< HEAD
	log("Loading o"),
	wait("8s"),
	set(v2, True),
	wait("1s")
=======
    log("Loading o"),
    wait("8s"),
    set(v2, True),
    wait("1s")
>>>>>>> bad-master
)

s.dependents.add(o1)
s.dependents.add(o2)

reactor.callLater(2, v.set, True)
reactor.callLater(4, v.set, True)
reactor.callLater(6, v.set, True)

run(s)

