# tags that identify nodes as POIs
node_tags = {
	'amenity': {
		'1': ['arts_centre', 'cinema', 'community_centre', 'foutain', 'planetorium', 'social_centre', 'stripclub', 'theatre', 'studio'],
		'2': ['bar', 'bbq', 'biergarten', 'cafe', 'drinking_water', 'fast_food', 'food_court', 'ice_cream', 'pub', 'restaurant', 'nightclub', 'gambling', 'casino', 'swingerclub'],
		'3': ['college', 'kindergarten', 'library', 'public_bookcase', 'school', 'university', 'bicycle_parking', 'bicycle_repair_station', 'bicycle_rental', 'boat_sharing', 'bus_station', 'car_rental', 'car_sharing', 'car_wash', 'charging_station', 'ferry_terminal', 'fuel', 'grit_bin', 'parking', 'parking_entrance', 'parking_space', 'taxi', 'atm', 'bank', 'bureau_de_change', 'baby-hatch', 'clinic', 'dentist', 'doctors', 'hospital', 'nursing_home', 'pharmacy', 'social_facility', 'veterinary', 'animal_boarding', 'animal_shelter', 'bench', 'clock', 'courthouse', 'coworking_space', 'crematorium', 'crypt', 'dojo', 'embassy', 'fire_station', 'grave_yard', 'gym', 'hunting_stand', 'game_feeding', 'marketplace', 'photo_booth', 'place_of_worship', 'police', 'post_box', 'post_office', 'prison', 'ranger_station', 'register_office', 'recycling', 'rescue_station', 'sauna', 'shelter', 'shower', 'telephone', 'toilets', 'townhall', 'vending_machine', 'waste_basket', 'waste_disposal', 'watering_place', 'water_point', ]
	}, 
	'building': {
		'1': ['cathedral', 'church', 'chapel', 'mosque', 'temple', 'synagogue', 'shrine', 'public'],
		'2': ['hotel'],
		'3': ['apartments', 'farm', 'house', 'detached', 'residential', 'dormitory', 'terrace', 'houseboat', 'static_caravan', 'commercial', 'industrial', 'retail', 'warehouse', 'civic', 'hospital', 'school', 'stadium', 'train_station', 'transportation', 'university', 'barn', 'bridge', 'bunker', 'cabin', 'construction', 'cowshed', 'farm_auxiliary', 'garage', 'garages', 'greenhouse', 'hanger', 'hut', 'roof', 'shed', 'stable', 'sty', 'transformer_tower', 'ruins']
	}, 
	'historic': {
		'1': ['archaeological_site', 'aircraft', 'battlefield', 'boundary_stone', 'building', 'castle', 'cannon', 'city_gate', 'citywalls', 'farm', 'fort', 'manor', 'memorial', 'monumnet', 'optical_telegraph', 'ruins', 'rune_stone', 'ship', 'tomb', 'wayside_cross', 'wayside_shrine', 'wreck'],
		'2': [],
		'3': []
	}, 
	'leisure': {
		'1': ['adult_gaming_centre', 'amusement_arcade', 'beach_resort', 'bandstand', 'bird_hide', 'dance', 'fishing', 'garden', 'golf_course', 'ice_rink', 'marina', 'miniature_golf', 'park', 'pitch', 'slipway', 'sports_centre', 'stadium', 'water_park', 'wildlife_hide', ''],
		'2': [],
		'3': ['dog_park', 'firepit', 'hackerspace', 'playground', 'summer_camp', 'swimming_pool', 'track']
	}, 
	'office': {
		'1': [],
		'2': [],
		'3': []
	}, 
	'shop': {
		'1': [],
		'2': ['alcohol', 'bakery', 'beverages', 'butcher', 'cheese', 'chocolate', 'coffee', 'confectionery', 'convenience', 'deli', 'dairy', 'farm', 'greengrocer', 'pasta', 'pastry', 'seafood', 'tea', 'wine', 'department_store', 'general', 'kiosk', 'mall', 'supermarket'],
		'3': []
	}, 
	'sport': {
		'1': ['9pin', '10pin', 'archery', 'base', 'billiards', 'bmx', 'bobsleigh', 'boules', 'bowls', 'canoe', 'cliff_diving', 'climbing', 'climbing_adventure', 'cockfighting', 'croquet', 'curling', 'cycling', 'darts', 'dog_racing', 'equistrian', 'fencing', 'free_flying', 'horse_racing', 'ice_skating', 'karting', 'kitesurfing', 'motor', 'motorcross', 'paragliding', 'racquet', 'rc_car', 'roller_skating', 'rowing', 'sailing', 'scuba_diving', 'shooting', 'skateboard', 'skiing', 'surfing', 'table_tennis', 'swimming', 'toboggan', 'water_ski'],
		'2': [],
		'3': []
	},
	'tourism': {
		'1': ['attraction', 'artwork', 'camp_site', 'gallery', 'museum', 'picnic_site', 'theme_park', 'viewpoint', 'zoo'],
		'2': ['hotel'],
		'3': ['apartment', 'caravan_site', 'chalet', 'alpine_hut', 'guest_house', 'hostel', 'motel', 'information', 'wilderness_hut']
	}
}

# Tags that identify ways as roads
way_tags = {
	'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'service', 'motorway_link', 'trunk_link', 'primary_link', 'secondary_link', 'tertiary_link', 'living_street', 'pedestrian', 'bus_guideway', 'road', 'path', 'footway', 'cycleway'],
	'route': ['bicycle', 'bus', 'road'],
	'busway': ['lane']
}

