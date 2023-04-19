
####### Problem 3 #######

test_cases = [('book', 'back'), ('kookaburra', 'kookybird'), ('relevant','elephant'), ('AAAGAATTCA', 'AAATCA')]
alignments = [('boo--k', 'b--ack'), ('kooka-bu-rra-', 'kook-yb-ir--d'), ('relev--ant','-ele-phant'), ('AAAGAATTCA', 'AAA---T-CA')]

def MED(S, T):
    if (S == ""):
        return(len(T))
    elif (T == ""):
        return(len(S))
    else:
        if (S[0] == T[0]):
            return(MED(S[1:], T[1:]))
        else:
            return(1 + min(MED(S, T[1:]), MED(S[1:], T)))


def fast_MED(S, T, MED={}):
    # TODO -  implement memoization
    if (S, T) in MED:
        return MED[(S, T)]
    elif len(S)==0:
        MED[(S, T)] = len(T)
    elif len(T)==0:
        MED[(S, T)] = len(S)
    else:
        if (S[0] == T[0]):
            MED[(S, T)] = fast_MED(S[1:], T[1:])
        else:
            MED[(S, T)] = 1 + min(fast_MED(S, T[1:]), fast_MED(S[1:], T))
    return MED[(S, T)]
    pass

def fast_align_MED(S, T, MED={}):
    # TODO - keep track of alignment
    align_S=""
    align_T=""
    while True:
        # three cases when editing
        same=fast_MED(S,T)
        insert=fast_MED(S, T[:-1])
        delete=fast_MED(S[:-1], T)

        # do the diogonal backtrace
        min_=min(same,insert,delete)
        
        if min_==same:
            # backtrace with no need to change
            align_S=S[-1]+align_S
            align_T=T[-1]+align_T       
            S=S[:-1]
            T=T[:-1]
        else:
            # backtrace is either insertion or deletion based on minimum
            if min_==insert:
                align_S="-"+align_S
                align_T=T[-1]+align_T
                T=T[:-1]  
            elif min_==delete:
                align_T="-"+align_T
                align_S=S[-1]+align_S           
                S=S[:-1]

        if len(S)==0 or len(T)==0:
            # when one of the letter is empty
            align_S="-"*len(T)+S+align_S
            align_T="-"*len(S)+T+align_T
            return align_S,align_T
    pass

def test_MED():
    for S, T in test_cases:
        assert fast_MED(S, T) == MED(S, T)
                                 
def test_align():
    for i in range(len(test_cases)):
        S, T = test_cases[i]
        align_S, align_T = fast_align_MED(S, T)
        assert (align_S == alignments[i][0] and align_T == alignments[i][1])
