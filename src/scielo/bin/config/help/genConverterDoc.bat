mx ..\..\convert\library\scielo\artmodel lw=99999 "pft=@genConverterArtmodel.pft" now | sort > genConverter_artmodel.seq
mx seq=genConverter_artmodel.seq create=genConverter_artmodel  now -all fst=@genConverter_artmodel.fst fullinv=genConverter_artmodel


rem mx "seq=..\..\convert\library\scielo\article.2db" create=genConverter_art2db now -all 
rem mx genConverter_art2db lw=9999 "pft=v1/" now | sort > article.2db
rem mx "seq=article.2db;" create=genConverter_art2db now -all  "fst=1 0 v1/" fullinv=genConverter_art2db

 
mx "seq=..\..\convert\library\scielo\article.trl,"  lw=9999  "pft=@genConverter_transl.pft" now > genConverter.xml
mx null count=1 "pft='</transl>'"  >> genConverter.xml

mx "seq=..\..\convert\library\scielo\article.2db;"  lw=9999 "pft=@genConverter_art2db.pft" now >> genConverter.xml
mx null count=1 "pft='</art2db>'"  >> genConverter.xml

mx genConverter_artmodel lw=9999 "pft=@genConverter_artmodel.pft" now >> genConverter.xml
mx null count=1 "pft='</artmodel>'"  >> genConverter.xml

mx null count=1 "pft='</root>'"  >> genConverter.xml

rem 1 tag
rem 2 tag/subc
rem 3 att
rem 4 tag/dist
rem 5
rem 6 group
rem 7 :1
rem p
rem i
rem h

rem echo > genConverter_geraschema.bat
rem mx genConverter_artmodel "bool=h" "pft=@genConverter_registro.pft" now >> genConverter_geraschema.bat

