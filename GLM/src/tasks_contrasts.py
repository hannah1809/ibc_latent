# SOLVE QUESTION: USE CONTRASTS OR INDIVIDUAL CONDITIONS TO BUILD BETA MAPS?

tasks_contrasts = {
    'ArchiStandard': [
        'video_computation - video_sentence', # isolates the computation part from the language part (removes audio part)
        'audio_computation - audio_sentence'  # isolates the computation part from the language part (removes visual part)
    ],

    'Attention': [
        'spatial_incongruent - spatial_congruent', # ignore distractors vs. no distractors with spatial cue (attentional control?)
        'double_incongruent - double_congruent',   # ignore distractors vs. no distractors without spatial cue (cognitive control?)
        'spatial_cue - double_cue'                 # cued vs. uncued probe (spatial attention?)
    ],

    'Catell': 
    '',

    'ColumbiaCards': 
    '',

    'Discount': 
    '',

    'Enumeration': 
    '',

    'HcpGambling': 
    '',

    'HcpLanguage': 
    '',

    'HcpRelational': 
    '',

    'HcpWm': 
    '',

    'MVEB': 
    '',

    'MathLanguage': 
    '',

    'SelectiveStopSignal': 
    '',

    'StopNogo': 
    '',

    'StopSignal': 
    '',

    'Stroop': 
    '',

    'TwoByTwo': 
    '',

    'VSTM': 
    '',

    'VSTMC': 
    '',

    'WardAndAllport': 
    ''
}