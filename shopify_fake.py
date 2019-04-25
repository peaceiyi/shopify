#this is a bot to consolidate all my shopfiy scripts
#scripts done: Shopnicekicks, kith

#todo haven, blends, undefeated, extrabutterny
from timelog import n_logging, c_logging
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process
from multiprocessing import Pool
import multiprocessing
#import re
from datetime import datetime
import time

sizes = ["6", "8.5", "9.5", "10", "10.5", "11", "11.5", "13"]

sites = {"1":"https://shopnicekicks.com",
"2":"https://shop.havenshop.com",
"3":"https://shop.extrabutterny.com",
"4":"https://www.xhibition.co",
"5":"https://www.deadstock.ca",
"6":"https://sneakerpolitics.com",
"7":"https://www.notre-shop.com",
"8":"https://rsvpgallery.com",
"9":"https://wishatl.com",
"10":"https://www.socialstatuspgh.com",
"11":"https://www.hanon-shop.com",
"12":"https://shoegallerymiami.com",
"13":"",
"14":"",
"15":"",
"16":"",
"17":"",
"18":"https://www.kith.com", #captcha, weird endpoint
"19":"https://www.blendsus.com", #captcha
"20":"https://undefeated.com", #login before checkout}}
}

weird_sites = {"1":"https://www.kith.com", #captcha, weird endpoint
"2":"https://www.blendsus.com", #captcha
"3":"https://undefeated.com", #login before checkout
"":"",
"":"",
"":"",
"":"",
"":"",}


class Shopify():

	def __init__(self, keywords, site):
		global sites
		self.keywords = keywords.lower().split(" ")
		self.site = sites[site]
		self.number = site

	def endpoint_monitor(self, endpoint):

		n_logging("looking for product on "+self.site+" endpoint!")
		while True:
			endpoint_json = endpoint.json()
			product_title = endpoint_json["products"][0]["title"].lower().split(" ")
			if len(set(product_title) & set(self.keywords)) >= 3: #have 3 or more matching keywords
				c_logging("Got it!","green")
				break
			else:
				c_logging("Try again...", "red")
				n_logging(product_title)
				time.sleep(.1)

		return endpoint_json


	def atc(self):
		start = time.time()
		s = requests.session()
		global sizes

		endpoint = s.get(self.site+"/products.json?limit=1")
		endpoint_json = self.endpoint_monitor(endpoint)

		for variant in reversed(endpoint_json["products"][0]["variants"]):
			if variant["title"] in sizes and variant["available"] == True:
				variant_id = variant["id"]
				c_logging("Found a size " + variant["title"] + "!", "green")

				break
			else:
				c_logging("Size " + variant["title"] + " not available!", "red")


		item_payload = {'id': variant_id, 'quantity': 1}


		add_item = s.post(self.site+"/cart/add.js", data=item_payload)
		c_logging('Added to cart', "green")


		if self.number == "20": #login in before checkout for undefeated
			login_headers = {
			    'Connection': 'keep-alive',
			    'Cache-Control': 'max-age=0',
			    'Origin': 'https://undefeated.com',
			    'Upgrade-Insecure-Requests': '1',
			    'Content-Type': 'application/x-www-form-urlencoded',
			    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
			    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			    'Referer': 'https://undefeated.com/account/login?checkout_url=https%3A%2F%2Fundefeated.com%2F2825850%2Fcheckouts%2F40b460321f1326a1d46a154f544fb41c',
			    'Accept-Encoding': 'gzip, deflate, br',
			    'Accept-Language': 'en,en-US;q=0.9,en-GB;q=0.8',
			}

			login_data = {
			  'form_type': 'customer_login',
			  'utf8': '\u2713',
			  'customer[email]': 'piyiewuare123@gmail.com', #enter email
			  'customer[password]': '********', #enter password
			  'checkout_url': self.site+"/checkout",
			}

			undft_login = s.post(self.site+'/account/login', headers=login_headers, data=login_data)

		####FILL OUT THE FORM###

		#self.site = "https://shopnicekicks.com"
		checkout_url = s.get(self.site+"/checkout")
		checkout_soup = BeautifulSoup(checkout_url.text, "lxml")
		novalidate = checkout_soup.find('form', attrs={'novalidate': 'novalidate'})['action']
		#print("AUTH TOKEN: "+ checkout_soup.find("input", {"name": "authenticity_token"})["value"])
		customer_payload = [
			('utf8', '\u2713'),
			('_method', 'patch'),
			('authenticity_token', checkout_soup.find("input", {"name": "authenticity_token"})["value"]),
			('previous_step', 'contact_information'),
			('step', 'shipping_method'),
			('checkout[email]', 'masterpeace@gmail.com'),
			('checkout[buyer_accepts_marketing]', '0'),
			('checkout[buyer_accepts_marketing]', '1'),
			('checkout[shipping_address][first_name]', 'ScHoolboy'),
			('checkout[shipping_address][first_name]', 'ScHoolboy'),
			('checkout[shipping_address][last_name]', 'Q'),
			('checkout[shipping_address][last_name]', 'Q'),
			('checkout[shipping_address][company]', ''),
			('checkout[shipping_address][company]', ''),
			('checkout[shipping_address][address1]', '1111 Groovy Lane'),
			('checkout[shipping_address][address1]', '1111 Groovy Lane'),
			('checkout[shipping_address][address2]', ''),
			('checkout[shipping_address][address2]', ''),
			('checkout[shipping_address][city]', 'Houston'),
			('checkout[shipping_address][city]', 'Houston'),
			('checkout[shipping_address][country]', 'United States'),
			('checkout[shipping_address][country]', 'United States'),
			('checkout[shipping_address][province]', 'Texas'),
			('checkout[shipping_address][province]', 'Texas'),
			('checkout[shipping_address][zip]', '77047'),
			('checkout[shipping_address][zip]', '77047'),
			('checkout[shipping_address][phone]', '(832) 111-1111'),
			('checkout[shipping_address][phone]', '(832) 111-1111'),
			('checkout[remember_me]', ''),
			('checkout[remember_me]', '0'),
			('button', ''),
			('checkout[client_details][browser_width]', '1680'),
			('checkout[client_details][browser_height]', '364'),
			('checkout[client_details][javascript_enabled]', '1'),
		]
		headers = {
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'en,en-US;q=0.9,en-GB;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
			'Accept': '*/*',
			'Referer': 'https://shopnicekicks.com/',
			'X-Requested-With': 'XMLHttpRequest',
			'Connection': 'keep-alive',
		}

		addressform = s.post(url=self.site + novalidate,
							 headers=headers, data=customer_payload, allow_redirects=True)

		c_logging('Filled out form!\n', "green")

		####FILL OUT SHIPPIG INFORMATION###
		checkout_url = s.get(self.site+"/checkout")
		checkout_soup = BeautifulSoup(checkout_url.text, "lxml")

		shipping_auth = checkout_soup.find(
			"input", {"name": "authenticity_token"})["value"]
		shipping_headers = {
			'Connection': 'keep-alive',
			'Cache-Control': 'max-age=0',
			'Origin': 'https://shopnicekicks.com',
			'Upgrade-Insecure-Requests': '1',
			'Content-Type': 'application/x-www-form-urlencoded',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Referer': 'https://shopnicekicks.com/',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'en-US,en;q=0.9',
		}

		shipping_data = [
			('utf8', '\u2713'),
			('_method', 'patch'),
			('authenticity_token', checkout_soup.find(
				"input", {"name": "authenticity_token"})["value"]),
			('previous_step', 'shipping_method'),
			('step', 'payment_method'),
			('checkout[shipping_rate][id]', checkout_soup.find("div",{"class":"radio-wrapper"})["data-shipping-method"]),
			('button', ''),
			#('checkout[client_details][browser_width]', '1680'),
			#('checkout[client_details][browser_height]', '150'),
			#('checkout[client_details][javascript_enabled]', '1')
		]

		shipping_response = s.post(
			self.site+novalidate, headers=shipping_headers, data=shipping_data)
		c_logging('Selected shipping!', "green")


		#*****CC CHECKOUT*******#
		checkout_url = s.get(self.site+"/checkout")
		checkout_soup = BeautifulSoup(checkout_url.text, "lxml")

		checkout_header = {
			'Pragma': 'no-cache',
			'Origin': 'https://checkout.shopifycs.com',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'en,en-US;q=0.9,en-GB;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
			'Content-Type': 'application/json',
			'Accept': 'application/json',
			'Cache-Control': 'no-cache',
			'Referer': 'https://checkout.shopifycs.com/number?identifier=d58ae35761c93619085627899fcb0daa&location=https%3A%2F%2Fshopnicekicks.com%2F2192362%2Fcheckouts%2Fd58ae35761c93619085627899fcb0daa%3Fvalidate%3Dtrue&fonts[]=Lato',
			'Connection': 'keep-alive',
		}

		checkout_payload = {"credit_card": {
			"number": "1111 1111 1111 1111",
			"name": "Random Random",
			"month": 11,
			"year": 1111,
			"verification_value": "111"}
		}

		checkout_response = s.post("https://elb.deposit.shopifycs.com/sessions",
								   headers=checkout_header, json=checkout_payload, allow_redirects=True)

		# CC checkout second request
		#checkout_soup = BeautifulSoup(checkout_url.text, "lxml")
		checkout2_headers = {
			'Connection': 'keep-alive',
			'Cache-Control': 'max-age=0',
			'Origin': 'https://shopnicekicks.com',
			'Upgrade-Insecure-Requests': '1',
			'Content-Type': 'application/x-www-form-urlencoded',
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Referer': 'https://shopnicekicks.com/',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'en-US,en;q=0.9',
		}


		checkout2_data = [
			('utf8', '\u2713'),
			('_method', 'patch'),
			('authenticity_token', checkout_soup.find("input", {"name": "authenticity_token"})["value"]),
			('previous_step', 'payment_method'),
			('step', ''),
			('s', checkout_response.json()['id']),
			('checkout[payment_gateway]', checkout_soup.find("div",{"data-gateway-group":"direct"})["data-select-gateway"]),
			('checkout[credit_card][vault]', 'false'),
			('checkout[different_billing_address]', 'false'),
			('checkout[vault_phone]', '+18327777777'),
			('checkout[total_price]', checkout_soup.find("span", {"class":"payment-due__price"})["data-checkout-payment-due-target"]),
			('complete', '1'),
			#('checkout[client_details][browser_width]', '1680'),
			#('checkout[client_details][browser_height]', '364'),
			#('checkout[client_details][javascript_enabled]', '1'),
		]

		checkout2_response = s.post(self.site+novalidate, headers=checkout2_headers, data=checkout2_data, allow_redirects=True)
		c_logging('Checked out! in ' + str(time.time()-start) + " seconds!" + "\n", "green")


print("""
   ______  __    __  ______  _______  ______ ________ __      __        _______   ______  ________
 /      \/  |  /  |/      \/       \/      /        /  \    /  |      /       \ /      \/        |
/$$$$$$  $$ |  $$ /$$$$$$  $$$$$$$  $$$$$$/$$$$$$$$/$$  \  /$$/       $$$$$$$  /$$$$$$  $$$$$$$$/
$$ \__$$/$$ |__$$ $$ |  $$ $$ |__$$ | $$ | $$ |__    $$  \/$$/        $$ |__$$ $$ |  $$ |  $$ |
$$      \$$    $$ $$ |  $$ $$    $$/  $$ | $$    |    $$  $$/         $$    $$<$$ |  $$ |  $$ |
 $$$$$$  $$$$$$$$ $$ |  $$ $$$$$$$/   $$ | $$$$$/      $$$$/          $$$$$$$  $$ |  $$ |  $$ |
/  \__$$ $$ |  $$ $$ \__$$ $$ |      _$$ |_$$ |         $$ |          $$ |__$$ $$ \__$$ |  $$ |
$$    $$/$$ |  $$ $$    $$/$$ |     / $$   $$ |         $$ |          $$    $$/$$    $$/   $$ |
 $$$$$$/ $$/   $$/ $$$$$$/ $$/      $$$$$$/$$/          $$/           $$$$$$$/  $$$$$$/    $$/
 """)

instructions = ["1 - https://shopnicekicks.com",
"2 - https://shop.havenshop.com",
"3 - https://shop.extrabutterny.com",
"4 - https://undefeated.com",
"5 - https://www.deadstock.ca/",
"6 - https://sneakerpolitics.com",
"7 - https://www.notre-shop.com",
"8 - https://rsvpgallery.com",
"9 - https://wishatl.com",
"8 - https://rsvpgallery.com",
"9 - https://wishatl.com",
"10 - https://www.socialstatuspgh.com",
"11 - https://www.hanon-shop.com",
"12 - https://shoegallerymiami.com",
"13 - ",
"14 - ",
"15 - ",
"16 - ",
"17 - ",
"18 - https://www.kith.com", #captcha, weird endpoint
"19 - https://www.blendsus.com", #captcha
"20 - https://undefeated.com", #login before checkout}}
]

for site in instructions:
	print(site)
print("\n")

which_site = input("What site? Each number corresponds to a site: ")
which_product = input("What product are you looking for? Enter the keywords for your product: ")


#Shopify(which_product, which_site).atc()

#pool = multiprocessing.Pool(processes=4)
"""
p = Process(Shopify("temper core run", "1").atc())
p.start()
p.join()


pool = multiprocessing.Pool(processes=4)
p = pool.map(Shopify("temper core run", "1").atc())
pool.close()
"""

Shopify("temper core run", "1").atc()
