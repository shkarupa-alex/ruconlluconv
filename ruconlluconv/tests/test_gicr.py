# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import tempfile
import unittest
from ..gicr import break_combined_paragraphs, join_gicr_splits, repair_broken_composites, join_gicr_composite, \
    convert_gicr_format


class TestBreakCombinedParagraphs(unittest.TestCase):
    def testBreak(self):
        source = [
            u'TEXTID=12541_1******************************77516444_1049.dat',
            u'', u'',
            u'519526	0058	Предполагается     	[предположить]             	Vi-s-3pysim- 	',
            u'519526	   P	,',
            u'519526	0059	что                	[что]                      	C            	',
            u'519526	0060	автовладельцы      	[автовладелец]             	Ncmpn-y      	',
            u'519526	0061	будут              	[быть]                     	Vi-p-3fnaim- 	',
            u'519526	0062	регистрироваться   	[регистрировать]           	Vn-----ysim- 	',
            u'519526	0063	на                 	[на]                       	Sps-l        	',
            u'519526	0064	сайте              	[сайт]                     	Ncmsl-n      	',
            u'519526	   P	,',
            u'519526	0065	после              	[после]                    	Sps-g        	',
            u'519526	0066	чего               	[что]                      	Pqnsg-n-     	',
            u'519526	0067	смогут             	[смочь]                    	Vi-p-3fnapm- 	',
            u'519526	0068	оспорить           	[оспорить]                 	Vn-----yapm- 	',
            u'519526	0069	штрафы             	[штраф]                    	Ncmpa-n      	',
            u'519526	0070	ГИБДД              	[ГИБДД]                    	Ncni--n      	',
            u'519526	0071	при                	[при]                      	Sps-l        	',
            u'519526	0072	помощи             	[помощь]                   	Ncfsl-n      	',
            u'519526	0073	специальной        	[специальный]              	Apfsgf       	',
            u'519526	0074	формы              	[форма]                    	Ncfsg-n      	',
            u'519526	   P	,',
            u'519526	0075	в                  	[в]                        	Sps-l        	',
            u'519526	0076	которой            	[который]                  	Pqfsl-a      	',
            u'519526	0077	надо               	[надо]                     	W            	',
            u'519526	0078	будет              	[быть]                     	Vi-s-3fnaim- 	',
            u'519526	0079	указать            	[указать]                  	Vn-----yapm- 	',
            u'519526	0080	номер              	[номер]                    	Ncmsa-n      	',
            u'519526	0081	и                  	[и]                        	C            	',
            u'519526	0082	дату               	[дата]                     	Ncfsa-n      	',
            u'519526	0083	постановления      	[постановление]            	Ncnsg-n      	',
            u'519526	   P	,',
            u'519526	0084	подразделение      	[подразделение]            	Ncnsa-n      	',
            u'519526	0085	ГИБДД              	[ГИБДД]                    	Ncni--n      	',
            u'519526	   P	,',
            u'519526	0086	выписавшее         	[выписать]                 	Vpnsa-syapmf 	',
            u'519526	0087	квитанцию          	[квитанция]                	Ncfsa-n      	',
            u'519526	   P	,',
            u'519526	0088	а_также            	[а_также]                  	C            	',
            u'519526	0089	приложить          	[приложить]                	Vn-----yapm- 	',
            u'519526	0090	свои               	[свой]                     	Ps-pa-a      	',
            u'519526	0091	фото               	[фото]                     	Xp           	c-',
            u'519526	   P	-',
            u'519526	0092	и                  	[и]                        	C            	',
            u'519526	0093	видео              	[видео]                    	Xp           	c-',
            u'519526	0094	доказательства     	[доказательство]           	Ncnpa-n      	c+',
            u'519526	   P	.',
            u'520028	0001	М                  	[#Acronym]                 	Xt           	',
            u'520028	   P	-',
            u'520028	0002	де                 	[де]                       	Xp           	c-',
            u'520028	   P	,',
            u'520028	0003	скока              	[сколько]                  	C            	',
            u'520028	0004	у                  	[у]                        	Sps-g        	',
            u'520028	0005	автора             	[автор]                    	Ncmsg-y      	',
            u'520028	0006	блога              	[блог]                     	Ncmsg-n      	',
            u'520028	0007	тараканов          	[таракан]                  	Ncmpg-y      	',
            u'520028	0008	то                 	[тот]                      	Pdnsn-a      	',
            u'520028	0009	относительно       	[относительно]             	Sps-g        	',
            u'520028	0010	женщин             	[женщина]                  	Ncfpg-y      	',
            u'520028	   P	.',
            u'', u''
        ]
        expected = [
            u'TEXTID=12541_1******************************77516444_1049.dat',
            u'', u'',
            u'519526	0058	Предполагается     	[предположить]             	Vi-s-3pysim- 	',
            u'519526	   P	,',
            u'519526	0059	что                	[что]                      	C            	',
            u'519526	0060	автовладельцы      	[автовладелец]             	Ncmpn-y      	',
            u'519526	0061	будут              	[быть]                     	Vi-p-3fnaim- 	',
            u'519526	0062	регистрироваться   	[регистрировать]           	Vn-----ysim- 	',
            u'519526	0063	на                 	[на]                       	Sps-l        	',
            u'519526	0064	сайте              	[сайт]                     	Ncmsl-n      	',
            u'519526	   P	,',
            u'519526	0065	после              	[после]                    	Sps-g        	',
            u'519526	0066	чего               	[что]                      	Pqnsg-n-     	',
            u'519526	0067	смогут             	[смочь]                    	Vi-p-3fnapm- 	',
            u'519526	0068	оспорить           	[оспорить]                 	Vn-----yapm- 	',
            u'519526	0069	штрафы             	[штраф]                    	Ncmpa-n      	',
            u'519526	0070	ГИБДД              	[ГИБДД]                    	Ncni--n      	',
            u'519526	0071	при                	[при]                      	Sps-l        	',
            u'519526	0072	помощи             	[помощь]                   	Ncfsl-n      	',
            u'519526	0073	специальной        	[специальный]              	Apfsgf       	',
            u'519526	0074	формы              	[форма]                    	Ncfsg-n      	',
            u'519526	   P	,',
            u'519526	0075	в                  	[в]                        	Sps-l        	',
            u'519526	0076	которой            	[который]                  	Pqfsl-a      	',
            u'519526	0077	надо               	[надо]                     	W            	',
            u'519526	0078	будет              	[быть]                     	Vi-s-3fnaim- 	',
            u'519526	0079	указать            	[указать]                  	Vn-----yapm- 	',
            u'519526	0080	номер              	[номер]                    	Ncmsa-n      	',
            u'519526	0081	и                  	[и]                        	C            	',
            u'519526	0082	дату               	[дата]                     	Ncfsa-n      	',
            u'519526	0083	постановления      	[постановление]            	Ncnsg-n      	',
            u'519526	   P	,',
            u'519526	0084	подразделение      	[подразделение]            	Ncnsa-n      	',
            u'519526	0085	ГИБДД              	[ГИБДД]                    	Ncni--n      	',
            u'519526	   P	,',
            u'519526	0086	выписавшее         	[выписать]                 	Vpnsa-syapmf 	',
            u'519526	0087	квитанцию          	[квитанция]                	Ncfsa-n      	',
            u'519526	   P	,',
            u'519526	0088	а_также            	[а_также]                  	C            	',
            u'519526	0089	приложить          	[приложить]                	Vn-----yapm- 	',
            u'519526	0090	свои               	[свой]                     	Ps-pa-a      	',
            u'519526	0091	фото               	[фото]                     	Xp           	c-',
            u'519526	   P	-',
            u'519526	0092	и                  	[и]                        	C            	',
            u'519526	0093	видео              	[видео]                    	Xp           	c-',
            u'519526	0094	доказательства     	[доказательство]           	Ncnpa-n      	c+',
            u'519526	   P	.',
            u'', u'',
            u'520028	0001	М                  	[#Acronym]                 	Xt           	',
            u'520028	   P	-',
            u'520028	0002	де                 	[де]                       	Xp           	c-',
            u'520028	   P	,',
            u'520028	0003	скока              	[сколько]                  	C            	',
            u'520028	0004	у                  	[у]                        	Sps-g        	',
            u'520028	0005	автора             	[автор]                    	Ncmsg-y      	',
            u'520028	0006	блога              	[блог]                     	Ncmsg-n      	',
            u'520028	0007	тараканов          	[таракан]                  	Ncmpg-y      	',
            u'520028	0008	то                 	[тот]                      	Pdnsn-a      	',
            u'520028	0009	относительно       	[относительно]             	Sps-g        	',
            u'520028	0010	женщин             	[женщина]                  	Ncfpg-y      	',
            u'520028	   P	.',
            u'', u''
        ]
        actual = break_combined_paragraphs('\n'.join(source))
        print(actual)

        self.assertListEqual(expected, actual.split('\n'))

    def testNoBreak(self):
        source = [
            u'TEXTID=12541_1******************************77516444_1049.dat',
            u'', u'',
            u'516444	   P	"',
            u'516444	0001	ИНТЕРАВТО          	[#Acronym]                 	Xt           	',
            u'516444	   P	—"',
            u'516444	0002	любые              	[любой]                    	Pn-pn-a      	',
            u'516444	0003	запчасти           	[запчасть]                 	Ncfpn-n      	',
            u'516444	0004	для                	[для]                      	Sps-g        	',
            u'516444	0005	твоего             	[твой]                     	Psmsg2a      	',
            u'516444	0006	автомобиля         	[автомобиль]               	Ncmsg-n      	',
            u'516444	   P	!',
            u'', u''
        ]
        expected = [
            u'TEXTID=12541_1******************************77516444_1049.dat',
            u'', u'',
            u'516444	   P	"',
            u'516444	0001	ИНТЕРАВТО          	[#Acronym]                 	Xt           	',
            u'516444	   P	—"',
            u'516444	0002	любые              	[любой]                    	Pn-pn-a      	',
            u'516444	0003	запчасти           	[запчасть]                 	Ncfpn-n      	',
            u'516444	0004	для                	[для]                      	Sps-g        	',
            u'516444	0005	твоего             	[твой]                     	Psmsg2a      	',
            u'516444	0006	автомобиля         	[автомобиль]               	Ncmsg-n      	',
            u'516444	   P	!',
            u'', u''
        ]
        actual = break_combined_paragraphs('\n'.join(source))

        self.assertListEqual(expected, actual.split('\n'))


class TestJoinGicrSplits(unittest.TestCase):
    def testSparse(self):
        source = [
            '', '',
            u'627448	0006	Ростов             	[Ростов]                   	Npmsn-n',
            u'627448	   P	-',
            u'627448	0007	на-Дону            	[на-Дону]                  	Xf',
            u'627448	0008	2                  	[#Number]                  	M*---d',
            '', '',
        ]
        expected = [
            '', '',
            u'627448	0006	Ростов-на-Дону	[Ростов-на-Дону]	Npmsn-n',
            u'627448	0008	2                  	[#Number]                  	M*---d',
            '', '',
        ]
        actual = join_gicr_splits('\n'.join(source))

        self.assertListEqual(expected, actual.split('\n'))

    def testDense(self):
        source = [
            '', '',
            u'528358	   P	"',
            u'528358	0124	Лента              	[лента]                    	Ncfsn-n',
            u'528358	0125	.ру                	[.ру]                      	Xf',
            u'528358	   P	"',
            u'528358	0126	вела               	[вести]                    	Vifs--syaim-',
            u'528358	0127	онлайн             	[онлайн]                   	Rp',
            u'528358	0128	этой               	[этот]                     	Pdfsi-a',
            u'528358	0129	встречи            	[встреча]                  	Ncfpa-n',
            u'528358	   P	.',
            '', '',
        ]
        expected = [
            '', '',
            u'528358	   P	"',
            u'528358	0124	Лента.ру	[лента.ру]	Ncfsn-n',
            u'528358	   P	"',
            u'528358	0126	вела               	[вести]                    	Vifs--syaim-',
            u'528358	0127	онлайн             	[онлайн]                   	Rp',
            u'528358	0128	этой               	[этот]                     	Pdfsi-a',
            u'528358	0129	встречи            	[встреча]                  	Ncfpa-n',
            u'528358	   P	.',
            '', '',
        ]
        actual = join_gicr_splits('\n'.join(source))

        self.assertListEqual(expected, actual.split('\n'))

    def testSkip(self):
        source = [
            '', '',
            u'619603	0261	Поддерживать       	[поддержать]               	Vn-----yaim-',
            u'619603	   P	"',
            u'619603	0262	статус             	[статус]                   	Ncmsa-n',
            u'619603	0263	кво                	[кво]                      	Xf',
            u'619603	   P	."',
            '', '',
        ]
        actual = join_gicr_splits('\n'.join(source))

        self.assertListEqual(source, actual.split('\n'))


class TestRepairGicrComposites(unittest.TestCase):
    def testNoChange(self):
        source = [
            '', '',
            u'524205	0054	видео              	[видео]                    	Xp           	c-c+',
            u'519526	0063	из                 	[из]                       	Sps-l        	',
            u'518836	0003	70х                 	[#Number]                  	M*---d       	',
            '', '',
        ]
        actual = repair_broken_composites('\n'.join(source))
        expected = '\n'.join(source).replace('\tc-c+', '\t')

        self.assertListEqual(expected.split('\n'), actual.split('\n'))

    def testDoubleNoJoin(self):
        source = [
            '', '',
            u'521342	0004	видео              	[видео]                    	Xp           	c-',
            u'521342	0005	и                  	[и]                        	C            	',
            u'521342	0006	аудио              	[аудио]                    	Xp           	c-',
            u'521342	0007	записи             	[запись]                   	Ncfpn-n      	c+',
            '', '',
            u'520174	0017	как                	[как]                      	C            	',
            u'520174	0018	сильно             	[сильный]                  	Xp           	c-',
            u'520174	   P	,-',
            u'520174	0019	так_и              	[так_и]                    	C            	',
            u'520174	0020	мало               	[малый]                    	Xp           	c-',
            u'520174	0021	пропагандистскими  	[пропагандистский]         	Ap-pif       	c+',
            u'520174	   P	.',
            '', '',
            u'524205	0052	мебель             	[мебель]                   	Ncfsa-n      	',
            u'524205	   P	,',
            u'524205	0053	аудио              	[аудио]                    	Xp           	c-',
            u'524205	   P	,-',
            u'524205	0054	видео              	[видео]                    	Xp           	c-c+',
            u'524205	   P	-',
            u'524205	0055	и                  	[и]                        	C            	',
            u'524205	0056	бытовую            	[бытовой]                  	Apfsaf       	',
            '', '',
        ]
        expected = [
            '', '',
            u'521342	0004	видео              	[видео]                    	Xp           	',
            u'521342	0005	и                  	[и]                        	C            	',
            u'521342	0006	аудио              	[аудио]                    	Xp           	c-',
            u'521342	0007	записи             	[запись]                   	Ncfpn-n      	c+',
            '', '',
            u'520174	0017	как                	[как]                      	C            	',
            u'520174	0018	сильно             	[сильный]                  	Xp           	',
            u'520174	   P	,-',
            u'520174	0019	так_и              	[так_и]                    	C            	',
            u'520174	0020	мало               	[малый]                    	Xp           	c-',
            u'520174	0021	пропагандистскими  	[пропагандистский]         	Ap-pif       	c+',
            u'520174	   P	.',
            '', '',
            u'524205	0052	мебель             	[мебель]                   	Ncfsa-n      	',
            u'524205	   P	,',
            u'524205	0053	аудио              	[аудио]                    	Xp           	',
            u'524205	   P	,-',
            u'524205	0054	видео              	[видео]                    	Xp           	',
            u'524205	   P	-',
            u'524205	0055	и                  	[и]                        	C            	',
            u'524205	0056	бытовую            	[бытовой]                  	Apfsaf       	',
            '', '',
        ]
        actual = repair_broken_composites('\n'.join(source))

        self.assertListEqual(expected, actual.split('\n'))

    def testEndNoJoin(self):
        source = [
            '', '',
            u'523370	0083	это                	[этот]                     	Pdnsn-n      	',
            u'523370	0084	как-то             	[как-то]                   	P-----r      	',
            u'523370	   P	-',
            u'523370	0085	связанно           	[связать]                  	Xp           	c-',
            u'523370	   P	?',
            '', '',
            u'519526	0091	фото               	[фото]                     	Xp           	c-',
            u'519526	   P	-',
            u'519526	0092	и                  	[и]                        	C            	',
            u'519526	0093	видео              	[видео]                    	Xp           	c-',
            u'519526	0094	доказательства     	[доказательство]           	Ncnpa-n      	c+',
            u'519526	   P	.',
            u'520028	0001	М                  	[#Acronym]                 	Xt           	',
            u'520028	   P	-',
            u'520028	0002	де                 	[де]                       	Xp           	c-',
            u'520028	   P	,',
            u'520028	0003	скока              	[сколько]                  	C            	',
            '', '',
        ]
        expected = [
            '', '',
            u'523370	0083	это                	[этот]                     	Pdnsn-n      	',
            u'523370	0084	как-то             	[как-то]                   	P-----r      	',
            u'523370	   P	-',
            u'523370	0085	связанно           	[связать]                  	Xp           	',
            u'523370	   P	?',
            '', '',
            u'519526	0091	фото               	[фото]                     	Xp           	c-',
            u'519526	   P	-			c+',
            u'519526	0092	и                  	[и]                        	C            	',
            u'519526	0093	видео              	[видео]                    	Xp           	c-',
            u'519526	0094	доказательства     	[доказательство]           	Ncnpa-n      	c+',
            u'519526	   P	.',
            u'520028	0001	М                  	[#Acronym]                 	Xt           	',
            u'520028	   P	-',
            u'520028	0002	де                 	[де]                       	Xp           	',
            u'520028	   P	,',
            u'520028	0003	скока              	[сколько]                  	C            	',
            '', '',
        ]
        actual = repair_broken_composites('\n'.join(source))

        self.assertListEqual(expected, actual.split('\n'))

    def testNormalJoin(self):
        source = [
            '', '',
            u'518836	0001	В                  	[в]                        	Sps-l',
            u'518836	0002	середине           	[середина]                 	Ncfsl-n',
            u'518836	0003	70                 	[#Number]                  	M*---d       	c-',
            u'518836	   P	-',
            u'518836	0004	х                  	[й]                        	Mo-pgl       	c+',
            u'518836	0005	были               	[быть]                     	Vi-p--snaim-',
            u'518836	0006	очень              	[очень]                    	Rp',
            u'518836	0007	модны              	[модный]                   	Ap-p-s',
            u'518836	0008	мини               	[мини]                     	Xp           	c-',
            u'518836	   P	-',
            u'518836	0009	мини               	[мини]                     	Xp           	c-c+',
            u'518836	   P	-',
            u'518836	0010	юбки               	[юбка]                     	Ncfpn-n      	c+',
            u'518836	0011	на                 	[на]                       	Sps-l',
            u'518836	0012	пуговицах          	[пуговица]                 	Ncfpl-n',
            '', '',
            u'518836	0014	Были               	[быть]                     	Vi-p--snaim-',
            u'518836	0015	одно               	[один]                     	Xp           	c-',
            u'518836	0016	бортные            	[бортный]                  	Ap-pnf       	c+',
            u'518836	0017	и                  	[и]                        	C',
            u'518836	0018	дву                	[два]                      	Xp           	c-',
            u'518836	0019	бортные            	[бортный]                  	Ap-pnf       	c+',
            u'518836	   P	,',
            u'518836	0020	с                  	[с]                        	Sps-i',
            u'518836	0021	пуговицами         	[пуговица]                 	Ncfpi-n',
            '', '',
        ]
        expected = [
            '', '',
            u'518836	0001	В                  	[в]                        	Sps-l',
            u'518836	0002	середине           	[середина]                 	Ncfsl-n',
            u'518836	0003	70                 	[#Number]                  	M*---d       	c-',
            u'518836	   P	-',
            u'518836	0004	х                  	[й]                        	Mo-pgl       	c+',
            u'518836	0005	были               	[быть]                     	Vi-p--snaim-',
            u'518836	0006	очень              	[очень]                    	Rp',
            u'518836	0007	модны              	[модный]                   	Ap-p-s',
            u'518836	0008	мини               	[мини]                     	Xp           	c-',
            u'518836	   P	-',
            u'518836	0009	мини               	[мини]                     	Xp           	',
            u'518836	   P	-',
            u'518836	0010	юбки               	[юбка]                     	Ncfpn-n      	c+',
            u'518836	0011	на                 	[на]                       	Sps-l',
            u'518836	0012	пуговицах          	[пуговица]                 	Ncfpl-n',
            '', '',
            u'518836	0014	Были               	[быть]                     	Vi-p--snaim-',
            u'518836	0015	одно               	[один]                     	Xp           	c-',
            u'518836	0016	бортные            	[бортный]                  	Ap-pnf       	c+',
            u'518836	0017	и                  	[и]                        	C',
            u'518836	0018	дву                	[два]                      	Xp           	c-',
            u'518836	0019	бортные            	[бортный]                  	Ap-pnf       	c+',
            u'518836	   P	,',
            u'518836	0020	с                  	[с]                        	Sps-i',
            u'518836	0021	пуговицами         	[пуговица]                 	Ncfpi-n',
            '', '',
        ]
        actual = repair_broken_composites('\n'.join(source))

        self.assertListEqual(expected, actual.split('\n'))

    def testDoubleJoin(self):
        source = [
            '', '',
            u'523419	0042	крово              	[кровь]                    	Xp           	c-',
            u'523419	   P	-',
            u'523419	0043	и                  	[и]                        	C            	',
            u'523419	0044	лимфо              	[лимфа]                    	Xp           	c-',
            u'523419	0045	обращение          	[обращение]                	Ncnsa-n      	c+',
            '', '',
            u'522651	0179	макро              	[макро]                    	Xp           	c-',
            u'522651	   P	-',
            u'522651	0180	и                  	[и]                        	C            	',
            u'522651	0181	микро              	[микро]                    	Xp           	c-',
            u'522651	0182	элементы           	[элемент]                  	Ncmpa-n      	c+',
            u'522651	   P	.',
            '', '',
            u'520346	0330	аудио              	[аудио]                    	Xp           	c-',
            u'520346	   P	-',
            u'520346	0331	и                  	[и]                        	C            	',
            u'520346	0332	видео              	[видео]                    	Xp           	c-',
            u'520346	0333	продукции          	[продукция]                	Ncfsg-n      	c+',
            u'520346	   P	,',
            u'520346	0334	пропагандирующей   	[пропагандировать]         	Vpfsg-pyaimf 	',
            u'520346	0335	насилие            	[насилие]                  	Ncnsa-n      	',
            '', '',
        ]
        expected = [
            '', '',
            u'523419	0042	крово              	[кровь]                    	Xp           	c-',
            u'523419	   P	-			c+',
            u'523419	0043	и                  	[и]                        	C            	',
            u'523419	0044	лимфо              	[лимфа]                    	Xp           	c-',
            u'523419	0045	обращение          	[обращение]                	Ncnsa-n      	c+',
            '', '',
            u'522651	0179	макро              	[макро]                    	Xp           	c-',
            u'522651	   P	-			c+',
            u'522651	0180	и                  	[и]                        	C            	',
            u'522651	0181	микро              	[микро]                    	Xp           	c-',
            u'522651	0182	элементы           	[элемент]                  	Ncmpa-n      	c+',
            u'522651	   P	.',
            '', '',
            u'520346	0330	аудио              	[аудио]                    	Xp           	c-',
            u'520346	   P	-			c+',
            u'520346	0331	и                  	[и]                        	C            	',
            u'520346	0332	видео              	[видео]                    	Xp           	c-',
            u'520346	0333	продукции          	[продукция]                	Ncfsg-n      	c+',
            u'520346	   P	,',
            u'520346	0334	пропагандирующей   	[пропагандировать]         	Vpfsg-pyaimf 	',
            u'520346	0335	насилие            	[насилие]                  	Ncnsa-n      	',
            '', '',
        ]
        actual = repair_broken_composites('\n'.join(source))

        self.assertListEqual(expected, actual.split('\n'))


class TestJoinGicrComposite(unittest.TestCase):
    def testDense(self):
        source = [
            ['2', 'одно', 'одно', 'X', '_', '_', '_', '_', '_', '_'],
            ['2', 'бортные', 'бортный', 'ADJ', '_', 'Number=Plur|Case=Nom|Degree=Pos', '_', '_', '_', '_'],
        ]
        expected = ['2', 'однобортные', 'однобортный', 'ADJ', '_', 'Number=Plur|Case=Nom|Degree=Pos', '_', '_', '_',
                    '_']
        actual = join_gicr_composite(source)

        self.assertListEqual(expected, actual)

    def testSparse(self):
        source = [
            ['17', 'экс', 'экс', 'X', '_', '_', '_', '_', '_', '_'],
            ['17', '-', '-', 'PUNCT', '_', '_', '_', '_', '_', '_'],
            ['17', 'глава', 'глава', 'NOUN', '_', 'Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing', '_', '_', '_', '_']
        ]
        expected = ['17', 'экс-глава', 'экс-глава', 'NOUN', '_', 'Animacy=Anim|Case=Nom|Gender=Masc|Number=Sing', '_',
                    '_', '_', '_']
        actual = join_gicr_composite(source)

        self.assertListEqual(expected, actual)

    def testHalf(self):
        source = [
            ['17', 'экс', 'экс', 'X', '_', '_', '_', '_', '_', '_'],
            ['17', '-', '-', 'PUNCT', '_', '_', '_', '_', '_', '_'],
        ]
        expected = ['17', 'экс-', 'экс-', 'X', '_', '_', '_', '_', '_', '_']
        actual = join_gicr_composite(source)

        self.assertListEqual(expected, actual)

    def testContinuous(self):
        source = [
            ['9', 'мини', 'мини', 'X', '_', '_', '_', '_', '_', 'SpaceAfter=No'],
            ['9', '-', '-', 'PUNCT', '_', '_', '_', '_', '_', 'SpaceAfter=No'],
            ['9', 'шорто', 'шорты', 'X', '_', '_', '_', '_', '_', 'SpaceAfter=No'],
            ['9', '-', '-', 'PUNCT', '_', '_', '_', '_', '_', 'SpaceAfter=No'],
            ['9', 'юбки', 'юбка', 'NOUN', '_', 'Animacy=Inan|Case=Nom|Gender=Fem|Number=Plur', '_', '_', '_', '_'],
        ]
        expected = [
            '9', 'мини-шорто-юбки', 'мини-шорты-юбка', 'NOUN', '_', 'Animacy=Inan|Case=Nom|Gender=Fem|Number=Plur', '_',
            '_', '_', '_']
        actual = join_gicr_composite(source)

        self.assertListEqual(expected, actual)


class TestConvertGicrFormat(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def testNormal(self):
        gicr_files = [
            os.path.join(os.path.dirname(__file__), 'data', 'gicr-man1-src.txt'),
            os.path.join(os.path.dirname(__file__), 'data', 'gicr-man2-src.txt')
        ]
        act_file = os.path.join(self.temp_dir, 'gicr-cnv-act.conllu')

        convert_gicr_format(gicr_files, act_file)
        with open(act_file, 'rb') as df:
            actual = df.read().decode('utf-8')
            # print(actual)

        trg_file = os.path.join(os.path.dirname(__file__), 'data', 'gicr-cnv-trg.conllu')
        with open(trg_file, 'rb') as tf:
            expected = tf.read().decode('utf-8')

        self.assertListEqual(expected.split('\n'), actual.split('\n'))

    def testGold(self):
        gicr_files = [
            os.path.join(os.path.dirname(__file__), 'data', 'gicr-gold-src.txt'),
        ]
        act_file = os.path.join(self.temp_dir, 'gicr-cnv-act.conllu')

        convert_gicr_format(gicr_files, act_file)
        with open(act_file, 'rb') as df:
            actual = df.read().decode('utf-8')

        trg_file = os.path.join(os.path.dirname(__file__), 'data', 'gicr-gold-trg.conllu')
        with open(trg_file, 'rb') as tf:
            expected = tf.read().decode('utf-8')

        actual = [w for w in actual.split('\n') if '\t~' not in w]
        expected = [w for w in expected.split('\n') if '\t~' not in w]
        self.assertListEqual(expected, actual)
