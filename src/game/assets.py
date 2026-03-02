
## Placeholders for now


bg_base = [
    [r'''
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
     '''],
]

sh_idle_frames = [
        [
        r"   /\_/\   ",
        r"  ( o.o )  ",
        r"   > ^ <   "
        ],
        [
        r"   /\_/\   ",
        r"  ( -.- )  ",
        r"   > ^ <   "
        ]
    ]

sh_play_frames = [
        [
        r"   /\_/\  / ",
        r"  ( ^.^ )/  ",
        r"   > ^ <    "
        ],
        [
        r" \ /\_/\    ",
        r"  \( ^.^ )  ",
        r"    > ^ <   "
        ] 
]

sh_feed_frames = [
            [
            r"   /\_/\   ",
            r"  ( O.O )  ",
            r"   > o <   "
            ], 
            [
            r"   /\_/\   ",
            r"  ( >.< )  ",
            r"   > ~ <   "
            ]    
        ] 

bg_anims = {
    "BG" : {
        "Position" : (0,0),
        "Frames" : bg_base
    }
}

shellcat_anims = {
    "SHELLCAT_IDLE" : {
        "Position" : (10,45),
        "Frames" : sh_idle_frames
    },
    "SHELLCAT_PLAY" : {
        "Position" : (10,45),
        "Frames" : sh_play_frames
    },
    "SHELLCAT_FEED" : {
        "Position" : (10,45),
        "Frames" : sh_feed_frames
    }
}





