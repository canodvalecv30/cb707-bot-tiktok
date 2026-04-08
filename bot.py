
"""
TikTok Bot - Modo Ninja 🥷
VERSION LIVE - CORREGIDO
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import config

class TikTokBot:
    def __init__(self):
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        print("[🔌] CONECTANDO CON CHROME...")
        options = Options()
        options.binary_location = "/data/data/com.termux/files/usr/bin/chromium-browser"
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"user-agent={config.USER_AGENT}")
        options.add_argument(f"window-size={config.WINDOW_SIZE}")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(15)
        print("[✅] CONECTADO EXITOSAMENTE!")

    def humanizar_texto(self, texto):
        variaciones = ["", " ", ".", "..", "!", "!!"]
        return texto + random.choice(variaciones)

    def comportamiento_humano(self):
        if random.randint(0, 2) == 1:
            scroll = random.randint(50, 150)
            self.driver.execute_script(f"window.scrollBy(0, {scroll})")
            time.sleep(random.uniform(1, 2))

    def enviar_comentario(self, texto):
        try:
            # ✅ VERSION CORREGIDA - SIN ERRORES
            self.driver.execute_script("""
                var cajas = document.querySelectorAll(div[contenteditable=true], textarea, input);
                for(var i=0; i<cajas.length; i++){
                    if(cajas[i].offsetParent !== null){
                        cajas[i].innerText = " + texto + ";
                        cajas[i].focus();
                        var evt = new Event(input, {bubbles:true});
                        cajas[i].dispatchEvent(evt);
                        break;
                    }
                }
            """)
            
            time.sleep(1.5)
            
            # ENVIAR
            self.driver.execute_script("""
                var e = new KeyboardEvent(keypress, {key: Enter, which:13});
                document.activeElement.dispatchEvent(e);
            """)
            
            print(f"[📤] ENVIADO: {texto}")
            
        except Exception as e:
            print(f"[⚠️] Error JS, usando metodo normal...")
            # METODO NORMAL
            try:
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(texto)
                time.sleep(0.5)
                body.send_keys(Keys.ENTER)
            except:
                pass

    def iniciar(self, url, cantidad, mensaje):
        try:
            print(f"[🌐] ABRIENDO LIVE: {url}")
            self.driver.get(url)
            print("[⏳] CARGANDO LIVE... ESPERA 20 SEGUNDOS")
            time.sleep(random.uniform(18, 25))

            total = 0
            for i in range(cantidad):
                msg_final = self.humanizar_texto(mensaje)
                self.comportamiento_humano()
                self.enviar_comentario(msg_final)
                
                espera = random.uniform(config.TIEMPO_ESPERA_MIN, config.TIEMPO_ESPERA_MAX)
                print(f"[⏳] ESPERANDO {round(espera,1)}s...\n")
                time.sleep(espera)
                total += 1

            self.driver.quit()
            print(f"\n✅ FINALIZADO! Total: {total}")

        except Exception as e:
            self.driver.quit()
            print(f"\n❌ ERROR: {str(e)[:150]}")

if __name__ == "__main__":
    print("="*60)
    print(" 🥷 TIKTOK BOT | MODO LIVE 📡 ")
    print("="*60)
    
    link = input("🔗 LINK DEL LIVE: ")
    cant = int(input("🔢 CANTIDAD: "))
    txt = input("💬 MENSAJE: ")
    
    print("\n[!] INICIANDO EN MODO LIVE...\n")
    bot = TikTokBot()
    bot.iniciar(link, cant, txt)

