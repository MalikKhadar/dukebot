import random

default = [
    "Let's do this!",
    "My time to shine.",
    "This should be fun.",
    "Good luck!",
    "Let the games begin.",
    "It's go time!",
    "Here I go!",
    "Let's duel!",
    "I'll do my best!",
    "An equal! Don't hold back!",
    "It's anyone's game.",
    "Victory is mine!"
]

age_neg = [
    "Let me take you out of your misery!",
    "You’ve been around long enough.",
    "Putting me up against this old timer?",
    "Out with the old, in with the new!",
    "You’ve had enough time in the spotlight.",
    "Impressive. You’ve survived many battles.",
    "It’s about time you retire.",
    "You belong under the -RETIRED- line.",
    "So, you’ve stood the test of time.",
    "They say old is gold. You're living disproof.",
    "Aren’t you getting a little old for this?",
    "You’re getting awfully stale.",
    "You’ve got something of a reputation."
]

age_pos = [
    "I could do this in my sleep.",
    "This is getting too easy.",
    "Another one? Here goes.",
    "I’m getting too old for this.",
    "More fodder, I see.",
    "Let’s end this little career of yours.",
    "I’ve faced many opponents. Prepare yourself.",
    "Hmph. You’re green.",
    "Haven’t been around very long, have ya?",
    "I won’t go easy on you, rookie.",
    "Let’s get this over with.",
    "Blah blah blah, I’ve seen this before.",
    "Hey, treat this like a learning experience."
]

ratio_neg = [
    "I need this win.",
    "Losing isn’t an option!",
    "You need to be knocked down a peg.",
    "People like an underdog... Right?",
    "I can do this!",
    "Here goes!",
    "This’ll be tough.",
    "Oh, a worthy opponent.",
    "I’m gonna lose, aren’t I?",
    "Oh no… I don't wanna lose!",
    "[recounts extensive dramatic backstory]",
    "This is my toughest challenge yet.",
    "You’re going down.",
    "Things aren't looking to good for me..."
]

ratio_pos = [
    "What makes you think you can win?",
    "Piece of cake.",
    "Is this even a competition?",
    "Yield! This is your last chance!",
    "Hmph. Fodder.",
    "What's this? An easy win?",
    "Prepare to lose.",
    "Good luck. You’ll need it.",
    "Too bad you can’t just surrender.",
    "What a joke.",
    "I hate that I have to do this to you…",
    "I don’t lose. Sorry.",
    "Oh come on, this is easy peasy."
]

hist_neg = [
    "You again?",
    "I won’t lose this time.",
    "You won’t beat me again!",
    "You... You won't be so lucky this time!",
    "Things have changed since our last battle."
]

hist_pos = [
    "Ah, my old friend.",
    "So we meet again.",
    "Let’s put an end to our little rivalry.",
    "What makes you think you’ll win this time?",
    "Hah, it's just like old times."
]

class Topics:
    def __init__(self, age_diff=0,
                 ratio_diff=0, history=0):
        self.age_diff = age_diff
        self.ratio_diff = ratio_diff
        self.history = history

def talk(topics=None):
    t = topics
    if t == None:
        t = Topics()
    '''return phrase based on parameters'''
    #use history if history exists
    if t.history < 0:
        return random.choice(hist_neg)
    elif t.history > 0:
        return random.choice(hist_pos)
    
    #generic phrase if no age/ratio diff
    if t.age_diff == 0 and t.ratio_diff == 0:
        return random.choice(default)

    #else, comment on age or ratio
    age_weight = abs(t.age_diff)
    ratio_weight = abs(t.ratio_diff)
    #random choice on number line
    thresh = age_weight + ratio_weight
    n = random.uniform(0, thresh)
    #n can land in age or ratio zone

    if n < age_weight:
        #in age zone, choose by age sign
        if t.age_diff < 0:
            return random.choice(age_neg)
        else:
            return random.choice(age_pos)
    #in ratio zone, choose by ratio sign
    if t.ratio_diff < 0:
        return random.choice(ratio_neg)
    return random.choice(ratio_pos)