__author__ = 'ShubhamTripathi'

from helpers import getresource as gre
from helpers import isAscii, unpack, char_ngram, word_normalisation
import re
import pickle
import os
import subprocess

class cleanTransform:
    def __init__(self, sent):
        self.sent = sent

    def rm_residual(self, sent):
        gr = gre()
        clean_list_punc = []
        bad_list_punc = []
        bad_list_rdf = []
        bad_list_unk = []

        list_punc = []
        index = 0
        for token in str.split(sent[0]):
            list_punc.append((token,index))
            index += 1
        index = 0
        for token in list_punc:
            if token[0] in gr[0] or re.findall(r'\.\.+', token[0]) or re.findall(r'--+', token[0]) or re.findall(
                    r'\*\*+', token[0]) or re.findall(r',,+', token[0]) or re.findall(r'!!+', token[0]) or re.findall(
                    r'\?\?+', token[0]) or re.findall(r'\'\'+', token[0]):
                token = list(token)
                token.append('RD_PUNC')
                bad_list_punc.append(tuple(token))
                index += 1
            elif token[0] in re.findall(r'~+', token[0]):
                token = list(token)
                token.append('RD_SYM')
                bad_list_rdf.append(tuple(token))
                index += 1
            elif not isAscii(token[0]):
                token = list(token)
                token.append('RD_UNK')
                bad_list_unk.append(tuple(token))
                index += 1
            else:
                clean_list_punc.append(token)
                index += 1
        return clean_list_punc, bad_list_punc, bad_list_rdf, bad_list_unk

    def rm_numeral(self, sent):
        gr = gre()
        clean_list_num = []
        bad_list_num = []
        for token in sent:
            if token[0][0].isdigit():
                token = list(token)
                token.append('$')
                bad_list_num.append(tuple(token))
                continue

            if token[0][0].isdigit() and token[0][-1].isdigit():
                token = list(token)
                token.append('$')
                bad_list_num.append(tuple(token))
                continue

            if re.findall(r'^[0-9]+', token[0]):
                if token[0].lower().endswith('th') or token[0].lower().endswith('st') or token[0].lower().endswith(
                        'nd') or token[0].lower().endswith('rd'):
                    token = list(token)
                    token.append('$')
                    bad_list_num.append(tuple(token))
                    continue

            if (token[0].isdigit() or token[0] in gr[2] or token[0].lower() in gr[2] or token[0] in gr[1] or token[0].startswith('+91')):
                token = list(token)
                token.append('$')
                bad_list_num.append(tuple(token))
                continue
            else:
                clean_list_num.append(token)
        return clean_list_num, bad_list_num

    def rm_misc(self, sent):
        sm_ex = """:-) :) :o) :] :3 :c) :> =] 8) =) :} :^) _/ O.o o.O \m/ _/\_ _|_ -_- _/\\_ [\\m/] ^_^ _/|\_ >.< <3 -.-
                     :v 8-D 8D B-) xD X-D XD =-D =D =-3 =3 B^D >_<""".split()
        pattern2 = "|".join(map(re.escape, sm_ex))
        clean_list_misc = []
        bad_list_u = []
        bad_list_at = []
        bad_list_hatch = []
        bad_list_emoji = []
        bad_list_rt = []
        for token in sent:
            if re.search(r'\.com', token[0]) or re.search(r'\.me', token[0]) or re.search(r'\.org',
                                                                                          token[0]) or re.search(
                    r'\.in', token[0]) or re.search(r'\.be', token[0]) or re.search(r'\.it', token[0]):
                token = list(token)
                token.append('U')
                bad_list_u.append(tuple(token))
                continue
            elif token[0].startswith('http://') or token[0].startswith('https') or token[0].startswith('www') or token[
                0].endswith('.com'):
                token = list(token)
                token.append('U')
                bad_list_u.append(tuple(token))
                continue
            elif token[0].startswith('@'):
                token = list(token)
                token.append('@')
                bad_list_at.append(tuple(token))
                continue

            elif token[0].startswith('#'):
                token = list(token)
                token.append('#')
                bad_list_hatch.append(tuple(token))
                continue
            elif re.match(r"(:|;|=)[-pPdDB)\\3(/'|\]}>oO]+", token[0]) or re.findall(pattern2, token[0]):
                token = list(token)
                token.append('E')
                bad_list_emoji.append(tuple(token))
                continue
            elif token[0] == 'RT':
                token = list(token)
                token.append('~')
                bad_list_rt.append(tuple(token))
                continue
            else:
                clean_list_misc.append(token)

        return clean_list_misc, bad_list_u, bad_list_emoji, bad_list_at, bad_list_hatch, bad_list_rt

    def fcheck(self, sent):
        sent_lst = []
        bad_lst = []
        data_rs, b_punc, b_rdf, b_unk = self.rm_residual(sent)
        data_num, b_num = self.rm_numeral(data_rs)
        data_misc, b_u, b_emoji, b_at, b_hatch, b_rt = self.rm_misc(data_num)
        sent_lst.append(data_misc)
        bb_list = [b_punc, b_rdf, b_unk, b_num, b_u, b_emoji, b_at, b_hatch, b_rt]
        bad_lst.append(unpack(bb_list))
        return sent_lst, bad_lst

class featureExtraction:
    def __init__(self, sent, lang):
        self.sent = sent
        self.lang = lang

    def ngram_extraction(self):
        max_l = pickle.load(open('./SMPOST/resources/{0}_maxl.p'.format(self.lang),'r'))
        ngram2 = []
        ngram3 = []
        ngram4 = []
        ngram5 = []
        for idx in xrange(len(self.sent)):
            ng2 = char_ngram(2, self.sent[idx][0])
            ng3 = char_ngram(3, self.sent[idx][0])
            ng4 = char_ngram(4, self.sent[idx][0])
            ng5 = char_ngram(5, self.sent[idx][0])
            while len(ng2) < max_l[0]:
                ng2.append('_NIL_')
            while len(ng3) < max_l[1]:
                ng3.append('_NIL_')
            while len(ng4) < max_l[2]:
                ng4.append('_NIL_')
            while len(ng5) < max_l[3]:
                ng5.append('_NIL_')

            ngram2.append(ng2)
            ngram3.append(ng3)
            ngram4.append(ng4)
            ngram5.append(ng5)

        return ngram2, ngram3, ngram4, ngram5

    def feat_extraction(self):
        wp = pickle.load(open('./SMPOST/resources/{0}_wp.p'.format(self.lang),'r'))
        word_pos = []
        word_len = []
        is_upper = []
        fcharup = []
        nocharup = []
        wordnorm = []
        prob1 = []
        prob2 = []
        for idx in xrange(len(self.sent)):
            word_pos.append(float(idx / len(self.sent)))
            word_len.append(len(self.sent[idx][0]))
            is_upper.append(self.sent[idx][0].isupper())
            fcharup.append(self.sent[idx][0].isupper())
            try:
                prob1.append(wp[0][self.sent[idx][0]])
            except:
                prob1.append(wp[2])
            try:
                prob2.append(wp[1][self.sent[idx][0]])
            except:
                prob2.append(wp[2])

            count = 0
            for letter in self.sent[idx][0]:
                if letter.isupper():
                    count += 1
            nocharup.append(float(count / len(self.sent[idx][0])))
            wordnorm.append(word_normalisation(self.sent[idx][0]))
        return word_pos, word_len, is_upper, fcharup, nocharup, wordnorm, prob1, prob2

    def make_test_file(self,ng2,ng3,ng4,ng5,f1,f2,f3,f4,f5,f6,f7,f8):
        with open('test.txt','a') as flp:
            ngra2 = []
            ngra3 = []
            ngra4 = []
            ngra5 = []
            for idx in xrange(len(self.sent)):
                nG2 = []
                nG3 = []
                nG4 = []
                nG5 = []
                for token in ng2[idx]:
                    nG2.append(token)
                for token in ng3[idx]:
                    nG3.append(token)
                for token in ng4[idx]:
                    nG4.append(token)
                for token in ng5[idx]:
                    nG5.append(token)

                ngra2.append(nG2)
                ngra3.append(nG3)
                ngra4.append(nG4)
                ngra5.append(nG5)

            for idx in xrange(len(self.sent)):
                flp.write(
                    "{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12}".format(
                        self.sent[idx][0], ' '.join(ngra2[idx]), ' '.join(ngra3[idx]), ' '.join(ngra4[idx]),
                        ' '.join(ngra5[idx]), f1[idx], f2[idx],
                        f3[idx], f4[idx], f5[idx],
                        f6[idx], f7[idx], f8[idx]))
                flp.write('\n')

    def get_tokens(self):
        with open('output.txt', 'r') as fp:
            oData = fp.readlines()
        my_pred = []
        for token in oData:
            splString = re.split(r'\t', token)
            if not splString[0] == '\n':
                my_pred.append(re.split(r'\n', splString[-1])[0])
        os.remove('output.txt')
        return my_pred

    def fextract(self):
        ng2, ng3, ng4, ng5 = self.ngram_extraction()
        f1, f2, f3, f4, f5, f6, f7, f8 = self.feat_extraction()
        try:
            os.remove('test.txt')
            os.remove('output.txt')
        except:
            pass
        self.make_test_file(ng2,ng3,ng4,ng5,f1,f2,f3,f4,f5,f6,f7,f8)
        cmd = "crf_test -m SMPOST/resources/{0} test.txt > output.txt".format(self.lang)
        subprocess.call(cmd, shell = True)
        os.remove('test.txt')
        ftokens = self.get_tokens()
        fi_token = []
        main_idx = 0
        for (tok,idx) in self.sent:
            mid_l = []
            mid_l.append(tok)
            mid_l.append(idx)
            mid_l.append(ftokens[main_idx])
            fi_token.append(tuple(mid_l))
            main_idx += 1
        return fi_token