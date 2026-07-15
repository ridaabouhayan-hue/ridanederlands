/* Nexus of Language — course content (plain JS global; no fetch, so it works
   from file:// / Google Drive).

   Unit schema:
     { id, title, subtitle, icon, comingSoon?, dialogue[], lessons[] }
   Dialogue line: { speaker, voice:'m'|'f', nl, en }
   Lesson: { id, label, title, newWords[]?, grammarNote?, exercises[] }
   Exercise.type: 'mcq' | 'wordbank' | 'typing' | 'listening'
     - itemId ties an exercise to a vocab item for SRS tracking
     - `correct` may be an array of accepted answers (alternatives)
     - typing exercises with audioText + a spoken prompt are production
       ("app asks, you answer") practice
     - listening: audioText + mode ('mcq'|'typing') + optional voice */

const COURSE = {
  sections: [
    {
      id: 's1',
      title: 'Sectie 1 · De Basis',
      units: [

        /* ---------------- UNIT 1 ---------------- */
        {
          id: 'u1',
          title: 'Jezelf voorstellen',
          subtitle: 'Introduce yourself',
          icon: '👋',
          dialogue: [
            { speaker: '👩', voice: 'f', nl: 'Hallo! Ik heet Fatima. Hoe heet jij?', en: "Hello! My name is Fatima. What's your name?" },
            { speaker: '🧑', voice: 'm', nl: 'Hoi Fatima, ik ben Youssef.', en: "Hi Fatima, I'm Youssef." },
            { speaker: '👩', voice: 'f', nl: 'Waar kom je vandaan?', en: 'Where are you from?' },
            { speaker: '🧑', voice: 'm', nl: 'Ik kom uit Marokko. En jij?', en: 'I come from Morocco. And you?' },
            { speaker: '👩', voice: 'f', nl: 'Ik kom uit Syrië. Ik woon nu in Utrecht.', en: 'I come from Syria. I live in Utrecht now.' },
            { speaker: '🧑', voice: 'm', nl: 'Leuk je te ontmoeten!', en: 'Nice to meet you!' }
          ],
          lessons: [
            {
              id: 'l1', label: 'Les 1', title: 'Nieuwe woorden',
              newWords: [
                { id: 'u1_w1', nl: 'hallo', en: 'hello' },
                { id: 'u1_w2', nl: 'ik heet...', en: 'my name is...' },
                { id: 'u1_w3', nl: 'ik kom uit...', en: 'I come from...' },
                { id: 'u1_w4', nl: 'ik woon in...', en: 'I live in...' },
                { id: 'u1_w5', nl: 'hoe heet jij?', en: "what's your name?" }
              ],
              exercises: [
                { id: 'u1_l1_e1', type: 'mcq', itemId: 'u1_w1', prompt: { en: 'What does "hallo" mean?' }, options: ['hello', 'goodbye', 'thank you', 'sorry'], correct: 0 },
                { id: 'u1_l1_e2', type: 'mcq', itemId: 'u1_w2', prompt: { en: 'How do you say "my name is..." in Dutch?' }, options: ['ik woon in...', 'ik heet...', 'ik kom uit...', 'hallo'], correct: 1 },
                { id: 'u1_l1_e3', type: 'wordbank', itemId: 'u1_w2', prompt: { en: 'Build the sentence: "My name is Fatima."' }, correct: 'Ik heet Fatima.', words: ['Ik', 'heet', 'Fatima.', 'woon', 'kom'] },
                { id: 'u1_l1_e4', type: 'typing', itemId: 'u1_w1', prompt: { en: 'Type the Dutch word for "hello".' }, correct: 'hallo' },
                { id: 'u1_l1_e5', type: 'listening', itemId: 'u1_w2', audioText: 'Hallo, ik heet Fatima.', lang: 'nl', voice: 'f', mode: 'mcq', prompt: { en: 'What did you hear?' }, options: ['Hallo, ik heet Fatima.', 'Hallo, ik woon in Utrecht.', 'Hallo, ik kom uit Syrië.', 'Tot ziens, Fatima.'], correct: 0 }
              ]
            },
            {
              id: 'l2', label: 'Les 2', title: 'Oefenen',
              newWords: [
                { id: 'u1_w6', nl: 'waar kom je vandaan?', en: 'where are you from?' },
                { id: 'u1_w7', nl: 'leuk je te ontmoeten', en: 'nice to meet you' },
                { id: 'u1_w8', nl: 'tot ziens', en: 'goodbye' }
              ],
              grammarNote: {
                nl: 'In het Nederlands begint een zin over jezelf met "ik" + het werkwoord: "ik heet...", "ik kom uit...", "ik woon in...".',
                en: 'In Dutch, a sentence about yourself starts with "ik" ("I") plus the verb: "ik heet..." (I am called), "ik kom uit..." (I come from), "ik woon in..." (I live in).'
              },
              exercises: [
                { id: 'u1_l2_e1', type: 'mcq', itemId: 'u1_w6', prompt: { en: 'How do you ask "where are you from?"' }, options: ['hoe heet jij?', 'waar kom je vandaan?', 'tot ziens', 'leuk je te ontmoeten'], correct: 1 },
                { id: 'u1_l2_e2', type: 'wordbank', itemId: 'u1_w3', prompt: { en: 'Build the sentence: "I come from Morocco."' }, correct: 'Ik kom uit Marokko.', words: ['Ik', 'kom', 'uit', 'Marokko.', 'woon'] },
                { id: 'u1_l2_e3', type: 'typing', itemId: 'u1_w4', prompt: { en: 'Translate: "I live in Utrecht."' }, correct: ['Ik woon in Utrecht', 'Ik woon nu in Utrecht'] },
                { id: 'u1_l2_e4', type: 'mcq', itemId: 'u1_w7', prompt: { en: 'What does "leuk je te ontmoeten" mean?' }, options: ['see you later', 'nice to meet you', 'how are you?', 'welcome'], correct: 1 },
                { id: 'u1_l2_e5', type: 'listening', itemId: 'u1_w8', audioText: 'Tot ziens!', lang: 'nl', voice: 'f', mode: 'typing', prompt: { en: 'Type what you hear (in Dutch).' }, correct: ['Tot ziens'] },
                { id: 'u1_l2_e6', type: 'wordbank', itemId: 'u1_w6', prompt: { en: 'Build the question: "Where are you from?"' }, correct: 'Waar kom je vandaan?', words: ['Waar', 'kom', 'je', 'vandaan?', 'heet'] }
              ]
            },
            {
              id: 'l3', label: 'Les 3', title: 'Herhalen & spreken',
              exercises: [
                { id: 'u1_l3_e1', type: 'mcq', itemId: 'u1_w5', prompt: { en: 'How do you ask someone their name?' }, options: ['hoe heet jij?', 'waar kom je vandaan?', 'tot ziens', 'ik woon in...'], correct: 0 },
                { id: 'u1_l3_e2', type: 'typing', itemId: 'u1_w2', prompt: { en: 'Translate: "My name is Youssef."' }, correct: ['Ik heet Youssef', 'Mijn naam is Youssef'] },
                { id: 'u1_l3_e3', type: 'wordbank', itemId: 'u1_w7', prompt: { en: 'Build the sentence: "Nice to meet you!"' }, correct: 'Leuk je te ontmoeten!', words: ['Leuk', 'je', 'te', 'ontmoeten!', 'heet'] },
                { id: 'u1_l3_e4', type: 'listening', itemId: 'u1_w1', audioText: 'Hallo! Hoe heet jij?', lang: 'nl', voice: 'f', mode: 'mcq', prompt: { en: 'What did you hear?' }, options: ['Hallo! Hoe heet jij?', 'Tot ziens! Hoe heet jij?', 'Hallo! Waar kom je vandaan?', 'Leuk je te ontmoeten!'], correct: 0 },
                { id: 'u1_l3_e5', type: 'typing', production: true, itemId: 'u1_w3', audioText: 'Waar kom je vandaan?', lang: 'nl', voice: 'f', prompt: { en: '🗣️ Answer the question — you are from Syria: "Waar kom je vandaan?"' }, correct: ['Ik kom uit Syrië', 'Ik kom uit Syrie'] },
                { id: 'u1_l3_e6', type: 'typing', production: true, itemId: 'u1_w5', audioText: 'Hoe heet jij?', lang: 'nl', voice: 'f', prompt: { en: '🗣️ Answer the question — your name is Sara: "Hoe heet jij?"' }, correct: ['Ik heet Sara', 'Mijn naam is Sara'] }
              ]
            }
          ]
        },

        /* ---------------- UNIT 2 ---------------- */
        {
          id: 'u2',
          title: 'Je familie beschrijven',
          subtitle: 'Describe your family',
          icon: '👨‍👩‍👧',
          dialogue: [
            { speaker: '🧑', voice: 'm', nl: 'Heb jij een grote familie?', en: 'Do you have a big family?' },
            { speaker: '👩', voice: 'f', nl: 'Ja, ik heb een broer en twee zussen.', en: 'Yes, I have one brother and two sisters.' },
            { speaker: '🧑', voice: 'm', nl: 'Ben je getrouwd?', en: 'Are you married?' },
            { speaker: '👩', voice: 'f', nl: 'Nee, ik ben niet getrouwd. En jij?', en: "No, I'm not married. And you?" },
            { speaker: '🧑', voice: 'm', nl: 'Ik ben getrouwd. Ik heb een dochter.', en: 'I am married. I have a daughter.' }
          ],
          lessons: [
            {
              id: 'l1', label: 'Les 1', title: 'Nieuwe woorden',
              newWords: [
                { id: 'u2_w1', nl: 'de vader', en: 'father' },
                { id: 'u2_w2', nl: 'de moeder', en: 'mother' },
                { id: 'u2_w3', nl: 'de broer', en: 'brother' },
                { id: 'u2_w4', nl: 'de zus', en: 'sister' },
                { id: 'u2_w5', nl: 'ik heb...', en: 'I have...' }
              ],
              exercises: [
                { id: 'u2_l1_e1', type: 'mcq', itemId: 'u2_w1', prompt: { en: 'What does "de vader" mean?' }, options: ['mother', 'father', 'brother', 'sister'], correct: 1 },
                { id: 'u2_l1_e2', type: 'mcq', itemId: 'u2_w4', prompt: { en: 'What does "de zus" mean?' }, options: ['sister', 'daughter', 'wife', 'mother'], correct: 0 },
                { id: 'u2_l1_e3', type: 'wordbank', itemId: 'u2_w5', prompt: { en: 'Build the sentence: "I have a brother."' }, correct: 'Ik heb een broer.', words: ['Ik', 'heb', 'een', 'broer.', 'zus'] },
                { id: 'u2_l1_e4', type: 'typing', itemId: 'u2_w3', prompt: { en: 'Type the Dutch word for "brother".' }, correct: ['de broer', 'broer'] },
                { id: 'u2_l1_e5', type: 'listening', itemId: 'u2_w2', audioText: 'Dit is mijn moeder.', lang: 'nl', voice: 'f', mode: 'mcq', prompt: { en: 'What did you hear?' }, options: ['Dit is mijn moeder.', 'Dit is mijn vader.', 'Dit is mijn zus.', 'Dit is mijn broer.'], correct: 0 }
              ]
            },
            {
              id: 'l2', label: 'Les 2', title: 'Oefenen',
              newWords: [
                { id: 'u2_w6', nl: 'het kind / de kinderen', en: 'child / children' },
                { id: 'u2_w7', nl: 'getrouwd', en: 'married' },
                { id: 'u2_w8', nl: 'mijn', en: 'my' }
              ],
              grammarNote: {
                nl: '"Mijn" betekent "van mij" en verandert niet: mijn vader, mijn moeder, mijn kinderen.',
                en: '"Mijn" means "my" and stays the same regardless of gender or number: mijn vader (my father), mijn kinderen (my children).'
              },
              exercises: [
                { id: 'u2_l2_e1', type: 'mcq', itemId: 'u2_w7', prompt: { en: 'What does "getrouwd" mean?' }, options: ['single', 'married', 'divorced', 'young'], correct: 1 },
                { id: 'u2_l2_e2', type: 'wordbank', itemId: 'u2_w8', prompt: { en: 'Build the sentence: "This is my sister."' }, correct: 'Dit is mijn zus.', words: ['Dit', 'is', 'mijn', 'zus.', 'broer'] },
                { id: 'u2_l2_e3', type: 'typing', itemId: 'u2_w6', prompt: { en: 'Translate: "I have two children."' }, correct: ['Ik heb twee kinderen'] },
                { id: 'u2_l2_e4', type: 'mcq', itemId: 'u2_w1', prompt: { en: 'How do you say "father" in Dutch?' }, options: ['de moeder', 'de vader', 'de zus', 'de broer'], correct: 1 },
                { id: 'u2_l2_e5', type: 'listening', itemId: 'u2_w7', audioText: 'Ik ben niet getrouwd.', lang: 'nl', voice: 'f', mode: 'typing', prompt: { en: 'Type what you hear (in Dutch).' }, correct: ['Ik ben niet getrouwd'] },
                { id: 'u2_l2_e6', type: 'wordbank', itemId: 'u2_w5', prompt: { en: 'Build the sentence: "I have a daughter."' }, correct: 'Ik heb een dochter.', words: ['Ik', 'heb', 'een', 'dochter.', 'zoon'] }
              ]
            },
            {
              id: 'l3', label: 'Les 3', title: 'Herhalen & spreken',
              exercises: [
                { id: 'u2_l3_e1', type: 'mcq', itemId: 'u2_w3', prompt: { en: 'What does "de broer" mean?' }, options: ['sister', 'brother', 'father', 'child'], correct: 1 },
                { id: 'u2_l3_e2', type: 'typing', itemId: 'u2_w1', prompt: { en: 'Translate: "This is my father."' }, correct: ['Dit is mijn vader'] },
                { id: 'u2_l3_e3', type: 'wordbank', itemId: 'u2_w7', prompt: { en: 'Build the sentence: "I am married."' }, correct: 'Ik ben getrouwd.', words: ['Ik', 'ben', 'getrouwd.', 'niet'] },
                { id: 'u2_l3_e4', type: 'listening', itemId: 'u2_w4', audioText: 'Ik heb een broer en twee zussen.', lang: 'nl', voice: 'f', mode: 'mcq', prompt: { en: 'What did you hear?' }, options: ['Ik heb een broer en twee zussen.', 'Ik heb een zus en twee broers.', 'Ik ben niet getrouwd.', 'Dit is mijn moeder.'], correct: 0 },
                { id: 'u2_l3_e5', type: 'typing', production: true, itemId: 'u2_w7', audioText: 'Ben je getrouwd?', lang: 'nl', voice: 'm', prompt: { en: '🗣️ Answer — say you are NOT married: "Ben je getrouwd?"' }, correct: ['Nee, ik ben niet getrouwd', 'Ik ben niet getrouwd', 'Nee ik ben niet getrouwd'] }
              ]
            }
          ]
        },

        /* ---------------- UNIT 3 ---------------- */
        {
          id: 'u3',
          title: 'Over je huis praten',
          subtitle: 'Talk about your home',
          icon: '🏠',
          dialogue: [
            { speaker: '🧑', voice: 'm', nl: 'Waar woon je, Fatima?', en: 'Where do you live, Fatima?' },
            { speaker: '👩', voice: 'f', nl: 'Ik woon in een kleine flat in Utrecht.', en: 'I live in a small apartment in Utrecht.' },
            { speaker: '🧑', voice: 'm', nl: 'Hoeveel kamers heeft de flat?', en: 'How many rooms does the apartment have?' },
            { speaker: '👩', voice: 'f', nl: 'Er is een woonkamer, een keuken en een slaapkamer.', en: 'There is a living room, a kitchen and a bedroom.' },
            { speaker: '🧑', voice: 'm', nl: 'Klinkt gezellig!', en: 'Sounds cozy!' }
          ],
          lessons: [
            {
              id: 'l1', label: 'Les 1', title: 'Nieuwe woorden',
              newWords: [
                { id: 'u3_w1', nl: 'de keuken', en: 'kitchen' },
                { id: 'u3_w2', nl: 'de slaapkamer', en: 'bedroom' },
                { id: 'u3_w3', nl: 'de badkamer', en: 'bathroom' },
                { id: 'u3_w4', nl: 'de woonkamer', en: 'living room' },
                { id: 'u3_w5', nl: 'groot / klein', en: 'big / small' }
              ],
              exercises: [
                { id: 'u3_l1_e1', type: 'mcq', itemId: 'u3_w1', prompt: { en: 'What does "de keuken" mean?' }, options: ['bedroom', 'kitchen', 'bathroom', 'living room'], correct: 1 },
                { id: 'u3_l1_e2', type: 'mcq', itemId: 'u3_w4', prompt: { en: 'What does "de woonkamer" mean?' }, options: ['living room', 'bathroom', 'kitchen', 'garden'], correct: 0 },
                { id: 'u3_l1_e3', type: 'wordbank', itemId: 'u3_w5', prompt: { en: 'Build the sentence: "The kitchen is small."' }, correct: 'De keuken is klein.', words: ['De', 'keuken', 'is', 'klein.', 'groot'] },
                { id: 'u3_l1_e4', type: 'typing', itemId: 'u3_w2', prompt: { en: 'Type the Dutch word for "bedroom".' }, correct: ['de slaapkamer', 'slaapkamer'] },
                { id: 'u3_l1_e5', type: 'listening', itemId: 'u3_w3', audioText: 'Waar is de badkamer?', lang: 'nl', voice: 'f', mode: 'mcq', prompt: { en: 'What did you hear?' }, options: ['Waar is de badkamer?', 'Waar is de keuken?', 'Waar is de slaapkamer?', 'Waar is de woonkamer?'], correct: 0 }
              ]
            },
            {
              id: 'l2', label: 'Les 2', title: 'Oefenen',
              newWords: [
                { id: 'u3_w6', nl: 'het huis / de flat', en: 'house / apartment' },
                { id: 'u3_w7', nl: 'er is / er zijn', en: 'there is / there are' },
                { id: 'u3_w8', nl: 'hoeveel kamers?', en: 'how many rooms?' }
              ],
              grammarNote: {
                nl: '"Er is" gebruik je voor één ding: "er is een keuken". "Er zijn" voor meer dingen: "er zijn twee slaapkamers".',
                en: '"Er is" is used for one thing ("there is a kitchen"); "er zijn" for more than one ("there are two bedrooms").'
              },
              exercises: [
                { id: 'u3_l2_e1', type: 'mcq', itemId: 'u3_w7', prompt: { en: 'Which is correct for "two bedrooms"?' }, options: ['er is twee slaapkamers', 'er zijn twee slaapkamers', 'er is een slaapkamer', 'er zijn een slaapkamer'], correct: 1 },
                { id: 'u3_l2_e2', type: 'wordbank', itemId: 'u3_w6', prompt: { en: 'Build the sentence: "I live in a small apartment."' }, correct: 'Ik woon in een kleine flat.', words: ['Ik', 'woon', 'in', 'een', 'kleine', 'flat.'] },
                { id: 'u3_l2_e3', type: 'typing', itemId: 'u3_w8', prompt: { en: 'Translate: "How many rooms?"' }, correct: ['Hoeveel kamers'] },
                { id: 'u3_l2_e4', type: 'mcq', itemId: 'u3_w5', prompt: { en: 'What does "groot" mean?' }, options: ['small', 'big', 'cozy', 'new'], correct: 1 },
                { id: 'u3_l2_e5', type: 'listening', itemId: 'u3_w4', audioText: 'Er is een woonkamer, een keuken en een slaapkamer.', lang: 'nl', voice: 'f', mode: 'mcq', prompt: { en: 'What did you hear?' }, options: ['Er is een woonkamer, een keuken en een slaapkamer.', 'Er is een badkamer en een keuken.', 'Er zijn twee slaapkamers.', 'Ik woon in een groot huis.'], correct: 0 },
                { id: 'u3_l2_e6', type: 'wordbank', itemId: 'u3_w1', prompt: { en: 'Build the sentence: "There is a kitchen."' }, correct: 'Er is een keuken.', words: ['Er', 'is', 'een', 'keuken.', 'zijn'] }
              ]
            },
            {
              id: 'l3', label: 'Les 3', title: 'Herhalen & spreken',
              exercises: [
                { id: 'u3_l3_e1', type: 'mcq', itemId: 'u3_w2', prompt: { en: 'What does "de slaapkamer" mean?' }, options: ['bedroom', 'kitchen', 'bathroom', 'living room'], correct: 0 },
                { id: 'u3_l3_e2', type: 'typing', itemId: 'u3_w6', prompt: { en: 'Translate: "The apartment is small."' }, correct: ['De flat is klein'] },
                { id: 'u3_l3_e3', type: 'wordbank', itemId: 'u3_w7', prompt: { en: 'Build the sentence: "There is a bathroom."' }, correct: 'Er is een badkamer.', words: ['Er', 'is', 'een', 'badkamer.', 'zijn'] },
                { id: 'u3_l3_e4', type: 'listening', itemId: 'u3_w5', audioText: 'De keuken is klein, maar gezellig.', lang: 'nl', voice: 'f', mode: 'typing', prompt: { en: 'Type what you hear (in Dutch).' }, correct: ['De keuken is klein, maar gezellig', 'De keuken is klein maar gezellig'] },
                { id: 'u3_l3_e5', type: 'typing', production: true, itemId: 'u3_w1', audioText: 'Waar woon je?', lang: 'nl', voice: 'm', prompt: { en: '🗣️ Answer — you live in Utrecht: "Waar woon je?"' }, correct: ['Ik woon in Utrecht'] }
              ]
            }
          ]
        },

        /* ---------------- UNIT 4 ---------------- */
        {
          id: 'u4',
          title: 'Eten en drinken bestellen',
          subtitle: 'Order food and drink',
          icon: '☕',
          dialogue: [
            { speaker: '🧑', voice: 'm', nl: 'Wat wil je drinken?', en: 'What would you like to drink?' },
            { speaker: '👩', voice: 'f', nl: 'Mag ik een koffie, alstublieft?', en: 'May I have a coffee, please?' },
            { speaker: '🧑', voice: 'm', nl: 'En wil je ook iets eten?', en: 'And would you like something to eat too?' },
            { speaker: '👩', voice: 'f', nl: 'Ja, een broodje kaas graag. Dat is lekker!', en: 'Yes, a cheese sandwich please. That is tasty!' },
            { speaker: '🧑', voice: 'm', nl: 'De rekening, alstublieft!', en: 'The bill, please!' }
          ],
          lessons: [
            {
              id: 'l1', label: 'Les 1', title: 'Nieuwe woorden',
              newWords: [
                { id: 'u4_w1', nl: 'de koffie', en: 'coffee' },
                { id: 'u4_w2', nl: 'het water', en: 'water' },
                { id: 'u4_w3', nl: 'het brood', en: 'bread' },
                { id: 'u4_w4', nl: 'mag ik...?', en: 'may I have...?' },
                { id: 'u4_w5', nl: 'alstublieft', en: 'please' }
              ],
              exercises: [
                { id: 'u4_l1_e1', type: 'mcq', itemId: 'u4_w1', prompt: { en: 'What does "de koffie" mean?' }, options: ['tea', 'coffee', 'water', 'milk'], correct: 1 },
                { id: 'u4_l1_e2', type: 'mcq', itemId: 'u4_w4', prompt: { en: 'How do you say "may I have...?"' }, options: ['ik wil...', 'mag ik...?', 'is er...?', 'lekker!'], correct: 1 },
                { id: 'u4_l1_e3', type: 'wordbank', itemId: 'u4_w5', prompt: { en: 'Build the sentence: "A coffee, please."' }, correct: 'Een koffie, alstublieft.', words: ['Een', 'koffie,', 'alstublieft.', 'water'] },
                { id: 'u4_l1_e4', type: 'typing', itemId: 'u4_w2', prompt: { en: 'Type the Dutch word for "water".' }, correct: ['het water', 'water'] },
                { id: 'u4_l1_e5', type: 'listening', itemId: 'u4_w4', audioText: 'Mag ik een koffie, alstublieft?', lang: 'nl', voice: 'f', mode: 'mcq', prompt: { en: 'What did you hear?' }, options: ['Mag ik een koffie, alstublieft?', 'Mag ik water, alstublieft?', 'Mag ik brood, alstublieft?', 'De rekening, alstublieft!'], correct: 0 }
              ]
            },
            {
              id: 'l2', label: 'Les 2', title: 'Oefenen',
              newWords: [
                { id: 'u4_w6', nl: 'lekker', en: 'tasty' },
                { id: 'u4_w7', nl: 'de rekening', en: 'the bill' },
                { id: 'u4_w8', nl: 'de menukaart', en: 'menu' }
              ],
              grammarNote: {
                nl: '"Mag ik..." is een beleefde manier om te bestellen. Voeg "alstublieft" toe om extra beleefd te zijn.',
                en: '"Mag ik..." ("may I have...") is the polite way to order. Add "alstublieft" ("please") to sound extra polite.'
              },
              exercises: [
                { id: 'u4_l2_e1', type: 'mcq', itemId: 'u4_w6', prompt: { en: 'What does "lekker" mean?' }, options: ['expensive', 'tasty', 'cold', 'small'], correct: 1 },
                { id: 'u4_l2_e2', type: 'wordbank', itemId: 'u4_w7', prompt: { en: 'Build the sentence: "The bill, please!"' }, correct: 'De rekening, alstublieft!', words: ['De', 'rekening,', 'alstublieft!', 'koffie'] },
                { id: 'u4_l2_e3', type: 'typing', itemId: 'u4_w8', prompt: { en: 'Translate: "May I have the menu?"' }, correct: ['Mag ik de menukaart'] },
                { id: 'u4_l2_e4', type: 'mcq', itemId: 'u4_w3', prompt: { en: 'How do you say "bread" in Dutch?' }, options: ['het water', 'het brood', 'de koffie', 'de rekening'], correct: 1 },
                { id: 'u4_l2_e5', type: 'listening', itemId: 'u4_w6', audioText: 'Dat is heel lekker!', lang: 'nl', voice: 'f', mode: 'typing', prompt: { en: 'Type what you hear (in Dutch).' }, correct: ['Dat is heel lekker'] },
                { id: 'u4_l2_e6', type: 'wordbank', itemId: 'u4_w4', prompt: { en: 'Build the sentence: "May I have some bread?"' }, correct: 'Mag ik wat brood?', words: ['Mag', 'ik', 'wat', 'brood?', 'water'] }
              ]
            },
            {
              id: 'l3', label: 'Les 3', title: 'Herhalen & spreken',
              exercises: [
                { id: 'u4_l3_e1', type: 'mcq', itemId: 'u4_w1', prompt: { en: 'What does "de koffie" mean?' }, options: ['tea', 'coffee', 'juice', 'milk'], correct: 1 },
                { id: 'u4_l3_e2', type: 'typing', itemId: 'u4_w7', prompt: { en: 'Translate: "The bill, please."' }, correct: ['De rekening, alstublieft', 'De rekening alstublieft'] },
                { id: 'u4_l3_e3', type: 'wordbank', itemId: 'u4_w6', prompt: { en: 'Build the sentence: "The bread is tasty."' }, correct: 'Het brood is lekker.', words: ['Het', 'brood', 'is', 'lekker.', 'duur'] },
                { id: 'u4_l3_e4', type: 'listening', itemId: 'u4_w8', audioText: 'Mag ik de menukaart, alstublieft?', lang: 'nl', voice: 'f', mode: 'mcq', prompt: { en: 'What did you hear?' }, options: ['Mag ik de menukaart, alstublieft?', 'Mag ik de rekening, alstublieft?', 'Mag ik koffie, alstublieft?', 'Dat is lekker!'], correct: 0 },
                { id: 'u4_l3_e5', type: 'typing', production: true, itemId: 'u4_w4', audioText: 'Wat wil je drinken?', lang: 'nl', voice: 'm', prompt: { en: '🗣️ Answer — politely order a coffee: "Wat wil je drinken?"' }, correct: ['Mag ik een koffie, alstublieft', 'Mag ik een koffie alstublieft', 'Een koffie, alstublieft'] }
              ]
            }
          ]
        },

        /* ---------------- UNIT 5 ---------------- */
        {
          id: 'u5',
          title: 'Boodschappen doen',
          subtitle: 'Buy groceries',
          icon: '🛒',
          dialogue: [
            { speaker: '👩', voice: 'f', nl: 'Hoeveel kosten deze appels?', en: 'How much do these apples cost?' },
            { speaker: '🧑', voice: 'm', nl: 'Twee euro per kilo.', en: 'Two euros per kilo.' },
            { speaker: '👩', voice: 'f', nl: 'Oké, en de melk? Is die duur?', en: 'Okay, and the milk? Is that expensive?' },
            { speaker: '🧑', voice: 'm', nl: 'Nee, de melk is goedkoop. Één euro.', en: 'No, the milk is cheap. One euro.' },
            { speaker: '👩', voice: 'f', nl: 'Fijn, ik ga naar de kassa.', en: "Good, I'll go to the checkout." }
          ],
          lessons: [
            {
              id: 'l1', label: 'Les 1', title: 'Nieuwe woorden',
              newWords: [
                { id: 'u5_w1', nl: 'de winkel', en: 'shop' },
                { id: 'u5_w2', nl: 'het geld', en: 'money' },
                { id: 'u5_w3', nl: 'hoeveel kost dit?', en: 'how much is this?' },
                { id: 'u5_w4', nl: 'de melk', en: 'milk' },
                { id: 'u5_w5', nl: 'de appels', en: 'apples' }
              ],
              exercises: [
                { id: 'u5_l1_e1', type: 'mcq', itemId: 'u5_w1', prompt: { en: 'What does "de winkel" mean?' }, options: ['shop', 'money', 'checkout', 'bag'], correct: 0 },
                { id: 'u5_l1_e2', type: 'mcq', itemId: 'u5_w3', prompt: { en: 'How do you ask "how much is this?"' }, options: ['hoeveel kost dit?', 'wat is dit?', 'waar is dit?', 'mag ik dit?'], correct: 0 },
                { id: 'u5_l1_e3', type: 'wordbank', itemId: 'u5_w5', prompt: { en: 'Build the sentence: "How much do the apples cost?"' }, correct: 'Hoeveel kosten de appels?', words: ['Hoeveel', 'kosten', 'de', 'appels?', 'melk'] },
                { id: 'u5_l1_e4', type: 'typing', itemId: 'u5_w4', prompt: { en: 'Type the Dutch word for "milk".' }, correct: ['de melk', 'melk'] },
                { id: 'u5_l1_e5', type: 'listening', itemId: 'u5_w3', audioText: 'Hoeveel kost dit?', lang: 'nl', voice: 'f', mode: 'mcq', prompt: { en: 'What did you hear?' }, options: ['Hoeveel kost dit?', 'Hoeveel kosten de appels?', 'Waar is de winkel?', 'Ik heb geen geld.'], correct: 0 }
              ]
            },
            {
              id: 'l2', label: 'Les 2', title: 'Oefenen',
              newWords: [
                { id: 'u5_w6', nl: 'goedkoop / duur', en: 'cheap / expensive' },
                { id: 'u5_w7', nl: 'de kassa', en: 'checkout' },
                { id: 'u5_w8', nl: 'ik ga naar...', en: "I'm going to..." }
              ],
              grammarNote: {
                nl: '"Deze" gebruik je bij dingen dichtbij en bij de-woorden: "deze appels". Bij het-woorden gebruik je "dit": "dit brood".',
                en: '"Deze" ("these/this") is used with plural or de-words: "deze appels". "Dit" is used with het-words: "dit brood".'
              },
              exercises: [
                { id: 'u5_l2_e1', type: 'mcq', itemId: 'u5_w6', prompt: { en: 'What does "goedkoop" mean?' }, options: ['expensive', 'cheap', 'tasty', 'fresh'], correct: 1 },
                { id: 'u5_l2_e2', type: 'wordbank', itemId: 'u5_w7', prompt: { en: 'Build the sentence: "I\'m going to the checkout."' }, correct: 'Ik ga naar de kassa.', words: ['Ik', 'ga', 'naar', 'de', 'kassa.'] },
                { id: 'u5_l2_e3', type: 'typing', itemId: 'u5_w2', prompt: { en: 'Translate: "I have no money."' }, correct: ['Ik heb geen geld'] },
                { id: 'u5_l2_e4', type: 'mcq', itemId: 'u5_w4', prompt: { en: 'What does "de melk" mean?' }, options: ['bread', 'milk', 'water', 'coffee'], correct: 1 },
                { id: 'u5_l2_e5', type: 'listening', itemId: 'u5_w6', audioText: 'De melk is goedkoop, maar de koffie is duur.', lang: 'nl', voice: 'f', mode: 'mcq', prompt: { en: 'What did you hear?' }, options: ['De melk is goedkoop, maar de koffie is duur.', 'De appels zijn goedkoop.', 'De melk is duur.', 'Ik ga naar de kassa.'], correct: 0 },
                { id: 'u5_l2_e6', type: 'wordbank', itemId: 'u5_w6', prompt: { en: 'Build the sentence: "The apples are expensive."' }, correct: 'De appels zijn duur.', words: ['De', 'appels', 'zijn', 'duur.', 'goedkoop'] }
              ]
            },
            {
              id: 'l3', label: 'Les 3', title: 'Herhalen & spreken',
              exercises: [
                { id: 'u5_l3_e1', type: 'mcq', itemId: 'u5_w7', prompt: { en: 'What does "de kassa" mean?' }, options: ['shop', 'checkout', 'money', 'bag'], correct: 1 },
                { id: 'u5_l3_e2', type: 'typing', itemId: 'u5_w3', prompt: { en: 'Translate: "How much is this?"' }, correct: ['Hoeveel kost dit'] },
                { id: 'u5_l3_e3', type: 'wordbank', itemId: 'u5_w1', prompt: { en: 'Build the sentence: "I\'m going to the shop."' }, correct: 'Ik ga naar de winkel.', words: ['Ik', 'ga', 'naar', 'de', 'winkel.'] },
                { id: 'u5_l3_e4', type: 'listening', itemId: 'u5_w5', audioText: 'Twee euro per kilo appels.', lang: 'nl', voice: 'm', mode: 'typing', prompt: { en: 'Type what you hear (in Dutch).' }, correct: ['Twee euro per kilo appels'] },
                { id: 'u5_l3_e5', type: 'typing', production: true, itemId: 'u5_w3', audioText: 'Hoeveel kost dit?', lang: 'nl', voice: 'm', prompt: { en: '🗣️ Answer — it costs two euros: "Hoeveel kost dit?"' }, correct: ['Twee euro', 'Dat kost twee euro', 'Het kost twee euro'] }
              ]
            }
          ]
        },

        /* ---------------- UNIT 6 ---------------- */
        {
          id: 'u6',
          title: 'Je dagelijkse routine',
          subtitle: 'Daily routine',
          icon: '⏰',
          dialogue: [
            { speaker: '🧑', voice: 'm', nl: 'Hoe laat sta jij op?', en: 'What time do you get up?' },
            { speaker: '👩', voice: 'f', nl: 'Ik sta altijd om zes uur op.', en: "I always get up at six o'clock." },
            { speaker: '🧑', voice: 'm', nl: 'Wat doe je dan?', en: 'What do you do then?' },
            { speaker: '👩', voice: 'f', nl: 'Ik ontbijt en dan ga ik naar mijn werk.', en: 'I have breakfast and then I go to work.' },
            { speaker: '🧑', voice: 'm', nl: "En 's avonds?", en: 'And in the evening?' },
            { speaker: '👩', voice: 'f', nl: "'s Avonds kook ik en soms ga ik vroeg slapen.", en: 'In the evening I cook and sometimes I go to sleep early.' }
          ],
          lessons: [
            {
              id: 'l1', label: 'Les 1', title: 'Nieuwe woorden',
              newWords: [
                { id: 'u6_w1', nl: 'opstaan', en: 'to get up' },
                { id: 'u6_w2', nl: 'ontbijten', en: 'to have breakfast' },
                { id: 'u6_w3', nl: 'werken', en: 'to work' },
                { id: 'u6_w4', nl: 'slapen', en: 'to sleep' },
                { id: 'u6_w5', nl: 'altijd', en: 'always' }
              ],
              exercises: [
                { id: 'u6_l1_e1', type: 'mcq', itemId: 'u6_w1', prompt: { en: 'What does "opstaan" mean?' }, options: ['to sleep', 'to get up', 'to work', 'to eat'], correct: 1 },
                { id: 'u6_l1_e2', type: 'mcq', itemId: 'u6_w5', prompt: { en: 'What does "altijd" mean?' }, options: ['sometimes', 'never', 'always', 'often'], correct: 2 },
                { id: 'u6_l1_e3', type: 'wordbank', itemId: 'u6_w1', prompt: { en: 'Build the sentence: "I always get up at six o\'clock."' }, correct: 'Ik sta altijd om zes uur op.', words: ['Ik', 'sta', 'altijd', 'om', 'zes', 'uur', 'op.'] },
                { id: 'u6_l1_e4', type: 'typing', itemId: 'u6_w3', prompt: { en: 'Type the Dutch word for "to work".' }, correct: 'werken' },
                { id: 'u6_l1_e5', type: 'listening', itemId: 'u6_w2', audioText: 'Ik ontbijt om zeven uur.', lang: 'nl', voice: 'f', mode: 'mcq', prompt: { en: 'What did you hear?' }, options: ['Ik ontbijt om zeven uur.', 'Ik sta om zeven uur op.', 'Ik werk om zeven uur.', 'Ik slaap om zeven uur.'], correct: 0 }
              ]
            },
            {
              id: 'l2', label: 'Les 2', title: 'Oefenen',
              newWords: [
                { id: 'u6_w6', nl: 'soms', en: 'sometimes' },
                { id: 'u6_w7', nl: "'s avonds", en: 'in the evening' },
                { id: 'u6_w8', nl: 'naar school gaan', en: 'to go to school' }
              ],
              grammarNote: {
                nl: 'Scheidbare werkwoorden zoals "opstaan" splitsen in een zin: "Ik sta om zes uur op" (niet "Ik opsta om zes uur").',
                en: 'Separable verbs like "opstaan" (to get up) split apart in a main clause: "Ik sta om zes uur op", not "Ik opsta...".'
              },
              exercises: [
                { id: 'u6_l2_e1', type: 'mcq', itemId: 'u6_w6', prompt: { en: 'What does "soms" mean?' }, options: ['always', 'never', 'sometimes', 'often'], correct: 2 },
                { id: 'u6_l2_e2', type: 'wordbank', itemId: 'u6_w7', prompt: { en: 'Build the sentence: "In the evening I cook."' }, correct: "'s Avonds kook ik.", words: ["'s", 'Avonds', 'kook', 'ik.', 'werk'] },
                { id: 'u6_l2_e3', type: 'typing', itemId: 'u6_w4', prompt: { en: 'Translate: "I go to sleep early."' }, correct: ['Ik ga vroeg slapen'] },
                { id: 'u6_l2_e4', type: 'mcq', itemId: 'u6_w2', prompt: { en: 'What does "ontbijten" mean?' }, options: ['to sleep', 'to cook', 'to have breakfast', 'to work'], correct: 2 },
                { id: 'u6_l2_e5', type: 'listening', itemId: 'u6_w7', audioText: "'s Avonds kook ik en soms ga ik vroeg slapen.", lang: 'nl', voice: 'f', mode: 'mcq', prompt: { en: 'What did you hear?' }, options: ["'s Avonds kook ik en soms ga ik vroeg slapen.", 'Ik sta altijd om zes uur op.', 'Ik ontbijt en ga naar mijn werk.', "'s Avonds ga ik naar school."], correct: 0 },
                { id: 'u6_l2_e6', type: 'wordbank', itemId: 'u6_w3', prompt: { en: 'Build the sentence: "I go to work."' }, correct: 'Ik ga naar mijn werk.', words: ['Ik', 'ga', 'naar', 'mijn', 'werk.'] }
              ]
            },
            {
              id: 'l3', label: 'Les 3', title: 'Herhalen & spreken',
              exercises: [
                { id: 'u6_l3_e1', type: 'mcq', itemId: 'u6_w4', prompt: { en: 'What does "slapen" mean?' }, options: ['to work', 'to sleep', 'to eat', 'to get up'], correct: 1 },
                { id: 'u6_l3_e2', type: 'typing', itemId: 'u6_w1', prompt: { en: 'Translate: "I get up at seven o\'clock."' }, correct: ['Ik sta om zeven uur op'] },
                { id: 'u6_l3_e3', type: 'wordbank', itemId: 'u6_w6', prompt: { en: 'Build the sentence: "Sometimes I work in the evening."' }, correct: "Soms werk ik 's avonds.", words: ['Soms', 'werk', 'ik', "'s", 'avonds.'] },
                { id: 'u6_l3_e4', type: 'listening', itemId: 'u6_w8', audioText: 'Mijn dochter gaat om acht uur naar school.', lang: 'nl', voice: 'f', mode: 'typing', prompt: { en: 'Type what you hear (in Dutch).' }, correct: ['Mijn dochter gaat om acht uur naar school'] },
                { id: 'u6_l3_e5', type: 'typing', production: true, itemId: 'u6_w1', audioText: 'Hoe laat sta jij op?', lang: 'nl', voice: 'm', prompt: { en: '🗣️ Answer — you get up at six: "Hoe laat sta jij op?"' }, correct: ['Ik sta om zes uur op', 'Ik sta altijd om zes uur op'] }
              ]
            }
          ]
        }
      ]
    },

    /* Placeholder sections shown on the map as "coming soon" so the shape of
       the wider course is visible. Units have no lessons yet. */
    {
      id: 's2',
      title: 'Sectie 2 · Onderweg',
      units: [
        { id: 'u7', title: 'Reizen met het OV', subtitle: 'Travel by public transport', icon: '🚆', comingSoon: true, lessons: [] },
        { id: 'u8', title: 'De weg vragen', subtitle: 'Ask for directions', icon: '🧭', comingSoon: true, lessons: [] },
        { id: 'u9', title: 'Naar de dokter', subtitle: 'Go to the doctor', icon: '🩺', comingSoon: true, lessons: [] },
        { id: 'u10', title: 'Afspraken maken', subtitle: 'Make appointments', icon: '📅', comingSoon: true, lessons: [] }
      ]
    },
    {
      id: 's3',
      title: 'Sectie 3 · Op het werk',
      units: [
        { id: 'u11', title: 'Jezelf voorstellen op werk', subtitle: 'Introduce yourself at work', icon: '💼', comingSoon: true, lessons: [] },
        { id: 'u12', title: 'Telefoneren', subtitle: 'Make a phone call', icon: '📞', comingSoon: true, lessons: [] },
        { id: 'u13', title: 'Een klacht bespreken', subtitle: 'Discuss a complaint', icon: '⚠️', comingSoon: true, lessons: [] },
        { id: 'u14', title: 'Werkoverleg', subtitle: 'Team meeting', icon: '🗣️', comingSoon: true, lessons: [] }
      ]
    }
  ]
};

/* Flat vocab index (itemId -> {nl, en, unitId}) used by lesson-player.js to
   auto-generate SRS review exercises and MC distractors. */
const VOCAB = {};
(function buildVocabIndex() {
  COURSE.sections.forEach(section => {
    section.units.forEach(unit => {
      (unit.lessons || []).forEach(lesson => {
        (lesson.newWords || []).forEach(w => { VOCAB[w.id] = { nl: w.nl, en: w.en, unitId: unit.id }; });
      });
    });
  });
})();
