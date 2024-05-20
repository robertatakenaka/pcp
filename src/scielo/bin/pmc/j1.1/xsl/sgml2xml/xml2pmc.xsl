<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xlink="http://www.w3.org/1999/xlink"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:util="http://dtd.nlm.nih.gov/xsl/util"
	xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl xlink mml">
	
	<xsl:include href="../../../v3.0/xsl/sgml2xml/xml2pmc.xsl"/>
	<xsl:template match="article/@specific-use"/>
	<xsl:template match="@dtd-version"></xsl:template>
		
	<xsl:template match="funding-group">
		<!--
			Issues conflitantes
			https://github.com/scieloorg/PC-Programs/issues/1902 (remover funding-group)
			https://github.com/scieloorg/pcp/issues/10 (manter funding-group)
			Provavelmente PMC passou a adotar uma versão mais recente de Schema
		-->
		<xsl:copy-of select="."/>
	</xsl:template>

</xsl:stylesheet>
