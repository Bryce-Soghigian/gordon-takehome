import xml.etree.ElementTree as ET
import json 
import re


seat_map_one_tree = ET.parse('seatmap1.xml')
def parse_flight_data(seat_map_tree):
	"""
	We want to build a dictionary that we will later dump into a json object that contains all of our flight data
	"""
	flight_data = {}
	flight_data_root = seat_map_tree.getroot()
	plane_seat_map = []
	seats = []
	#flight data
	for ele in flight_data_root.findall(".//{http://www.opentravel.org/OTA/2003/05/common/}FlightSegmentInfo"):
		flight_data["departure_time"] = ele.attrib["DepartureDateTime"]
		flight_data["flight_number"] = ele.attrib["FlightNumber"]


	#seat data
	"""
		self.seat_number = seat_number
		self.features = features
		self.price = price
		self.is_available = is_available
	"""
	curr_dict = {"features":"",'price':"NA"}
	for ele in flight_data_root.findall(".//{http://www.opentravel.org/OTA/2003/05/common/}*"):
		if ele.tag == "{http://www.opentravel.org/OTA/2003/05/common/}Summary":
			row_atr = ele.attrib
			curr_dict["seat_number"] = ele.attrib["SeatNumber"]
			curr_dict["is_available"] = ele.attrib["AvailableInd"]

		if ele.tag == "{http://www.opentravel.org/OTA/2003/05/common/}Features":
			row_txt = ele.text
			final_txt = ""
			if row_txt == "Other_":
				final_txt = "Chargable"
			else:
				final_txt = row_txt
			curr_dict["features"] = final_txt
		if ele.tag == "{http://www.opentravel.org/OTA/2003/05/common/}Fee":
			row_atr = ele.attrib
			x = slice(2)
			curr_dict["price"] = f"{row_atr['Amount'][x]}.00 {row_atr['CurrencyCode']}"
		if ele.tag == "{http://www.opentravel.org/OTA/2003/05/common/}SeatInfo" and len(curr_dict) > 2:

			seats.append(curr_dict)
			curr_dict = {"features":"",'price':"NA"}



	#lets fetch all of the row info
	for ele in flight_data_root.findall(".//{http://www.opentravel.org/OTA/2003/05/common/}RowInfo"):
		row_atr = ele.attrib
		new_row = {'row_number':row_atr["RowNumber"],'cabin_type':row_atr["CabinType"],'seats':[]}
		plane_seat_map.append(new_row)
	
	#Get warnings
	warnings = []
	for ele in flight_data_root.findall(".//{http://www.opentravel.org/OTA/2003/05/common/}Warning"):
		warnings.append({'warning_code':ele.attrib["Code"], 'warning_message': ele.text})
	
	flight_data['warnings'] = warnings
	flight_data['plane_seat_map'] = plane_seat_map
	# Go through plane_seat_map and map row to seat
	for item in plane_seat_map:
		for seat in seats:
			s_number = seat["seat_number"]
			if item["row_number"] == re.findall("\d+",s_number)[0]:
				item["seats"].append(seat)

	return flight_data


seat_map_two_tree = ET.parse('seatmap2.xml')
def parse_other(seatmap):
	mapping_def = {'SD1': 'SEAT_SUITABLE_FOR_ADULT_WITH_AN_INFANT', 'SD2': 'SEAT_IN_A_QUIET_ZONE', 'SD3': 'WINDOW', 'SD4': 'AVAILABLE', 'SD5': 'AISLE_SEAT', 'SD6': 'SEAT_NOT_SUITABLE_FOR_CHILD', 'SD7': 'SEAT_NOT_ALLOWED_FOR_INFANT', 'SD8': 'RESTRICTED_RECLINE_SEAT', 'SD9': 'SEAT_TO_BE_LEFT_VACANT_OR_OFFERED_LAST', 'SD10': 'RESTRICTED_SEAT_GENERAL', 'SD11': 'RESTRICTED', 'SD12': 'WING', 'SD13': 'SEAT_NOT_ALLOWED_FOR_MEDICAL', 'SD14': 'EXIT', 'SD15': 'LEG_SPACE_SEAT', 'SD16': 'PREFERENTIAL_SEAT', 'SD17': 'SEAT_WITH_FACILITIES_FOR_HANDICAPPED', 'SD18': 'SEAT_WITH_FACILITIES_FOR_HANDICAPPED_INCAPACITATED_PASSENGER', 'SD19': 'OCCUPIED', 'SD20': 'SEAT_SUITABLE_FOR_UNACCOMPANIED_MINORS', 'SD21': 'REAR_FACING_SEAT', 'SD22': 'CREW_SEAT'}
	prices = {"OFIa20ae42f-6417-11eb-b326-15132ca0c3353":"17.70 GBP","OFIa20ae42f-6417-11eb-b326-15132ca0c3351":"22.10","OFIa20ae42f-6417-11eb-b326-15132ca0c3352":"35.40 GBP","OFIa20ae42f-6417-11eb-b326-15132ca0c3354":"11.50 GBP"}
	output = {}
	## Fists sets set up our rows
	rows = []
	tree_root = seatmap.getroot()
	for ele in tree_root:
		if ele.tag == "{http://www.iata.org/IATA/EDIST/2017.2}SeatMap":
			seat_map = {"seats":[]}
			for child in ele:
				# if child.tag == "{http://www.iata.org/IATA/EDIST/2017.2}SegmentRef":
				# 	seat_map["seg_ref"] = child.text
				if child.tag == "{http://www.iata.org/IATA/EDIST/2017.2}Cabin":
					for cabin in child:
						# grab our seat data from each row
						if cabin.tag == "{http://www.iata.org/IATA/EDIST/2017.2}Row":
							for row in cabin:
								curr_row = row.text
								if row.tag == "{http://www.iata.org/IATA/EDIST/2017.2}Number":
									row_number = row.text
									curr_row = row.text
									seat_map["row_number"] = row_number
									if len(seat_map) > 0:
										rows.append(seat_map)
										seat_map = {"seats":[]}	
									
								if row.tag == "{http://www.iata.org/IATA/EDIST/2017.2}Seat":
									#Here we grab the column definition and offer_ref

									"""
									"""
									seat_def_refs = []
									single_seat = {}
									for seat in row:
										if seat.tag == "{http://www.iata.org/IATA/EDIST/2017.2}OfferItemRefs":
											print(seat.text)
											single_seat["offer_ref"] = seat.text
										if seat.tag == "{http://www.iata.org/IATA/EDIST/2017.2}Column":
											single_seat["seat_id"] = f"{seat.text}"
										if seat.tag == "{http://www.iata.org/IATA/EDIST/2017.2}SeatDefinitionRef":
											seat_def_refs.append(seat.text)
											single_seat["definitions"] = seat_def_refs
										# if seat.tag == "{http://www.iata.org/IATA/EDIST/2017.2}Seat":
										# 	print("seat")
										# 	# if len(single_seat)>0:
										# 	# 	seat_map["seats"].append(single_seat)
										# 	# 	print(single_seat)
									print(single_seat)
									seat_map["seats"].append(single_seat)

								


			
	## loop through rows and

	filter_rows = []
	for row in rows:
		new_obj = {}
		rn = row["row_number"]
		if rn is not None:
			new_obj["row_number"] = rn
			new_obj["seats"] = []
			new_seat = {}
			
			for seat in row["seats"]:
				new_seat["seat_id"] = f"{rn}{seat['seat_id']}"
				print(seat,"FJFJF")
				if "offer_ref" in seat and "offer_ref" in prices:
					new_seat["price"] = prices[new_seat['offer_ref']]
				else:
					new_seat["price"] = "NA"
				for item in seat["definitions"]:
					if item == "SD4":
						new_seat["is_available"] = True
					if item == "SD19":
						new_seat["is_available"] = False
					if item == "SD5":
						new_seat["features"] = "Aisle"
					if item == "SD3":
						new_seat["features"] = "Window"
					if item == "SD22":
						new_seat["features"] = "Center"
					
				new_obj["seats"].append(new_seat)
		if len(new_obj) > 0:
			filter_rows.append(new_obj)

	# print(filter_rows[2])
	output["rows"] = filter_rows
	return output



#Save our parsed xml to json
print(f"Parsing our xml seatmap data for first file")
json_data = parse_flight_data(seat_map_one_tree)
with open('seatmap1_parsed.json',"w") as json_file:
	json.dump(json_data,json_file)

print(f"Parsing second xml seatmap")
second_tree_data = parse_other(seat_map_two_tree)
with open('seatmap2_parsed.json',"w") as json_file:
	json.dump(second_tree_data,json_file)

print(f"Finished Parsing Our XML To JSON")

