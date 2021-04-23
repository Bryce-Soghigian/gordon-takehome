import xml.etree.ElementTree as ET
import json 
import re


seat_map_one_tree = ET.parse('seatmap1.xml')
seat_map_two_tree = ET.parse('seatmap2.xml')


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
			curr_dict["price"] = f"{row_atr['Amount']} {row_atr['CurrencyCode']}"
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



#Save our parsed xml to json
print(f"Parsing our xml seatmap data")
json_data = parse_flight_data(seat_map_one_tree)
with open('seatmap1_parsed.json',"w") as json_file:
	json.dump(json_data,json_file)

print(f"Finished Parsing Our XML To JSON")

