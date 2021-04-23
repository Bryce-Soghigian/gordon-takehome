import xml.etree.ElementTree as ET
import json 


seat_map_one_tree = ET.parse('seatmap1.xml')
seat_map_two_tree = ET.parse('seatmap2.xml')

class Seat:
	def __init__(self,seat_number,features,price,is_available):
		self.seat_number = seat_number
		self.features = features
		self.price = price
		self.is_available = is_available

def parse_flight_data(seat_map_tree):
	"""
	We want to build a dictionary that we will later dump into a json object that contains all of our flight data
	"""
	flight_data = {}
	flight_data_root = seat_map_tree.getroot()
	plane_seat_map = []
	#flight data
	for ele in flight_data_root.findall(".//{http://www.opentravel.org/OTA/2003/05/common/}FlightSegmentInfo"):
		flight_data["departure_time"] = ele.attrib["DepartureDateTime"]
		flight_data["flight_number"] = ele.attrib["FlightNumber"]

	#lets fetch all of the row info
	for ele in flight_data_root.findall(".//{http://www.opentravel.org/OTA/2003/05/common/}RowInfo"):
		row_atr = ele.attrib
		new_row = {'row_number':row_atr["RowNumber"],'cabin_type':row_atr["CabinType"],'seats':[]}
		plane_seat_map.append(new_row)
	
	#Get warnings
	warnings = []
	for ele in flight_data_root.findall(".//{http://www.opentravel.org/OTA/2003/05/common/}Warning"):
		print(ele.attrib)
		warnings.append({'warning_code':ele.attrib["Code"], 'warning_message': ele.text})
	
	print(warnings)
	flight_data['warnings'] = warnings
	flight_data['plane_seat_map'] = plane_seat_map
	return flight_data



#Save our parsed xml to json
json_data = parse_flight_data(seat_map_one_tree)
with open('seatmap1_parsed.json',"w") as json_file:
	json.dump(json_data,json_file)

print(f"Finished Parsing Our XML To JSON")

