from datetime import datetime
from integrations.shipping import shipping
from requests import RequestException
import logging

class Jadlog(shipping.Shipping):
    def __init__(self) -> None:
        self.nav.verify = False
        super().__init__()

    def _get_header(self):
        self.nav.headers = {
            "Authorization": self.env.get("F2B_JADLOG_TOKEN_TYPE")+" "+self.env.get("F2B_JADLOG_TOKEN_ACCESS"),
            "Content-type": "application/json"
        }
    
    def tracking(self, _taxvat: str, _invoice: str, _invoice_serie: str = None, _cte: str = None, _code:str = None):
        self._get_header()
        try:
            resp = self.nav.get("https://jadlog.com.br/api/tracking/consultar",params={
                "consulta":[{
                    "df":{
                        "nf": _invoice,
                        "serie": _invoice_serie,
                        "tpDocumento": 2,
                        "cnpjRemetente": _taxvat
                    }
                }]
            })

            if resp.status_code==200:
                consulta = resp.json()

                return [{
                    "shipping":"JADLOG",
                    "forecast": datetime.strptime(cons['previsaoEntrega'],"%Y-%m-%d").strftime("%d/%m/%Y"),
                    "timeline": [{
                        "date": datetime.strptime(evt['data'],"%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M"),
                        "status": evt['status']
                    }for evt in cons['tracking']['eventos']]
                }for cons in consulta['consulta']]
            return False
        except RequestException as e:
            logging.error(e.strerror)
            return False