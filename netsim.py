
import string, sys
import random
import time
from multiprocessing import Pool
class Host():
	def __init__(self, name):
		self.name = name
		self.links_to = []
	def add_link_to(self, link_host):
		self.links_to.append(link_host)

class Message():
	def __init__(self, sending_host, receiving_host):
		self.sending_host = sending_host
		self.receiving_host = receiving_host
		self.sending_host_name = sending_host.name
		self.hops = 1
		self.number_message_bits = random.randint(10,100)
		self.last_error = 0
	
	def route(self,msg_objs,new_bandwidth):
     	
		if not self.sending_host.links_to:
			self.hops = 0
			self.last_error = 1
		else:	
			self.rand = random.randint(1,100)
			self.take_route = self.rand % len(self.sending_host.links_to)
			self.temp = self.sending_host.name
			self.sending_host = self.sending_host.links_to[self.take_route]
			if(self.sending_host.name == "hostMed"):
				print("On est sur le noeud de milleux Amplification de la bande passante à appliqué")
				print("Bande Passante augementé à "+ str(new_bandwidth) +"bits/seconde" )
				time.sleep(5)
			if self.sending_host == self.receiving_host:
				self.last_error = 0
			else:
				self.route(msg_objs,new_bandwidth)
				return self.last_error
 
# Cette partie pour parser la confinguration papillon dans le fichier papillon.txt
def find_word(lines, string):
	temp = 0
	for element in lines:
		if element == string:
			return temp
		temp = temp + 1
def parse(item):
	_from = item[0:str.find(item, "TO")].strip()
	_to = item[str.find(item, "TO")+2:].strip()
	return [_from, _to]

def return_object_from_name(name, host_objects_list):
	for element in host_objects_list:
		if element.name == name:
			return element
	

def initialize_host_objects(hosts, links, messages):
	host_objects = []
	for element in hosts:
		host_objects.append(Host(element))
	for element in host_objects:
		for link in links:
			if parse(link)[0] == element.name:
				element.add_link_to(return_object_from_name(parse(link)[-1], host_objects))
	
	return host_objects

def initialize_msg_objects(messages, host_objs):
	msg_objs = []
	for msg in messages:
		msg_objs.append(Message(return_object_from_name(parse(msg)[0], host_objs), return_object_from_name(parse(msg)[1], host_objs)))
	return msg_objs

def read_from_file(filename):
	random.seed()
	try:
		file_stream = open(filename, 'r')
	except IOError:
		print ("File name does not exist. Exiting program...")
		sys.exit()
	 
	lines = []	
	for line in file_stream:
		clean_line = line.strip()
		lines.append(clean_line)
	network_name = lines[1]
	hosts = lines[3:find_word(lines, "LINKS")]
	links = lines[find_word(lines, "LINKS")+1:find_word(lines, "MESSAGES")]	
	messages = lines[find_word(lines, "MESSAGES")+1:find_word(lines, "END")]
	file_stream.close()
	return [hosts, links, messages, network_name]

def simulate(msg_objs, network_name):
	print ("Simulation Papillon: " + network_name)
	average = 0.0
	delivered = 0.0
	compt =0;
	new_bandwidth =0
     
	for obj in msg_objs:
		new_bandwidth += obj.number_message_bits
		print ("Envoi de paquet de  " + obj.sending_host_name + " à " + obj.receiving_host.name)
		print("Le paquet est de " + str(obj.number_message_bits) + " bits")
		compt=compt+1
		if(compt < 2): 
			time.sleep(2)
			continue
		obj.route(obj,new_bandwidth)
		if obj.last_error == 0:
			print ("Communication avec succée " + obj.sending_host_name + " et " + obj.receiving_host.name)
			print ("Message reçu après " + str(obj.hops) + " sauts")
			delivered += 1
			average += obj.hops
		elif obj.last_error == 1:
			print (" Disscution echoué la hote " + obj.sending_host.name + " n'a pas trouvé d'issu!")
   
	print("------------------------")
	print ("Simulation terminée")
	print ("------------------------")
	print ("Reçu ---" + str(delivered) + "---  Envoi  ----" + str(len(msg_objs)) + "---- messages, taux de succès est de  " + str(100*delivered/len(msg_objs)) + "%")
	print ("Transmmission dans " + str(average) + " sauts en moyenne")
	average = average/len(msg_objs)

# If this is not an imported module, run the simulation on some file
if __name__ == '__main__':
	_file = input("Entrez le nom de votre configuration Papillon:")
	
	read_data = read_from_file(_file)
	hosts = read_data[0]
	links = read_data[1]
	messages = read_data[2]
	network_name = read_data[3]

	host_objs = initialize_host_objects(hosts, links, messages)
	msg_objs = initialize_msg_objects(messages, host_objs)
	simulate(msg_objs, network_name)
	