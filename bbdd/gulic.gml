Creator	"DbVis"
Whatever	"Stuff"
graph
[
	label	""
	directed	1
	node
	[
		id	0
		label	"public.chargetype"
		graphics
		[
			x	85.5
			y	575.713623046875
			w	171.0
			h	99.66943359375
			type	"rectangle"
			fill	"#FFFFCC"
			outline	"#000000"
		]
	]
	node
	[
		id	1
		label	"public.charge"
		graphics
		[
			x	307.97222900390625
			y	588.6906127929688
			w	158.0
			h	117.30517578125
			type	"rectangle"
			fill	"#FFFFCC"
			outline	"#000000"
		]
	]
	node
	[
		id	2
		label	"public.partner"
		graphics
		[
			x	529.0558471679688
			y	583.0082397460938
			w	134.0
			h	82.03369140625
			type	"rectangle"
			fill	"#FFFFCC"
			outline	"#000000"
		]
	]
	node
	[
		id	3
		label	"public.people"
		graphics
		[
			x	689.8648681640625
			y	395.9620666503906
			w	144.0
			h	134.94091796875
			type	"rectangle"
			fill	"#FFFFCC"
			outline	"#000000"
		]
	]
	node
	[
		id	4
		label	"public.ftpusers"
		graphics
		[
			x	779.385009765625
			y	618.0326538085938
			w	164.0
			h	134.94091796875
			type	"rectangle"
			fill	"#FFFFCC"
			outline	"#000000"
		]
	]
	node
	[
		id	5
		label	"public.imtype"
		graphics
		[
			x	998.218505859375
			y	41.016845703125
			w	159.0
			h	82.03369140625
			type	"rectangle"
			fill	"#FFFFCC"
			outline	"#000000"
		]
	]
	node
	[
		id	6
		label	"public.im"
		graphics
		[
			x	855.2911987304688
			y	207.08616638183594
			w	171.0
			h	117.30517578125
			type	"rectangle"
			fill	"#FFFFCC"
			outline	"#000000"
		]
	]
	node
	[
		id	7
		label	"public.jabberusers"
		graphics
		[
			x	933.4545288085938
			y	434.3877868652344
			w	164.0
			h	134.94091796875
			type	"rectangle"
			fill	"#FFFFCC"
			outline	"#000000"
		]
	]
	node
	[
		id	8
		label	"public.mailusers"
		graphics
		[
			x	458.2760925292969
			y	334.65814208984375
			w	164.0
			h	134.94091796875
			type	"rectangle"
			fill	"#FFFFCC"
			outline	"#000000"
		]
	]
	node
	[
		id	9
		label	"public.partnertype"
		graphics
		[
			x	652.8636474609375
			y	990.568115234375
			w	158.0
			h	64.39794921875
			type	"rectangle"
			fill	"#FFFFCC"
			outline	"#000000"
		]
	]
	node
	[
		id	10
		label	"public.quota"
		graphics
		[
			x	517.6820068359375
			y	817.2474975585938
			w	152.0
			h	152.57666015625
			type	"rectangle"
			fill	"#FFFFCC"
			outline	"#000000"
		]
	]
	node
	[
		id	11
		label	"public.quotatype"
		graphics
		[
			x	356.1258850097656
			y	990.0894775390625
			w	171.0
			h	117.30517578125
			type	"rectangle"
			fill	"#FFFFCC"
			outline	"#000000"
		]
	]
	node
	[
		id	12
		label	"public.webusers"
		graphics
		[
			x	620.1637573242188
			y	159.15476989746094
			w	164.0
			h	134.94091796875
			type	"rectangle"
			fill	"#FFFFCC"
			outline	"#000000"
		]
	]
	edge
	[
		source	1
		target	0
		label	"charge_chargetype_fk"
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	1
		target	2
		label	"charge_partner_fk"
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	4
		target	3
		label	"ftpusers_people_fk"
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	6
		target	5
		label	"im_fk"
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	6
		target	3
		label	"im_people_fk"
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	7
		target	3
		label	"jabberusers_people_fk"
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	8
		target	3
		label	"mailusers_people_fk"
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	2
		target	3
		label	"partner_people_fk"
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	10
		target	2
		label	"quota_partner_fk"
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	10
		target	9
		label	"quota_partnertype_fk"
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	10
		target	11
		label	"quota_quotatype_fk"
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
	edge
	[
		source	12
		target	3
		label	"webusers_people_fk"
		graphics
		[
			fill	"#000000"
			targetArrow	"standard"
		]
	]
]
