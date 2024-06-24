<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:tei="http://www.tei-c.org/ns/1.0"  
    version="1.0">

<xsl:output method="html" indent="yes"/> <!-- controllare-->

    <xsl:template match="/">
        <html>
            <head>
                <title><xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/></title>
            </head>
            <body>
                <h1><xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/></h1>
                <h2>By <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author"/></h2>
                <h3>Publication Details</h3>
                <p>Publisher: <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:publisher"/></p>
                <p>Date: <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:date"/></p>
                <p>Id: <xsl:value-of select="tei:TEI/tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:idno"/></p>
                <h3>Characters</h3>
                <ul> <!-- unordered list-->
                    <xsl:for-each select="tei:TEI/tei:teiHeader/tei:profileDesc/tei:particDesc/tei:listPerson/tei:person">
                        <li> <!--list element-->
                            <xsl:choose>
                                <xsl:when test="persName/forename">
                                    <xsl:value-of select="persName/forename"/><xsl:value-of select="persName/surname"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:value-of select="persName/addName"/> <!-- Mostra il nickname -->
                                </xsl:otherwise>
                            </xsl:choose>
                        </li>
                    </xsl:for-each>
                </ul>
                <!-- Testo principale -->
                <xsl:for-each select="tei:TEI/tei:text/tei:body/tei:div">
                    <div>
                        <h3>Chapter <xsl:value-of select="@n"/>: <xsl:value-of select="head"/></h3>
                        <xsl:for-each select="tei:div[@type='paragraph']">
                            <p>
                                <xsl:value-of select="tei:p"/>
                            </p>
                        </xsl:for-each>
                    </div>
                </xsl:for-each>                
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
