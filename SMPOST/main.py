__author__ = 'ShubhamTripathi'

from rule_transform import cleanTransform, featureExtraction
from helpers import unpack

class smpost:
    def __init__(self, lang = 'BN'):
        self.lang = lang + '_FN'

    def predict(self, sent):
        sl, bl = self.rule_tag(sent)
        fi_token = self.test_format(sl)
        tok_lst = [fi_token,bl]
        tok_lst = unpack(tok_lst)
        main_idx = 0
        ftokens = []
        for idx in range(0,len(tok_lst)):
            for (tok,idx,lbl) in tok_lst:
                if idx == main_idx:
                    str_lst = tok + "/" + lbl
                    ftokens.append(str_lst)
                    main_idx += 1
        return ' '.join(ftokens)
    def rule_tag(self, sent):
        sent_lst, bad_lst = cleanTransform(sent).fcheck(sent)
        max_l = 20
        for token in unpack(sent_lst):
            if len(token[0]) >= max_l:
                exit('Length of word in the sentence is too long. Length must be less than {0}'.format(max_l))
        return unpack(sent_lst), unpack(bad_lst)

    def test_format(self, sl):
        return featureExtraction(sl, self.lang).fextract()