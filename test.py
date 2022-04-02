sentence = 'இவர் ஒரு சட்ட மாணவராக இருந்து, 1920களின் தொடக்கத்தில் பல்கலைக்கழக சீர்திருத்த இயக்கத்தின் தலைவராக ஆகி, தொழிலாள வர்க்கம் பக்கம் திரும்புவதற்கு முயற்சித்தவர்.அவர் மச்சாடோவை "வெப்ப மண்டலத்து முசோலினி"என்றழைத்தார்.'

f1=open("test.tsv","r",encoding='UTF-8')
for line in f1:
    #sentence_count+=1
    new_string = line.strip('"')
    print(new_string)
#new_string =sentence.strip('"')


