from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.db import models
import datetime


# Create your models here.

no_photo_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAACAASURBVHic7d13lF1V2cfx76QHkkCI9BJAem/SkSIidkBQFAVUXitiQQTLK2BH7ICIigiCUpSiKEgRLAjSQXrvhJIESEIgycx9/3gybybJzNn73nv2eU75fdY6C9bKzNzfObec556z97NBRERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERESkQz3eAUREJGgCsBqw+vz/rghMApaZv00Clp7/s0sBwwb8/4vz/78XeGn+/09bZJsKPAU8Bjw6f5uZamekHFQAiIiUx6rABsDG8/+7EbA2C07uRZoG3A/8F7gLuGP+f590yCIJqAAQEfExHtgU2BLYAdgZWM41UZwXgRuAa4CbgH8B010TSUdUAIiIFGMssBPwxvnbxiy4VF9lvcCtwOXzt2uAV10TiYiIOFsDOBy4ApgNtBqwzQIuBQ7DbmmIiIg0wprAp7FL4334n5C9tzuBY4D1ujimIiIipbQs8BngNvxPuGXergc+CUzs7DCLiIj4GwG8A7gAmIP/ybVK2yvAOcCbqcc4iErSIEARkfZMAv4H+ATF3eOexYL5+Y/N36aw+Hz+2fN/ftFR+T0smEo4loV7CCyD9RVYbcC2+vyfK8JDwEnAqSzoWSAFUAEgIhJnY2xg2wGkOznOAW6fv93Fgjn4TyR6vCyTWdCLYENs/zcGRiZ6vJnA6cAJwL2JHkNERCTa64A/kWZA3xPA77DxA9sBYwrap06NBXbEZjacBzxN/sekd/7f3qSgfRIREVnItuR/4p+FzZU/EmsAVIersGsCHwHOxS7h53Ws+rDjv1VxuyIiIk22KTaPPa8T2RTgZ8AepLt8Xhajgbdi9/OfI79C4AJg3QL3Q0REGmQl7MTVS/cnreeAH2Od/5o6yn048AbgZGxQYrfHdA5wIjblUkREpGtLAsdig9C6OUHNxS5Z7wOMKnQPym8MsD/wV7ovsF7AbqGUfbyEiIiU2NuxqXXdnJCeAr6CTaWTsFWBrwPP0N1xvw+7wiAiIhJtReAMujsB3YgNftM30c6MAvYDrqW75+FcqrGKooiIOOoBDqW70eqXANsXHbzmdgOuovPnZCrwocJTi4hIJawI/IXOTzKXA9sUnrpZdsDGUXT6HF2KDeYUEREBrHtfpyPRr0Bz0Yu2I3ANnT1fzwJ7FR9ZRETKZCK26EwnJ5I7sTnt4qMH2Bd4gM6ev1OBcYWnFhERd1tgC8108g3yY9hqf+JvFPA5OruCcxewfvGRRUTEy4FY2912ThZ92MwANZoppxXobObGDKwHgYiI1NhorANfuyeJ+4HdHfJK+3bFVgts9zk+BTVoEhGppRWA/9DeSWEu8A2scJDqWAL4Ae13FbwaWKb4uCIiksqGwMO0dzJ4COvVL9W1A/Ag7T3vD6CFhUREamF32h8gdgYaIV4XE7DL++08/1OB13uEFRGRfHwYWyUu9oN/OvBOl6SS2gG0t6DTbOA9LklFRKQrn8RG7sd+4N8KvNYlqRRlPax/Q+xrog/4lEtSERHpyJG0d8n3N9jAMam/8bTX/KkPONwlqYiIROsBvkv8h/s8bPEfaZYe4Cjau0J0tEtSEREJ6gFOJP4D/SXgLS5JpSz2A14m/jXzHZ+YIiKS5TjiP8ifxFoBi2wDTEFXAkREKulY2hvspyVhZaA1gHuIfw193iemiIgM9AXiP7ivw1YAFFnU8lhxGDsw8OM+MUVEBGxRn9iBXFdhI8BFhjIRKxJjXk+9qE+AiIiLXYBXiPuw/gsw1iWlVM2SwOXEva5exRYfqqUe7wAiIoPYBPgn1uY15BJgL6wjYNMsjTW/WQVYGRv7sCL2TXcMdkVkBAvfFnkZO7G9gHVGfA4bJPco8DhwH/BEMfHdjMWKxl0ifnYqsD12XGql6gXAithiEOthizusgPX3HukZSkS6tgZxq7ZdBbwVa+taZz3AOtiI9tcB6wMbYJ+BKbwI3AXcDFw/f+tfgrcuxmNXAraJ+NkHsCLguaSJClbFAmBzrOfz29CKTiJNdh3wRqz/e930AJsBewA7A9viP7jxWeBvwBXApdhUy6qbiBWRm0b87N+xhafmJU0kixmBnfRvIX40sDZt2uq73YJd/q6T8cD+wJnAM/gf46ytDyvAvoBdramy5YifIvgDp4yNtTftr/esTZu2+m6Pku7Sd9EmAO8HLsRuY3gf2062Puxb9IHYALsqWoP4ouu9ThkbZWXsMpP3i1ubNm3l2V4ENqbaerC16E8HZuF/TPPcpgPHA6vndbAKtC1xbYNnUv3XYKm9A3ge/xezNm3ayrPNBfakupYGjmDBYLo6b/OwFfk2yuXIFWdfbP5/aP/uRqtLJnE4cU+ANm3amrVVtTPbmsBPgBn4Hbt5wDSKv+LQC5yLzVioiqOI27dTvALmpWyzAI5HPZhFZHG/Aj7sHaJNmwBfxXoUDE/0GC9i89Pvw64sPIzdy56CTVl7DjsJL2opbC78RGAydsm+/7/rYpe4R+SYcx7wC2yhnbJPpevBipZ9I352H+CCtHHSKVMBcCz2ZmnXw8A/sFHBDzD0C15EymUN4GzCJ8ebsX4fryRPlI+NsBPdu8j3M7YXuBH4Dwvm5t+f498faAlsNcVtsHvjO2G99Lv1InZsTqTcn9MTsOMbmmo+FZtCWIcpkW4Oob3LSjOwS2pa7lOkmnqAKwm/16dRnWlmywFnke8tzPuxk+Ve2Ld2L8OwRjjfxa42dLtfN2A9XcpsQ2zAX2hf/uwVsA62JH76yxxsHmZMhzARKa+PE36/92Fd/qpgPDYwLI+T/n+BYyj3SPMNgO9gzYE63c+5wNfI91ZD3g4gbl/e7xWwysYQPyL2LspfMYpI2OrAS4Tf8yc45etE7MCxobansTFQVRosBzAaO/n9m873/T/A2kUHb8OZhPfhOewKkLThG8S9QC7BevyLSPVdQvg9fw/VmmYVs0+Lbr3An7C25mX+FhxrS2x/OikCZmBdEMtoaaz5VGgffusVsIomYytShQ7qhWhxH5G62Jvwe34OtuBNlVxM/MnuJWwMU5m/9XZjO6wzYCeFwI8o5+f9rsSN7XiTV8CqOZnwwbwGu8QkItW3BPAI4ff90U75unEY8Se5Y3wiFu6NdLZ+y9+BSQ55Q75POPvdlLOAKZXlCH/7fx5rBywi9RBzy+8OYJRXwC6MxhbHiT3JHeETs3AjsPER7a5zcC+wlkPeLEsADxHO/jmvgFXxOcIH8SC3dCKSt9WxefxZ7/lebL5/VS0D3ISKgMGsg32zb6cIeA7rQVAmexLO/QL59EyordvIPoC3UK4mRSLSnZiR1D9zS5efibRXBHzBJ6aLHuBjxC2407/NAHbzCJvhbMK5f+6WruRWJnzw3u2WTkTytjnhAVRPY6Ot62Ai1rFPRcDgNsO6tsYen9mUqx/ECtiqh1mZ52JXPWQRBxK+7FPFe4AiMrjLCH/If8gtXRrtFgFH+sR0M5H2pgy+SrlG2Mfcxj7bLV2J/YTsg/Zrt2QikrfdCH9Q3kq6xXI8TcRa3sae5I7yiemmB/gytlBQzPGZSXnGBIwifBWjF7vaIQNcTvZBO8gvmojk7CrCH+y7u6VLT0VA2H6EB4j2b89jPfrLYF/Cef/klq6kQtMotvSLJiI52oHwB+Rf3NIVZ2lsZbnYIuCLPjFd7Y4N+Is5Po9jjeS89QD/IjtrH7oKsJCpZB+wMjaAEJH2hdrj9gGbuKUrloqAsK2xMWAxx+ce4DU+MRcSU+SqRfAAoQZA6qIkUn1bEv5g/INbOh/tFgFf8onpan3sG37M8bmccowdCd3Wnges6ZauZEJPqohUX2jefx/NvN23FO11DPxfn5iu1gamEHd8vuaUcaDtCef8qVu6klEBIFJvKxK+0neBWzp/S2NL4MYWAV/2ielqK+KWjO4F3uKUcaC/kZ3zZaxTZOOpABCpt2MJv8+b+O1/oHavBHzFJ6arXYlbQ2Aq1mra066Ec2qNAFQAiNTZaMKXb6/2Clcyuh0Qtjdxy/DegP/4sdDKh/ehFvcqAERq7D2E3+N7u6Urn6WAa4kvAo72ienqf4k7Nt4zJw4mnHEPr3BloQJApL4uJfv9/TDlGLldJu0WAV/1ielmGPBHwsdlNr7990cDzwySa+B2vlu6klABIFJPqxBu63q4W7pym4CuBGQZD9xF+Lhcje9l9q8NkmngNody9C9wowJApJ6+TPZ7+xXK0ejrfcA/gEewTm5lWX10AvBvVAQMZSNgFuHj8mGvgMQVwZ9wS1cCKgBE6ulest/b5/pF+3/fYvBs3/EMNUC7RcAxLin9fIbwMZkGLOcVkPBtsGv8ovlTASBSP5sSfm97z9fekuwR5d/2i7aQCdhJQkXA4oYR7r/fAn7kFRDYPyNXC2uC9Vq3dM5UAIjUzzfIfl8/if/gv/MJf/58wy3dwtotAo71ieliHayxTtbxmA2s6pRvDHYVIitfE9s8AyoAROoodPn/OL9ogN0/7qNaJ9PxtFcElKEtblE+T/h4/NwtHfwsI1cL6wTZSCoAROplE8Lv663c0pmzCGccuJVlqt144i55N60IGIGtCJh1LOYAaznle0MgWx+wslM2VyoAROrli2S/px/Bd2rWWoRHZg+2laUHf7tFwNd9YhZuL8LH4jdO2UYAzweyfdwpmysVACL18g+y39M/9IsG2KXgdk/+/duRDnkHMx74JyoCFhU6JnPx+6b9q0C2S51yuVIBIFIfS2GXWrPe0zu6pbN8MXPHszbvFrP9lgSuIj73d31iFmprwmM7jnbK9rZArtnAWKdsblQAiNTHvmS/n5/Hpm55+dQQudrdyrKS2zjCV1wGbt/0iVmoi8k+Bk9gl+SLNoZw8bmbQy5XKgBE6iM02vkcv2gA3EH4Myd2+3TB2YeiImBhoQF3LfwWoAo1Bar7c7MYFQAi9RHqz36IXzR2zMjVv/2c+M57fcChhe7B0NotAr7lE7Mwt5G9/391ynV4INd1TrncqAAQqYdlCd9/neyWzkaAh07oa2PjBK4L/OzA3ynL6O1xwN+JLwLK0ukwhYMJP2+rOOQKdciciw3wbAwVACL1sA/Z7+V7/aIxjnC3uMsG/PzSwPWBnx94MvlIETsRYUlUBIAtxfsc2fvusQhPDzAlkGtXh1xuVACI1MMPyH4vn+oXjfdk5Orf9lnkdyYCN0b8XgtbU8Dz9sZAS2LL4MYWAWVZ+ChvJ5O93163Af4QyHWUUy4XKgBE6iH0zdPzW/LvM3K1sLUJBhsZvgxwc+B3BxYBH0y5E21QEQA7k73Pr2K3e4p2RCDXBQ6Z3KgA6MxorJ3qAdiCJedilyzvAR5nweIT07FpL/fO//ffYyNNP4DNmW3cvFNJYhjwItnv5U2csi1JePrV9zN+fxJwa+D3BxYBB6bYiQ602yfAe32GvA3DPvuy9nl/h1w7BTI95ZDJjQqAOMOAbbFVoy4nfD8zdpsN/A34CrAD/iu0STWtTfbrbAZ+r639AtlaWDGc5TXA7RF/p4W1GX5/3jvRoaY3CwrdljrLIdMShJtlreiQy4UKgGwbYpfnQpVsXttTwPfw+7Ym1RS6x361WzL43RCZ+rcHiVubYFngv4G/NbAIeG+eO9GFJbEiv4lFQKgnwCNOuUK3lXZ3ylU4FQCLGw68j/gBSKm2W4CDgJFpd1dq4Btkv5ZOcMrVQ3g0eDtz4pcH7gz8vf5tLvDuPHYiB0vQXhFwvE/M3I0FXiF7Xz2+bZ8RyFSWJlPJqQBYYBQ2kvh+fE/8i24PAR/Dxh2IDOY8sl9DH3XKFbM08RZt/s0VgLsj/m5/EbBvtzuRk6YWAaEGSXs5ZDoykOnnDplcqAAwb8NOtN4n+6ztUfxaaEq5hTqveS0A9OlAril0tjTxitjA2pj3zRwWn2LoZQngSuLf89/ziZmrY8neR48ZEKGFga5xyOSi6QXAati0D++TezvbxcCaKQ6GVNIwwoNSJzpluzCQq5v14VcG7gv8/YFFwDu7eKw8tVsEZM2QqILdyd6/qxwyrRHINMUhk4smFwAfBmbif0LvZHuZ8rRAFV+TKeeH2TAWTIcdaut2tP4qwAOBx+jfXgXe3uXj5WUJ4AqaUQQsT/a+TXPINAybgTVUpj7sOaq9JhYA4wj3JY/ZZmGV/I+wk/EbgHWxD6X+b1xLY99U1sWWmvwYNjXmcvIpPs4BJuR4bKR6Qovs/Mcp18aBXH3YyaFbq2IzCWLeL68Ab8nhMfPQbhHwA5+YuQgNBF3aIVPo6tF6DpkK17QCYH3iBxANtt0LfA1rJjGqyywjsQ/vowmv4pa13Y992Eoz7U/26+M8p1wHBHLdleNjTQYeDjzewCJgzxwfuxtjsS8DdS8CQl0qN3fIFDruZXmNJNWkAmBb4HnaP8HOwvpab5c43+uw6VozOsg4HXh94nxSTqElTr0Gkn03kOuMnB9vdWygbMz7ZTawR86P36l2i4Af0tnASU+hdQE8Bmn+MpCpLAtMJdWUAuDNtH/JfTo2v3rZgrMuAxwDTG0z72x8ptSIr1C3tcOccl3qkGtN4LHA4/ZvL1Oehi9jsdUQ61oEhPrvH+6Q6X8Dmf7XIVPhmlAA7EW49ePAbR5wIj73pQaagL3R59Je9rJ0QJNi/Jbs14RXM5ynArm2T/S4a2HrccS8X2ZRnuVf2y0CfkR1ioCDyd4Xj0ZV/xPI9GOHTIWrewGwM9mjPRfdbgC2dEk6tE2AfxO/D68Cb3JJKh4uIfv14PEtd9lApnmkHWW9NrbCYMz7ZSb2OVEGY7FlcmPf6z+mGkXAW8nejzMdMr0rkMljnYLC1bkA2JjwNKT+rQ97M3U7sC+V4dhtgV7iv9mk+oYl5XId2a8FjwFW2wYyPVhAhnaKgFnALgVkijEa+BPxRcDPKH8RsDXZ++CxBO+ugUyXOWQqXF0LgBUJX4Ls36ZhnaGq4I2Ep9T0b89iU6Sk3u4h+3Uw2SHTPoFMlxeUY32sD0LM++UlbEXOMhhDeAzFwO0nlLsICDXeKer1MFCoTfWNDpkKV8cCYDjxPbefADbyidmxdYif8nQNWkyo7kInOI8+EZ8KZPpZgVk2AJ4J5OnfXiT9bJ9YdSoCViY7+7UOmVYNZLrTIVPh6lgAHEPcG+YefL4d5WEl4tdHr9PyorK4F8l+/j0KwO8EMh1RcJ6NsCtiMe+XF4BtCs43lDGEx3gM3E6gnEXASmTnvt0h06RApoccMhWubgXA67EBRqH9ehh7UVbZssQtiNKHBgXWWdYg116nTKFOm/s5ZNqE+Ntn07G+HGXQbhFwIuUrAlYgO/N9DpnGBzI97ZCpcHUqAEYR11HvWewyeh2sTtxApwexEcZSP1kF7ytOmUKNbd7glGsz4puBTaM8M4LGAH+hukVAaD0AjysAowOZXnDIVLg6FQBHEd6fVynP5b28bEZ4NbgWtiyn1Mtwsp/zl5xy/SuQy/PEugXxs4Om4jOLYjDtFgEnUZ4iYEWys3qsV9GDXR0dKtNMh0yFq0sBMBmbyhPaH6+uaKkdQnjfX8GmRkl9hL7FeKy0BjaCOivXa51y9dsKu8wfcyJ9HtjUJ+ZiRlPNImADsnNe7ZQrq8maV/FcqLoUAKcR3pfzKcebIZWzCB+Ds93SSQrDyH6+vT7E/hvINckp10BbY5d5Y06kz1GeBbdGA38mvgj4Kf6fe6EVKy91yBS6AjDdIVPh6lAATCbc6ncqxff0L9rShKeEzcOWJpb6KOMYgNBSq2VZa31bwrMo+rdngQ19Yi6makXAO4bI1b95NAIaFcj0vEOmwtWhADiJ8H581C1dsQ4kfCxOc0snKZRxFkBoQZ7xTrkGsz12pSTmRDoFu5xdBqOBi4kvAk7Grwg4OJDtVIdMoVkAzzpkKlzVC4DlCff6vx67VNoEPcA/yT4ec4DVvAJK7kInrxEOmULL8novtLWoHYlfhvtpYD2fmItptwjwahv8xUCuYxwyhfoAPOqQqXBVLwBCa6G3sKWAm2QXwsfkq17hJHeh2z4e37bvCGQqwxiARb2e+CXDn6I8U4mrsHbAqYFMHy44D8AqgUz/dchUuKoXALeSnf8m/AfAeAhNw7qPZh6XOrqb7Od6skOm0OqVyztkirELcbOJWlgb8bLMqhlFe0XAKRT7/v9HII9Ho7LQWgDXOGQqXJULgE0J5/foOFYGbyF8bMrS81y6cy3Zz7PHPPbQkrZluYQ+mN2ILwIex39KY79RwB8pZxEQWpjNY1zFLoFMlzhkKlyVC4DjyM7+LM1dCGcY4YFYJ7ilkzyF2sR6dN07L5BpF4dM7diduOZaLexe8Ro+MRfTbhHwc9KPjxpH9nS7Fj63qUIrVp5TdKCmDFTLyx6Bf/8d1uihifqwvgBZQsdPqiE0X3mZQlIsLNR/oKy3APpdAexN3DTK1YCrsLbc3uYA+2JFQIz/wcYEpDz3bEb2lYbHsAGYRQu9LwqfBaACIN4k7B5Olt8UEaTEzgz8+zrYQBipttCiJSsUkmJhjwf+vewFANhtjH2w9uEhk7ElyMswu2YOduuznSLgFNKdf0Kt129N9LghofdF4YsBqQCItwvZx2sKNgCwye7EVj3MslsRQSSpJwP/7nFSCi2lunIhKbp3CfAu7KQasgZ2JWDVpIni9BcBF0X+/CGkKwJCBcBtCR4zxuTAv6sAKLGdA/9+NeUfw1CEqwL/HjqOUn5PBf499EGXQqgAKEtHvRh/xi6rxxQBa2JXAspQ4MwB3k17RUCKMQFlvQIQel9MKSSFs6oOAryS7Nwf8YtWKgeQfZyu84smOdmJ8j3HKwUyha5MldFehFuO92/3YsegDEZhrXZjBwb+kvyKgNDroIXfLIp7A7lCt5hroaoFwBNk5y7L6l3e1iL7ODViwYuaW43s57jwS5nYoK+sUfR9lKsdcKx9iC8C7sGWwS2DkbRXBJxKPkXAQYHHmYpPP5IesjvI9gFLOuQqXBULgPFkTyvppTyLjXgbgQ1iynqOqzAgS4Y2jPCUNY/Wu7cEMoUuDZfVfmQvIztwu4vyvL9GYiuixhYBv6L7IuDswGP8vsu/36nVA7lC42pqo4oFwBZkZ25ED+c23EX28drJL5rk5Hayn+MdHDKdHMj0WYdMeXkP2aswDtzuAJbzibmYIouA4dg3/Ky///EO/3a33hrIdbVHKA0CjBPqI/5AISmqI3Q8ytiXXdpzb+DfPQbdhcYe7FpIijTOwVbejFltcUOsr0AZliOfixUv50f+/Afp/HbANoTn2l/Zwd/NQ6jz4P2FpFiECoA44wL//mIhKarjhcC/V/FerCzsvsC/b1RIioWFCoCd8VmpMC+/xZa5jSkCNsaKgDIU23OB/YE/RP78wXRWBLw98O+PEX7dphIqiO8pJMUiVADECZ2wPLpKlVnoeKgAqL7bA//uUQDch10CHsoEYMuCsqRyJraSXV/Ez26CFQEenRkXNRd4L+0VAe3cDujBiowsXt/+Ifx+cOlNoAIgjgqA9qgAqL9bAv++FXZPtkgtwlcB6tCO+nSsm15MEbAZcDkwMWmiOP1FQOxAvIOILwJ2INwa+eLIx83bWMJT/Fx6E6gAkBRC02zKOthT4t1Pdv/98fisuPaXwL+/r5AU6f2K+CJgC+zbb1muBOyP3c6IcRC2xkjo1k3oeZ2B32p7W5G9SNzjwPMFZVmICoA4oYVGJhSSojpC3/BnFpJCUmoRvg3gMe3uIrILzPWoT8OVXwGfIK6g3hw7AS6VNFGcXuzEfl7kz++PjQkY6orSSMLLsP8Rm4fvYevAv4feR8moAIgTOmGFBgk2jW6ZNMONgX/ftpAUC3sSuCHwM+8tIkhBTgEOJa4I2Bq4lHJ8YZmHfWuPLQIOBE5j8CLgHcBrAr9/bny03IXeB/8pJEVJVLEPwO5kZ77KL1opXUz28drLL5rkKLS++d1Oub4YyPUw9fvy8ymym5UN3K6hPONwRmAn59g+AWeweBHwt8DvvACMTrwfQ+nBOmNm5dvFKZuLKhYAm5GdObQUadPcQ/bx8mgSI/lbjvBJx2OluvUDmVrA2xxypfYZ4k+k/6Q8Vy5HYH0OYrP/hgVFwIYRP//rYnZjUBsPkal/e5WGdZGtYgGwJNkfdI3p4xxhJOHe5WVoUCL5CBV7H3LKdVMg19+ccqX2OeJPpH+nPJ9bIwi38R24nYkVAT+N+NntCtyPRX02I1cLuNYvmo8qFgBgTSSycm/uF61U1iX7OGXN05bq+QXZz/fvnHIdEsjVwkbH19ERxJ9I/0Z5voG2WwScg40nyvqZmwvdg8X9hex8x/lF81HVAuAysnN79Zgum4PIPk7X+EWTBN5N9vP9LD7325fEVp4MfYusq6OIP5Fegc1VL4MRWNEYmz20HVJs/IWMxgaQZ+Xb3S2dk6oWAD8kO3fsaNa6O53s43SKXzRJYCLhRWq2d8r2o0CuOdgVq7r6MvEnysuoXxEwHd9bHG8eIlf/NhO/wYluqloA7EV27uep38jiTjxK9nGq0xQsMdeQ/Zx/zynX2oQHKV7glK0oRxN/wvwrMMYn5mKGY4P9uikAflB46oX9kux8f/KL5qeqBcDSlPebTllsTvbx6QNWcEsnqfwv2c/7Q37RuCQjV/9W9+WpjyX+pPkXyvOtdDjWMbCTk/9cYM3ie1hTawAAIABJREFUI/+/4djtr6yMh7qlc1TVAgCswUhW9pP9opXC98k+Pnf6RZOEQoVfC78Bd1sRvgpwHeH21VX3DeJPnn8CRvnEXMxwrBVwuwXArx2yDrQL4S9Dqztlc1XlAiD0JppKearnog0HniL7+HhfkpN07if7uf+WXzTOz8jVvx3olq443yb+BHoR1S0C5mG3fzydRHbG6/2i+apyAbAB4fzvd0vna2/Cx2Yrt3SSWujk8jjFrw7Yb0Os/3yoeF/RKV+Rvkv8ifR8shexKdJwbNZGTG7v2R2jsddTVsYj3NI5q3IBAOHbAHfRzMGA1xM+LlJfWxJ+b3suxRtz8mjKoKx2rgT8gXIVAaFZRr3ARl4B59uP8HH1HJ/gquoFwKcI78Pebul87En4mBzllk6K8gDZrwGvpkBgH7izh8g1cPuAV8CChaZIDtzOIbwcb1FCswNO94v2//5M9vFs7OV/qH4BMIlwc4fbKc8bJrVhhK+KvAKs5BVQCvNVsl8Hs7G+AV6+NESugdtUYLJXwAL1ACcQXwT8Dr9bOIsaDvyMxTNei83W8rQSNgMh61g2cvR/v6oXAGCD2UL78Vm3dMX6OOFj8TO3dFKkyYTvtXu+L0YCtw6Ra+B2A+WZD59SD3G99Pu3/v77ZfF6bEzDiVhHyjJkCxXBrwDLuKUrgToUACsQvpz4ErCyV8CCTMIaIGUdhznAGl4BpXBXkv16eBjfD+rXEe7n0cKWnW2CHsIj1gduZ1OOE20ZjSK89O/ZbulKog4FANic/9C+/JX6DgjsAS4kfAx+7ZRPfBxA+DXxTrd0JuYKXgv4mFfAgvUQXtRp4HYa9f1c68YHCB+7Pd3SlURdCoAVgRcI78+XvAImFrP2+ExgNa+A4mIM4Q5oV7qlM0sC9xF+/b6KXWZugmHAr4gvAn6JioBF3Uj2MXsYXT2pTQEAcBjh/ZkL7OoVMJHtsA/H0L4f6RVQXH2T8GtjM7d0ZhNgFuGcL9Ccpb6HYVfsYouAn1P/DoqxXk/4eH3eLV2J1KkAGI6tNx3apxepz4fIWsAzhPf5XprbFbHpVsLGfmS9Psqweub7iDvRPQus55SxaMOw8Q+xRcAvUBEAcDnZx2kWDR/8169OBQDYoKLQh10La5O7uk/E3KwMPEJ4X+dR/wVWJNs5ZL9GytCwBQafTjbY9giwik/EwrW7CM+JNLsI2J7wMTrJLV3J1K0AADic+A+Rqq4/vgZx901b2Opw0mzbEH6dnOOWboHRhPtY9G9305wiYAQ2Yj22CPgxzS0CLiVc7Fb1cz93dSwAeoA/EvdGeQ7Y2idmxzYjvNBP/3YZGhwkJnRZtBfr0+9tMvAk8UX8Oi4pizcCu1UTWwQ0cbGvbQkflzLc7iqNOhYAYPd3HiLujTITmy5VBftiYxhi9utxYHmfmFJCuxB+zfzRK9wiNgKmEfc6f4b6jOkJGYmtBxBbBHzPJ6abq8k+Hn3Apl7hyqiuBQDYN4PQFKiB2y+AsS5Jw0Zj9/Zi92Ua5binK+XyL8KvnbLMktmeuJkBLWx2QFOmCI4ELiD+s+A4n5iF24vwsbjQLV1J1bkAABsUOIP4N8vdlOcDsN+O2HoGsfvw8vzfEVnUmwi/fm6iPLeN3kLcoN4WNhW2Kc2CRhF/m7MFfMsnZmFGYjOdQsdBS6Avou4FAMAbsZNi7JulBZyF/4I5K2DzgPuIz/0q8HaHrFIdfyP8OjrQLd3iDiC8psHA7VSasXbAaOBi4o/L13xiFiKmB4y+/Q+iCQUA2DS46bRXBMzGpotMLjjrKtgo3tjLn/3bS8DuBWeV6tmacFH5JDDBK+AgDiD+SkALW+J1VZekxRoNXEL8cTnGJWVay2GrRmbt91ya0zuiLU0pAAA2Jn508cBtDjYP982kax05HLtScQZxXf0W3aYAWybKJvVzLuHX1Ilu6Qb3Ftoriqdh/eDrbgy2zknscfmKT8xkfkN4n092S1dyTSoAwL7Nh3pEZ21PY+t2v5Pu17qegF2u/zGdFSb9263Aa7vMIs2yNuFCsxfrH1AmOxA/O6B/uwhbK6TOxhKe5jlw+6JPzNztTnhfZ2C3U2UQTSsAwC6bnUDnJ9z+bR42YOo07A31LuwDc0Os0JiILb6zAXbZdR/gKGyRjxuIWwY1tJ1CeWcuSLkdR1xxOcIr4BA2Jr4PRv82FRvXUOfmOEsQXv554PYFn5i5GUNcM7S6XfHIVRMLgH7vInzvqKzbC8B78z8k0iDjgCcIv9bK+G1xMvEdAwdu11Pv6YJLEJ4LP3CrSv+TwXyb8P7dh9ZAydTkAgBgWewbeTsj7T23Puyely5pSR72J/yae5VyNtoZTfzaAYtuF1DfDoJbYM3NYo7Dk1RzSdwdibuCuodXwKpoegHQb0fscqf3CT5ruwPr5iaSp5hpgXdQ3ql1B9L+jJkWNjL8d9RjbvgYbDXFq2n/y8xaxcftygTiuryWYW2L0lMBsMAw7D79Tfif7AdutwHvoTzNWaRe1iLuBFrm3vKbENcIZqjt78A7qNZ7bBg2vfkndHcrs2rTJU8jvE8vYqulSoAKgMX1YFOOLqe9BiR5bn3AVdiHUp0HLkk5fIbwa7KXcl9SXQI4Hvtm3+n77gng+9hl9DIajo1h+AndzRzq324tNn7X3k3cfn3IK2DVqADItgo2cv9Oijnx34ONWp1cxM6JzDcMuIbw6/M5bGZLmW0J3EL378W7se55O2Gtd72sA3wCWwSo3SmQWdtMyjfNM8u6WLOz0H792StgFakAiLcu8HFsOcnnyOdNOBU4HzgUmy4o4mVd4lpm/4fyj6wegc1emE1+J8tLgCOwtUImJcq9LLZew5eA32Mreub9JaMP641Qpc54S2LjUEL7Ng3/Fu4d87jUGzrJ6/Lz4IYBa2JvovWwKn0y1hxo3PxtPNaEYiZ2j/UF4FFsasq92Lf9B7A3pEgZfIy4rmknY99Ky24y1v72A+Q/2v0p7KR0N9YgbAq2NPGT2PsdbKT6DOxzdGlgKWwQ2wRsqe7VB2xrkrZh0Vyso+l3gbsSPk4KZ2GDHEPeP/9nJZKuAIjIQLHrzX/QK2AH1seu3FVlum+e2wxsAGfVBvv1ixmf0gJO9wpYZSoARGSgZYDHCH82vArs5pSxU1tiK+h5De4tcrsRu6JTpkWd2vUO4ub7343dJpA2qQAQkUXtRNzqe9Owb9dVsxbwParbCXSo7QVsBdMyNm5qV2xDo5ex9tDSARUAIjKYTxN30nkQW5K1isZiU8aux//k3ek2DesOug/1WRdkVeKnOR7qlLEWVACIyFBillptYTMDxjtlzMuawOHAvyj/LYInsIGYewAjUxwMR5OA/xJ/LLb1iVkPKgBEZChjgZuJ+yC+mvp8A10B+Ag2FS+Phjvdbo8BZwAfxpZyrqsJtH81RgVAF1QAiEiWydg0t5gP40vwbZqTymRsGtoJ2NWOPBvyDNzmYgPazsOmL+4LrJF+90phCawlc7vHrDYFgPoAiEgZbYV9w48ZaX0+tnbFvJSBSmAZbDDha+f/d3nsNkj/PP+lsLn/M1lwLF7Cbi+8hF1ZeGbAfx8H7sdmVzTNKKw50Z4d/O52wHX5xmkOXQEQkRhvIb7P/h8p7+qBUi6jgQvp/KpJba4AeFABICKxPkL8B/OVWEdMkaEsCVxBd7dNVAB0QQWAiLTjGOI/nP9BtRvRSDoTgWvpftyECoAuqAAQkXZ9j/gP6P9Q3T4BksYqwO10f/JXAdAlFQAi0q4e4KfEf0g/RDU7Bkr+Nsf6GMS+dkKtgFUAdEEFgIh0YhjwK+I/yKdRvbUDJF9vwxYnin3NnIiN8FcBkIgKABHp1DCs93zsB/qrWOtdaZ7DiFvYp3/7LnalKTROQAVAF1QAiEi3jqW9+7ZnUJ+ugZJtDHAq7b0+vjPg91UAJKQCQETycCTtfcjfRHO63DXV2sBtxL8m+oDPLfI3VAAkpAJA8rQysCmwAdYFTZrlUNq7zPsc8CaXpJLau4AXiX8tzAEOHuTvqABISAWAdGt34Czsw3zR1889wHHom16TvJ32Bnr1AT9EnQPrYhzwC9q7GjQdeMMQf08FQEIqAKRTm2BLp8a8wedh08Z0VaAZtqD9VfTuwKaISXVtBzxAe8/7Q9gVw6GoAEhIBYB04sPAK7T3Rm8BDwIbO+SV4q0C3Ep7r49XgS8CIxzySudGA18nfq2I/u1awk2iVAAkpAJA2nU47Z/4B27PAOsWnlo8LIndHmr3NXIrsI1DXmnfztgSxu0+xz8n7raPCoCEVABIO/bD7tl2UwC0sKVPVys4u/g5FPt2385rpBdrBLOUQ14JmwScRvufBy8DB7XxOCoAElIBILHWo73BXaHteuzSoTTDtsBjtP86eRI7YQwrPrIMYgTwMQYf9Bva7sdmCbVDBUBCKgAkxpLYIK28Tv7920lF7oS4Wxa4iM5eKzcDuxYfWQZ4K3AnnT1/v6WzqzkqABJSASAxTifuTd4L3EV7i328t8D9kHI4hM6vJv0R2LD4yI22BXA5nT1f04D9u3hsFQAJqQCQkEOIe6PfxILBfT3APsALEb83A60U10SvBa6hs5NKL3AumlGS2lZYwdXpuJ8rsNkg3VABkJAKAMmyKTZoJ/Q6uQdYZpDffz1xg7/uxG4zSLMMB74AzKKzE0wf8Adgs6KD19y2wJ/p7DlpYR0AD8W+CHRLBUBCKgBkKOOIm94zm+wP4E9F/I0W8LsUOyGVsDJ2Iu/0hNPCmlLth3oIdGoY1sWx00v9/dufgFVzzKUCICEVADKUc4l7wx8c8bfOjvxbH8tzB6Ry9gOeorsT0IPAZ4GJBWevqtdgCzl1MkNj4PYwNkgwbyoAElIBIIOJ/dZ+auTfG4/dJgj9vVeALfPaCamkpbD1I2bT3QlpNnZVaU/sVoMsMAL7tn8+7fdnWHSbCRwNLJEoqwqAhFQAyKK2Ju5D4TbaW9N9I+zDIvR3H0Lf3gQmY1PH8mo89R2aXVz2YL36vw9MoftjOg/4JbBS4twqABJSASADLQM8Qvh18RKwTgd//8CIv93CRh7nMYBIqm9r4O90f8Lq3x4BfgDsSP2bCw3HeiecQHtTc0PbpdhiYEVQAZCQCgDp1wNcQNwHwAFdPM4pkY9xVBePIfWzIzbALK+TWAt4Hhvr8hHqs2T1mtj+nAtMJd/j9S+Kb8akAiAhFQDS70jiPgRO6PJxxmA9A0KPMxdbaERkoNdj88vzPLH1b/dh/e0/in3DLfvYgRFYk55PAmdgt8/yPiZ9WOG1dUH7tCgVAAmpABCwD9WYpTzz6t+/JjA94vGeAlbI4fGkfrbGVhqcQ5pioIU1qboaW5ToY9j7ZFIB+zaYZbFv358ETgb+Sef9E2K22dgg33Z79+etMQWAxz3P0Ele92HrbzngFsKDeaZj3zYeyelx34ndcgi9xq4Gdse6v4ksaiXgE9hl72ULeszngUexqXOPYu+JZ7FL7tPm//cFrICYl/F3RmL9NpaZv02a/9/lgdWxgZCrzf/vYI22Unga+Cl2q+65gh4zy7Vkn+S3A64rKEvt6ApAsw0n7nJqHzZtKG/fjXjsFvCtBI8t9TIGG5tyGVYspvpm3MnWhxUG/Zt3nkW3ucDFwL7AqHYPfGKNuQLgQQVAsx1L3AfEcYkefwRxI7z7gL0SZZD6WRkb03Iv/ifXMm93AcdgVxnKSgVAQioAmms37PJk6DVwLXapMpXliev+No36jNSW4myIneQ6Xca2btudWE+EHbs4pkVSAZCQCoBmWhm7Zxl6/p+Z/7OpxRYjeQ1ClGbaAPgKtgphzKDXOmxzsKtsRwJrdX8IC6cCICEVAM0zEpvPG3rue7HBd0X5ckSmFjZASaRbS2G3lU6kfrcK7gB+hPXmH5fXAXOiAiAhFQDNczxxHyJHF5yrB7gwMtuBBWeT+lsKK3iPwea9l3Gw3mDbDKyg/zG2mFJRMyGKogIgIRUAzfJO4nqrX4ZPm9RJxLUinoFdzhVJZTjW7vpd2G2Ds4Hb6X6Rok63l7Hpur8FvohdvViL+rczbkwBoD4AktIaWAe+0EI7T2Lz/Z9NnmhwW2NNTkLTke4CtsEWGBIp0gosmJ+/GjZOZplBtv7X8FIsfKLuxdbTAFt4a9og2xMs6DXwGH7vR2/qA5CQrgA0w2jgBsLP91xgJ6eMAx1K3Leis70CikghGnMFwIMKgGY4ibgT6hFeAQfxG+Iyf9wroIgkpwIgIRUA9fdu4k6kF1OuWz7jiJu7/QqwlVNGEUlLBUBCKgDqbW3gRcLP86P4LXKSZV3sXmlV84tId1QAJKQCoL7GYKOGQ8/xHGwgTVm9l/grGHUfES3SNCoAElIBUF+nEXfi/KRXwDb8jLh9OcoroIgkoQIgIRUA9fQh4k6Y53gFbNNo4EbC+zOPYrsXikhaKgASUgFQPxsBswg/t/cBE5wydmIytg57aL+mYGvEi0j1qQBISAVAvYzDGuSEntfZwOZOGbvxNuI6GV6NLTUsItWmAiAhFQD1Ejt3/oNeAXNwHHH7+G2vgCKSGxUACakAqI/Y7nlneQXMyQhsedPQfvYBeztlFJF8qABISAVAPbwOa4gTej7/CyzhlDFPywNPEd7f6cCaThlFpHuNKQB0z1I6MRE4Fxspn2UGtlzoy8kTpfcMcABwObZq21CWxmY67IgtuiL1sRzwBmBDbDDrGGzBnPuAm4E7/KKJVIOuAFRbD3ARcZf+93fKmNKXiNv3n3oFlFyNAA4Gric8GPRW4LPU44pXkzXmCoAHFQDVdgRxJ8CTvAImNgz4M3HH4ACnjJKP1wG3E/dcD9weBN7okFfyoQIgIRUA1bUjtnxv6Dm8gfDtgSpbBniE8HGYCWzgE1G6dDB2C6fdk//A7XuoVXQVqQBISAVANS0HPEH4+ZsGrOGUsUhbEzcI8i6sV4JUx0eJ6/0Qs51ccHbpngqAhFQAVM8w4DLCz10f8E6njB4+SdxJ4LdeAaVtBwK95HPy798+X+geSLdUACSkAqB6jiHug+54p3yeziDu2HzCK6BE25u4W1ztbr3AngXuh3RHBUBCKgCqZVdswZvQ83YtMMopo6dxwJ2Ej0/Zl0Buuj2Iu6XT6TYV9YeoChUACakAqI6VsPnvoefsWWAVp4xlsCE24C90nB7GBhBKubwBW6si5kT+PPAZbKGo5bBbXjdH/u5NwNiC9kk6pwIgIRUA1TAC+Adxlzf3cMpYJu8n7iRwMdZLQcphB+KKtxbW6GewQnc0cF7k3zgj3a5ITlQAJKQCoBpiF8A51itgCf2MuGP2Ra+AspAtgReIe87uxr7xD2UU8M/Iv3VY/rsiOVIBkJAKgPJ7K3HToP5GdlvcphkN3EjcVRM1ivG1EXY5P+aE/SiwWsTfXB54POLvzQV2zm9XJGcqABJSAVBuqxH3wTgFWNEpY5lNJv74reSUsenWIm5hpxZ2Qm+nr8W2xA0mnEKzx82UmQqAhFQAlNdI4N+En6N52MApGdzbiLuC8m/smEtxVsUGY8ac/J8B1u/gMT4a+fdvRoMCy0gFQEIqAMrrBOI+uI70Clgh3yHuWH7HK2ADLQ/cQ9zzMh3YvIvH+nnk45zexWNIGioAElIBUE7vJu4D689oFHuM4cAVhI9nH9aARtJalrh+DS3gRWwhoG6MJH5Q4Ee7fCzJlwqAhFQAlM9a2Ide6Ll5DHiNU8YqWp64e83TUZOYlJYibnBmC5gFvD6nx10ReDLiMecAO+X0mNI9FQAJqQAolzHENTKZA2zvlLHKdiGuveyt6H5wCksS/038VeDNOT/+9sStKvg0sHLOjy2dUQGQkAqAcjmVuA9HzV3u3JeIO8ZaOS5fY4GriDv2c4C3J8pxWGSGf9PMdtplowIgIRUA5fE+4j6YLkT3/bvRA1xA3LE+yClj3YzCui7GHPN5wP6J8/wqMsuJiXNImAqAhFQAlMNG2P3O0PNxP3YPVbozEXiI8PGeia0tIJ0bDpxD3Am3DzikgExjgBsiM324gDwyNBUACakA8DcOuIvwczEb2MIpYx29jrgmMfcCE5wyVt0w4EziT/5FLtO8GrZwVsz7rttZCNI5FQAJqQDwF7uGfRHfjJrmk8Qd+7O9AlZYD/HrMbTw6WexG3GDQh8je+0BSUcFQEIqAHx9grgPx996BWyA2ALsk14BK+p44k/+RztlBPh8Rq6B2z9Rp0gPKgASUgHgZ1PgZcLPwR3Y9ClJY0nimtJo6mW8bxJ/8v+hU8aBziYu6/e9AjaYCoCEVAD4WBp4kPDxnwls4JSxSdYFXiL8fKj5UtiXiT/5/5JyzGgZC9xEXOaDnDI2lQqAhFQAFK8H+ANxHzYfcMrYRPsT95z8GRvcJov7FPEn/9Mp13FcnbiVI18GtvSJ2EgqABJSAVC82HuOakRTvJOJe26+5BWwxA4mbtXFFlYAj3BJme2NWB+CUP5H0JWgoqgASEgFQLG2Ja4V6W2oFa2H0cTND+/FThZi9iXuxNkCLsWOc1nF3sK4HOtxIGmpAEhIBUBxlsG+OYSO+XTgtT4RBZsfHnMp+BnULx5gL+Km0rWwFRnH+MSM1gOcR9z+fNspY5OoAEhIBUAxhgGXED7efcA+ThllgbcSdzn73zR7atgbiWum1H+sxvnEbNs4bPZNzPv13U4Zm0IFQEIqAIrxVeI+JDXNqDy+Q9xzdpxXQGc7YLNUYo7RLVj75SpZB3iB8L7NwFp5SxoqABJSAZDersTdH70OrT5WJsOx+7wx3wL3dsroZRvipk22gNuBST4xu/YObLxHaB/vw6b2Sv5UACSkAiCt5YGnCB/nqdg0JCmX5YEnCT9/04E1nTIWbRPs9Rpz8r8PWNEnZm6+Rty+XooGBaagAiAhFQDpDMcGPYWOcS+wp1NGCduZuEFut1L/mRvrAFOIOyE+Ckz2iZmrYcCfiNvnY3wi1poKgIRUAKTzbeI+NL7uFVCifZG45/JnXgEL8Friroa0gCeo1xWR8cSt2NkHvMspY12pAEhIBUAabyHu3uFV6LJhFfQAFxB38jvIKWNKqwAPEbf/z1LP9tXrAS8S3v+XqOf+e1EBkJAKgPytCjxH+NhOAVZyyijtm0jcSfBlYDOnjCksB9xN3Ml/OrCFT8xC7E3c9NB7gAlOGetGBUBCKgDyNRK4hvBx7QV2d8oonduMuBUc76MeJ4DXAP8l7uT/IrC1T8xCHUfc8biQcix0VHUqABJSAZCvHxP34aBe8tX1CeKe43O8AuZkKeLaIvdf9djFJWXxhgF/Ie64fNEpY52oAEhIBUB+3knc5cG/UK5V0KR9pxN3AjjUK2CXlgD+Qdw+voqNeWmSZYhbzruX5h2bvKkASEgFQD7WIq5rmNaTr4clgTsJP99zgO2dMnZqFHFtq1tYg6v9fGK62xSYRfgYTUNre3RDBUBCKgC6Nwa4ibiTwQ5OGSV/6xDXDa9KRd9I4ue89wLv84lZGu8j7ljdhhWN0j4VAAmpAOjeL4j7EPiMV0BJZn/invsq3PYZDpxN3P70AR/xiVk6PyLumP3OK2DFqQBISAVAd95L3Jv/IjQiuK5+Stxr4MteASP0AL8kbj9awOE+MUtpBNbPI+a4fc4pY5WpAEhIBUDn1iXuEvAD2IhqqafRxI2W78WWzy2bHuKLmBZwlE/MUpsEPEz42M0D3uSUsapUACSkAqAzsYPAZlPvxihiVgOeJ/x6eAZY2SnjUGLntbewhXFkcJsT1yNiKrCGU8YqUgGQkAqAzsROA9N90uZ4K3HTQP+NDbYrg9iV7lpYjwvJ9gHijuUt2FRLCVMBkJAKgPZ9jLg3uQb9NE/sAlDf9Qo4wGeIP/mfisawxIq9nfIbr4AVowIgIRUA7dmEuMt892IriEmzDAcuJ/z66AP2ccoI8Mkhcg11oir7DIYyGUl8E6WqNooqkgqAhFQAxFsaG9AXOmYzgQ2dMoq/5YlbNnc6Pg1iDiJupcoWcD42yl3aswK2JHLo+M4BdnbKWBUqABJSARCnB/g9cR+aBzpllPLYGZhL+LVyGzC2wFzviszVAv6KzXCQzmwHvEL4OE/BlluWwakASEgFQJzPEfeheYpXQCmdoyjXa+Yd2DfOmExXUmxhUlcfJ+54X4uKraGoAEhIBUDYNtiCJ2X7Nifl1gNcQNwJ4ODEWXbHpqTGnozGJc7TJLGdQvXlYXAqABJSAZBtGeIafLyENQYSGWgicavGzQY2S5Rhe2BGRIYWcOv8zJKf0cB/iDv+/+OUscxUACSkAmBo7az7va9TRim/TYmbOXIfMCHnx94cG2wY8xq+BxvAKPlbEXiK8HMwB9jRKWNZqQBISAXA0L5C3AfnD70CSmXE3gs+J8fH3Ji47oQt4H7sJCXp7EDcrcSngJWcMpaRCoCEVAAMbhesb3fo+PwHWz9dJCS2e+SncnistYGnIx/vMWD1HB5TwmKbL12DPlf6qQBISAXA4pYn7nLdNPTBKfFi14+Yg31b7NRqwCMRj9PCpqBp7EqxTiPuufmJV8CSUQGQkAqAhQ0jvpPbO50ySnWtA7xI3Lfy13Tw91cmbtBhC3gONazyMAa4kbjn6ENOGctEBUBCKgAW9k3i3pjf9Aoolfce4l5jV2CthWMtC9wV+bdfALbsflekQ5OxAiz0PM0GtnLKWBYqABJSAbDAm4lrkXo1ao8q3TmJuBP1VyL/3tLATZF/cxYaaV4GbyBunNGjWHHXVCoAElIBYFYlriJ/Bo3Qle6NxJYFDr3eeoE9An9rAnB9xN9qYdMRd813V6QLRxL3vF1Jc790qABISAWAfRiHXmQtrFrfzSmj1M/qwFTiis6hFg0aT/zKc68CeybZE+lUD3Aecc/f8U4ZvakASEgFgM3jj3kDxl6OFYn1NmxAaei19wjwukV+dwPglojfbWELAO2ddE+kU+OAOwg/h33Y+JGmUQGoQOuKAAAMdUlEQVSQUNMLgH2I+wC+BK2JLml8i7iTeC82MPAk7PUYu7BPL3BAYXsjnVibuI6NM4FNnDJ6UQGQUJMLgNdio6FDx+BxOpuSJRJjGHAZcSfzdrc+4KPF7Yp0YQ/iBgU+TLM+j1QAJNTUAmAMcaOm56IR05Le8sCT5F8AfL7InZCufZW45/Uy2psiWmUqABJqagFwCnFvtM95BZTG2Z74JXtjti8VG19y0ANcRNzz+w2njEVTAZBQEwuA9xP3BrsAe0OKFOXt5FME6ORfXROwlRlDz3EfzRjYqQIgoaYVABsQtzb6g1hzFZGibU3cmgGDbS8B7ys+suRsfey5jHm+13fKWBQVAAk1qQCIXYxlNrCFU0YRgNHA14kbGd7CBo+diTW0knrYm7gZSvdgVw3qSgVAQk0qAM4g7sP0414BRRYxFpvC93vsg34uC16nzwB/BD6N9ZaX+oldm+Qi6nu7UgVAQk0pAD5C3BvpLK+AIhFGYVeypBmGYT0fYj67vuqUMTUVAAk1oQDYBOuBHtrXe6n3pTQRqZ6JwP2EP796sc6SdaMCIKG6FwDjiRtROxvY1CmjiEiWjbEugKHPsToOClQBkFDdC4DYhTYOdsonIhIjtm353dTrSqYKgITqXAB8hriT/y+8AoqItOF44j7T6tTDRAVAQnUtALbGlj8N7d/twBJOGUVE2jEcuJS4IuBIp4x5UwGQUB0LgInYghmhfZsBrOeUUUSkE8tgjcpCn2+9wJudMuZJBUBCdSsAeoALiauQtUSqiFTRpsAswp9xU7FVT6tMBUBCdSsAvkTcyf/HXgFFRHJwAHGfdbdR7ducKgASqlMBsDMLd0obarsea7UqIlJlPyGuCKhygzMVAAnVpQBYjrj11KcBazhlFBHJ0wjgauKKgM/4ROyaCoCE6lAADAMuI7wvfcBeThlFRFJYHnic8OffXGBXp4zdUAGQUB0KgK8TVwF/2yugiEhC2wCvEP4MfJ7qXQFVAZBQ1QuAN2BLoYb249/ASKeMIiKpHUjcF6GbsVUmq0IFQEJVLgBWAZ4jvA/PACs7ZRQRKcopxBUBZ3gF7IAKgISqWgCMAP5JOH8vsIdTRhGRIo0k7nOxBXzcKWO7VAAkVNUC4PvEvcjruka2iMhgViBuRtQc4PVOGduhAiChKhYAbyduVawrsd7ZIiJNsh1xa6FMofy3R1UAJFS1AmAy1t4ylPtprBIWEWmiQ4m7Snot5W6MpgIgoSoVAKOBGwlnngvs5JRRRKQsTiWuCDjZK2AEFQAJVakAOJm4F/PnvQKKiJTIGKz1eczn5iFOGUNUACRUlQLgPcS9iP+ErQgoIiKwGvAs4c/OV4CtnTJmUQGQUBUKgHWAFwlnfRSY5JRRRKSsdiVuobSngBWdMg5FBUBCZS8AxgK3Es45Bxv5KiIiizucuKuo/wJGOWUcjAqAhMpeAJxG3Iv2E14BRUQq4tfEfZ7+yCnfYFQAJFTmAuAQ4l6s53gFFBGpkLHATcR9rn7QKeOiVAAkVNYCYGNgVkau/u0+YIJTRhGRqplM3Boqs4EtnTIOpAIgoTIWAOOAuyOyzQY2c8ooIlJVuxO3iuojwGt8Iv4/FQAJlbEAODMiV5kuUYmIVM2XiPucvQJbfM2LCoCEylYAHBaRqYV1uBIRkc70AOcS93l7nFNGUAGQVJkKgNdhzShCmf4LLFFwNhGRuhkH3EH4M7cPa8bmQQVAQmUpACYCD0XkmQGsX2AuEZE6WxuYTvizdyawkUM+FQAJlaEA6AEuiMjSAt5fUCYRkaZ4O9BL+PP3YYrvtqoCIKEyFABHReRoAScUlEdEpGmOIe5z+DJgeIG5VAAk5F0AbIe18Q3luJ5yr1ktIlJlPcAfiCsCvlZgLhUACXkWAMsBT0RkmA6skTiLiEjTjQfuIvyZ3AfsW1AmFQAJeRUAw4C/Rjx+H7B3whwiIrLAusStvvoSsEEBeVQAJORVABwb8dgtfOefiog00V7Yl6/Q5/M9wFKJs6gASMijANiNuDaU1wIjE2UQEZGhfZu4L2kXYeMHUlEBkFDRBcAKwNMRj/sssHKCxxcRkbBhwF+IKwK+kjCHCoCEiiwARgD/iHjMXuBNOT+2iIi0ZyLwAHGf2W9NlEEFQEJFFgDHRzxeC5uPKiIi/jbBugCGPrenAWsleHwVAAkVVQC8jbhBJX+j2CYTIiKS7b3EfXm7C5iQ82OrAEioiAJgNeD5iMd6Glgxp8cUEZH8/IC4IuB88h0UqAIgodQFwGjghojHmQvslMPjiYhI/oYT17ulBRyR4+OqAEgodQFwUsRjtIAv5PBYIiKSziTiVm3tBfbM6TFVACSUsgB4d8TfbwEXk3YeqYiI5GMz4GXCn+tTgTVzeDwVAAmlKgDWJq6d5KMUv7ykiIh07gPEfbm7FViiy8dSAZBQigJgDHBLxN+eg60GKCIi1RJ7e/fMLh9HBUBCKQqAX0X83RZwaDfBRUTEzUjg78R91h/WxeOoAEgo7wLgQxF/swWc221wERFxtTxxS7rPBXbu8DFUACSUZwGwETAr4m/eT/oVpEREJL1tgVcIf+5PAVbp4O+rAEgorwJgHNYFKvT3ZgOb55RdRET8fZS4K783A2Pb/NsqABLKqwD4TcTfamG3CEREpF5+Qdw54PQ2/64KgITyKAAOjfg7LeCsPIOLiEhpjAT+Rdy54KNt/F0VAAl1WwC8jrj7P3fQ/XxQEREprxWBpwifD+YQ3/pdBUBC3RQASxPXFnIGsEGC7CIiUi7bA68SPi88Dawc8fdUACTUaQHQA1wU8fstbClJERFphsOIOzf8E7t1kOW6wN9QAdCF2WQf3KFGbH4h8Hv9208TZhcRkXKKbQh3YuDv3BH4/U0SZG+MZ8g+uCsN8js7Yo0dQk/sjdhywCIi0ixjsWl/MUXAwRl/J9RoaPUU4ZsiNHd/l0V+flniOj9NJ5+VoEREpJpWB54nfL6YDWw1yO+Pw5YWzvrd8Sl3oO4uIPvgfnbAzw4DLgv8fAvoA/YqJr6IiJTY7sA8wueNR7EvmAPtGPidJ9PHr7dvkX2ALx3ws0cHfrZ/+15B2UVEpPyOIO7c8TdgxIDf+1rg568oJn59vYXsA/wK8BqsigtdimkB1xAe1SkiIs3RA5xDXBHwgwG/d3fgZ48pJH2NjSM8Z/MnhAcLtoDn6GyxBxERqbclgduJKwLeB7wx4ud2KHQPauoS4p6UrK0XeFPRwUVEpDLWAqYRPp/MAm4L/MzTLHy7QDr0HrovAL5WeGoREamaNxI3KDC0fbfo4HU1GlurudMn4kpgeOGpRUSkir5C91ec1y08dY0dTmdPxBRsAQgREZEYPcB5dF4A/K74yPW2BDansp0nYS6ws0dYERGptAmER/kPdd5Z3yFv7e1He0/EUT4xRUSkBtYBXqC98853XJI2xIXEPxHfYOjFgkREREJ+Qvw5537sarUksgzwMPFPyIPYLAI1/xERkVjbAv8g/lzzMrCZS9KG2QKYQXuXZZ7EWgVvjmYEiIjI4iYDhxK/SmD/1ge83yFvoXq8AwzwBuBiYEwHv/sScC1WFDyHrQwoIiLNsiQwCVtWfmsGX14+xueAH+YVqqzKVACArRNwLvYkioiIFKkFHAkc7x2kCGUrAMDWaP4TsIJ3EBERaYxXgA8CZ3sHKcow7wCDuBHYFFsvQEREJLV7gO1p0Mkfyjt4bhbWeWkqsB2djQsQERHJMhf4MbA/8LhzlsKVtQAAuxdzPXAatoTwJmglJhER6V4Lu9W8L3AWVgg0ThnHAAxlReAw4EA6H9kpIiLN9RLwe+AHwJ3OWdxVqQDoNwzYBXj7/P9uQjnHMoiIiL8Hgb8Dl2JTzWf7ximPKhYAi5qA9XdeG7syMA61CxYRaaI5wEzgGezEfy/WG0ZERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERBL6P4Z7e0bdK5hVAAAAAElFTkSuQmCC"


def get_html_img(picture):
    return mark_safe(f'<img src="{picture.url if picture else no_photo_base64}" style="max-height: 50px;">')


class Menu(models.Model):
    title = models.CharField(max_length=200)
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    price = models.FloatField(default=0, validators=[MinValueValidator(0, "Price can't be negative!")])
    guid_1c = models.CharField(max_length=100, default="")
    internal_id = models.IntegerField(default=-1, verbose_name="ID из внутренней базы")
    weight = models.IntegerField(verbose_name="Вес товара", blank=True, null=True)
    meat_weight = models.IntegerField(verbose_name="Вес мяса в товаре", blank=True, null=True)
    # category = models.ForeignKey(MenuCategory, on_delete=models.SET_NULL, null=True)
    is_by_weight = models.BooleanField(verbose_name="На развес", default=False)
    note = models.TextField(verbose_name="Описание", blank=True, null=True)
    customer_appropriate = models.BooleanField(verbose_name="Показывать", default=False)
    icon = models.ImageField(upload_to="img/icons", blank=True, null=True, verbose_name="Иконка")

    def preview(self):
        return get_html_img(self.icon)

    def __str__(self):
        return u"{}".format(self.title) if self.title else f'Noname id:{self.internal_id}'


class MacroProduct(models.Model):
    """
    Шаурма, Бурум, Холодные напитки...
    """
    title = models.CharField(max_length=200)
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    slug = models.SlugField(unique=True, default='')
    picture = models.ImageField(upload_to="img/category_pictures", blank=True, null=True, verbose_name="Иконка")
    internal_id = models.IntegerField(default=-1, verbose_name="ID из внутренней базы")
    customer_appropriate = models.BooleanField(verbose_name="Показывать", default=False)
    ordering = models.IntegerField('ordering', default=0)

    def __str__(self):
        return u"{}".format(self.title) if bool(self.picture) else u"{} [No Photo]".format(self.title)

    def preview(self):
        return get_html_img(self.picture)

    def with_content(self):
        if self.contents.all():
            return mark_safe('✅')
        else:
            return mark_safe('◽')

    class Meta:
        ordering = ('ordering', )


class SizeOption(models.Model):
    """
    Большая, Средняя, 0.33л, 0.5л...
    """
    title = models.CharField(max_length=200)
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    internal_id = models.IntegerField(default=-1, verbose_name="ID из внутренней базы")

    def __str__(self):
        return u"{}".format(self.title)


class ContentOption(models.Model):
    """
    Курица, Свинина, Чай, Кола...
    """
    title = models.CharField(max_length=200)
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    picture = models.ImageField(upload_to="img/content_pictures", blank=True, null=True, verbose_name="Иконка")
    internal_id = models.IntegerField(default=-1, verbose_name="ID из внутренней базы")

    def preview(self):
        return get_html_img(self.picture)

    def __str__(self):
        return u"{}".format(self.title) if bool(self.picture) else u"{} [No Photo]".format(self.title)


class MacroProductContent(models.Model):
    """
    Шаурма со свининой, Говяжий шашлык, Coca-cola...
    """
    title = models.CharField(max_length=200)
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    customer_description = models.TextField(max_length=312, default="", verbose_name="Описание товара", blank=True, null=True)
    slug = models.SlugField(unique=True, default='')
    picture = models.ImageField(upload_to="img/category_pictures", blank=True, null=True, verbose_name="Иконка")
    customer_appropriate = models.BooleanField(verbose_name="Показывать", default=False)
    content_option = models.ForeignKey(ContentOption, on_delete=models.CASCADE, verbose_name="Вариант содержимого")
    macro_product = models.ForeignKey(MacroProduct, related_name='contents', on_delete=models.CASCADE, verbose_name="Макротовар")
    internal_id = models.IntegerField(default=-1, verbose_name="ID из внутренней базы")

    def preview(self):
        return get_html_img(self.picture)

    def __str__(self):
        return u"{}".format(self.title) if bool(self.picture) else u"{} [No Photo]".format(self.title)


class ProductVariant(models.Model):
    """
    Should be used to link different contents and sizes of products of one type. (Большая Куриная Шаурма, 0.33л Кола)
    """
    title = models.CharField(max_length=200)
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="Товар из меню 1С")
    size_option = models.ForeignKey(SizeOption, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Вариант размера")
    content_option = models.ForeignKey(ContentOption, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Вариант содержимого")
    macro_product = models.ForeignKey(MacroProduct, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Макротовар")
    macro_product_content = models.ForeignKey(MacroProductContent, on_delete=models.CASCADE,
                                              verbose_name="Содержимое макротовара", null=True)
    internal_id = models.IntegerField(default=-1, verbose_name="ID из внутренней базы")

    def __str__(self):
        return u"{}".format(self.title)


class ProductOption(models.Model):
    """
    Should be used to link toppings menu_items, such as cheese, onion rings, sugar, etc. with product_variants
    """
    title = models.CharField(max_length=200)
    customer_title = models.CharField(max_length=200, default="", verbose_name="Название для покупателя")
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="Товар из меню 1С")
    product_variants = models.ManyToManyField(ProductVariant, verbose_name="Вариант товара")
    internal_id = models.IntegerField(default=-1, verbose_name="ID из внутренней базы")

    def __str__(self):
        return u"{}".format(self.title)


class Order(models.Model):
    message = models.TextField(verbose_name='message')
    data = models.TextField(verbose_name='data', default='')
    paid = models.BooleanField(verbose_name="оплачено", default=False)
    date = models.DateTimeField('дата, время', default=timezone.now)

    def __str__(self):
        return str(self.pk)
