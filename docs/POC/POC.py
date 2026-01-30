#!/usr/bin/env python3


import time
import re
from datetime import datetime
from decimal import Decimal
import warnings

# Web scraping libraries
try:
    import requests
    from bs4 import BeautifulSoup
    from lxml import etree
    # Disable SSL warnings för företagsnätverk
    from urllib3.exceptions import InsecureRequestWarning
    warnings.simplefilter('ignore', InsecureRequestWarning)
    SCRAPING_AVAILABLE = True
except ImportError:
    SCRAPING_AVAILABLE = False
    print("⚠️  VARNING: requests, beautifulsoup4 eller lxml saknas!")
    print("   Installera med: pip install requests beautifulsoup4 lxml")
    print("   Kör POC i simulerat läge...\n")


# ============================================================================
# FAKE DATA (Simulerar databas)
# ============================================================================


monitors = []

'''
monitors = [
    {
        "id": 1,
        "name": "iPhone 15 Pro - Elgiganten",
        "url": "https://www.elgiganten.se/product/mobil-wearables/mobiltelefon/iphone-15-pro-128-gb/392754",
        "selector_type": "css",
        "selector": ".product-price-number",
        "type": "price",
        "threshold": 11000,
        "current_price": None,
        "is_active": True
    },
    {
        "id": 2,
        "name": "Exempel - Wikipedia (text)",
        "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "selector_type": "css",
        "selector": "#firstHeading",
        "type": "text",
        "threshold": 0,
        "current_price": None,
        "is_active": True
    },
    {
        "id": 3,
        "name": "Kategori - Elgiganten Tvättmaskiner",
        "url": "https://www.elgiganten.se/vitvaror/tvatt-tork/tvattmaskin",
        "selector_type": "css",
        "selector": ".product-card",
        "type": "category",
        "threshold": None,
        "current_price": None,
        "is_active": True
    }
]
'''


price_history = {
    1: [],
    2: [],
    3: []
}


# ============================================================================
# WEB SCRAPING FUNCTIONS
# ============================================================================

def fetch_html(url: str, timeout: int = 10) -> str:
    """Hämta HTML från URL"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        # verify=False för företagsnätverk med SSL-problem
        response = requests.get(
            url, 
            headers=headers, 
            timeout=timeout,
            verify=False  # Skippa SSL verification för företagsproxy
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise Exception(f"Kunde inte hämta sidan: {e}")


def extract_with_css(html: str, selector: str) -> str:
    """Extrahera element med CSS selector"""
    soup = BeautifulSoup(html, 'lxml')
    element = soup.select_one(selector)
    
    if not element:
        raise Exception(f"Hittade inget element för CSS selector: {selector}")
    
    return element.get_text(strip=True)


def extract_with_xpath(html: str, xpath: str) -> str:
    """Extrahera element med XPath"""
    tree = etree.HTML(html)
    elements = tree.xpath(xpath)
    
    if not elements:
        raise Exception(f"Hittade inget element för XPath: {xpath}")
    
def extract_with_xpath(html: str, xpath: str) -> str:
    """Extrahera element med XPath"""
    tree = etree.HTML(html)
    result = tree.xpath(xpath)
    
    if not result:
        raise Exception(f"Hittade inget element för XPath: {xpath}")
    
    element = result[0]
    
    # Hantera olika typer av resultat från XPath
    if isinstance(element, str):
        # XPath returnerade direkt text (t.ex. //text())
        return element.strip()
    
    # För element-objekt, använd ALLTID text_content() först
    # (text_content() ger all text inklusive barn-element)
    if hasattr(element, 'text_content'):
        text = element.text_content().strip()
        if text:
            return text
    
    # Fallback: försök .text (bara direkt text, inte barn)
    if hasattr(element, 'text') and element.text:
        return element.text.strip()
    
    # Sista utväg: konvertera till string
    text = str(element).strip()
    if text and not text.startswith('<Element'):
        return text
    
    raise Exception(f"Element har ingen synlig text: {xpath}")


def extract_category(html: str, selector: str) -> dict:
    """Extrahera alla produkter från en kategorisida"""
    soup = BeautifulSoup(html, 'lxml')
    
    # Hitta alla produkt-containers
    product_cards = soup.select(selector)
    
    products = []
    
    for card in product_cards:
        try:
            # Försök hitta produktnamn (testa olika möjligheter)
            name_elem = (
                card.select_one('.product-name') or
                card.select_one('.product-title') or
                card.select_one('h3') or
                card.select_one('h2') or
                card.select_one('h4') or
                card.select_one('[class*="name"]') or
                card.select_one('[class*="title"]') or
                card.select_one('[data-testid*="name"]') or
                card.select_one('[data-testid*="title"]')
            )
            
            # Försök hitta pris - PRIORITERA SPECIFIKA PRIS-SELECTORS!
            price_elem = None
            
            # 1. Först: Leta efter TYDLIGA pris-indikatorer
            price_selectors = [
                '[data-testid*="price"]',
                '[data-price]',
                '.price-amount',
                '.price-value',
                '.product-price-amount',
                'span[class*="price"][class*="value"]',
                'div[class*="price"][class*="amount"]',
                '[class*="inc-vat"]',  # Inkl. moms
                '[itemprop="price"]',  # Schema.org
            ]
            
            for sel in price_selectors:
                price_elem = card.select_one(sel)
                if price_elem:
                    break
            
            # 2. Om inget specifikt hittades, testa mer generella
            if not price_elem:
                general_selectors = [
                    '.price',
                    '[class*="price"]',
                    '.product-price'
                ]
                for sel in general_selectors:
                    price_elem = card.select_one(sel)
                    if price_elem:
                        break
            
            # Försök hitta URL
            link_elem = card.select_one('a')
            
            if name_elem and price_elem:
                name = name_elem.get_text(strip=True)
                price_text = price_elem.get_text(strip=True)
                
                # Försök parsa pris MED VALIDERING
                try:
                    price = float(parse_price_smart(price_text))
                    
                    # VALIDERING: Priser under 100 kr eller över 1 000 000 kr är suspekta
                    if price < 100 or price > 1000000:
                        # Skippa denna produkt (troligen felaktig parsing)
                        continue
                    
                except:
                    # Kunde inte parsa pris, skippa
                    continue
                
                url = link_elem.get('href', '') if link_elem else ''
                
                # Lägg till om vi har både namn och pris
                if name and price:
                    products.append({
                        'name': name[:80],  # Trunkera långa namn
                        'price': price,
                        'url': url[:150] if url else None
                    })
        except Exception as e:
            # Skippa produkter som inte går att parsa
            continue
    
    return {
        'products': products,
        'count': len(products),
        'timestamp': datetime.now().isoformat()
    }


def parse_price_smart(text: str) -> Decimal:
    """
    Smartare prisextrahering som identifierar FAKTISKA priser
    
    Prioriterar:
    1. Siffror med valutasymboler (kr, SEK, $, €, .-)
    2. Siffror med prisformat (mellanslag/punkter som tusentalsavgränsare)
    3. Större siffror (>1000) före mindre (<100)
    """
    # Ta bort whitespace
    text = text.strip()
    
    # STRATEGI 1A: Elgiganten format: "6995.-" eller "6 995.-"
    # Exempel: "6995.-", "6 995.-", "12995.-"
    pattern_elgiganten = r'(\d+(?:\s*\d+)*)\s*\.\-'
    match = re.search(pattern_elgiganten, text)
    if match:
        price_str = match.group(1)
        return parse_price_string(price_str)
    
    # STRATEGI 1B: Hitta pris med "kr" eller ":-" (Svenskt format)
    # Exempel: "6 999 kr", "6999 kr", "6.999 kr", "6999:-"
    pattern_kr = r'(\d[\d\s.,]*\d|\d+)\s*(?:kr|:-|SEK)\b'
    match = re.search(pattern_kr, text, re.IGNORECASE)
    if match:
        price_str = match.group(1)
        return parse_price_string(price_str)
    
    # STRATEGI 2: Hitta pris med andra valutor
    # Exempel: "$1,299", "€1.299"
    pattern_currency = r'[$€£]\s*(\d[\d\s.,]*\d|\d+)'
    match = re.search(pattern_currency, text)
    if match:
        price_str = match.group(1)
        return parse_price_string(price_str)
    
    # STRATEGI 3: Hitta stora tal (>1000) med tusentalsavgränsare
    # Exempel: "6 999", "6.999", "6,999"
    pattern_large = r'(\d{1,3}[\s.]\d{3}(?:[\s.,]\d{3})*)'
    match = re.search(pattern_large, text)
    if match:
        price_str = match.group(1)
        try:
            price = parse_price_string(price_str)
            # Validera att det är ett rimligt pris (>1000)
            if price >= 1000:
                return price
        except:
            pass
    
    # STRATEGI 4: Hitta vilket nummer som helst (sista utvägen)
    pattern_any = r'(\d[\d\s.,]*\d|\d+)'
    matches = re.findall(pattern_any, text)
    
    if matches:
        # Välj det STÖRSTA numret (troligen priset)
        candidates = []
        for match in matches:
            try:
                price = float(parse_price_string(match))
                # Filtrera bort orealistiska värden
                if 100 <= price <= 1000000:
                    candidates.append(price)
            except:
                continue
        
        if candidates:
            # Returnera största kandidaten (troligen priset)
            return Decimal(str(max(candidates)))
    
    raise Exception(f"Kunde inte hitta pris i text: {text}")


def parse_price_string(price_str: str) -> Decimal:
    """
    Parsa en prissträng till Decimal
    Hanterar olika format: "6 999", "6.999", "6,999", "6999.50"
    """
    # Normalisera: ta bort mellanslag
    price_str = price_str.replace(' ', '').replace('\xa0', '')
    
    # Hantera decimaler
    if '.' in price_str and ',' in price_str:
        if price_str.rindex('.') > price_str.rindex(','):
            # 1,234.50 format (Amerikansk)
            price_str = price_str.replace(',', '')
        else:
            # 1.234,50 format (Europeisk)
            price_str = price_str.replace('.', '').replace(',', '.')
    elif ',' in price_str:
        # Kolla om det är decimal eller tusentalsavgränsare
        parts = price_str.split(',')
        if len(parts[-1]) == 2:
            # Troligen decimal: 1234,50
            price_str = price_str.replace(',', '.')
        else:
            # Troligen tusentalsavgränsare: 1,234 → ta bort
            price_str = price_str.replace(',', '')
    elif '.' in price_str:
        # Kolla om det är decimal eller tusentalsavgränsare
        parts = price_str.split('.')
        if len(parts[-1]) == 2:
            # Troligen decimal: 1234.50
            pass
        else:
            # Troligen tusentalsavgränsare: 1.234 → ta bort
            price_str = price_str.replace('.', '')
    
    return Decimal(price_str)


def scrape_monitor(monitor: dict) -> dict:
    """Scrapa en monitor och returnera resultat"""
    result = {
        "success": False,
        "value": None,
        "error": None,
        "raw_text": None,
        "type": monitor.get("type", "price")
    }
    
    try:
        # 1. Hämta HTML
        html = fetch_html(monitor["url"])
        
        # 2. Hantera olika typer
        monitor_type = monitor.get("type", "price")
        
        if monitor_type == "category":
            # Extrahera alla produkter från kategorisidan
            category_data = extract_category(html, monitor["selector"])
            result["value"] = category_data
            result["raw_text"] = f"Hittade {category_data['count']} produkter"
            result["success"] = True
            return result
        
        # 3. För vanliga monitors: Extrahera element
        selector_type = monitor.get("selector_type", "css")
        selector = monitor["selector"]
        
        if selector_type == "css":
            raw_text = extract_with_css(html, selector)
        else:
            raw_text = extract_with_xpath(html, selector)
        
        result["raw_text"] = raw_text
        
        # 4. Försök parsa som pris (om det ser ut som ett pris)
        if any(char.isdigit() for char in raw_text):
            try:
                price = parse_price_smart(raw_text)
                result["value"] = float(price)
            except Exception as e:  
                print(f"Parse error: {e}") 
        else:
            result["value"] = raw_text
        
        result["success"] = True
        
    except Exception as e:
        result["error"] = str(e)
    
    return result


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def clear_screen():
    """Rensa skärmen"""
    print("\n" * 50)


def print_header():
    """Visa header"""
    print("=" * 70)
    print(" " * 20 + "McYfee POC - REAL SCRAPING")
    print(" " * 25 + "Team YFEE")
    print("=" * 70)
    print()


def print_divider():
    """Visa separator"""
    print("-" * 70)


def pause():
    """Vänta på Enter"""
    input("\nTryck Enter för att fortsätta...")


# ============================================================================
# MENU FUNCTIONS
# ============================================================================

def show_main_menu():
    """Visa huvudmeny"""
    clear_screen()
    print_header()
    
    if not SCRAPING_AVAILABLE:
        print("⚠️  SIMULERAT LÄGE - Installera dependencies för riktig scraping!")
        print()
    
    print("HUVUDMENY")
    print_divider()
    print("1. Visa monitors")
    print("2. Lägg till ny monitor")
    print("3. Kolla priser NU (riktig web scraping!)")
    print("4. Visa rapport")
    print("5. Testa selector/xpath")
    print("9. Avsluta")
    print_divider()
    
    choice = input("Välj alternativ [1-9]: ")
    return choice


def show_monitors():
    """Visa alla monitors"""
    clear_screen()
    print_header()
    print("DINA MONITORS")
    print_divider()
    print(f"{'ID':<5} {'Produkt':<35} {'Type':<12} {'Värde':<20} {'Status'}")
    print_divider()
    
    for m in monitors:
        status = "✅ Active" if m["is_active"] else "⏸️  Paused"
        monitor_type = m.get("type", "price")
        selector_type = m.get("selector_type", "css").upper()
        
        # Visa värde beroende på typ
        if m["current_price"] is not None:
            if monitor_type == "category":
                # För category: visa antal produkter
                if isinstance(m["current_price"], dict):
                    value_str = f"{m['current_price'].get('count', 0)} produkter"
                else:
                    value_str = "Category data"
            elif isinstance(m["current_price"], (int, float)):
                value_str = f"{m['current_price']:,.0f} kr".replace(',', ' ')
            else:
                value_str = str(m["current_price"])[:20]
        else:
            value_str = "Inte kollad än"
        
        type_display = f"{monitor_type} ({selector_type})"
        
        print(f"{m['id']:<5} {m['name']:<35} {type_display:<12} {value_str:<20} {status}")
    
    print_divider()
    print(f"\nTotalt: {len(monitors)} monitors")
    print("\nTryck 'v' för att se detaljer, Enter för att gå tillbaka: ", end="")
    
    choice = input().lower()
    if choice == 'v':
        show_monitor_details()


def show_monitor_details():
    """Visa detaljer för en monitor"""
    try:
        monitor_id = int(input("\nVälj monitor ID: "))
        monitor = next((m for m in monitors if m["id"] == monitor_id), None)
        
        if not monitor:
            print("❌ Monitor finns inte!")
            pause()
            return
    except ValueError:
        print("❌ Ogiltigt ID!")
        pause()
        return
    
    clear_screen()
    print_header()
    print(f"MONITOR DETALJER - ID: {monitor['id']}")
    print_divider()
    print()
    print(f"Namn:           {monitor['name']}")
    print(f"URL:            {monitor['url']}")
    print()
    print(f"Selector Type:  {monitor.get('selector_type', 'css').upper()}")
    print(f"Selector:       {monitor['selector']}")
    print()
    
    if monitor["current_price"] is not None:
        print(f"Senaste värde:  {monitor['current_price']}")
    else:
        print(f"Senaste värde:  Inte kollad än")
    
    print(f"Threshold:      {monitor['threshold']:,} kr".replace(',', ' '))
    print(f"Status:         {'✅ Active' if monitor['is_active'] else '⏸️  Paused'}")
    print()
    print_divider()
    
    pause()


def add_monitor():
    """Lägg till ny monitor"""
    clear_screen()
    print_header()
    print("LÄGG TILL NY MONITOR")
    print_divider()
    
    print("\nOBS: Detta är en POC - data sparas inte permanent!")
    print()
    
    name = input("Produktnamn: ")
    url = input("URL (full URL till produktsida): ")
    
    print("\nSelector Type:")
    print("1. CSS Selector (t.ex. '.product-price')")
    print("2. XPath (t.ex. '//span[@class=\"price\"]')")
#    print("3. Hela sidan")
    
    selector_choice = input("\nVälj [1-2]: ")
    
    if selector_choice == "1":
        selector_type = "css"
        print("\n💡 Tips: Högerklicka på priset i Chrome → Inspect")
        print("   Högerklicka på elementet → Copy → Copy selector")
#    elif selector_choice == "3":
#        selector_type = "body"
    else:
        selector_type = "xpath"
        print("\n💡 Tips: Högerklicka på priset i Chrome → Inspect")
        print("   Högerklicka på elementet → Copy → Copy XPath")
    
    print()

    #if selector_choice == '3':
    #    selector = 'body'
    #else:
    selector = input(f"Ange {selector_type.upper()} selector: ")
    
    try:
        threshold = int(input("Notifiera om priset går under (0 om inte pris): "))
    except ValueError:
        print("\n❌ Ogiltigt värde!")
        pause()
        return
    
    # Testa scraping direkt
    print("\n⏳ Testar selector...")
    test_monitor = {
        "url": url,
        "selector_type": selector_type,
        "selector": selector
    }
    
    if SCRAPING_AVAILABLE:
        result = scrape_monitor(test_monitor)
        
        if result["success"]:
            print(f"✅ Funkar! Hittade: {result['raw_text']}")
            confirm = input("\nLägg till denna monitor? [Y/n]: ")
            if confirm.lower() == 'n':
                return
        else:
            print(f"❌ Fel: {result['error']}")
            print("\nKontrollera URL och selector!")
            pause()
            return
    else:
        print("⚠️  Kan inte testa - dependencies saknas")
    
    new_monitor = {
        "id": len(monitors) + 1,
        "name": name,
        "url": url,
        "selector_type": selector_type,
        "selector": selector,
        "type": "price",
        "threshold": threshold,
        "current_price": None,
        "is_active": True
    }
    
    monitors.append(new_monitor)
    price_history[new_monitor["id"]] = []
    
    print(f"\n✅ Monitor skapad!")
    print(f"   ID: {new_monitor['id']}")
    print(f"   Type: {selector_type.upper()}")
    print(f"   Selector: {selector}")
    pause()


def test_selector():
    """Testa en selector/xpath"""
    clear_screen()
    print_header()
    print("TEST AV SELECTOR")
    print_divider()
    
    print()
    
    #name = input("Produktnamn: ")
    name = 'Testing'
    url = input("URL (full URL till produktsida): ")
    
    print("\nSelector Type:")
    print("1. CSS Selector (t.ex. '.product-price')")
    print("2. XPath (t.ex. '//span[@class=\"price\"]')")
#    print("3. Hela sidan")
    
    selector_choice = input("\nVälj [1-2]: ")
    
    if selector_choice == "1":
        selector_type = "css"
        print("\n💡 Tips: Högerklicka på priset i Chrome → Inspect")
        print("   Högerklicka på elementet → Copy → Copy selector")
#    elif selector_choice == "3":
#        selector_type = "body"
    else:
        selector_type = "xpath"
        print("\n💡 Tips: Högerklicka på priset i Chrome → Inspect")
        print("   Högerklicka på elementet → Copy → Copy XPath")
    
    print()

    #if selector_choice == '3':
    #    selector = 'body'
    #else:

    while True:
        selector = input(f"Ange {selector_type.upper()} selector: ")

        '''
        try:
            threshold = int(input("Notifiera om priset går under (0 om inte pris): "))
        except ValueError:
            print("\n❌ Ogiltigt värde!")
            pause()
            return
        '''
        threshold = 0

        # Testa scraping direkt
        print("\n⏳ Testar selector...")
        test_monitor = {
            "url": url,
            "selector_type": selector_type,
            "selector": selector
        }

        if SCRAPING_AVAILABLE:
            result = scrape_monitor(test_monitor)

            if result["success"]:
                print(f"✅ Funkar! Hittade: {result['raw_text']}")
                #confirm = input("\nLägg till denna monitor? [Y/n]: ")
                #if confirm.lower() == 'n':'
                pause()
                continue
            else:
                print(f"❌ Fel: {result['error']}")
                print("\nKontrollera URL och selector!")
                pause()
                continue
        else:
            print("⚠️  Kan inte testa - dependencies saknas")




def check_prices():
    """Riktig priskontroll genom web scraping"""
    clear_screen()
    print_header()
    print("KOLLAR PRISER - RIKTIG WEB SCRAPING")
    print_divider()
    print()
    
    if not SCRAPING_AVAILABLE:
        print("❌ Kan inte scrapa - saknar dependencies!")
        print("   Installera: pip install requests beautifulsoup4 lxml")
        pause()
        return
    
    alerts = []
    category_results = []
    
    for m in monitors:
        if not m["is_active"]:
            continue
        
        monitor_type = m.get("type", "price")
        selector_type = m.get("selector_type", "css").upper()
        
        print(f"⏳ Kollar {m['name']}...")
        print(f"   URL: {m['url'][:60]}...")
        print(f"   Type: {monitor_type} | Selector ({selector_type}): {m['selector']}")
        
        result = scrape_monitor(m)
        
        if result["success"]:
            if monitor_type == "category":
                # Hantera category monitor
                category_data = result["value"]
                print(f"   ✅ {result['raw_text']}")
                
                # Visa några exempel-produkter
                if category_data['products']:
                    print(f"   📦 Exempel produkter:")
                    for prod in category_data['products'][:3]:
                        print(f"      • {prod['name'][:40]} - {prod['price']:,.0f} kr".replace(',', ' '))
                    if category_data['count'] > 3:
                        print(f"      ... och {category_data['count'] - 3} till")
                
                m["current_price"] = category_data
                category_results.append({
                    "monitor": m,
                    "data": category_data
                })
                
                # Spara i historik
                if m["id"] in price_history:
                    price_history[m["id"]].append(category_data['count'])
            else:
                # Hantera vanliga monitors
                print(f"   ✅ Hittade: {result['raw_text']}")
                
                old_price = m["current_price"]
                m["current_price"] = result["value"]
                
                # Spara i historik
                if m["id"] in price_history:
                    price_history[m["id"]].append(result["value"])
                
                # Kolla threshold (bara för numeriska värden)
                #print(f"   💡 DEBUG: result['value'] = {result['value']} (type: {type(result['value'])})")
                #print(f"   💡 DEBUG: m.get('threshold') = {m.get('threshold')}")
                #print(f"   💡 DEBUG: isinstance check = {isinstance(result['value'], (int, float))}")
                if isinstance(result["value"], (int, float)) and m.get("threshold"):
                    #print(f"   💡 DEBUG: Värde={result['value']}, Threshold={m['threshold']}")
                    #print(f"   💡 DEBUG: {result['value']} < {m['threshold']} = {result['value'] < m['threshold']}")
                    if result["value"] < m["threshold"]:
                        alerts.append({
                            "monitor": m,
                            "old_price": old_price,
                            "new_price": result["value"]
                        })
                        print(f"   🔔 ALERT! Under threshold ({m['threshold']:,} kr)!".replace(',', ' '))
                    elif old_price and old_price != result["value"]:
                        print(f"   📊 Prisändring: {old_price} → {result['value']}")
                else:
                    print("Inget pris har hittats")
        else:
            print(f"   ❌ Fel: {result['error']}")
        
        print()
        time.sleep(1)  # Var snäll mot servrar
    
    print_divider()
    
    # Visa alerts
    if alerts:
        print(f"\n🔔 {len(alerts)} ALERTS TRIGGADE!")
        print("\nNotifikationer som skulle skickas:")
        for alert in alerts:
            m = alert["monitor"]
            print(f"\n📱 Telegram:")
            print(f"   {m['name']}")
            print(f"   Pris: {alert['new_price']:,.0f} kr".replace(',', ' '))
            if alert['old_price']:
                print(f"   Var: {alert['old_price']:,.0f} kr".replace(',', ' '))
                print(f"   Spara: {alert['old_price'] - alert['new_price']:,.0f} kr!".replace(',', ' '))
    
    # Visa category summaries
    if category_results:
        print(f"\n📊 KATEGORI-SAMMANFATTNING:")
        for cat in category_results:
            m = cat["monitor"]
            data = cat["data"]
            products = data['products']
            
            if products:
                prices = [p['price'] for p in products]
                print(f"\n{m['name']}:")
                print(f"   Totalt: {data['count']} produkter")
                print(f"   Lägsta pris: {min(prices):,.0f} kr".replace(',', ' '))
                print(f"   Högsta pris: {max(prices):,.0f} kr".replace(',', ' '))
                print(f"   Genomsnitt: {sum(prices)/len(prices):,.0f} kr".replace(',', ' '))
    
    if not alerts and not category_results:
        print("\n✅ Inga alerts denna gång!")
    
    pause()


def show_report():
    """Visa rapport"""
    clear_screen()
    print_header()
    print("RAPPORTER")
    print_divider()
    print("1. Prishistorik för en produkt")
    print("2. Jämför alla produkter")
    print("3. Tillbaka")
    print_divider()
    
    choice = input("Välj [1-3]: ")
    
    if choice == "1":
        show_price_history()
    elif choice == "2":
        compare_products()


def show_price_history():
    """Visa prishistorik"""
    clear_screen()
    print_header()
    print("PRISHISTORIK")
    print_divider()
    
    for m in monitors:
        print(f"{m['id']}. {m['name']}")
    
    try:
        monitor_id = int(input("\nVälj monitor ID: "))
        monitor = next((m for m in monitors if m["id"] == monitor_id), None)
        
        if not monitor:
            print("Monitor finns inte!")
            pause()
            return
    except ValueError:
        print("Ogiltigt ID!")
        pause()
        return
    
    clear_screen()
    print_header()
    print(f"HISTORIK - {monitor['name']}")
    print_divider()
    print()
    
    history = price_history.get(monitor_id, [])
    
    if not history:
        print("Ingen historik ännu! Kör 'Kolla priser' först.")
        pause()
        return
    
    print(f"{'Check #':<10} {'Värde':<20}")
    print_divider()
    
    for i, value in enumerate(history, 1):
        if isinstance(value, (int, float)):
            value_str = f"{value:,.0f} kr".replace(',', ' ')
        else:
            value_str = str(value)[:30]
        print(f"Check {i:<4} {value_str}")
    
    print()
    print_divider()
    
    # Statistik för numeriska värden
    numeric_values = [v for v in history if isinstance(v, (int, float))]
    if numeric_values:
        print(f"\nLägsta: {min(numeric_values):,.0f} kr".replace(',', ' '))
        print(f"Högsta: {max(numeric_values):,.0f} kr".replace(',', ' '))
        print(f"Genomsnitt: {sum(numeric_values)/len(numeric_values):,.0f} kr".replace(',', ' '))
    
    pause()


def compare_products():
    """Jämför produkter"""
    clear_screen()
    print_header()
    print("JÄMFÖRELSE")
    print_divider()
    print()
    
    # Filtrera bara de med numeriska priser
    price_monitors = [m for m in monitors if isinstance(m.get("current_price"), (int, float))]
    
    if not price_monitors:
        print("Inga priser att jämföra! Kör 'Kolla priser' först.")
        pause()
        return
    
    sorted_monitors = sorted(price_monitors, key=lambda m: m["current_price"])
    
    print(f"{'#':<5} {'Produkt':<40} {'Pris':<15}")
    print_divider()
    
    for i, m in enumerate(sorted_monitors, 1):
        price_str = f"{m['current_price']:,.0f} kr".replace(',', ' ')
        print(f"{i:<5} {m['name']:<40} {price_str:<15}")
    
    pause()


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Huvudloop"""
    clear_screen()
    print("\nMcYfee POC - MED RIKTIG WEB SCRAPING!")
    print("\nDetta är en demonstration som faktiskt hämtar data från sajter.")
    
    if not SCRAPING_AVAILABLE:
        print("\n⚠️  VIKTIGT: För att testa riktigt scraping, installera:")
        print("   pip install requests beautifulsoup4 lxml")
    
    
    while True:
        choice = show_main_menu()
        
        if choice == "1":
            show_monitors()
        elif choice == "2":
            add_monitor()
        elif choice == "3":
            check_prices()
        elif choice == "4":
            show_report()
        elif choice == "5":
            test_selector()
        elif choice == "9":
            clear_screen()
            break
        else:
            print("\n Ogiltigt val! Välj 1-9.")
            pause()


if __name__ == "__main__":
    main()