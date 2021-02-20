import re
from termcolor import colored

suffixes = {
	    1: ["ो", "े", "ू", "ु", "ी", "ि", "ा"],  
            2: ["तृ","ान","ैत","ने","ाऊ","ाव","कर", "ाओ", "िए", "ाई", "ाए", "नी", "ना", "ते", "ीं", "ती",
                "ता", "ाँ", "ां", "ों", "ें","ीय", "ति","या", "पन", "पा","ित","ीन","लु","यत","वट","लू"],     
            3: ["ेरा","त्व","नीय","ौनी","ौवल","ौती","ौता","ापा","वास","हास","काल","पान","न्त","ौना","सार","पोश","नाक",
                "ियल","ैया", "ौटी","ावा","ाहट","िया","हार", "ाकर", "ाइए", "ाईं", "ाया", "ेगी", "वान", "बीन",
                "ेगा", "ोगी", "ोगे", "ाने", "ाना", "ाते", "ाती", "ाता", "तीं", "ाओं", "ाएं", "ुओं", "ुएं", "ुआं","कला","िमा","कार",
                "गार", "दान","खोर"],     
            4: ["ावास","कलाप","हारा","तव्य","वैया", "वाला", "ाएगी", "ाएगा", "ाओगी", "ाओगे", 
                "एंगी", "ेंगी", "एंगे", "ेंगे", "ूंगी", "ूंगा", "ातीं", "नाओं", "नाएं", "ताओं", "ताएं", "ियाँ", "ियों", "ियां",
                "त्वा","तव्य","कल्प","िष्ठ","जादा","क्कड़"],     
            5: ["ाएंगी", "ाएंगे", "ाऊंगी", "ाऊंगा", "ाइयाँ", "ाइयों", "ाइयां", "अक्कड़","तव्य:","निष्ठ"],
}


special_suffixes = ["र्", "ज्य","त्य"]
dict_special_suffixes = {"र्":"ृ",
                         "ज्य":"ज्",
                         "त्य":"त्"}




def import_stop_words():
	stop_words_list=[]
	with open('stop_words.txt') as reader:
		for i in reader:
			if i =='\n':
				pass
			else:
				stop_words_list.append(i.strip('\n'))
	return stop_words_list



def clean_text(with_stop_words):


	cleaned_text=re.sub(r'[\x00-\x7F]+',' ', with_stop_words)
    
	return cleaned_text

def remove_stop_words(with_stop_words_cleaned):
	without_stopwords_list=[]
	for i in with_stop_words_cleaned.split():
		stop_words_list=import_stop_words()
		if i in stop_words_list:
			pass
		else:
			without_stopwords_list.append(i)

	without_stopwords=" ".join(without_stopwords_list)    

	l1=list(set(with_stop_words_cleaned.split())-set(without_stopwords_list))
	result = " ".join(colored(t,'white','on_red') if t in l1 else t for t in with_stop_words_cleaned.lower().split())
	print(result)
	return without_stopwords


def hindi_stem(word):
    bl = False
    ans = word
    for L in 5, 4, 3, 2, 1:
        if len(word) > L + 1:
            for suf in suffixes[L]:
                if word.endswith(suf):
                    ans = word[:-L]
                    bl =True
        if bl == True:
            break
                    
    if bl == True:
        for suf in suffixes[1]:
            if ans.endswith(suf):
                ans = hindi_stem(ans)
   
    for suf in special_suffixes:
        if ans.endswith(suf):
            l = len(suf)
            ans = ans[:-l]
            ans += dict_special_suffixes[suf]
    return ans


def stem_words(removed):
	ftemps = [hindi_stem(i) for i in removed.split()]
	l1=list(set(removed.split())-set(ftemps))
	result = " ".join(colored(t,'white','on_red') if t in l1 else t for t in removed.split())
	print(result)
	return ' '.join(ftemps)