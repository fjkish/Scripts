from arcrest.security import AGOLTokenSecurityHandler
from arcrest.agol import FeatureService
from arcrest.common.filters import LayerDefinitionFilter

if __name__ == "__main__":
    username = "fkish_PS_CC"
    password = "<add here>"
    url = "http://www.arcgis.com/sharing/content/items/5fd018a7fd11469f8ed0df927d542829/data"
    proxy_port = None
    proxy_url = None
    agolSH = AGOLTokenSecurityHandler(username=username,password=password)
    fs = FeatureService(
        url=url,
        securityHandler=agolSH,
        proxy_port=proxy_port,
        proxy_url=proxy_url,
        initialize=True)
    ldf = LayerDefinitionFilter()
    ldf.addFilter(0, where="1=1")
    print fs.query(layerDefsFilter=ldf,returnCountOnly=True)
    # should see something like : {'layers': [{'count': 4, 'id': 0}]}