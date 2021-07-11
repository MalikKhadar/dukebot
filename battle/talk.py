import random

default = [
    "Let's do this!",
    "My time to shine.",
    "This should be fun.",
    "Good luck!",
    "It's go time!",
    "Here I go!",
    "Let's duel!",
    "I'll do my best!",
    "I won't hold back!",
    "It's anyone's game.",
    "Victory is mine!",
    "Let me show ya what I've got!",
    "(:<",
    "I was made for this!",
    "I'm ready!",
    "Prepare yourself!",
    "En garde!",
    "Are you ready?",
    "This is it!",
    "SHOW ME YOUR MOVES"
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
    "You’ve got something of a reputation.",
    "You've lost your luster.",
    "It's my turn! You're going down!",
    "YOUR CRUEL REIGN SHALL COME TO AN END",
    "I will be the champion!",
    "Time's up! Your lucky streak is over.",
    "Your little tune's getting old.",
    "Got any last words?"
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
    "There's a reason I've been around so long.",
    "I've been around a long time. And you won't!",
    "You lack practice.",
    "I've got the experience, amateur.",
    "YOU ARE UNTESTED. I STAND UNBENT LIKE STEEEEEEEL",
    "I've withstood the sands of time. This is nothing.",
    "A gnarled old branch dulls the blade that severs a sapling.",
    "I'm an expert. It's a shame you have to face me!"
]

ratio_neg = [
    "I need this win.",
    "Losing isn’t an option!",
    "You need to be knocked down a peg.",
    "People like an underdog... Right?",
    "I can do this!",
    "Here goes!",
    "This’ll be tough.",
    "I’m gonna lose, aren’t I?",
    "Oh no… I don't wanna lose!",
    "[recounts extensive dramatic backstory]",
    "This is my toughest challenge yet.",
    "You’re going down.",
    "Things aren't looking to good for me...",
    "It's time to even the odds.",
    "I won't give up hope!",
    "It's not over yet!",
    "THE FLAME OF HOPE BURNS WITHIN MEEEEEEE",
    "Winners never quit... and quitters never win!",
    "I'll never stop fighting!",
    "I believe..."
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
    "I don’t lose. Sorry.",
    "Oh come on, this is too easy.",
    "I'm going to win. Why bother?",
    "Give up while you still can.",
    "Take this: L",
    "You'll need more than luck.",
    "There's no chance I'll lose.",
    "I FORSEE VICTORY. FACE YOUR DEMISE",
    "Your defeat is statistically likely.",
    "This is a waste of my abilities."
]

hist_neg = [
    "I won’t lose this time.",
    "You won’t beat me again!",
    "You... You won't be so lucky this time!",
    "Things have changed since our last battle.",
    "I've been waiting for this moment.",
    "I'm back. And I'm stronger now.",
    "And so we clash once again.",
    "I hope you didn't get too used to winning.",
    "I'm not holding back this time!",
    "IT'S TIME TO TILT THE SCALES"
]

hist_pos = [
    "Ah, my old friend.",
    "So we meet again.",
    "Let’s put an end to our little rivalry.",
    "What makes you think you’ll win this time?",
    "Hah, it's just like old times, isn't it?",
    "You're persistent, I'll give you that.",
    "Look who came crawling back.",
    "You again? Back for more?",
    "How about I put you down for good?",
    "CRUSHING YOU AGAIN SHALL FILL ME WITH GLEE"
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