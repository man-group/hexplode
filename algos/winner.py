"""
This is the winning algo from the Man AHL Coder Prize 2016
Written by Hamed Ahmadi from the University of Oxford
"""
from hexplode import algo_player
import os
import time
import string
import random

Verbose = True

#Names of tiles (used in interface with code bundle)
names =	 ['tile_0_0', 'tile_0_1', 'tile_0_2', 'tile_0_3', 'tile_1_0', 'tile_1_1', 'tile_1_2', 'tile_1_3', 'tile_1_4', 'tile_2_0', 'tile_2_1', 'tile_2_2', 'tile_2_3', 'tile_2_4', 'tile_2_5', 'tile_3_0', 'tile_3_1', 'tile_3_2', 'tile_3_3', 'tile_3_4', 'tile_3_5', 'tile_3_6', 'tile_4_0', 'tile_4_1', 'tile_4_2', 'tile_4_3', 'tile_4_4', 'tile_4_5', 'tile_5_0', 'tile_5_1', 'tile_5_2', 'tile_5_3', 'tile_5_4', 'tile_6_0', 'tile_6_1', 'tile_6_2', 'tile_6_3']

#Number of neighbours
Deg = (3, 4, 4, 3, 4, 6, 6, 6, 4, 4, 6, 6, 6, 6, 4, 3, 6, 6, 6, 6, 6, 3, 4, 6, 6, 6, 6, 4, 4, 6, 6, 6, 4, 3, 4, 4, 3)

#Neighbours of Tiles
Nei = (
	(1, 4, 5), (0, 2, 5, 6), (1, 3, 6, 7), (2, 7, 8), (5, 9, 10, 0), (4, 6, 10, 11, 0, 1), 
	(5, 7, 11, 12, 1, 2), (6, 8, 12, 13, 2, 3), (7, 13, 14, 3), (10, 15, 16, 4), (9, 11, 16, 17, 4, 5), 
	(10, 12, 17, 18, 5, 6), (11, 13, 18, 19, 6, 7), (12, 14, 19, 20, 7, 8), (13, 20, 21, 8), 
	(16, 9, 22), (15, 17, 9, 22, 10, 23), (16, 18, 10, 23, 11, 24), (17, 19, 11, 24, 12, 25), 
	(18, 20, 12, 25, 13, 26), (19, 21, 13, 26, 14, 27), (20, 14, 27), (23, 15, 16, 28), 
	(22, 24, 16, 17, 28, 29), (23, 25, 17, 18, 29, 30), (24, 26, 18, 19, 30, 31), (25, 27, 19, 20, 31, 32), 
	(26, 20, 21, 32), (29, 22, 23, 33), (28, 30, 23, 24, 33, 34), (29, 31, 24, 25, 34, 35), 
	(30, 32, 25, 26, 35, 36), (31, 26, 27, 36), (34, 28, 29), (33, 35, 29, 30), (34, 36, 30, 31), (35, 31, 32)
  )

#Scores of tiles based on number of pieces
TileScore = ((0, 76, 120, 0, 0, 0), (0, 51, 115, 140, 0, 0), (0, 51, 115, 140, 0, 0), (0, 76, 120, 0, 0, 0), (0, 51, 115, 140, 0, 0), (0, 10, 53, 92, 127, 238), (0, 10, 53, 92, 127, 238), (0, 10, 53, 92, 127, 238), (0, 51, 115, 140, 0, 0), (0, 51, 115, 140, 0, 0), (0, 10, 53, 92, 127, 238), (0, 10, 53, 92, 127, 238), (0, 10, 53, 92, 127, 238), (0, 10, 53, 92, 127, 238), (0, 51, 115, 140, 0, 0), (0, 76, 120, 0, 0, 0), (0, 10, 53, 92, 127, 238), (0, 10, 53, 92, 127, 238), (0, 10, 53, 92, 127, 238), (0, 10, 53, 92, 127, 238), (0, 10, 53, 92, 127, 238), (0, 76, 120, 0, 0, 0), (0, 51, 115, 140, 0, 0), (0, 10, 53, 92, 127, 238), (0, 10, 53, 92, 127, 238), (0, 10, 53, 92, 127, 238), (0, 10, 53, 92, 127, 238), (0, 51, 115, 140, 0, 0), (0, 51, 115, 140, 0, 0), (0, 10, 53, 92, 127, 238), (0, 10, 53, 92, 127, 238), (0, 10, 53, 92, 127, 238), (0, 51, 115, 140, 0, 0), (0, 76, 120, 0, 0, 0), (0, 51, 115, 140, 0, 0), (0, 51, 115, 140, 0, 0), (0, 76, 120, 0, 0, 0))

#Used to update scores quickly.  TileDelta[i][j] = TileScore[i][j+1]-TileScore[i][j]
TileDelta = ((76, 44, 0, 0, 0), (51, 64, 25, 0, 0), (51, 64, 25, 0, 0), (76, 44, 0, 0, 0), (51, 64, 25, 0, 0), (10, 43, 39, 35, 111), (10, 43, 39, 35, 111), (10, 43, 39, 35, 111), (51, 64, 25, 0, 0), (51, 64, 25, 0, 0), (10, 43, 39, 35, 111), (10, 43, 39, 35, 111), (10, 43, 39, 35, 111), (10, 43, 39, 35, 111), (51, 64, 25, 0, 0), (76, 44, 0, 0, 0), (10, 43, 39, 35, 111), (10, 43, 39, 35, 111), (10, 43, 39, 35, 111), (10, 43, 39, 35, 111), (10, 43, 39, 35, 111), (76, 44, 0, 0, 0), (51, 64, 25, 0, 0), (10, 43, 39, 35, 111), (10, 43, 39, 35, 111), (10, 43, 39, 35, 111), (10, 43, 39, 35, 111), (51, 64, 25, 0, 0), (51, 64, 25, 0, 0), (10, 43, 39, 35, 111), (10, 43, 39, 35, 111), (10, 43, 39, 35, 111), (51, 64, 25, 0, 0), (76, 44, 0, 0, 0), (51, 64, 25, 0, 0), (51, 64, 25, 0, 0), (76, 44, 0, 0, 0))

#Zobrist hashing, random but precomputed in order to have deterministic behaviour that can be tested and compared across separate runs
HashValue = [[0, 957404739, 737627720, 506909541, 603316298, 743530335], [0, 419034014, 871807847, 396048410, 491725293, 877117765], [0, 660359045, 806270242, 953615266, 319078269, 124811863], [0, 464680278, 1058824884, 116506195, 139883665, 89588615], [0, 287088092, 919366470, 800010390, 117881596, 1034673060], [0, 231089532, 153707825, 38209871, 469612018, 921408234], [0, 1010075367, 440649716, 128763651, 942505994, 728497233], [0, 612439690, 560636471, 161384706, 451051018, 68638516], [0, 162702047, 899865245, 440567965, 885444876, 760828847], [0, 523251953, 591528692, 703884277, 859442972, 1013734810], [0, 167298075, 541891971, 654990718, 470491928, 408170938], [0, 196523232, 1026390851, 684102165, 568763501, 247388494], [0, 440569334, 244898437, 52466807, 391576047, 288776022], [0, 24221028, 871385973, 679877987, 456182704, 923546870], [0, 455108317, 176400336, 116205608, 385225077, 339832554], [0, 656417129, 692583211, 844652771, 10060768, 100761832], [0, 1030917337, 593373931, 56035629, 144660163, 242049369], [0, 45192516, 143872095, 336586955, 871286468, 848372605], [0, 326220215, 854470029, 301057975, 398385977, 961630744], [0, 584896555, 135644371, 454995623, 196466617, 277224538], [0, 1017834009, 169928022, 69281945, 134646546, 307770314], [0, 375421648, 128874843, 792346196, 560599466, 797287761], [0, 547730378, 893563011, 158171373, 632232505, 92784125], [0, 387331304, 132498688, 608068533, 947389939, 155838190], [0, 927355297, 131540820, 112936392, 481532855, 475510096], [0, 675306458, 116957507, 596043458, 312253620, 883632654], [0, 600277408, 581639647, 570813782, 73375080, 537469812], [0, 325906122, 409959815, 583296362, 167907127, 610117418], [0, 695562130, 409360960, 816655001, 418802572, 785221123], [0, 480499666, 679843530, 767376724, 963430942, 677503321], [0, 103262362, 411767477, 1034235967, 764239616, 628382276], [0, 454733641, 952894708, 526040728, 455768771, 551967479], [0, 50289568, 1045357488, 157504432, 431894735, 856032001], [0, 644376939, 762761194, 840151426, 680470993, 802227478], [0, 560790392, 555716849, 381825418, 271367150, 815931712], [0, 100531698, 825073531, 488025153, 747231431, 803405150], [0, 247111689, 1065589964, 491608349, 815445598, 874740707]]
HashDelta = [[957404739, 317167627, 901881133, 1036202799, 262455061], [419034014, 722422009, 611156861, 181672439, 688447656], [660359045, 391312039, 148485760, 735296735, 343196970], [464680278, 615389154, 971889895, 245877442, 218199830], [287088092, 668006042, 425941968, 682199658, 984441176], [231089532, 82788429, 191786110, 431668413, 756426520], [1010075367, 645349651, 502202615, 1065436937, 323386459], [612439690, 99333309, 687090485, 326956808, 519383358], [162702047, 1007712322, 803230208, 780425617, 429884067], [523251953, 1014116869, 179726593, 449733865, 257315462], [167298075, 699685272, 122077437, 989953638, 73339554], [196523232, 916180899, 367782230, 153106040, 794328355], [440569334, 349853555, 230182642, 343305624, 106997433], [24221028, 847371793, 460740118, 867620563, 742195014], [455108317, 295944461, 208572408, 270219613, 45580191], [656417129, 241687106, 455056328, 851567363, 110625544], [1030917337, 506242610, 537469894, 197681134, 116537242], [45192516, 170050843, 480032916, 669068815, 25159097], [326220215, 564106298, 589294138, 105849998, 787460385], [584896555, 717821176, 319515252, 279673118, 456379363], [1017834009, 915017551, 234999247, 203924363, 442415320], [375421648, 298713995, 680806159, 240136190, 250590459], [547730378, 367461193, 1009725550, 750951124, 539549636], [387331304, 284422632, 601597621, 474375750, 825352989], [927355297, 814839541, 23880348, 436788863, 14954215], [675306458, 783874713, 629032833, 823818870, 641185466], [600277408, 23895167, 11464841, 643461182, 609664540], [325906122, 184783693, 984291565, 684091997, 778020893], [695562130, 823342546, 684421337, 677069077, 909897103], [480499666, 874922264, 87600030, 349304650, 286075719], [103262362, 514636335, 623780490, 271085375, 150537540], [454733641, 601271229, 664189548, 74499163, 1003233332], [50289568, 1018279952, 925741056, 282944383, 716714958], [644376939, 186558081, 526745192, 446470227, 123612359], [560790392, 7564169, 937271675, 116296292, 546216622], [100531698, 886071945, 742077242, 832533638, 57353625], [247111689, 825834693, 583976401, 769126211, 79285693]]

#Zobrist hashes added for the damaged squares
HashValueC = [[0, 1276501963009977160, 4088172142995423328, 280090744475219446, 3573919172305981897, 3612569311715104909], [0, 2691251497347002730, 1260803886667310114, 1304004741778739529, 336751064060271249, 3077381975381127980], [0, 95684190084171570, 3185014639425545343, 119302865903059806, 2623096932122859572, 428705146146624874], [0, 10282288364157881, 909625060860585543, 4106209314998555676, 246999705911415560, 421073214019827005], [0, 2285977307425084560, 3282033966153816162, 3852661186847099571, 2637455765914151205, 147056806023815194], [0, 2200084217690641161, 196656743776201671, 3353142000559317385, 368478615372920971, 3602821415576626014], [0, 4252354917878930397, 536399635051780101, 1729173003933979707, 2941001165881086030, 804505859742031973], [0, 3960437687182606528, 1022093036257312837, 898936984883536008, 3992229504867035541, 4408645881646317666], [0, 3476982050921218066, 3257794193943899853, 3466043264574990293, 904405301152523817, 1360933653645364167], [0, 1586888225112129228, 396907974691354649, 1827951897083467932, 469717998259225568, 4166920352354519823], [0, 1090789678173301671, 1201510311982871951, 2309734871726322061, 438054943448624487, 3182433530837985420], [0, 3475380071463827064, 3289209760394082352, 3238274288400990561, 4014451234385529999, 1854915304654209566], [0, 1785214173431784767, 4516733839155330196, 3801725686766392406, 3302700948739864310, 2787441489764849854], [0, 4163670295694147690, 276798584837350501, 693282806833815200, 3394435745476847979, 4486263644921700669], [0, 749463752838082661, 2701279008944639216, 2473252729502503732, 1318012320419085395, 4028584339809170515], [0, 2514291101913299088, 561001430973792483, 3027216428955593598, 3326909927442372257, 1964045077653388265], [0, 2263526654716239294, 4385145354241600948, 3733524436953264812, 1715041488923659258, 262842983133999756], [0, 2199865944800827233, 784439101054158975, 1390639322590330661, 3331488381828487334, 2092548923499634416], [0, 1720160377704727810, 1004668902430258205, 842582536587581779, 4222515958925727464, 1620212693655885683], [0, 3777233680727053055, 4369623213236861944, 2723015597561880837, 3529336895211336229, 614862573322451823], [0, 881500200963342605, 2798802679042922353, 4239381437511517585, 2121852812496500248, 2570712498581227156], [0, 2473581433079116241, 3351461499972085945, 2881300311837231315, 3328953246060685502, 3808431115799432992], [0, 2023035647514886709, 1099795071011283579, 1344243777307657327, 3801502561604722440, 3523100758695857603], [0, 3789180145290713916, 1641325678227470703, 987474988595580949, 3507580809791917935, 4076176515055926201], [0, 940746155699173242, 3823190641913973319, 2699759198233611704, 2753018200675376098, 1148566505759586184], [0, 981839304363928013, 3755464181004856187, 1459054192807363160, 3831206044574340361, 3071778001554401604], [0, 455445024916489055, 1116675114181111491, 1702659335864176455, 3354157063905796092, 2365584789417656243], [0, 962736576180393782, 1514679765426763322, 2658369442710007651, 3629597680999765438, 2926868441321099058], [0, 2204878264813339290, 4036064057349528956, 4601635534651597611, 2251014622020280068, 2017801957453069052], [0, 1396544967591122395, 331137177085105900, 2006325554325372737, 1029682069073163944, 1268666191199225658], [0, 2992950313048781793, 4388375565924614149, 1369746380164678738, 2902211222358567483, 971911509692991834], [0, 4365806697529640452, 3878896474556435565, 2495795999630063778, 4392501173711101718, 95560878389260487], [0, 2190283169465479625, 830871795267025805, 46403599003039511, 4300823021185199264, 3205210136477538459], [0, 2561433001825466243, 2287516788160987473, 1286179644633792440, 963374046491588714, 796374790120078614], [0, 3059305926016974522, 2571764504851249422, 440634730809879094, 97876858225907379, 3880398409512244589], [0, 2054294713378736831, 4362800598166299740, 3437655820653654769, 3548622155590907372, 3064309947780889405], [0, 2880974875649580022, 481417786582439662, 2847860772685800780, 90970691135069475, 4226326235837436289]]
HashDeltaC = [[1276501963009977160, 2957476421375601448, 4278155674001749398, 3637230098980037695, 268931934187424068], [2691251497347002730, 3757823491050018120, 245313221179290987, 1636108665350622168, 3321809160374593981], [95684190084171570, 3269755935739241293, 3284435448536393505, 2720391397672688490, 2419574069896285534], [10282288364157881, 917367097213787646, 3775015607431393883, 4292400422948849428, 484830992036308533], [2285977307425084560, 3617882259034492146, 1800109919637705425, 1291766615337771926, 2778812682047064383], [2200084217690641161, 2031948839901198542, 3184725149776661070, 3140655714228672770, 3810840936443550677], [4252354917878930397, 4355766873911329752, 1193151600890678334, 4553079115455136885, 2592566141050089515], [3960437687182606528, 4096438533107105925, 168496168189632717, 4260007198247045405, 741290221893216759], [3476982050921218066, 2123089126890319583, 2103138639628962072, 4365338412560777724, 2192714424937426414], [1586888225112129228, 1407335154769299157, 2079582362329817221, 2295418088951126908, 4564145319359973615], [1090789678173301671, 2274278425220587048, 3504166525347120130, 2745395900796869866, 3043886655384061419], [3475380071463827064, 2134311616191909448, 96044089902201169, 1965429185027608046, 3317967121944940177], [1785214173431784767, 2767729890889439659, 751212871406758082, 1808191252140417696, 827385006105210440], [4163670295694147690, 4188126420817257487, 740960690767444677, 2775479993407256523, 1250061533611264086], [749463752838082661, 3394165721598311573, 517382561154883524, 3465598494082461543, 2711990665346811904], [2514291101913299088, 2678970783410845811, 3299949516197866397, 299871723593121247, 3848957432110656840], [2263526654716239294, 2572262410416762890, 1083976381442858776, 2602281875364706646, 1470640134935148918], [2199865944800827233, 1469753885543866142, 1850531036693083994, 4429105587868264323, 3688985897608939094], [1720160377704727810, 1886570315513229599, 450422984494853454, 3542107215453196219, 3235068017912021403], [3777233680727053055, 634843910784952583, 1832434443815394045, 1526897804965204768, 4067550308015884618], [881500200963342605, 3093110884258076284, 2018200605268480736, 2857282247760163721, 4530432665921466508], [2473581433079116241, 923560419981089128, 684167966777679978, 706711136654024813, 1938960971331643294], [2023035647514886709, 1391618854937534542, 2154118503289431572, 2766917608088017767, 298705462232486603], [3789180145290713916, 2473309926919610963, 1977957952520923514, 4402648434130902906, 593369970787579094], [940746155699173242, 4035366025181674813, 1187203238352357375, 235268930191365722, 3009574781357321322], [981839304363928013, 4160806413106381494, 2315286476971878691, 2383731964143015761, 2272638067689700429], [455445024916489055, 661231792507153820, 1791928785489584516, 4120041254011998395, 1033684696518008911], [962736576180393782, 1754551074590155020, 3594248350343387481, 1637770055534590685, 1927743549008009868], [2204878264813339290, 2782019478633291750, 567086054871629399, 2369314500659887151, 233512011037238776], [1396544967591122395, 1727668932819911479, 2256173620026894765, 1557625436034025961, 2292648109576794514], [2992950313048781793, 1544660044251558884, 3451152873153823831, 4270794162384825961, 2682550968134460257], [4365806697529640452, 667357127889980009, 1690612342300734671, 2186380755230468020, 4442463032774864849], [2190283169465479625, 1577011449183177284, 802488101462609050, 4254577919909747639, 1717180303621583931], [2561433001825466243, 4337790904519685842, 1037949923077144297, 2055886657810991058, 455951192700798332], [3059305926016974522, 703802577482991540, 2715051288265134904, 524326893543373957, 3783669859313681374], [2054294713378736831, 2308545811622358755, 1386767587610531501, 2200638223117371165, 1997804544225922769], [2880974875649580022, 2401845285239524632, 2390273019449308066, 2794082333738088559, 4316097767808355490]]

nodecnt = 0

class Timer:
		
	def reset(self):
		self.base = time.time()
		self.count = 100
		self.timeout = False
		
	def gettime(self):
		return time.time() - self.base
		
	def hastimedout(self):
		return self.timeout
		
	def checkexpired(self):
		if self.timeout:
			return True
		self.count -= 1
		if (self.count<0):
			self.count = 100
			if time.time()-self.base > 4.70:
				self.timeout = True
				
timer = Timer()

class Board:
			
	def __init__(self):		
		self.a=[0 for i in range(37)]	# Current player's pieces
		self.b=[0 for i in range(37)]	# Opponent's pieces
		self.c=[0 for i in range(37)]	# Damaged squares
		self.pval = 0					# Total value of current player's pieces in tiles
		self.opval = 0					# Total value of opponent's pieces in tiles
		self.hval = 0					# Current player's combined Zobrist Hash value 
		self.ohval = 0					# Opponent's combined Zobrist Hash value
		self.chval = 0					# Hash value for damaged squares

	def calcdata(self):
		for i in range(37):
			self.add(i)
	
	# Register a tile and update values (Used when initializing a game state read from the bundle)
	def add(self, i):
		if (self.a[i]>0):
			self.pval += TileScore[i][self.a[i]]
			self.hval ^= HashValue[i][self.a[i]]

		if (self.b[i]>0):
			self.opval += TileScore[i][self.b[i]]
			self.ohval ^= HashValue[i][self.b[i]]
		
		if (self.c[i]>0):
			self.chval ^= HashValueC[i][self.c[i]]
	
	def eval(self):
		return self.pval - self.opval
				
	#place a piece in the position, return true if it results in a win
	def place(self, pos):
		if (self.c[pos] > 0):
			self.c[pos] -= 1
			return False

		if (self.b[pos] > 0):
			self.opval -= TileScore[pos][self.b[pos]]
			
			if (self.opval == 0):
				return True
			self.a[pos] = self.b[pos]
			self.b[pos] = 0 
		else:
			self.pval -= TileScore[pos][self.a[pos]]

		self.a[pos] += 1		
		if self.a[pos] == Deg[pos]:
			self.a[pos] = 0
			for nei in Nei[pos]:
				if (self.place(nei)):
					return True
		else:
			#inline special case
			self.pval += TileScore[pos][self.a[pos]]
					
		return False
				
	#place a piece in the position for the opponent, return true if it results in a win (for the opponent)
	def place_rev(self, pos):
		if (self.c[pos] > 0):
			self.c[pos] -= 1
			return False
		
		if (self.a[pos] > 0):
			self.pval -= TileScore[pos][self.a[pos]]
			if (self.pval == 0):
				return True
			self.b[pos] = self.a[pos]
			self.a[pos] = 0
		else:
			self.opval -= TileScore[pos][self.b[pos]]
		
		self.b[pos] += 1		
		if self.b[pos] == Deg[pos]:
			self.b[pos] = 0
			for nei in Nei[pos]:
				if (self.place_rev(nei)):
					return True
		else:
			#inline special case
			self.opval += TileScore[pos][self.b[pos]]
					
		return False
	
	#same as place_rev, but updates hash values
	def place_rev_hash(self, pos):
		if (self.c[pos] > 0):
			self.c[pos] -= 1
			self.chval ^= HashDeltaC[pos][self.c[pos]]
			return False
		
		if (self.a[pos] > 0):
			self.pval -= TileScore[pos][self.a[pos]]
			self.hval ^= HashValue[pos][self.a[pos]]
			if (self.pval == 0):
				return True
			self.b[pos] = self.a[pos]
			self.a[pos] = 0
		else:
			self.opval -= TileScore[pos][self.b[pos]]
			self.ohval ^= HashValue[pos][self.b[pos]]
		
		self.b[pos] += 1		
		if self.b[pos] == Deg[pos]:
			self.b[pos] = 0
			for nei in Nei[pos]:
				if (self.place_rev_hash(nei)):
					return True
		else:
			#inline special case
			self.opval += TileScore[pos][self.b[pos]]
			self.ohval ^= HashValue[pos][self.b[pos]]
					
		return False
	
	#builds a reversed copy of the board, and places a piece at pos
	def build_rev(self,b,pos):
		self.a[:] = b.b
		self.b[:] = b.a
		self.c[:] = b.c
		
		self.pval = b.opval
		self.opval = b.pval
		
		return self.place_rev(pos)

	#same as build_rev, but updates hash values
	def build_rev_hash(self,b,pos):
		self.a[:] = b.b
		self.b[:] = b.a
		self.c[:] = b.c
		
		self.pval = b.opval
		self.opval = b.pval
		self.hval = b.ohval
		self.ohval = b.hval
		self.chval = b.chval
		
		return self.place_rev_hash(pos)	
		
	#Minor optimization: Save a few if statements if we already know the position will explode
	def build_rev_cap(self,b,pos):	
		#based on assumption that opponent owns pos (after rev), and position will pop
		self.a[:] = b.b
		self.b[:] = b.a
		self.c[:] = b.c
		
		self.pval = b.opval
		self.opval = b.pval - TileScore[pos][self.b[pos]]
		
		self.b[pos] = 0
		for nei in Nei[pos]:
			if (self.place_rev(nei)):
				return True
				
		return False

	#Same as build_rev_cap, but updates hash values
	def build_rev_cap_hash(self,b,pos):	
		#based on assumption that opponent owns pos (after rev), and position will pop
		self.a[:] = b.b
		self.b[:] = b.a
		self.c[:] = b.c
		
		self.pval = b.opval
		self.opval = b.pval - TileScore[pos][self.b[pos]]
		self.hval = b.ohval
		self.ohval = b.hval ^ HashValue[pos][self.b[pos]]
		self.chval = b.chval
		
		self.b[pos] = 0
		for nei in Nei[pos]:
			if (self.place_rev_hash(nei)):
				return True
				
		return False
		
	#Builds a copy of the board, and places a piece for the opponent.  (i.e. opponent moves, and then it's our turn in the copy)
	def build(self,b,pos):
		self.a[:] = b.a
		self.b[:] = b.b
		self.c[:] = b.c
		
		self.pval = b.pval
		self.opval = b.opval
		
		return self.place_rev(pos)  #NOT A BUG! we always move for negative

	#Minor optimization, used if we already know that the position will hexplode
	def build_cap(self,b,pos):
		#based on assumption that player owns pos and position will pop
		self.a[:] = b.a
		self.b[:] = b.b
		self.c[:] = b.c
		self.pval = b.pval
		self.opval = b.opval - TileScore[pos][self.b[pos]]
		
		self.b[pos] = 0
		for nei in Nei[pos]:
			if (self.place_rev(nei)):
				return True
				
		return False
		
	def gethash(self):
		return ((self.hval<<30) | self.ohval) ^ self.chval
	
	#used for testing
	def gethash_slow(self):
		x = 0
		for i in range(37):
			x^=HashValue[i][self.a[i]]<<30
			x^=HashValue[i][self.b[i]]
			x^=HashValueC[i][self.c[i]]
		return x
		
	#Reverse Board
	def reverse(self): 
		self.a,self.b = self.b,self.a
		self.pval, self.opval = self.opval, self.pval
		self.hval, self.ohval = self.ohval, self.hval

	#helper functions, not used in execution:
		
	def write(self):
		x=[0 for i in range(37)]
		y=[0 for i in range(37)]
		k=0
		maxx=0; maxy=0;
		for i in range(7):
			for j in range (7-abs(i-3)):
				x[k]=3+i*4;
				y[k]=j*2+abs(i-3);
				maxx=max(maxx, x[k]);
				maxy=max(maxy, y[k]);
				k+=1

		for yy in range (maxy+1):
			xx=0
			while xx <= maxx:
				found=False 				
				for i in range(37):
					if (x[i]==xx and y[i]==yy):
						if (self.a[i] != 0):
							print('{:2d}'.format(self.a[i]),end='')
						elif (self.b[i] != 0):
							print('{:2d}'.format(-self.b[i]),end='')
						else:
							print(' .',end='')
						found = True
						xx+=1
						break
				if not found:
					print(' ',end='')					
				xx+=1
			print('')
	
	
class Entry:
	def __init__(self):
		self.depth = 0
		self.bestmove = -1
		self.lo = -999999
		self.hi = 999999		

mcache = [[Board() for j in range(37)] for i in range(100)]

hashtable = {}
	
#Tight search function for minimizer, for the bottom few levels of the tree
#This is a bit copy&paste work, but it works faster than negamax, and additionally it saves having to reverse or copy the game board
def search_rev(b, d, alpha, beta): 
	#global nodecnt
	global mcache
	
	#nodecnt+=1
	
	base = b.pval - b.opval
	
	#Instead of searching all the way down to leaves, we determine the value of nodes one level above the leaf level
	#This saves a bit of time that we would have spent building and sorting the moves (Actually it results in a 2x speed increase)
	if d==1:
		cache = mcache[1][0]
		for i in range(37):
			if b.a[i]==0:
				if b.b[i] == Deg[i] - 1:
					if cache.build_cap(b, i):
						return alpha
					x = cache.pval - cache.opval
				elif b.c[i]==0:
					x = base - TileDelta[i][b.b[i]]
				else:
					x = base
				if x < beta:
					if x <=alpha:
						return alpha
					beta = x
		return beta
	
	if (timer.checkexpired()):
		return 0
	
	moves = []		

	for i in range(37):
		if (b.a[i]==0):
			if (b.b[i] == Deg[i]-1): #hot
				if mcache[d][i].build_cap(b, i): #game over 
					return alpha
				if (mcache[d][i].opval>0) :
					moves.append((mcache[d][i].eval(),i))
			elif b.c[i]==0:
				moves.append((base - TileDelta[i][b.b[i]],i))
			elif b.opval>0:
				moves.append((base, i))
				
	moves.sort()
	
	for move in moves:
		k = move[1]
		if (b.b[k] == Deg[k]-1): #hexplode
			x = search(mcache[d][k], d-1, alpha, beta)
		elif b.c[k]==0:
			delta = TileDelta[k][b.b[k]]
			b.opval+=delta
			b.b[k]+=1
			x = search(b, d-1, alpha, beta)
			b.b[k]-=1
			b.opval-=delta
		else:
			b.c[k]-=1
			x=search(b,d-1,alpha,beta)
			b.c[k]+=1
		
		if (x < beta):
			if x <= alpha:
				return alpha
			beta = x
		
	return beta
	
#Tight function, used to search the bottom of the tree	
#Note that it avoids function calls, preferring to do the work inline -- this results in significant performance improvements
def search(b, d, alpha, beta):
	#global nodecnt
	global mcache
	
	#nodecnt+=1
	
	base = b.pval - b.opval
		
	#Instead of searching all the way down to leaves, we determine the value of nodes one level above the leaf level
	#This saves a bit of time that we would have spent building and sorting the moves (Actually it results in a 2x speed increase)
	if d==1:
		cache = mcache[1][0]  # just grab a board
		for i in range(37):
			if b.b[i] == 0:
				if b.a[i] == Deg[i] - 1:
					if cache.build_rev_cap(b, i):
						return beta
					x = cache.opval - cache.pval
				elif b.c[i]==0:
					x = base + TileDelta[i][b.a[i]]
				else:
					x=base
				if (x > alpha):
					if (x>=beta):
						return beta
					alpha = x
		return alpha
	
	if (timer.checkexpired()):
		return 0
	
	moves = []		
	
	for i in range(37):
		if (b.b[i]==0):
			if (b.a[i] == Deg[i]-1): #hot
				if mcache[d][i].build_rev_cap(b, i): #game over
					return beta
				if (mcache[d][i].opval>0):
					moves.append((-mcache[d][i].eval(),i))
			elif b.c[i]==0:
				moves.append((base + TileDelta[i][b.a[i]],i))
			elif b.pval>0:
				moves.append((base,i))
				
	moves.sort(reverse = True)
	
	for move in moves:
		k = move[1]
		
		if (b.a[k] == Deg[k]-1): #hexplode
			x = -search(mcache[d][k], d-1, -beta, -alpha)
		elif b.c[k]==0:
			delta = TileDelta[k][b.a[k]]
			b.pval += delta
			b.a[k]+=1
			x = search_rev(b, d-1, alpha, beta)
			b.a[k]-=1
			b.pval -= delta
		else:
			b.c[k]-=1
			x = search_rev(b, d-1, alpha, beta)
			b.c[k]+=1
		
		if (x > alpha):
			if x >= beta:
				return beta
			alpha = x  
		
	return alpha	
	
#Used to search the top levels of the tree
def search_hi(b, d, alpha, beta):
	global mcache
	#global nodecnt
	global hashtable
	
	if d<=2:
		return search(b,d,alpha,beta)

	if (timer.checkexpired()):
		return 0
		
	hash = b.gethash()
	if hash in hashtable:
		hashe = hashtable[hash]
	else:
		hashe = Entry()
		hashtable[hash]=hashe
	
	if (hashe.depth==d):
		if hashe.hi<=alpha: 
			return alpha
		if hashe.lo>=beta: 
			return beta
		if hashe.lo==hashe.hi: 
			return hashe.lo
		if hashe.hi<beta:
			beta = hashe.hi
		if hashe.lo>alpha:
			alpha = hashe.lo
	else:
		hashe.depth = d
		hashe.lo=-999999
		hashe.hi=999999
	
	#nodecnt+=1

	moves = []

	for i in range(37):
		if (b.b[i]==0):
			if (b.a[i] == Deg[i]-1): #hot
				if mcache[d][i].build_rev_cap_hash(b, i): #Hexmate, game over!
					hashe.bestmove = i
					hashe.lo = 999999
					return beta
				if (mcache[d][i].opval==0):
					continue
				score = -mcache[d][i].eval()
			elif b.c[i]==0:
				score = b.pval - b.opval + TileDelta[i][b.a[i]]
			elif b.pval>0:
				score = b.pval - b.opval
			else:
				continue
			if (i==hashe.bestmove):
				score+=100000
			moves.append((score,i))

	moves.sort(reverse = True)
	
	for move in moves:
		k = move[1]
		
		if (b.a[k] == Deg[k]-1): #capture 
			x = -search_hi(mcache[d][k], d-1, -beta, -alpha)
			
		elif b.c[k]==0:
			delta = TileDelta[k][b.a[k]]
			hdelta = HashDelta[k][b.a[k]]
			b.pval += delta
			b.hval ^= hdelta
			b.a[k]+=1
			b.reverse()
			x = -search_hi(b, d-1, -beta, -alpha)
			b.reverse()
			b.a[k]-=1
			b.pval -= delta
			b.hval ^= hdelta
		else:
			hdelta = HashDeltaC[k][b.c[k]-1]
			b.c[k]-=1
			b.chval^=hdelta
			b.reverse()
			x = -search(b,d-1,-beta,-alpha)
			b.reverse()
			b.chval^=hdelta
			b.c[k]+=1

	
		if (x > alpha):
			hashe.bestmove = k
			if x >= beta:
				hashe.lo = beta
				return beta
			alpha = x
			hashe.lo = x
			
	hashe.hi = alpha
		
	return alpha	
	
def search_top(b, d, alpha, beta, bestmove):
	global mcache
	#global nodecnt

	#nodecnt+=1
	
	moves = []		
	
	for i in range(37):
		if (b.b[i]==0):
			if mcache[d][i].build_rev_hash(b, i): #game over
				return beta, i
			if mcache[d][i].opval==0:
				continue
			score = -mcache[d][i].eval()
			if i == bestmove:
				score += 100000
			moves.append((score,i))

	moves.sort(reverse = True)
	
	if (bestmove==-1):	#to avoid making illegal moves when value is -inf
		bestmove = moves[0][1]

	#Negascout at root level, very helpful for positive scores
	k=moves[0][1]
	x=-search_hi(mcache[d][k], d-1, -beta, -alpha)
	start = 1
	if (x>alpha):
		bestmove = k
		alpha=x
		if x>=beta:
			return beta, bestmove
		fail = False

		for i in range(1, len(moves)):
			l = moves[i][1]
			y = -search_hi(mcache[d][l], d-1, -alpha-1, -alpha)
			if y>alpha:
				fail = True
				start = i
				break

		if not fail:
			return alpha, bestmove
			
	for move in moves[start:]:
		l = move[1]
		y = -search_hi(mcache[d][l], d-1, -beta, -alpha)
		if y>alpha:
			bestmove = l
			alpha=y
			if y>=beta:
				return beta, bestmove
	
	return alpha, bestmove


def findbestmove(b):
	global nodecnt
	nodecnt = 0 
	global timer
	global hashtable
	
	timer.reset()
	hashtable.clear()
	
	bestmove = -1
	move = -1
	
	for depth in range(3,100):
		if Verbose:
			print ("Depth = ", depth, end=' ')
	
		value,bestmove = search_top(b, depth, -999999, 999999, bestmove)
		
		if (timer.hastimedout()):
			if Verbose:
				print ("  (timeout) ")
			break

		if Verbose:
			print ("  bestmove =", bestmove, " value =", value)
		
		# Anti Self-Sabotage Clause: Value is -Inf, so we know we've "lost" but maybe the opponent 
		# doesn't. (Maybe he doesn't search as deep as we do.)  Instead of giving up and making a 
		# potentially bad move, stick with the best move from the previous depth level.
		if (value <= -999999 and move!=-1):  
			break
		
		move = bestmove
		
		# Win Clause: If we find a win for a particular depth, take it and make the move.  This ensures
		# that we not only win in a winning position, but due to the iterative deepening, we force the 
		# win in the shortest number of moves.
		if value >= 999999:
			break
	
	if Verbose:
		t = timer.gettime()			
		if t==0:
			t= 0.000001
				
		print ("nodecnt = ", nodecnt)
		print ("time = ", t)
		print ("Nodes/s = ", nodecnt/t/1000, " K")	
			
	return move
	
@algo_player(name="GenHex-Fast-v18b",
			 description="GenHex-Fast-v18b")
def pyhex(board, game_id, player_id):
		
	b = Board()
	for i in range(37):
		tile = board[names[i]]
		if tile["counters"] is not None:
			if tile["counters"]<0:
				b.c[i] = -tile["counters"]
			else:
				if tile["player"] == player_id:
					b.a[i] = tile["counters"]
				else:
					b.b[i] = tile["counters"]

	b.calcdata()
	
	move = findbestmove(b)
			
	return names[move]

