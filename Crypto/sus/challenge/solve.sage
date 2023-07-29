from Crypto.Util.number import *

n = 1125214074953003550338693571791155006090796212726975350140792193817691133917160305053542782925680862373280169090301712046464465620409850385467397784321453675396878680853302837289474127359729865584385059201707775238870232263306676727868754652536541637937452062469058451096996211856806586253080405693761350527787379604466148473842686716964601958192702845072731564672276539223958840687948377362736246683236421110649264777630992389514349446404208015326249112846962181797559349629761850980006919766121844428696162839329082145670839314341690501211334703611464066066160436143122967781441535203415038656670887399283874866947000313980542931425158634358276922283935422468847585940180566157146439137197351555650475378438394062212134921921469936079889107953354092227029819250669352732749370070996858744765757449980454966317942024199049138183043402199967786003097786359894608611331234652313102498596516590920508269648305903583314189707679
e = 65537
c = 27126515219921985451218320201366564737456358918573497792847882486241545924393718080635287342203823068993908455514036540227753141033250259348250042460824265354495259080135197893797181975792914836927018186710682244471711855070708553557141164725366015684184788037988219652565179002870519189669615988416860357430127767472945833762628172190228773085208896682176968903038031026206396635685564975604545616032008575709303331751883115339943537730056794403071865003610653521994963115230275035006559472462643936356750299150351321395319301955415098283861947785178475071537482868994223452727527403307442567556712365701010481560424826125138571692894677625407372483041209738234171713326474989489802947311918341152810838321622423351767716922856007838074781678539986694993211304216853828611394630793531337147512240710591162375077547224679647786450310708451590432452046103209161611561606066902404405369379357958777252744114825323084960942810
k = 3

R = Zmod(n)["x"]
while True:
    Q = R.quo(R.random_element(k))
    pp = gcd(ZZ(list(Q.random_element() ^ n)[1]), n)
    if pp != 1:
        qq = sum([pp**i for i in range(k)])
        rr = n // (pp * qq)
        assert n == pp * qq * rr
        break
phi = (pp - 1) * (qq - 1) * (rr - 1)
d = pow(e, -1, phi)
m = pow(c, d, n)
print(long_to_bytes(m))
