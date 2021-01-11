from octopus.sequence.runtime import *

def fn ():
<<<<<<< HEAD
	return sequence(
		log("fn called")
	)

run(sequence(
	call(fn)
=======
    return sequence(
        log("fn called")
    )

run(sequence(
    call(fn)
>>>>>>> bad-master
))

