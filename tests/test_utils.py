def repeat(times):
    def repeat_helper(f):
        def call_helper(*args):
            for i in range(0, times):
                print("Run Nr. %i for %s" % (i, f.__name__))
                f(*args)

        return call_helper

    return repeat_helper